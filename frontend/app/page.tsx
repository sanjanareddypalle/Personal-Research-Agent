"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { 
  Sparkles, 
  ArrowRight, 
  Layers, 
  Search, 
  FileText, 
  Sliders, 
  CheckSquare, 
  AlertCircle,
  HelpCircle,
  Languages,
  GraduationCap,
  Clock,
  Youtube,
  BookOpen
} from "lucide-react";
import { createResearchJob } from "@/lib/api";
import LiveProgressTimeline from "@/components/LiveProgressTimeline";

const EXAMPLE_PROMPTS = [
  "How can I become a Generative AI Engineer in 6 months?",
  "What GenAI skills should I learn to become an AI engineer in 2027?",
  "How will compound AI systems and multi-agent workflows evolve by 2026?",
  "Comparing vLLM, TensorRT-LLM, and Ollama for high-throughput enterprise serving."
];

const LANGUAGE_OPTIONS = [
  { id: "en", label: "English", sublabel: "Global resources & docs", flag: "🌐" },
  { id: "te", label: "Telugu (తెలుగు)", sublabel: "తెలుగు వీడియోలు & ట్యుటోరియల్స్", flag: "🇮🇳" },
  { id: "hi", label: "Hindi (हिन्दी)", sublabel: "हिन्दी वीडियो व ट्यूटोरियल", flag: "🇮🇳" }
];

const SKILL_LEVEL_OPTIONS = [
  { id: "beginner", label: "Beginner", desc: "Starting fresh with fundamentals" },
  { id: "intermediate", label: "Intermediate", desc: "Prior programming or ML basics" },
  { id: "advanced", label: "Advanced", desc: "Production scaling & systems" }
];

const STUDY_TIME_OPTIONS = [
  { id: "5-10", label: "5-10 hrs/wk", desc: "Steady part-time" },
  { id: "10-15", label: "10-15 hrs/wk", desc: "Recommended pace" },
  { id: "15-20", label: "15-20 hrs/wk", desc: "Intensive track" },
  { id: "20+", label: "20+ hrs/wk", desc: "Full-time immersion" }
];

export default function WorkspacePage() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [depth, setDepth] = useState<"quick" | "standard" | "comprehensive">("standard");
  const [language, setLanguage] = useState<string>("en");
  const [skillLevel, setSkillLevel] = useState<string>("beginner");
  const [studyTime, setStudyTime] = useState<string>("10-15");
  const [constraints, setConstraints] = useState("");
  const [selectedSources, setSelectedSources] = useState<string[]>([
    "documentation",
    "research_papers",
    "industry_reports",
    "general_web"
  ]);
  const [includeKb, setIncludeKb] = useState(true);

  // Active Research State
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const [currentStageIdx, setCurrentStageIdx] = useState(0);
  const [latestLogMessage, setLatestLogMessage] = useState("");
  const [isCompleted, setIsCompleted] = useState(false);
  const [isFailed, setIsFailed] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const toggleSource = (src: string) => {
    if (selectedSources.includes(src)) {
      if (selectedSources.length > 1) {
        setSelectedSources(selectedSources.filter((s) => s !== src));
      }
    } else {
      setSelectedSources([...selectedSources, src]);
    }
  };

  const handleStartResearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!query.trim() || isSubmitting) return;

    setIsSubmitting(true);
    setIsCompleted(false);
    setIsFailed(false);
    setCurrentStageIdx(1);
    setLatestLogMessage("Initializing research agent graph...");

    try {
      const { id } = await createResearchJob({
        query: query.trim(),
        depth,
        constraints: constraints.trim() || undefined,
        source_preferences: selectedSources,
        include_knowledge_base: includeKb,
        language,
        skill_level: skillLevel,
        study_time_hours_per_week: studyTime,
      });

      setActiveJobId(id);

      // Connect to SSE stream
      const eventSource = new EventSource(`http://localhost:8005/api/research/${id}/events`);

      eventSource.addEventListener("stage_change", (event) => {
        try {
          const data = JSON.parse(event.data);
          setCurrentStageIdx(data.stage_index);
          setLatestLogMessage(data.message || `Processing Stage ${data.stage_index}...`);
        } catch (err) {
          console.error("Error parsing SSE event:", err);
        }
      });

      eventSource.addEventListener("complete", (event) => {
        try {
          const data = JSON.parse(event.data);
          setCurrentStageIdx(9);
          setIsCompleted(true);
          setIsSubmitting(false);
          setLatestLogMessage("Research report and roadmap compiled successfully.");
          eventSource.close();
        } catch (err) {
          console.error("Error parsing complete event:", err);
        }
      });

      eventSource.addEventListener("error", (event) => {
        try {
          const data = JSON.parse((event as any).data || "{}");
          setIsFailed(true);
          setErrorMessage(data.message || "An unexpected error occurred during execution.");
        } catch {
          // If network error
        }
        setIsSubmitting(false);
        eventSource.close();
      });

    } catch (err: any) {
      setIsFailed(true);
      setErrorMessage(err.message || "Failed to start research");
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-6 py-10 w-full space-y-10">
      {/* Header Section */}
      <div className="space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-50 border border-brand-100 text-brand-700 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5" />
          Autonomous Multi-Stage Evidence & Learning Agent
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Turn research into action.
        </h1>
        <p className="text-slate-600 text-base max-w-2xl leading-relaxed">
          Transform open research inquiries into verified, empirical research reports, curated multilingual YouTube tutorials, and personalized execution roadmaps.
        </p>
      </div>

      {!activeJobId ? (
        /* Setup & Input Form */
        <form onSubmit={handleStartResearch} className="bg-white rounded-2xl border border-slate-200/90 p-6 sm:p-8 shadow-xs space-y-6">
          {/* Main Question Area */}
          <div className="space-y-2">
            <label htmlFor="query" className="block text-sm font-bold text-slate-800">
              Research Inquiry or Learning Goal
            </label>
            <div className="relative">
              <textarea
                id="query"
                rows={3}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. How can I become a Generative AI Engineer in 6 months?"
                className="w-full text-slate-900 placeholder:text-slate-400 p-4 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-all resize-none text-base"
              />
            </div>
          </div>

          {/* Example Prompts */}
          <div className="space-y-2">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Example Inquiries</span>
            <div className="flex flex-wrap gap-2">
              {EXAMPLE_PROMPTS.map((prompt, i) => (
                <button
                  type="button"
                  key={i}
                  onClick={() => {
                    setQuery(prompt);
                    if (prompt.includes("6 months")) {
                      setConstraints("6-month timeline, practical focus");
                    }
                  }}
                  className="text-xs bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200/70 rounded-lg px-3 py-1.5 transition-colors text-left font-medium"
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>

          {/* Multilingual Learning Language Selection */}
          <div className="pt-2 border-t border-slate-100 space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                <Languages className="w-4 h-4 text-brand-600" />
                Preferred Learning Language
              </label>
              <span className="text-xs text-slate-500">Curates native tutorials in selected language</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {LANGUAGE_OPTIONS.map((lang) => (
                <button
                  type="button"
                  key={lang.id}
                  onClick={() => setLanguage(lang.id)}
                  className={`p-3 rounded-xl border text-left transition-all ${
                    language === lang.id
                      ? "bg-brand-50/70 border-brand-500 ring-2 ring-brand-500/20 text-slate-900"
                      : "bg-white border-slate-200 text-slate-600 hover:border-slate-300"
                  }`}
                >
                  <div className="flex items-center justify-between font-bold text-sm">
                    <span className="flex items-center gap-1.5">
                      <span>{lang.flag}</span>
                      <span>{lang.label}</span>
                    </span>
                    {language === lang.id && <div className="w-2 h-2 rounded-full bg-brand-600" />}
                  </div>
                  <div className="text-[11px] text-slate-500 mt-1">{lang.sublabel}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Skill Level & Study Time Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5 pt-2 border-t border-slate-100">
            {/* Skill Level */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                <GraduationCap className="w-4 h-4 text-brand-600" />
                Current Skill Level
              </label>
              <div className="grid grid-cols-3 gap-2">
                {SKILL_LEVEL_OPTIONS.map((lvl) => (
                  <button
                    type="button"
                    key={lvl.id}
                    onClick={() => setSkillLevel(lvl.id)}
                    className={`p-2.5 rounded-lg border text-center transition-all ${
                      skillLevel === lvl.id
                        ? "bg-brand-50 border-brand-500 text-brand-900 font-bold"
                        : "bg-white border-slate-200 text-slate-600 hover:border-slate-300 font-medium text-xs"
                    }`}
                  >
                    <div className="text-xs">{lvl.label}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Weekly Study Commitment */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                <Clock className="w-4 h-4 text-brand-600" />
                Weekly Study Time
              </label>
              <div className="grid grid-cols-4 gap-2">
                {STUDY_TIME_OPTIONS.map((time) => (
                  <button
                    type="button"
                    key={time.id}
                    onClick={() => setStudyTime(time.id)}
                    className={`p-2.5 rounded-lg border text-center transition-all ${
                      studyTime === time.id
                        ? "bg-brand-50 border-brand-500 text-brand-900 font-bold"
                        : "bg-white border-slate-200 text-slate-600 hover:border-slate-300 font-medium text-xs"
                    }`}
                  >
                    <div className="text-xs">{time.label}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Research Depth & Source Preferences */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2 border-t border-slate-100">
            {/* Depth Selector */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                <Sliders className="w-4 h-4 text-brand-600" />
                Research Depth
              </label>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { id: "quick", label: "Quick", desc: "Rapid summary" },
                  { id: "standard", label: "Standard", desc: "Balanced research" },
                  { id: "comprehensive", label: "Comprehensive", desc: "Exhaustive deep-dive" },
                ].map((d) => (
                  <button
                    type="button"
                    key={d.id}
                    onClick={() => setDepth(d.id as any)}
                    className={`p-2.5 rounded-lg border text-center transition-all ${
                      depth === d.id
                        ? "bg-brand-50 border-brand-500 text-brand-900 font-bold"
                        : "bg-white border-slate-200 text-slate-600 hover:border-slate-300 font-medium text-xs"
                    }`}
                  >
                    <div className="text-xs">{d.label}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Source Preferences */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                <Search className="w-4 h-4 text-brand-600" />
                Source Preferences
              </label>
              <div className="grid grid-cols-2 gap-2 text-xs">
                {[
                  { id: "documentation", label: "Official Docs" },
                  { id: "research_papers", label: "Papers (arXiv)" },
                  { id: "industry_reports", label: "Industry Reports" },
                  { id: "general_web", label: "General Web" },
                ].map((src) => {
                  const isChecked = selectedSources.includes(src.id);
                  return (
                    <label
                      key={src.id}
                      onClick={() => toggleSource(src.id)}
                      className={`flex items-center gap-2 p-2 rounded-lg border cursor-pointer select-none transition-all ${
                        isChecked
                          ? "bg-slate-50 text-slate-900 border-slate-300"
                          : "text-slate-400 border-slate-100 opacity-60"
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={isChecked}
                        onChange={() => {}}
                        className="rounded border-slate-300 text-brand-600 focus:ring-brand-500 w-3.5 h-3.5"
                      />
                      <span className="font-medium">{src.label}</span>
                    </label>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Optional Constraints & KB Inclusion */}
          <div className="pt-4 border-t border-slate-100 flex flex-col sm:flex-row gap-4 items-center justify-between">
            <div className="w-full sm:w-2/3">
              <input
                type="text"
                value={constraints}
                onChange={(e) => setConstraints(e.target.value)}
                placeholder="Optional constraints (e.g. 6-month timeline, focus on open-source LLMs)"
                className="w-full text-xs text-slate-800 placeholder:text-slate-400 px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500"
              />
            </div>
            <label className="flex items-center gap-2 text-xs text-slate-600 cursor-pointer self-start sm:self-center">
              <input
                type="checkbox"
                checked={includeKb}
                onChange={(e) => setIncludeKb(e.target.checked)}
                className="rounded border-slate-300 text-brand-600 focus:ring-brand-500 w-3.5 h-3.5"
              />
              <span>Include Knowledge Base (RAG)</span>
            </label>
          </div>

          {/* Primary Action Button */}
          <div className="pt-2 flex justify-end">
            <button
              type="submit"
              disabled={!query.trim() || isSubmitting}
              className="inline-flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold text-sm px-6 py-3 rounded-xl shadow-sm hover:shadow transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span>Start Research</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </form>
      ) : (
        /* Live Execution Workspace */
        <div className="space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs flex items-center justify-between">
            <div>
              <span className="text-xs uppercase font-bold text-slate-400">Research Inquiry</span>
              <h2 className="text-lg font-bold text-slate-900 mt-0.5">{query}</h2>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-medium">
                  {language === "te" ? "Telugu (తెలుగు)" : language === "hi" ? "Hindi (हिन्दी)" : "English"}
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-medium capitalize">
                  {skillLevel}
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-medium">
                  {studyTime} hrs/wk
                </span>
              </div>
            </div>
            {isCompleted && (
              <button
                onClick={() => router.push(`/report/${activeJobId}`)}
                className="inline-flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold text-sm px-5 py-2.5 rounded-xl shadow-sm transition-all"
              >
                <span>View Full Report & Roadmap</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>

          <LiveProgressTimeline
            currentStageIndex={currentStageIdx}
            latestMessage={latestLogMessage}
            isCompleted={isCompleted}
            isFailed={isFailed}
            errorMessage={errorMessage}
          />

          {isCompleted && (
            <div className="p-6 bg-emerald-50 border border-emerald-200 rounded-2xl text-center space-y-3">
              <h3 className="text-base font-bold text-emerald-900">
                Research Analysis, Learning Resources & Roadmap Complete!
              </h3>
              <p className="text-xs text-emerald-700 max-w-lg mx-auto">
                All 9 stages have resolved. Explore your verified evidence, curated {language === "te" ? "Telugu" : language === "hi" ? "Hindi" : "English"} YouTube tutorials & docs, and interactive execution roadmap.
              </p>
              <button
                onClick={() => router.push(`/report/${activeJobId}`)}
                className="inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm px-6 py-2.5 rounded-xl shadow-xs transition-all"
              >
                <span>Open Research Report & Learning Hub</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
