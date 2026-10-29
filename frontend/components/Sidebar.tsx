"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  Compass, 
  History, 
  BookOpen, 
  Settings, 
  Sparkles, 
  Layers, 
  ChevronRight,
  ExternalLink
} from "lucide-react";
import { getSettings } from "@/lib/api";

export default function Sidebar() {
  const pathname = usePathname();
  const [isDemo, setIsDemo] = useState<boolean>(true);

  useEffect(() => {
    getSettings()
      .then((data) => setIsDemo(data.is_demo_mode))
      .catch(() => setIsDemo(true));
  }, [pathname]);

  const navItems = [
    { label: "New Research", href: "/", icon: Compass },
    { label: "Research History", href: "/history", icon: History },
    { label: "Knowledge Base", href: "/knowledge", icon: BookOpen },
    { label: "Settings", href: "/settings", icon: Settings },
  ];

  return (
    <aside className="w-64 bg-white border-r border-slate-200 flex flex-col h-screen select-none shrink-0 sticky top-0 z-30">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-100 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center text-white shadow-sm shadow-brand-500/20 group-hover:scale-105 transition-transform">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="font-semibold text-slate-900 leading-tight tracking-tight flex items-center gap-1.5">
              ResearchFlow <span className="text-brand-600 text-xs font-bold px-1.5 py-0.5 rounded bg-brand-50 border border-brand-100">AI</span>
            </div>
            <div className="text-[11px] text-slate-400 font-medium">Research-to-Action</div>
          </div>
        </Link>
      </div>

      {/* Navigation */}
      <div className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
        <div className="text-[10px] uppercase font-bold tracking-wider text-slate-400 px-3 py-1.5">
          Workspace
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? "bg-brand-50 text-brand-700 shadow-xs"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? "text-brand-600" : "text-slate-400"}`} />
                <span>{item.label}</span>
              </div>
              {isActive && <ChevronRight className="w-3.5 h-3.5 text-brand-500" />}
            </Link>
          );
        })}
      </div>

      {/* Mode Status Pill */}
      <div className="p-4 border-t border-slate-100 bg-slate-50/60">
        <div className="bg-white p-3 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between text-xs mb-1">
            <span className="font-semibold text-slate-700">Agent Engine</span>
            <span className={`inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full ${
              isDemo ? "bg-amber-50 text-amber-700 border border-amber-200" : "bg-emerald-50 text-emerald-700 border border-emerald-200"
            }`}>
              <span className={`w-1.5 h-1.5 rounded-full ${isDemo ? "bg-amber-500" : "bg-emerald-500 animate-pulse"}`}></span>
              {isDemo ? "Demo Synthesis" : "Live API Grounded"}
            </span>
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed">
            {isDemo
              ? "Running in offline synthesis mode. Add API keys in Settings for live web crawling."
              : "Full live multi-agent graph with web search & evidence verification active."}
          </p>
        </div>
      </div>
    </aside>
  );
}
