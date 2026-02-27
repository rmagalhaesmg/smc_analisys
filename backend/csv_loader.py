"""
CSV Loader para o SMC Core Engine.
Suporta dados exportados do Profit Pro.
Formato esperado: timestamp,open,high,low,close,volume,vol_compra,vol_venda,trades
"""

import csv
import math
from core_engine import SMCCoreEngine, Bar, SMCResult


def calcular_true_range(high, low, close_anterior):
    return max(high - low, abs(high - close_anterior), abs(low - close_anterior))


def parse_hhmm(timestamp_str: str) -> int:
    """Converte string de timestamp para formato HHMM inteiro."""
    try:
        # Tenta formatos comuns: "09:30", "09:30:00", "2024-01-01 09:30:00"
        parts = timestamp_str.strip().replace("-", " ").replace(":", " ").split()
        if len(parts) >= 2:
            hora = int(parts[-2]) if len(parts) > 2 else int(parts[0])
            minuto = int(parts[-1]) if len(parts) > 2 else int(parts[1])
        else:
            return 1000  # fallback
        return hora * 100 + minuto
    except Exception:
        return 1000


def carregar_csv(caminho: str, tick_minimo: float = 5.0,
                 tf_base: int = 5, modo: int = 2,
                 tipo_ativo: int = 1) -> list:
    """
    Carrega CSV e processa cada barra pelo Core Engine.
    Retorna lista de (bar, resultado).
    """
    engine = SMCCoreEngine(
        tf_base_minutos=tf_base,
        modo_operacao=modo,
        tipo_ativo=tipo_ativo
    )

    resultados = []
    close_anterior = None

    with open(caminho, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Suporte a diferentes nomes de colunas
                ts  = row.get("timestamp") or row.get("data") or row.get("time") or "10:00"
                op  = float(row.get("open")  or row.get("abertura") or 0)
                hi  = float(row.get("high")  or row.get("maxima")   or 0)
                lo  = float(row.get("low")   or row.get("minima")   or 0)
                cl  = float(row.get("close") or row.get("fechamento") or 0)
                vol = float(row.get("volume") or 0)
                vc  = float(row.get("vol_compra") or row.get("volume_compra") or vol * 0.5)
                vv  = float(row.get("vol_venda")  or row.get("volume_venda")  or vol * 0.5)
                tr_raw = int(float(row.get("trades") or row.get("negocios") or 100))

                if close_anterior is None:
                    close_anterior = cl
                tr = calcular_true_range(hi, lo, close_anterior)

                bar = Bar(
                    open=op, high=hi, low=lo, close=cl,
                    volume=vol, volume_compra=vc, volume_venda=vv,
                    trades=tr_raw, true_range=tr,
                    timestamp_hhmm=parse_hhmm(ts),
                    tick_minimo=tick_minimo
                )

                resultado = engine.process(bar)
                resultados.append((bar, resultado))
                close_anterior = cl

            except (ValueError, KeyError) as e:
                print(f"Linha ignorada: {e} — {row}")
                continue

    return resultados


def resumo_resultados(resultados: list):
    """Imprime resumo dos resultados processados."""
    validos = [(b, r) for b, r in resultados if r is not None]
    print(f"\n{'='*60}")
    print(f"SMC CORE ENGINE — RESUMO DO PROCESSAMENTO")
    print(f"{'='*60}")
    print(f"Total de barras: {len(resultados)}")
    print(f"Barras processadas: {len(validos)}")
    print(f"Barras em aquecimento: {len(resultados) - len(validos)}")

    if not validos:
        print("Nenhuma barra processada ainda (aguardando aquecimento).")
        return

    compras  = [r for _, r in validos if r.permissao_compra]
    vendas   = [r for _, r in validos if r.permissao_venda]
    bloq     = [r for _, r in validos if r.estado_mercado == 4]
    traps    = [r for _, r in validos if r.evento_trap]
    conf     = [r for _, r in validos if r.confluencia_forte]

    print(f"\nSetups de COMPRA liberados: {len(compras)}")
    print(f"Setups de VENDA  liberados: {len(vendas)}")
    print(f"Barras BLOQUEADAS:          {len(bloq)}")
    print(f"Traps detectados:           {len(traps)}")
    print(f"Confluência MTV ativa:      {len(conf)}")

    # Últimas 5 barras processadas
    print(f"\n{'─'*60}")
    print("ÚLTIMAS 5 BARRAS PROCESSADAS:")
    print(f"{'─'*60}")
    for b, r in validos[-5:]:
        estado_str = {1: "✅ COMPRA", 2: "✅ VENDA", 3: "⚪ NEUTRO", 4: "🚫 BLOQ"}.get(r.estado_mercado, "?")
        print(f"  Close={b.close:.2f} | C={r.score_compra:.1f} V={r.score_venda:.1f} | "
              f"HFZ={r.score_hfz*100:.0f} FBI={r.score_fbi*100:.0f} "
              f"DTM={r.score_dtm*100:.0f} SDA={r.score_sda*100:.0f} "
              f"MTV={r.score_mtv*100:.0f} | {estado_str} Q={r.qualidade_setup}")

    # Melhor setup encontrado
    if compras or vendas:
        todos = compras + vendas
        melhor = max(todos, key=lambda r: r.qualidade_setup)
        direcao = "COMPRA" if melhor.permissao_compra else "VENDA"
        print(f"\n{'─'*60}")
        print(f"MELHOR SETUP: {direcao} | Score={max(melhor.score_compra, melhor.score_venda):.1f} "
              f"| Qualidade={melhor.qualidade_setup}/10 | Risco={melhor.risco_contextual}")
        print(f"  Confluência MTV: camada={melhor.confluencia_camada} | Renko={melhor.renko_sugestao:.1f}")
    print(f"{'='*60}\n")


def gerar_csv_teste(caminho: str = "dados_teste.csv", num_barras: int = 200):
    """Gera CSV de dados sintéticos para teste do engine."""
    import random
    random.seed(42)

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "open", "high", "low", "close",
                         "volume", "vol_compra", "vol_venda", "trades"])
        preco = 120000.0
        hora = 9; minuto = 0

        for i in range(num_barras):
            delta = random.gauss(0, 200)
            op = preco
            cl = preco + delta
            hi = max(op, cl) + random.uniform(0, 100)
            lo = min(op, cl) - random.uniform(0, 100)
            vol = random.uniform(800, 3000)
            vc = vol * random.uniform(0.3, 0.7)
            vv = vol - vc
            trades = random.randint(50, 500)
            ts = f"{hora:02d}:{minuto:02d}"

            writer.writerow([ts, f"{op:.0f}", f"{hi:.0f}", f"{lo:.0f}", f"{cl:.0f}",
                              f"{vol:.0f}", f"{vc:.0f}", f"{vv:.0f}", trades])
            preco = cl
            minuto += 5
            if minuto >= 60:
                minuto = 0; hora += 1


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        caminho = sys.argv[1]
        tick = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
        tf   = int(sys.argv[3])   if len(sys.argv) > 3 else 5
        tipo = int(sys.argv[4])   if len(sys.argv) > 4 else 1
        print(f"Carregando: {caminho} | tick={tick} | tf={tf}min | ativo={tipo}")
        resultados = carregar_csv(caminho, tick_minimo=tick, tf_base=tf, tipo_ativo=tipo)
    else:
        print("Gerando dados de teste...")
        gerar_csv_teste("dados_teste.csv", 200)
        resultados = carregar_csv("dados_teste.csv", tick_minimo=5.0, tf_base=5, tipo_ativo=1)

    resumo_resultados(resultados)
