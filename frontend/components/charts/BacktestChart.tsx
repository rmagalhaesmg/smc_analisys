"use client";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

interface BacktestChartProps {
  data?: Array<{ time: string; points: number }>;
}

export default function BacktestChart({ data = [] }: BacktestChartProps) {
  const defaultData = [
    { time: "09:00", points: 0 },
    { time: "09:30", points: 1.2 },
    { time: "10:00", points: 0.8 },
    { time: "10:30", points: 2.5 },
    { time: "11:00", points: 3.2 },
    { time: "11:30", points: 2.8 },
    { time: "12:00", points: 4.1 },
    { time: "12:30", points: 3.5 },
    { time: "13:00", points: 5.2 },
    { time: "13:30", points: 4.8 },
    { time: "14:00", points: 6.1 },
    { time: "14:30", points: 5.5 },
    { time: "15:00", points: 7.2 },
    { time: "15:30", points: 6.8 },
    { time: "16:00", points: 8.5 },
  ];

  const chartData = data.length > 0 ? data : defaultData;

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <h3 className="text-lg font-bold text-white mb-4">📈 Backtest - Pontos Acumulados</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <XAxis dataKey="time" stroke="#6B7280" />
          <YAxis stroke="#6B7280" />
          <Tooltip
            contentStyle={{ backgroundColor: "#1F2937", border: "1px solid #374151" }}
            labelStyle={{ color: "#F9FAFB" }}
          />
          <Line
            type="monotone"
            dataKey="points"
            stroke="#06B6D4"
            strokeWidth={2}
            dot={{ fill: "#06B6D4", r: 3 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
