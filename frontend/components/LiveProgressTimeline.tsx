"use client";

import React from "react";
import { CheckCircle2, Loader2, Clock, AlertCircle } from "lucide-react";

export const STAGES = [
  { index: 1, name: "Understanding the goal", desc: "Extracting objectives, boundaries, and scope constraints" },
  { index: 2, name: "Creating a research plan", desc: "Decomposing queries into targeted investigative pathways" },
  { index: 3, name: "Searching for sources", desc: "Crawling web engines and querying personal knowledge base" },
  { index: 4, name: "Extracting relevant information", desc: "Isolating atomic claims, empirical data, and statistics" },
  { index: 5, name: "Comparing evidence", desc: "Evaluating cross-source agreement, conflicts, and repetition" },
  { index: 6, name: "Verifying claims", desc: "Checking factual grounding and weeding out unverified assertions" },
  { index: 7, name: "Synthesizing findings", desc: "Clustering insights with evidence-strength indicators and caveats" },
  { index: 8, name: "Creating the action roadmap", desc: "Structuring phases, milestones, deliverables, and dependencies" },
  { index: 9, name: "Generating the final report", desc: "Compiling 10-section publication-ready strategic documentation" },
];

interface LiveProgressTimelineProps {
  currentStageIndex: number;
  latestMessage?: string;
  isCompleted: boolean;
  isFailed: boolean;
  errorMessage?: string;
}

export default function LiveProgressTimeline({
  currentStageIndex,
  latestMessage,
  isCompleted,
  isFailed,
  errorMessage,
}: LiveProgressTimelineProps) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <div className="flex items-center justify-between pb-5 border-b border-slate-100 mb-6">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            {!isCompleted && !isFailed && <Loader2 className="w-4 h-4 text-brand-600 animate-spin" />}
            {isCompleted && <CheckCircle2 className="w-5 h-5 text-emerald-600" />}
            {isFailed && <AlertCircle className="w-5 h-5 text-rose-600" />}
            {isCompleted ? "Research Complete & Verified" : isFailed ? "Research Process Halted" : "Agent Graph Executing..."}
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Real-time LangGraph orchestration across 9 dedicated state machines
          </p>
        </div>
        <div className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700">
          Stage {Math.min(currentStageIndex, 9)} of 9
        </div>
      </div>

      {/* Progress Stepper */}
      <div className="space-y-4">
        {STAGES.map((s) => {
          const isDone = isCompleted || currentStageIndex > s.index;
          const isActive = !isCompleted && !isFailed && currentStageIndex === s.index;
          const isPending = currentStageIndex < s.index;

          return (
            <div key={s.index} className="flex items-start gap-3.5 group">
              <div className="pt-0.5">
                {isDone ? (
                  <div className="w-6 h-6 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-xs shadow-xs">
                    ✓
                  </div>
                ) : isActive ? (
                  <div className="w-6 h-6 rounded-full bg-brand-600 text-white flex items-center justify-center shadow-xs">
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  </div>
                ) : (
                  <div className="w-6 h-6 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center text-xs font-medium">
                    {s.index}
                  </div>
                )}
              </div>

              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h4 className={`text-sm font-semibold ${
                    isActive ? "text-brand-700" : isDone ? "text-slate-800" : "text-slate-400"
                  }`}>
                    {s.index}. {s.name}
                  </h4>
                  {isActive && (
                    <span className="text-[11px] font-medium text-brand-600 bg-brand-50 px-2 py-0.5 rounded-md border border-brand-100 animate-pulse">
                      In progress
                    </span>
                  )}
                  {isDone && (
                    <span className="text-[11px] font-medium text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-100">
                      Verified
                    </span>
                  )}
                </div>
                <p className={`text-xs mt-0.5 ${isActive ? "text-slate-600" : "text-slate-400"}`}>
                  {s.desc}
                </p>

                {isActive && latestMessage && (
                  <div className="mt-2.5 p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs font-mono text-slate-700 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-brand-500 animate-ping"></span>
                    <span>{latestMessage}</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {isFailed && (
        <div className="mt-6 p-4 bg-rose-50 border border-rose-200 rounded-xl text-rose-800 text-xs">
          <strong>Error encountered:</strong> {errorMessage || "Execution interrupted."}
        </div>
      )}
    </div>
  );
}
