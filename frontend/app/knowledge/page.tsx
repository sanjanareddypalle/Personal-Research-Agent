"use client";

import React, { useEffect, useState } from "react";
import { 
  BookOpen, 
  Upload, 
  Trash2, 
  FileText, 
  Search, 
  CheckCircle2, 
  Layers,
  ArrowRight
} from "lucide-react";
import { uploadDocument, listDocuments, deleteDocument, searchKnowledge } from "@/lib/api";
import { DocumentResponse, DocumentChunk } from "@/types";

export default function KnowledgePage() {
  const [documents, setDocuments] = useState<DocumentResponse[]>([]);
  const [uploading, setUploading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<DocumentChunk[]>([]);
  const [searching, setSearching] = useState(false);

  const fetchDocs = () => {
    listDocuments()
      .then(setDocuments)
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      await uploadDocument(file);
      fetchDocs();
    } catch (err: any) {
      alert(err.message || "Upload failed");
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this document from the knowledge base?")) return;
    try {
      await deleteDocument(id);
      setDocuments(documents.filter((d) => d.id !== id));
      setSearchResults([]);
    } catch (err) {
      alert("Failed to delete document.");
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setSearching(true);
    try {
      const res = await searchKnowledge(searchQuery.trim(), 4);
      setSearchResults(res.chunks || []);
    } catch (err) {
      console.error(err);
    } finally {
      setSearching(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-6 py-10 w-full space-y-8">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Personal Knowledge Base (RAG)
        </h1>
        <p className="text-slate-600 text-sm mt-1">
          Upload PDF, TXT, and Markdown documents to ground your research in private institutional evidence.
        </p>
      </div>

      {/* Upload Box */}
      <div className="bg-white rounded-2xl border-2 border-dashed border-slate-200 p-8 text-center hover:border-brand-400 transition-colors">
        <div className="max-w-sm mx-auto space-y-3">
          <div className="w-10 h-10 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center mx-auto">
            <Upload className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">Upload Reference Document</h3>
            <p className="text-xs text-slate-500 mt-0.5">Supports PDF, Markdown (.md), and plain text (.txt)</p>
          </div>
          <label className="inline-flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold text-xs px-4 py-2 rounded-xl cursor-pointer shadow-xs transition-colors">
            <span>{uploading ? "Indexing chunks..." : "Browse Files"}</span>
            <input
              type="file"
              accept=".pdf,.txt,.md,.markdown"
              onChange={handleFileUpload}
              disabled={uploading}
              className="hidden"
            />
          </label>
        </div>
      </div>

      {/* Document Library */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
          Indexed Documents ({documents.length})
        </h3>
        {documents.length === 0 ? (
          <div className="p-8 bg-white rounded-xl border border-slate-200 text-center text-xs text-slate-400">
            No private documents indexed yet. Upload a file above to activate RAG grounding.
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {documents.map((doc) => (
              <div key={doc.id} className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs flex items-center justify-between">
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center text-slate-600 shrink-0 font-bold text-[10px] uppercase">
                    {doc.file_type}
                  </div>
                  <div className="min-w-0">
                    <h4 className="text-xs font-bold text-slate-900 truncate">{doc.filename}</h4>
                    <p className="text-[11px] text-slate-400">
                      {doc.chunk_count} chunks indexed • {(doc.file_size_bytes / 1024).toFixed(1)} KB
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleDelete(doc.id)}
                  className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                  title="Delete document"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Semantic Search Test */}
      {documents.length > 0 && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Test Semantic Retrieval</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Verify how your uploaded document chunks are retrieved against test queries.
            </p>
          </div>
          <form onSubmit={handleSearch} className="flex gap-2">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Query indexed knowledge base..."
              className="flex-1 px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500"
            />
            <button
              type="submit"
              disabled={searching || !searchQuery.trim()}
              className="bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold px-4 py-2 rounded-xl transition-colors disabled:opacity-50"
            >
              {searching ? "Searching..." : "Search"}
            </button>
          </form>

          {searchResults.length > 0 && (
            <div className="space-y-3 pt-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Top Matching Chunks:</span>
              <div className="space-y-2">
                {searchResults.map((chunk) => (
                  <div key={chunk.id} className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs space-y-1">
                    <div className="flex items-center justify-between text-[11px] font-semibold text-slate-500">
                      <span>{chunk.document_name} {chunk.page_number ? `(Page ${chunk.page_number})` : ""}</span>
                      {chunk.score !== undefined && (
                        <span className="text-brand-600 font-mono">Similarity: {chunk.score.toFixed(3)}</span>
                      )}
                    </div>
                    <p className="text-slate-800 leading-relaxed font-mono text-[11px]">{chunk.text}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
