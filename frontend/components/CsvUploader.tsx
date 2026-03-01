"use client";
import { useState } from "react";

interface CsvUploaderProps {
  onUpload?: (file: File) => void;
}

export default function CsvUploader({ onUpload }: CsvUploaderProps) {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  const handleUpload = async (e: any) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith(".csv")) {
      setMessage({ type: "error", text: "Por favor, envie um arquivo CSV." });
      return;
    }

    setUploading(true);
    setMessage(null);

    try {
      // Simula upload - substitua pela chamada real à API
      // const formData = new FormData();
      // formData.append("file", file);
      // await fetch("/api/data/upload-csv", { method: "POST", body: formData });
      
      await new Promise((resolve) => setTimeout(resolve, 1500));
      
      setMessage({ type: "success", text: `Arquivo "${file.name}" processado com sucesso!` });
      onUpload?.(file);
    } catch (error) {
      setMessage({ type: "error", text: "Erro ao processar arquivo. Tente novamente." });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <h3 className="text-lg font-bold text-white mb-4">📁 Upload de CSV (Profit)</h3>
      
      <div className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center hover:border-cyan-500 transition-colors">
        <input
          type="file"
          accept=".csv"
          onChange={handleUpload}
          disabled={uploading}
          className="hidden"
          id="csv-upload"
        />
        <label htmlFor="csv-upload" className="cursor-pointer">
          <div className="text-4xl mb-3">📤</div>
          <p className="text-gray-300 font-medium">
            {uploading ? "Processando..." : "Clique para selecionar um arquivo CSV"}
          </p>
          <p className="text-gray-500 text-sm mt-1">
            Formato aceito: .csv (Profit Pro, Profit Excel)
          </p>
        </label>
      </div>

      {message && (
        <div
          className={`mt-4 p-3 rounded-lg text-sm ${
            message.type === "success"
              ? "bg-green-500/20 text-green-400 border border-green-500/30"
              : "bg-red-500/20 text-red-400 border border-red-500/30"
          }`}
        >
          {message.text}
        </div>
      )}

      <div className="mt-4 p-4 bg-gray-700/50 rounded-lg">
        <h4 className="text-sm font-semibold text-gray-300 mb-2">📋 Estratura esperada:</h4>
        <code className="text-xs text-gray-400 block">
          Data,Hora,Ativo,Direção,Entrada,Saída,Pontos
        </code>
        <code className="text-xs text-gray-400 block">
          01/02/2025,09:45,WDO,FALSE,250.00,251.50,+1.5
        </code>
      </div>
    </div>
  );
}
