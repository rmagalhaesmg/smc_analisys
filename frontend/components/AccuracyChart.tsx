import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
  { date: "2026-01-01", accuracy: 60 },
  { date: "2026-01-02", accuracy: 62 },
  { date: "2026-01-03", accuracy: 64 },
];

const AccuracyChart: React.FC = () => (
  <ResponsiveContainer width="100%" height={300}>
    <LineChart data={data}>
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="accuracy" stroke="#8884d8" />
    </LineChart>
  </ResponsiveContainer>
);

export default AccuracyChart;
