"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import {
  ArrowLeft,
  Download,
  Copy,
  Check,
  Trash2,
  ExternalLink,
  ShieldCheck,
  AlertTriangle,
  Clock,
  Layers,
  CheckCircle2,
  Calendar,
  Sparkles,
  Info,
  Youtube,
  BookOpen,
  Code2,
  Video,
  Languages,
  GraduationCap,
  Briefcase,
  PlayCircle
} from "lucide-react";
import { getResearchJob, updateTaskStatus, deleteResearchJob } from "@/lib/api";
import { ResearchJobDetail, ResearchReport, LearningResourceItem } from "@/types";

type TabType = "overview" | "findings" | "comparison" | "roadmap" | "resources" | "sources" | "methodology";

export default function ReportPage() {
  const { id } = useParams() as { id: string };
  const router = useRouter();

  const [job, setJob] = useState<ResearchJobDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<TabType>("overview");
  const [copiedRoadmap, setCopiedRoadmap] = useState(false);
  const [resourceFilter, setResourceFilter] = useState<string>("all");

  useEffect(() => {
    if (!id) return;
    getResearchJob(id)
      .then((data) => {
        setJob(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  const handleToggleTask = async (taskId: string, currentStatus: boolean) => {
    if (!job || !job.report || !job.report.roadmap) return;
    const newStatus = !currentStatus;

    // Optimistically update state
    const updatedPhases = job.report.roadmap.phases.map((phase) => ({
      ...phase,
      tasks: phase.tasks.map((t) => (t.id === taskId ? { ...t, is_completed: newStatus } : t)),
    }));

    setJob({
      ...job,
      report: {
        ...job.report,
        roadmap: {
          ...job.report.roadmap,
          phases: updatedPhases,
        },
      },
    });

    try {
      await updateTaskStatus(id, taskId, newStatus);
    } catch (err) {
      console.error("Failed to sync task status:", err);
    }
  };

  const handleCopyRoadmap = () => {
    if (!job || !job.report || !job.report.roadmap) return;
    const rm = job.report.roadmap;
    let text = `ROADMAP: ${job.report.title}\n`;
    text += `Timeline: ${rm.total_estimated_timeline}\n`;
    if (job.language) {
      text += `Language: ${job.language} | Skill Level: ${job.skill_level || 'beginner'} | Hours: ${job.study_time_hours_per_week || '10-15'} hrs/wk\n`;
    }
    text += "\n";
    rm.phases.forEach((p) => {
      text += `Phase ${p.phase_number}: ${p.phase_title} (${p.duration})\n`;
      text += `Milestone: ${p.milestone}\n`;
      if (p.phase_project) {
        text += `Project: ${p.phase_project}\n`;
      }
      p.tasks.forEach((t) => {
        text += `  [${t.is_completed ? "X" : " "}] ${t.title} - ${t.deliverable}\n`;
        if (t.practical_exercise) {
          text += `      Exercise: ${t.practical_exercise}\n`;
        }
      });
      text += "\n";
    });

    navigator.clipboard.writeText(text);
    setCopiedRoadmap(true);
    setTimeout(() => setCopiedRoadmap(false), 2000);
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this research report?")) return;
    try {
      await deleteResearchJob(id);
      router.push("/history");
    } catch (err) {
      alert("Failed to delete report.");
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center p-12">
        <div className="text-center space-y-3">
          <div className="w-8 h-8 border-3 border-brand-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-xs text-slate-500 font-medium">Loading research report...</p>
        </div>
      </div>
    );
  }

  if (!job || !job.report) {
    return (
      <div className="max-w-4xl mx-auto px-6 py-16 text-center space-y-4">
        <h2 className="text-xl font-bold text-slate-900">Report Not Found or Still Processing</h2>
        <p className="text-sm text-slate-500">This report has not finished compiling or was removed.</p>
        <Link href="/" className="inline-flex items-center gap-2 text-sm text-brand-600 font-semibold hover:underline">
          <ArrowLeft className="w-4 h-4" /> Back to Workspace
        </Link>
      </div>
    );
  }

  const report = job.report;
  const roadmap = report.roadmap;
  const learningResources: LearningResourceItem[] = report.learning_resources || job.learning_resources || [];

  let totalTasks = 0;
  let completedTasks = 0;
  if (roadmap && roadmap.phases) {
    roadmap.phases.forEach((p) => {
      p.tasks.forEach((t) => {
        totalTasks++;
        if (t.is_completed) completedTasks++;
      });
    });
  }
  const completionPct = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  const filteredResources = learningResources.filter((r) => {
    if (resourceFilter === "all") return true;
    if (resourceFilter === "youtube") return r.resource_type.includes("youtube");
    if (resourceFilter === "docs") return r.resource_type === "documentation";
    if (resourceFilter === "practice") return r.resource_type === "practice";
    return true;
  });

  const languageLabel = job.language === "te" ? "Telugu (తెలుగు)" : job.language === "hi" ? "Hindi (हिन्दी)" : "English";

  const tabs: { id: TabType; label: string; count?: number }[] = [
    { id: "overview", label: "Overview" },
    { id: "findings", label: "Key Findings", count: report.key_findings.length },
    { id: "comparison", label: "Evidence Matrix", count: report.evidence_comparisons.length },
    { id: "roadmap", label: "Action Roadmap", count: totalTasks },
    { id: "resources", label: "Learning Resources", count: learningResources.length },
    { id: "sources", label: "Sources", count: report.sources_and_citations.length },
    { id: "methodology", label: "Methodology" },
  ];

  return (
    <div className="max-w-6xl mx-auto px-6 py-8 w-full space-y-8">
      {/* Top Navigation & Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-200">
        <Link href="/history" className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-900 transition-colors">
          <ArrowLeft className="w-3.5 h-3.5" /> Back to History
        </Link>
        
        <div className="flex flex-wrap items-center gap-2">
          <a
            href={`http://localhost:8005/api/research/${id}/export/markdown`}
            download
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 shadow-2xs transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-slate-500" /> Export Markdown
          </a>
          <a
            href={`http://localhost:8005/api/research/${id}/export/pdf`}
            download
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 shadow-2xs transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-slate-500" /> Export PDF
          </a>
          <button
            onClick={handleCopyRoadmap}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 shadow-2xs transition-colors"
          >
            {copiedRoadmap ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-slate-500" />}
            {copiedRoadmap ? "Copied!" : "Copy Roadmap"}
          </button>
          <button
            onClick={handleDelete}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-rose-50 border border-rose-200 text-rose-700 hover:bg-rose-100 shadow-2xs transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5 text-rose-600" /> Delete
          </button>
        </div>
      </div>

      {/* Report Header Card */}
      <div className="bg-white rounded-2xl border border-slate-200/90 p-6 sm:p-8 shadow-xs space-y-4">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs px-2.5 py-1 rounded-md bg-brand-50 border border-brand-100 text-brand-700 font-semibold flex items-center gap-1">
            <Languages className="w-3 h-3" />
            {languageLabel}
          </span>
          <span className="text-xs px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 font-medium capitalize flex items-center gap-1">
            <GraduationCap className="w-3 h-3" />
            Level: {job.skill_level || "Beginner"}
          </span>
          <span className="text-xs px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 font-medium flex items-center gap-1">
            <Clock className="w-3 h-3" />
            {job.study_time_hours_per_week || "10-15"} hrs/week
          </span>
          {report.is_demo_mode ? (
            <span className="text-xs px-2.5 py-1 rounded-md bg-amber-50 border border-amber-200 text-amber-700 font-medium">
              Demo Synthesis Mode
            </span>
          ) : (
            <span className="text-xs px-2.5 py-1 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-700 font-medium flex items-center gap-1">
              <ShieldCheck className="w-3 h-3" /> Verified Web Synthesis
            </span>
          )}
        </div>

        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight leading-tight">
          {report.title}
        </h1>

        <div className="flex flex-wrap items-center gap-x-6 gap-y-2 text-xs text-slate-500 pt-2 border-t border-slate-100">
          <span>Inquiry: <strong className="text-slate-800">{job.query}</strong></span>
          <span>•</span>
          <span>Timeline: <strong className="text-slate-800">{roadmap?.total_estimated_timeline || "Flexible"}</strong></span>
          <span>•</span>
          <span>Roadmap Progress: <strong className="text-slate-800">{completionPct}% ({completedTasks}/{totalTasks} tasks)</strong></span>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex items-center gap-1 border-b border-slate-200 overflow-x-auto pb-px">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2.5 text-xs font-bold rounded-t-lg transition-all flex items-center gap-1.5 whitespace-nowrap ${
                isActive
                  ? "bg-white text-brand-600 border-t-2 border-brand-600 border-x border-slate-200 shadow-2xs"
                  : "text-slate-500 hover:text-slate-800 hover:bg-slate-50"
              }`}
            >
              <span>{tab.label}</span>
              {typeof tab.count === "number" && (
                <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                  isActive ? "bg-brand-50 text-brand-700 font-semibold" : "bg-slate-100 text-slate-500"
                }`}>
                  {tab.count}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Tab 1: Overview */}
      {activeTab === "overview" && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs space-y-4">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-brand-600" />
              Executive Summary
            </h2>
            <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">
              {report.executive_summary}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs space-y-3">
              <h3 className="text-sm font-bold text-slate-900">Research Objective & Scope</h3>
              <p className="text-xs text-slate-600 leading-relaxed whitespace-pre-line">
                {report.objective_and_scope}
              </p>
            </div>

            <div className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs space-y-3">
              <h3 className="text-sm font-bold text-slate-900">Strategic Recommendations</h3>
              <ul className="space-y-2">
                {report.strategic_recommendations.map((rec, i) => (
                  <li key={i} className="text-xs text-slate-700 flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-brand-500 mt-1.5 flex-shrink-0" />
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Quick Learning Snapshot Card */}
          {learningResources.length > 0 && (
            <div className="bg-gradient-to-r from-brand-50 to-indigo-50/40 rounded-2xl border border-brand-100 p-6 shadow-xs flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="space-y-1">
                <span className="text-xs uppercase font-bold text-brand-700 flex items-center gap-1.5">
                  <Youtube className="w-4 h-4 text-red-600" />
                  Personalized Learning Hub Available
                </span>
                <p className="text-sm font-bold text-slate-900">
                  {learningResources.length} curated {languageLabel} tutorials, playlists, and official docs ready for your roadmap.
                </p>
              </div>
              <button
                onClick={() => setActiveTab("resources")}
                className="bg-brand-600 hover:bg-brand-700 text-white font-semibold text-xs px-4 py-2.5 rounded-xl shadow-xs transition-all whitespace-nowrap"
              >
                Explore Learning Resources
              </button>
            </div>
          )}

          {report.conflicts_and_uncertainties && (
            <div className="bg-amber-50/70 border border-amber-200 rounded-2xl p-6 shadow-xs space-y-2">
              <h3 className="text-sm font-bold text-amber-900 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-amber-600" />
                Conflicting Claims & Uncertainties
              </h3>
              <p className="text-xs text-amber-800 leading-relaxed whitespace-pre-line">
                {report.conflicts_and_uncertainties}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Key Findings */}
      {activeTab === "findings" && (
        <div className="space-y-4">
          {report.key_findings.map((f, idx) => (
            <div key={idx} className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h3 className="text-base font-bold text-slate-900">{f.title}</h3>
                <span className={`text-[11px] font-bold px-2 py-0.5 rounded-md ${
                  f.confidence_level === "High"
                    ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                    : "bg-blue-50 text-blue-700 border border-blue-200"
                }`}>
                  Confidence: {f.confidence_level}
                </span>
              </div>
              <p className="text-xs text-slate-700 leading-relaxed">{f.explanation}</p>
              
              <div className="pt-2 border-t border-slate-100 space-y-1.5">
                <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Supporting Evidence</span>
                <ul className="space-y-1">
                  {f.supporting_evidence.map((ev, i) => (
                    <li key={i} className="text-xs text-slate-600 flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-slate-400 mt-1.5 flex-shrink-0" />
                      <span>{ev}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {f.caveats && (
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/60 text-xs text-slate-600">
                  <strong>Caveat / Nuance:</strong> {f.caveats}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Tab 3: Evidence Matrix */}
      {activeTab === "comparison" && (
        <div className="bg-white rounded-2xl border border-slate-200/90 overflow-hidden shadow-xs">
          <div className="p-5 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-900">Cross-Source Evidence & Consensus Analysis</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Distinguishing independent empirical corroboration from repeated claims.
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-50 text-slate-500 font-bold border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Topic / Assertion</th>
                  <th className="py-3 px-4">Consensus Level</th>
                  <th className="py-3 px-4">Corroboration Nature</th>
                  <th className="py-3 px-4">Evaluation Rationale</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {report.evidence_comparisons.map((item, i) => (
                  <tr key={i} className="hover:bg-slate-50/50">
                    <td className="py-3 px-4 font-semibold text-slate-900 max-w-xs">{item.topic_or_claim}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                        item.consensus_level === "Strong"
                          ? "bg-emerald-50 text-emerald-700"
                          : item.consensus_level === "Moderate"
                          ? "bg-blue-50 text-blue-700"
                          : "bg-amber-50 text-amber-700"
                      }`}>
                        {item.consensus_level}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-600">{item.is_repetition_vs_independent}</td>
                    <td className="py-3 px-4 text-slate-600 max-w-md">{item.evidence_strength_rationale}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 4: Action Roadmap */}
      {activeTab === "roadmap" && (
        <div className="space-y-6">
          {/* Personalized Learning Strategy Banner */}
          <div className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
              <div>
                <span className="text-[11px] uppercase tracking-wider font-bold text-brand-600">Personalized Learning Strategy</span>
                <h3 className="text-lg font-bold text-slate-900 mt-0.5">
                  Milestone-Driven Execution Roadmap
                </h3>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs px-2.5 py-1 rounded-lg bg-brand-50 text-brand-800 font-semibold">
                  {languageLabel}
                </span>
                <span className="text-xs px-2.5 py-1 rounded-lg bg-slate-100 text-slate-700 font-semibold capitalize">
                  {job.skill_level || "Beginner"}
                </span>
                <span className="text-xs px-2.5 py-1 rounded-lg bg-slate-100 text-slate-700 font-semibold">
                  {job.study_time_hours_per_week || "10-15"} hrs/wk
                </span>
              </div>
            </div>

            {roadmap?.learning_strategy_summary && (
              <p className="text-xs text-slate-600 leading-relaxed">
                {roadmap.learning_strategy_summary}
              </p>
            )}

            <div className="flex flex-wrap items-center justify-between gap-4 pt-1">
              <div className="text-xs text-slate-500">
                <strong>Timeline:</strong> {roadmap.total_estimated_timeline} | <strong>Assumptions:</strong> {roadmap.planning_assumptions}
              </div>
              <div className="flex items-center gap-2">
                <div className="w-24 bg-slate-100 rounded-full h-2 overflow-hidden">
                  <div className="bg-brand-600 h-2 rounded-full transition-all duration-300" style={{ width: `${completionPct}%` }} />
                </div>
                <span className="text-xs font-bold text-slate-700">{completionPct}% Complete</span>
              </div>
            </div>
          </div>

          {/* Phases */}
          <div className="space-y-6">
            {roadmap.phases.map((phase) => (
              <div key={phase.phase_number} className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs space-y-5">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                  <div>
                    <span className="text-xs font-bold text-brand-600 uppercase tracking-wider">
                      Phase {phase.phase_number} • {phase.duration}
                    </span>
                    <h4 className="text-base font-extrabold text-slate-900 mt-0.5">
                      {phase.phase_title}
                    </h4>
                  </div>
                  <div className="text-xs text-slate-500 font-medium">
                    Milestone: <strong className="text-slate-800">{phase.milestone}</strong>
                  </div>
                </div>

                {/* Skills & Prerequisites */}
                <div className="flex flex-wrap gap-1.5 items-center">
                  <span className="text-[11px] font-bold text-slate-400 mr-1">Skills:</span>
                  {phase.skills_covered.map((s, idx) => (
                    <span key={idx} className="text-[11px] bg-slate-100 text-slate-700 px-2 py-0.5 rounded font-medium">
                      {s}
                    </span>
                  ))}
                </div>

                {/* Capstone Phase Project */}
                {phase.phase_project && (
                  <div className="p-3.5 bg-brand-50/60 border border-brand-100 rounded-xl flex items-start gap-3">
                    <Briefcase className="w-4 h-4 text-brand-600 mt-0.5 flex-shrink-0" />
                    <div>
                      <div className="text-xs font-bold text-brand-900">Phase Capstone Project</div>
                      <div className="text-xs text-slate-700 mt-0.5">{phase.phase_project}</div>
                    </div>
                  </div>
                )}

                {/* Weekly Breakdown */}
                {phase.weekly_breakdown && phase.weekly_breakdown.length > 0 && (
                  <div className="space-y-1.5 bg-slate-50/70 p-3.5 rounded-xl border border-slate-200/60">
                    <div className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                      <Calendar className="w-3.5 h-3.5 text-slate-500" />
                      Weekly Study Schedule
                    </div>
                    <ul className="space-y-1">
                      {phase.weekly_breakdown.map((wb, i) => (
                        <li key={i} className="text-xs text-slate-600 flex items-start gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-slate-400 mt-1.5 flex-shrink-0" />
                          <span>{wb}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Video Tutorials for this Phase */}
                {phase.video_tutorials && phase.video_tutorials.length > 0 && (
                  <div className="space-y-2">
                    <div className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                      <Youtube className="w-4 h-4 text-red-600" />
                      Recommended Video Tutorials for Phase {phase.phase_number} ({languageLabel})
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {phase.video_tutorials.map((vid, idx) => (
                        <a
                          key={idx}
                          href={vid.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 p-2.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 hover:border-brand-300 transition-all text-xs text-slate-800 font-medium group"
                        >
                          <PlayCircle className="w-4 h-4 text-red-600 group-hover:scale-110 transition-transform flex-shrink-0" />
                          <span className="truncate flex-1">{vid.title}</span>
                          {vid.channel && (
                            <span className="text-[10px] text-slate-400 flex-shrink-0">({vid.channel})</span>
                          )}
                          <ExternalLink className="w-3 h-3 text-slate-400 flex-shrink-0" />
                        </a>
                      ))}
                    </div>
                  </div>
                )}

                {/* Tasks Checklist with Practical Exercises */}
                <div className="space-y-3 pt-2">
                  <div className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                    Tasks & Practical Exercises
                  </div>
                  <div className="space-y-2.5">
                    {phase.tasks.map((task) => (
                      <div
                        key={task.id}
                        className={`p-3.5 rounded-xl border transition-all ${
                          task.is_completed
                            ? "bg-emerald-50/50 border-emerald-200"
                            : "bg-slate-50/60 border-slate-200/80 hover:bg-white"
                        }`}
                      >
                        <div className="flex items-start gap-3">
                          <input
                            type="checkbox"
                            checked={task.is_completed}
                            onChange={() => handleToggleTask(task.id, task.is_completed)}
                            className="mt-0.5 rounded border-slate-300 text-brand-600 focus:ring-brand-500 w-4 h-4 cursor-pointer"
                          />
                          <div className="flex-1 space-y-1">
                            <div className="flex flex-wrap items-center justify-between gap-2">
                              <span className={`text-xs font-bold ${task.is_completed ? "line-through text-slate-500" : "text-slate-900"}`}>
                                {task.title}
                              </span>
                              <span className="text-[10px] bg-white border border-slate-200 text-slate-600 px-2 py-0.5 rounded">
                                Deliverable: {task.deliverable}
                              </span>
                            </div>
                            <p className="text-xs text-slate-600">{task.description}</p>
                            
                            {/* Practical Exercise Box */}
                            {task.practical_exercise && (
                              <div className="mt-2 p-2.5 rounded-lg bg-white border border-slate-200 text-xs text-slate-700 flex items-start gap-2">
                                <Code2 className="w-3.5 h-3.5 text-brand-600 mt-0.5 flex-shrink-0" />
                                <div>
                                  <strong className="text-slate-800">Practical Exercise:</strong> {task.practical_exercise}
                                </div>
                              </div>
                            )}

                            {/* Project Idea Box */}
                            {task.project_idea && (
                              <div className="mt-1 p-2 rounded-lg bg-indigo-50/50 border border-indigo-100 text-xs text-indigo-900 flex items-start gap-2">
                                <Sparkles className="w-3.5 h-3.5 text-indigo-600 mt-0.5 flex-shrink-0" />
                                <div>
                                  <strong>Project Idea:</strong> {task.project_idea}
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 5: Recommended Learning Resources */}
      {activeTab === "resources" && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <span className="text-xs font-bold text-brand-600 uppercase tracking-wider">Multilingual Learning Hub</span>
              <h3 className="text-lg font-bold text-slate-900 mt-0.5">
                Recommended YouTube Videos, Playlists & Official Docs
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Prioritizing {languageLabel} tutorials for your {job.skill_level || "beginner"} learning pathway.
              </p>
            </div>
            
            {/* Filter Buttons */}
            <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl self-start sm:self-center">
              {[
                { id: "all", label: "All Resources" },
                { id: "youtube", label: "YouTube" },
                { id: "docs", label: "Official Docs" },
                { id: "practice", label: "Practice" },
              ].map((f) => (
                <button
                  key={f.id}
                  onClick={() => setResourceFilter(f.id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    resourceFilter === f.id
                      ? "bg-white text-slate-900 shadow-2xs"
                      : "text-slate-500 hover:text-slate-800"
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>
          </div>

          {/* Resources Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredResources.map((res) => {
              const isYoutube = res.resource_type.includes("youtube");
              return (
                <div
                  key={res.id}
                  className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-xs hover:shadow-md transition-all flex flex-col justify-between space-y-4"
                >
                  <div className="space-y-2.5">
                    <div className="flex items-center justify-between gap-2">
                      <div className="flex items-center gap-1.5">
                        {isYoutube ? (
                          <div className="w-7 h-7 rounded-lg bg-red-50 border border-red-100 flex items-center justify-center text-red-600">
                            <Youtube className="w-4 h-4" />
                          </div>
                        ) : (
                          <div className="w-7 h-7 rounded-lg bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600">
                            <BookOpen className="w-4 h-4" />
                          </div>
                        )}
                        <span className="text-xs font-bold text-slate-700">{res.source}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <span className="text-[10px] px-2 py-0.5 rounded font-bold bg-slate-100 text-slate-600">
                          {res.language_label}
                        </span>
                        <span className="text-[10px] px-2 py-0.5 rounded font-bold capitalize bg-brand-50 text-brand-700">
                          {res.skill_level}
                        </span>
                      </div>
                    </div>

                    <h4 className="text-sm font-bold text-slate-900 leading-snug">
                      <a
                        href={res.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="hover:text-brand-600 hover:underline flex items-start gap-1"
                      >
                        <span>{res.title}</span>
                        <ExternalLink className="w-3.5 h-3.5 mt-0.5 flex-shrink-0 text-slate-400" />
                      </a>
                    </h4>

                    <p className="text-xs text-slate-600 leading-relaxed">
                      {res.description}
                    </p>

                    <div className="p-3 bg-slate-50/80 rounded-xl border border-slate-100 text-xs text-slate-700 space-y-1">
                      <div className="font-bold text-[11px] text-brand-700 uppercase tracking-wider flex items-center gap-1">
                        <Sparkles className="w-3 h-3" />
                        Why This Resource is Useful
                      </div>
                      <p className="text-slate-600">{res.why_useful}</p>
                    </div>
                  </div>

                  <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                    <span className="text-[11px] text-slate-400 font-medium">
                      {isYoutube ? "Verified YouTube Link" : "Official Reference"}
                    </span>
                    <a
                      href={res.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 text-xs font-bold text-brand-600 hover:text-brand-700 hover:underline"
                    >
                      <span>{isYoutube ? "Watch on YouTube" : "Open Documentation"}</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Tab 6: Sources & Citations */}
      {activeTab === "sources" && (
        <div className="space-y-4">
          {report.sources_and_citations.map((src, i) => (
            <div key={src.id || i} className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-xs space-y-2">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <a
                  href={src.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm font-bold text-slate-900 hover:text-brand-600 flex items-center gap-1.5"
                >
                  <span>{src.title}</span>
                  <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
                </a>
                <div className="flex items-center gap-2 text-[11px] text-slate-400">
                  <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-medium uppercase">
                    {src.source_type}
                  </span>
                  {src.publisher && <span>{src.publisher}</span>}
                  {src.publication_date && <span>• {src.publication_date}</span>}
                </div>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed italic bg-slate-50 p-3 rounded-xl border border-slate-100">
                "{src.snippet}"
              </p>
            </div>
          ))}
        </div>
      )}

      {/* Tab 7: Methodology */}
      {activeTab === "methodology" && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs space-y-3">
            <h3 className="text-sm font-bold text-slate-900">Multi-Stage LangGraph Agent Methodology</h3>
            <p className="text-xs text-slate-700 leading-relaxed whitespace-pre-line">
              {report.methodology}
            </p>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs space-y-3">
            <h3 className="text-sm font-bold text-slate-900">Research Limitations & Suggested Follow-up</h3>
            <p className="text-xs text-slate-700 leading-relaxed whitespace-pre-line">
              {report.limitations_and_future_work}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
