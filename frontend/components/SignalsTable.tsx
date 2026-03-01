"use client";
import { useState, useEffect } from "react";

interface Signal {
  time: string;
  direction: "BUY" | "SELL";
  score: number;
  partial_points: number;
  result?: "WIN" | "LOSS" | "PENDING";
}

interface SignalsTableProps {
  signals?: Signal[];
}

export default function SignalsTable({ signals: initialSignals = [] }: SignalsTableProps) {
  const [signals, setSignals] = useState<Signal[]>(initialSignals);

  const defaultSignals: Signal[] = [
    { time: "14:30", direction: "BUY", score: 0.82, partial_points: 1.5, result: "WIN" },
    { time: "13:45", direction: "SELL", score: 0.78, partial_points: -0.8, result: "LOSS" },
    { time: "12:20", direction: "BUY", score: 0.85, partial_points: 2.1, result: "WIN" },
    { time: "11:15", direction: "BUY", score: 0.75, partial_points: 0.5, result: "WIN" },
    { time: "10:30", direction: "SELL", score: 0.88, partial_points: -1.2, result: "LOSS" },
    { time: "09:45", direction: "BUY", score: 0.79, partial_points: 1.8, result: "WIN" },
  ];

  const displaySignals = signals.length > 0 ? signals : defaultSignals;

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <h3 className="text-lg font-bold text-white mb-4">🎯 Sinais Recentes</h3>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="text-gray-400 text-sm border-b border-gray-700">
              <th className="text-left py-3 px-2">Hora</th>
              <th className="text-left py-3 px-2">Direção</th>
              <th className="text-left py-3 px-2">Score</th>
              <th className="text-left py-3 px-2">Pontos</th>
              <th className="text-left py-3 px-2">Resultado</th>
            </tr>
          </thead>
          <tbody>
            {displaySignals.map((signal, index) => (
              <tr key={index} className="border-b border-gray-700/50 hover:bg-gray-700/30">
                <td className="py-3 px-2 text-gray-300">{signal.time}</td>
                <td className="py-3 px-2">
                  <span
                    className={`px-2 py-1 rounded text-xs font-bold ${
                      signal.direction === "BUY"
                        ? "bg-green-500/20 text-green-400"
                        : "bg-red-500/20 text-red-400"
                    }`}
                  >
                    {signal.direction}
                  </span>
                </td>
                <td className="py-3 px-2 text-gray-300">{(signal.score * 100).toFixed(0)}%</td>
                <td
                  className={`py-3 px-2 font-bold ${
                    signal.partial_points >= 0 ? "text-green-400" : "text-red-400"
                  }`}
                >
                  {signal.partial_points > 0 ? "+" : ""}
                  {signal.partial_points}
                </td>
                <td className="py-3 px-2">
                  {signal.result && (
                    <span
                      className={`px-2 py-1 rounded text-xs ${
                        signal.result === "WIN"
                          ? "bg-green-500/20 text-green-400"
                          : signal.result === "LOSS"
                          ? "bg-red-500/20 text-red-400"
                          : "bg-yellow-500/20 text-yellow-400"
                      }`}
                    >
                      {signal.result}
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
