"use client";
import { useEffect, useRef, useCallback, useState } from "react";

interface WebSocketMessage {
  type: string;
  data: any;
}

interface UseWebSocketOptions {
  url?: string;
  onMessage?: (data: WebSocketMessage) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  reconnectAttempts?: number;
  reconnectInterval?: number;
}

export function useWebSocket({
  url,
  onMessage,
  onConnect,
  onDisconnect,
  reconnectAttempts = 5,
  reconnectInterval = 3000,
}: UseWebSocketOptions = {}) {
  const ws = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const attemptsRef = useRef(0);

  const connect = useCallback(() => {
    if (!url) return;

    const wsUrl = url || "ws://localhost:8000/ws/realtime";
    const token = localStorage.getItem("token");
    const finalUrl = token ? `${wsUrl}?token=${token}` : wsUrl;

    ws.current = new WebSocket(finalUrl);

    ws.current.onopen = () => {
      setIsConnected(true);
      attemptsRef.current = 0;
      onConnect?.();
    };

    ws.current.onmessage = (event: any) => {
      try {
        const data = JSON.parse(event.data);
        setLastMessage(data);
        onMessage?.(data);
      } catch (e) {
        console.error("Failed to parse WebSocket message:", e);
      }
    };

    ws.current.onclose = () => {
      setIsConnected(false);
      onDisconnect?.();

      // Tentativa de reconexão
      if (attemptsRef.current < reconnectAttempts) {
        attemptsRef.current += 1;
        setTimeout(connect, reconnectInterval);
      }
    };

    ws.current.onerror = (error: any) => {
      console.error("WebSocket error:", error);
    };
  }, [url, onMessage, onConnect, onDisconnect, reconnectAttempts, reconnectInterval]);

  const send = useCallback((message: any) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  }, []);

  const disconnect = useCallback(() => {
    if (ws.current) {
      ws.current.close();
      ws.current = null;
    }
  }, []);

  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    isConnected,
    lastMessage,
    send,
    connect,
    disconnect,
  };
}
