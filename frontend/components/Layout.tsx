import React from "react";
import Link from "next/link";

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col">
      <nav className="bg-gray-800 text-white p-4">
        <Link href="/dashboard" className="mr-4">Dashboard</Link>
        <Link href="/history" className="mr-4">Histórico</Link>
        <Link href="/upload" className="mr-4">Upload CSV</Link>
        <Link href="/billing" className="mr-4">Assinatura</Link>
      </nav>
      <main className="flex-grow p-6">{children}</main>
    </div>
  );
};

export default Layout;
