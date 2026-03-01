"use client";
import { useState } from "react";
import { useWebSocket } from "../lib/useWebSocket";

interface DataSource {
  active: boolean;
  latency?: number;
}

interface DataSourceStatusData {
  csv?: DataSource;
  rtd?: DataSource;
  api?: DataSource;
  dll?: DataSource;
}

export default function DataSourceStatus() {
  const [status, setStatus] = useState<DataSourceStatusData>({
    csv: { active: false },
    rtd: { active: true, latency: 120 },
    api: { active: true },
    dll: { active: false },
  });

  useWebSocket({
    onMessage: (msg) => {
      if (msg.type === "datasource_status") {
        setStatus(msg.data);
      }
    },
  });

  const getSourceIcon = (key: string) => {
    switch (key) {
      case "csv":
        return "📄";
      case "rtd":
        return "📡";
      case "api":
        return "🌐";
      case "dll":
        return "🔗";
      default:
        return "❓";
    }
  };

  const getSourceName = (key: string) => {
    switch (key) {
      case "csv":
        return "CSV (Profit)";
      case "rtd":
        return "RTD (Tempo Real)";
      case "api":
        return "API Externa";
      case "dll":
        return "DLL Local";
      default:
        return key.toUpperCase();
    }
  };

  return (
    <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
      <h3 className="text-sm font-bold text-gray-400 mb-3">📡 Status das Fontes de Dados</h3>
      <div className="flex flex-wrap gap-3">
        {Object.entries(status).map(([key, value]: [string, any]) => (
          <div
            key={key}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg ${
              value.active ? "bg-green-500/10" : "bg-gray-700/50"
            }`}
          >
            <span className="text-lg">{getSourceIcon(key)}</span>
            <div>
              <p className="text-sm font-medium text-gray-300">{getSourceName(key)}</p>
              <div className="flex items-center gap-1">
                <span
                  className={`w-2 h-2 rounded-full ${
                    value.active ? "bg-green-500" : "bg-gray-500"
                  }`}
                ></span>
                <span className="text-xs text-gray-400">
                  {value.active ? "Conectado" : "Inativo"}
                  {value.latency && ` • ${value.latency}ms`}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
