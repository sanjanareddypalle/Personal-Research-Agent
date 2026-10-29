"use client";

import React, { useEffect, useState } from "react";
import { Settings as SettingsIcon, Key, CheckCircle2, AlertTriangle, ShieldCheck } from "lucide-react";
import { getSettings, updateSettings } from "@/lib/api";
import { SettingsResponse } from "@/types";

export default function SettingsPage() {
  const [settings, setSettings] = useState<SettingsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [savedMessage, setSavedMessage] = useState("");

  const [llmProvider, setLlmProvider] = useState("gemini");
  const [searchProvider, setSearchProvider] = useState("duckduckgo");
  const [demoMode, setDemoMode] = useState(false);

  useEffect(() => {
    getSettings()
      .then((data) => {
        setSettings(data);
        setLlmProvider(data.llm_provider);
        setSearchProvider(data.search_provider);
        setDemoMode(data.is_demo_mode);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await updateSettings({
        llm_provider: llmProvider,
        search_provider: searchProvider,
        demo_mode: demoMode,
      });
      setSavedMessage("Settings saved successfully!");
      setTimeout(() => setSavedMessage(""), 3000);
    } catch (err: any) {
      alert("Failed to save settings");
    }
  };

  if (loading || !settings) {
    return <div className="p-12 text-center text-xs text-slate-400">Loading settings...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-10 w-full space-y-8">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          System Settings & Credentials
        </h1>
        <p className="text-slate-600 text-sm mt-1">
          Configure model providers, web search services, and execution modes.
        </p>
      </div>

      {savedMessage && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-semibold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{savedMessage}</span>
        </div>
      )}

      {/* Credential Status Cards */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
          <Key className="w-4 h-4 text-brand-600" /> API Key Detection Status
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl border border-slate-100 bg-slate-50/70 space-y-1">
            <span className="text-xs font-semibold text-slate-500">Google Gemini API</span>
            <div className="flex items-center gap-1.5 pt-1">
              <span className={`w-2 h-2 rounded-full ${settings.has_gemini_key ? "bg-emerald-500" : "bg-amber-400"}`}></span>
              <span className="text-xs font-bold text-slate-800">
                {settings.has_gemini_key ? "Detected & Active" : "Not Configured"}
              </span>
            </div>
          </div>
          <div className="p-4 rounded-xl border border-slate-100 bg-slate-50/70 space-y-1">
            <span className="text-xs font-semibold text-slate-500">OpenAI API</span>
            <div className="flex items-center gap-1.5 pt-1">
              <span className={`w-2 h-2 rounded-full ${settings.has_openai_key ? "bg-emerald-500" : "bg-amber-400"}`}></span>
              <span className="text-xs font-bold text-slate-800">
                {settings.has_openai_key ? "Detected & Active" : "Not Configured"}
              </span>
            </div>
          </div>
          <div className="p-4 rounded-xl border border-slate-100 bg-slate-50/70 space-y-1">
            <span className="text-xs font-semibold text-slate-500">Tavily Search API</span>
            <div className="flex items-center gap-1.5 pt-1">
              <span className={`w-2 h-2 rounded-full ${settings.has_tavily_key ? "bg-emerald-500" : "bg-amber-400"}`}></span>
              <span className="text-xs font-bold text-slate-800">
                {settings.has_tavily_key ? "Detected & Active" : "DuckDuckGo Default"}
              </span>
            </div>
          </div>
        </div>

        <p className="text-xs text-slate-500 leading-relaxed pt-2 border-t border-slate-100">
          To supply live API keys, populate your backend <code className="bg-slate-100 px-1 py-0.5 rounded font-mono text-[11px]">.env</code> file with 
          <code className="bg-slate-100 px-1 py-0.5 rounded font-mono text-[11px]"> GEMINI_API_KEY</code> or 
          <code className="bg-slate-100 px-1 py-0.5 rounded font-mono text-[11px]"> OPENAI_API_KEY</code>.
        </p>
      </div>

      {/* Configuration Form */}
      <form onSubmit={handleSave} className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-6">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
          Runtime Configuration
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1.5">
              LLM Provider
            </label>
            <select
              value={llmProvider}
              onChange={(e) => setLlmProvider(e.target.value)}
              className="w-full text-xs p-2.5 rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-brand-500 font-medium"
            >
              <option value="gemini">Google Gemini (gemini-2.5-flash)</option>
              <option value="openai">OpenAI (gpt-4o-mini)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1.5">
              Web Search Engine
            </label>
            <select
              value={searchProvider}
              onChange={(e) => setSearchProvider(e.target.value)}
              className="w-full text-xs p-2.5 rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-brand-500 font-medium"
            >
              <option value="duckduckgo">DuckDuckGo Search (Default, Free)</option>
              <option value="tavily">Tavily Research API</option>
            </select>
          </div>
        </div>

        <div className="pt-4 border-t border-slate-100">
          <label className="flex items-start gap-3 cursor-pointer">
            <input
              type="checkbox"
              checked={demoMode}
              onChange={(e) => setDemoMode(e.target.checked)}
              className="mt-0.5 w-4 h-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
            />
            <div>
              <span className="text-xs font-bold text-slate-900">Force Demo Mode</span>
              <p className="text-[11px] text-slate-500">
                When enabled, the agent executes offline with deterministic synthesized data without calling external LLM endpoints.
              </p>
            </div>
          </label>
        </div>

        <div className="pt-2 flex justify-end">
          <button
            type="submit"
            className="bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold px-5 py-2.5 rounded-xl transition-colors shadow-xs"
          >
            Save Configuration
          </button>
        </div>
      </form>
    </div>
  );
}
