"use client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

interface AccuracyChartProps {
  data?: Array<{ label: string; value: number }>;
}

export default function AccuracyChart({ data = [] }: AccuracyChartProps) {
  const defaultData = [
    { label: "WIN", value: 67 },
    { label: "LOSS", value: 33 },
  ];

  const chartData = data.length > 0 ? data : defaultData;

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <h3 className="text-lg font-bold text-white mb-4">📊 Assertividade</h3>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={chartData} layout="vertical">
          <XAxis type="number" domain={[0, 100]} stroke="#6B7280" />
          <YAxis type="category" dataKey="label" stroke="#6B7280" width={60} />
          <Tooltip
            contentStyle={{ backgroundColor: "#1F2937", border: "1px solid #374151" }}
            labelStyle={{ color: "#F9FAFB" }}
            formatter={(value: number) => [`${value}%`, "Percentual"]}
          />
          <Bar dataKey="value" radius={[0, 4, 4, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={index === 0 ? "#10B981" : "#EF4444"} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="flex justify-center gap-6 mt-4">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-green-500"></div>
          <span className="text-gray-400 text-sm">WIN ({chartData[0]?.value}%)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-red-500"></div>
          <span className="text-gray-400 text-sm">LOSS ({chartData[1]?.value}%)</span>
        </div>
      </div>
    </div>
  );
}
