import React from "react";

const dummy = [
  { date: "2026-01-01", direction: "Buy", points: 1.2, result: "Fav" },
  { date: "2026-01-02", direction: "Sell", points: -0.5, result: "Contra" },
];

const SignalsTable: React.FC = () => (
  <table className="min-w-full bg-white">
    <thead>
      <tr>
        <th className="py-2">Data</th>
        <th className="py-2">Direção</th>
        <th className="py-2">Pontos</th>
        <th className="py-2">Resultado</th>
      </tr>
    </thead>
    <tbody>
      {dummy.map((row, idx) => (
        <tr key={idx} className="text-center">
          <td className="py-2">{row.date}</td>
          <td className="py-2">{row.direction}</td>
          <td className="py-2">{row.points}</td>
          <td className="py-2">{row.result}</td>
        </tr>
      ))}
    </tbody>
  </table>
);

export default SignalsTable;
