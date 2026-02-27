/**
 * Theme Configuration
 * Cores e estilos da marca SMC Analysis
 */

export const COLORS = {
  // Primary Colors - Marca SMC
  primary: "#00d4ff",      // Cyan brilhante
  primaryDark: "#0f4c75",  // Azul escuro
  
  // Status Colors
  success: "#00ff88",      // Verde
  warning: "#ffd700",      // Ouro/Amarelo
  danger: "#ff6b6b",       // Vermelho
  
  // Background Colors
  bgPrimary: "#0f0f1a",    // Preto - fundo principal
  bgSecondary: "#1a1a2e",  // Cinza escuro - cards/sidebar
  bgTertiary: "#0a0a15",   // Preto mais escuro - headers
  
  // Text Colors
  textPrimary: "#ffffff",  // Branco
  textSecondary: "#888888", // Cinza médio
  textMuted: "#555555",    // Cinza escuro
  
  // Border & Backgrounds
  border: "#333333",       // Border cinza
  borderLight: "#444444",  // Border mais claro
};

export const THEME = {
  colors: COLORS,
  
  // Common Styles
  cardStyle: {
    background: COLORS.bgSecondary,
    borderRadius: "12px",
    padding: "20px",
    border: `1px solid ${COLORS.border}`,
    color: COLORS.textPrimary,
  },
  
  containerStyle: {
    display: "flex",
    minHeight: "100vh",
    background: COLORS.bgPrimary,
    color: COLORS.textPrimary,
  },
  
  sidebarStyle: {
    width: "250px",
    background: COLORS.bgSecondary,
    borderRight: `1px solid ${COLORS.border}`,
    padding: "20px",
    display: "flex",
    flexDirection: "column",
    overflow: "hidden",
  },
  
  headerStyle: {
    background: COLORS.bgSecondary,
    borderBottom: `1px solid ${COLORS.border}`,
    padding: "15px 30px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  
  buttonPrimary: {
    background: COLORS.primary,
    color: COLORS.bgPrimary,
    border: "none",
    borderRadius: "5px",
    padding: "10px 20px",
    fontWeight: "bold",
    cursor: "pointer",
  },
  
  buttonSecondary: {
    background: COLORS.primaryDark,
    color: COLORS.primary,
    border: `1px solid ${COLORS.primary}`,
    borderRadius: "5px",
    padding: "8px 12px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  
  buttonDanger: {
    background: COLORS.danger,
    color: COLORS.textPrimary,
    border: "none",
    borderRadius: "5px",
    padding: "8px 16px",
    fontWeight: "bold",
    cursor: "pointer",
  },
};

// Função para gerar cor baseada em score
export const getScoreColor = (score) => {
  if (score >= 80) return COLORS.success;
  if (score >= 60) return COLORS.primary;
  if (score >= 40) return COLORS.warning;
  return COLORS.danger;
};

// Função para gerar label baseado em score
export const getScoreLabel = (score) => {
  if (score >= 80) return "🟢 Excelente";
  if (score >= 60) return "🔵 Bom";
  if (score >= 40) return "🟡 Moderado";
  return "🔴 Baixo";
};

// Função para gerar estilo de badge
export const getBadgeStyle = (color = COLORS.primary) => ({
  display: "inline-block",
  padding: "4px 8px",
  background: color + "20",
  border: `1px solid ${color}`,
  borderRadius: "3px",
  color: color,
  fontSize: "11px",
  fontWeight: "bold",
});

export default THEME;
