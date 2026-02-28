from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timezone

from core_engine import SMCCoreEngine, Bar
from alert_engine import AlertEngine

router = APIRouter()

# Lazy imports - will be resolved during runtime, not at module load time
def get_globals():
    """Get the global engine instances from main module."""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import main
    return main.smc_engine, main.alert_engine, main.ultimo_resultado, main._resultado_para_dict, main.get_user_com_plano


class BarInput(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: float
    volume_compra: float
    volume_venda: float
    trades: int
    true_range: float
    timestamp_hhmm: int
    tick_minimo: float = 5.0
    ativo: str = "WIN"


@router.post("/processar-barra")
async def processar_barra(
    bar_input: BarInput,
    background_tasks: BackgroundTasks,
    user=Depends(lambda: None)  # placeholder - implement user auth
):
    smc_engine, alert_engine, ultimo_resultado, _resultado_para_dict, _ = get_globals()
    
    bar = Bar(
        open=bar_input.open, high=bar_input.high,
        low=bar_input.low, close=bar_input.close,
        volume=bar_input.volume, volume_compra=bar_input.volume_compra,
        volume_venda=bar_input.volume_venda, trades=bar_input.trades,
        true_range=bar_input.true_range, timestamp_hhmm=bar_input.timestamp_hhmm,
        tick_minimo=bar_input.tick_minimo
    )

    resultado = smc_engine.process(bar)

    if resultado is None:
        return {
            "aquecendo": True,
            "barras_restantes": max(0, 60 - smc_engine.contador_barras),
            "mensagem": "Engine em aquecimento (60 barras necessárias)"
        }

    ultimo_resultado[bar_input.ativo] = resultado
    background_tasks.add_task(alert_engine.processar, resultado)
    return _resultado_para_dict(resultado)


@router.get("/ultimo-sinal/{ativo}")
def ultimo_sinal(ativo: str = "WIN", user=Depends(lambda: None)):
    _, _, ultimo_resultado, _, _ = get_globals()
    r = ultimo_resultado.get(ativo)
    if not r:
        return {"mensagem": f"Sem dados para {ativo} ainda"}
    return _resultado_para_dict(r)


