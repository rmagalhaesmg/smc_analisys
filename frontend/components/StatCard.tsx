import React from "react";

interface Props {
  title: string;
  value: string;
}

const StatCard: React.FC<Props> = ({ title, value }) => (
  <div className="p-4 shadow rounded bg-white">
    <div className="text-sm text-gray-500">{title}</div>
    <div className="text-2xl font-bold">{value}</div>
  </div>
);

export default StatCard;
