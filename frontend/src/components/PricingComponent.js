/**
 * PricingComponent
 * Mostra planos e permite checkout
 */

import { useState, useEffect } from "react";
import { usePaymentPlans, useCheckout } from "../hooks";

function PricingComponent() {
  const { fetch: fetchPlans, plans, loading: plansLoading } = usePaymentPlans();
  const { checkout, loading: checkoutLoading, error: checkoutError } = useCheckout();
  const [selectedPlan, setSelectedPlan] = useState(null);

  useEffect(() => {
    fetchPlans();
  }, [fetchPlans]);

  const [gateway, setGateway] = useState("stripe");

  const handleCheckout = async (planId) => {
    try {
      const result = await checkout(planId, gateway);
      console.log("✅ Checkout iniciado:", result);
      alert("Redirecionando para pagamento...");
      // window.location.href = result.url || result.checkout_url;
    } catch (err) {
      console.error("❌ Erro no checkout:", checkoutError);
    }
  };

  const containerStyle = {
    background: "#0f0f1a",
    color: "#fff",
    padding: "40px 20px",
    minHeight: "60vh",
  };

  const contentStyle = {
    maxWidth: "1200px",
    margin: "0 auto",
  };

  const titleStyle = {
    textAlign: "center",
    color: "#00d4ff",
    fontSize: "32px",
    marginBottom: "10px",
  };

  const subtitleStyle = {
    textAlign: "center",
    color: "#888",
    marginBottom: "40px",
  };

  const plansGridStyle = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
    gap: "30px",
    marginBottom: "40px",
  };

  const planCardStyle = (isSelected) => ({
    background: "#1a1a2e",
    borderRadius: "10px",
    padding: "30px 20px",
    border: isSelected ? "2px solid #00d4ff" : "1px solid #333",
    textAlign: "center",
    transition: "all 0.3s",
    transform: isSelected ? "scale(1.05)" : "scale(1)",
  });

  const planNameStyle = {
    fontSize: "20px",
    fontWeight: "bold",
    color: "#00d4ff",
    marginBottom: "10px",
  };

  const planPriceStyle = {
    fontSize: "32px",
    fontWeight: "bold",
    color: "#ffd700",
    margin: "20px 0",
  };

  const featureListStyle = {
    textAlign: "left",
    margin: "20px 0",
    padding: "20px 0",
    borderTop: "1px solid #333",
    borderBottom: "1px solid #333",
  };

  const featureStyle = {
    padding: "8px 0",
    color: "#888",
    display: "flex",
    alignItems: "center",
    gap: "10px",
  };

  const buttonStyle = (isSelected) => ({
    padding: "12px 24px",
    background: isSelected ? "#ff6b6b" : "#00d4ff",
    color: isSelected ? "#fff" : "#000",
    border: "none",
    borderRadius: "5px",
    fontWeight: "bold",
    cursor: "pointer",
    width: "100%",
    marginTop: "20px",
  });

  if (plansLoading) {
    return (
      <div style={containerStyle}>
        <div style={contentStyle}>
          <p style={{ textAlign: "center", color: "#888" }}>⏳ Carregando planos...</p>
        </div>
      </div>
    );
  }

  return (
    <div style={containerStyle}>
      <div style={contentStyle}>
        <h1 style={titleStyle}>💰 Nossos Planos</h1>
        <h2 style={subtitleStyle}>Escolha o plano ideal para você</h2>

        {/* gateway selector */}
        <div style={{ marginBottom: "20px", textAlign: "center" }}>
          <label style={{ marginRight: "10px" }}>
            <input
              type="radio"
              value="stripe"
              checked={gateway === "stripe"}
              onChange={() => setGateway("stripe")}
            />
            Stripe
          </label>
          <label>
            <input
              type="radio"
              value="mp"
              checked={gateway === "mp"}
              onChange={() => setGateway("mp")}
            />
            MercadoPago
          </label>
        </div>
        {/* Plans Grid */}
        <div style={plansGridStyle}>
          {plans.length > 0 ? (
            plans.map((plan) => (
              <div
                key={plan.id}
                style={planCardStyle(selectedPlan === plan.id)}
                onClick={() => setSelectedPlan(plan.id)}
              >
                <div style={planNameStyle}>{plan.name}</div>

                <div style={{ color: "#888", fontSize: "14px", minHeight: "40px" }}>
                  {plan.description}
                </div>

                <div style={planPriceStyle}>
                  R$ {plan.price || plan.valor || "0"}
                  <span style={{ fontSize: "14px", color: "#888" }}>/mês</span>
                </div>

                {/* Features */}
                {plan.features && (
                  <div style={featureListStyle}>
                    {Array.isArray(plan.features) ? (
                      plan.features.map((feature, idx) => (
                        <div key={idx} style={featureStyle}>
                          <span>✅</span>
                          <span>{feature}</span>
                        </div>
                      ))
                    ) : (
                      <div style={featureStyle}>
                        <span>✅</span>
                        <span>{plan.features}</span>
                      </div>
                    )}
                  </div>
                )}

                {/* Button */}
                <button
                  style={buttonStyle(selectedPlan === plan.id)}
                  onClick={() => handleCheckout(plan.id)}
                  disabled={checkoutLoading}
                >
                  {checkoutLoading
                    ? "⏳ Processando..."
                    : selectedPlan === plan.id
                    ? "Desselecionar"
                    : "Escolher"}
                </button>
              </div>
            ))
          ) : (
            <p style={{ gridColumn: "1 / -1", textAlign: "center", color: "#888" }}>
              Nenhum plano disponível
            </p>
          )}
        </div>

        {checkoutError && (
          <div style={{ background: "#ff6b6b", padding: "15px", borderRadius: "5px", marginTop: "20px" }}>
            <p style={{ margin: 0, color: "#fff" }}>❌ Erro: {checkoutError}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default PricingComponent;
