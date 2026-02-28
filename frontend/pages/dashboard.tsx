import Layout from "../components/Layout";
import StatCard from "../components/StatCard";
import AccuracyChart from "../components/AccuracyChart";
import PointsChart from "../components/PointsChart";

export default function Dashboard() {
  return (
    <Layout>
      <div className="grid grid-cols-4 gap-4">
        <StatCard title="Total de Sinais" value="124" />
        <StatCard title="Assertividade" value="63.7%" />
        <StatCard title="Pontos Médios" value="+1.8" />
        <StatCard title="Último Sinal" value="Compra" />
      </div>

      <div className="grid grid-cols-2 gap-6 mt-6">
        <AccuracyChart />
        <PointsChart />
      </div>
    </Layout>
  );
}
