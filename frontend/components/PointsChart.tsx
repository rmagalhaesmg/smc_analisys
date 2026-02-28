import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
  { date: "2026-01-01", points: 1.2 },
  { date: "2026-01-02", points: -0.5 },
  { date: "2026-01-03", points: 0.8 },
];

const PointsChart: React.FC = () => (
  <ResponsiveContainer width="100%" height={300}>
    <BarChart data={data}>
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="points" fill="#82ca9d" />
    </BarChart>
  </ResponsiveContainer>
);

export default PointsChart;
