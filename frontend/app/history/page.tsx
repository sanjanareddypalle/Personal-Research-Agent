"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { 
  Search, 
  Trash2, 
  ArrowRight, 
  Calendar, 
  Clock, 
  Layers, 
  CheckCircle2, 
  AlertCircle,
  FileText
} from "lucide-react";
import { listResearchJobs, deleteResearchJob } from "@/lib/api";
import { ResearchJobSummary } from "@/types";

export default function HistoryPage() {
  const [jobs, setJobs] = useState<ResearchJobSummary[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchJobs = () => {
    setLoading(true);
    listResearchJobs()
      .then((data) => {
        setJobs(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!confirm("Are you sure you want to delete this research session?")) return;
    try {
      await deleteResearchJob(id);
      setJobs(jobs.filter((j) => j.id !== id));
    } catch (err) {
      alert("Failed to delete session.");
    }
  };

  const filteredJobs = jobs.filter((j) =>
    j.query.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-5xl mx-auto px-6 py-10 w-full space-y-8">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Research History
        </h1>
        <p className="text-slate-600 text-sm mt-1">
          Review, reopen, and export previous research investigations and action plans.
        </p>
      </div>

      {/* Search Input */}
      <div className="relative">
        <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search research questions..."
          className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
        />
      </div>

      {/* List */}
      {loading ? (
        <div className="p-12 text-center text-xs text-slate-400">Loading research history...</div>
      ) : filteredJobs.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
          <FileText className="w-10 h-10 text-slate-300 mx-auto" />
          <h3 className="text-sm font-bold text-slate-700">No Research Found</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            {searchTerm ? "No records matched your search." : "Start your first research inquiry from the workspace."}
          </p>
          <Link
            href="/"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-brand-600 hover:underline pt-2"
          >
            Go to New Research <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredJobs.map((job) => {
            const isDone = job.status === "completed";
            return (
              <div
                key={job.id}
                className="bg-white rounded-xl border border-slate-200 p-4 hover:border-brand-300 hover:shadow-xs transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4 group"
              >
                <div className="space-y-1.5 flex-1 min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      isDone
                        ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                        : job.status === "failed"
                        ? "bg-rose-50 text-rose-700 border border-rose-200"
                        : "bg-blue-50 text-blue-700 border border-blue-200"
                    }`}>
                      {job.status.toUpperCase()}
                    </span>
                    <span className="text-[10px] uppercase font-semibold text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
                      {job.depth}
                    </span>
                    {job.is_demo_mode && (
                      <span className="text-[10px] font-semibold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                        Demo Mode
                      </span>
                    )}
                    <span className="text-xs text-slate-400 flex items-center gap-1">
                      <Calendar className="w-3 h-3" /> {job.created_at}
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-slate-900 group-hover:text-brand-600 transition-colors truncate">
                    {job.query}
                  </h3>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <Link
                    href={`/report/${job.id}`}
                    className="inline-flex items-center gap-1 text-xs font-semibold px-3 py-1.5 rounded-lg bg-brand-50 hover:bg-brand-100 text-brand-700 transition-colors"
                  >
                    <span>View Report</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                  <button
                    onClick={(e) => handleDelete(job.id, e)}
                    className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                    title="Delete research"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
