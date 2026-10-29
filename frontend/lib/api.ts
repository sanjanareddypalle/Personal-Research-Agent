const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8005/api";

export async function createResearchJob(payload: {
  query: string;
  depth?: string;
  constraints?: string;
  source_preferences?: string[];
  include_knowledge_base?: boolean;
  language?: string;
  skill_level?: string;
  study_time_hours_per_week?: string;
}): Promise<{ id: string; message: string }> {
  const res = await fetch(`${API_BASE}/research`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to create research job");
  }
  return res.json();
}

export async function getResearchJob(id: string) {
  const res = await fetch(`${API_BASE}/research/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch research details");
  return res.json();
}

export async function listResearchJobs() {
  const res = await fetch(`${API_BASE}/research`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to list research jobs");
  return res.json();
}

export async function deleteResearchJob(id: string) {
  const res = await fetch(`${API_BASE}/research/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete research job");
  return res.json();
}

export async function updateTaskStatus(researchId: string, taskId: string, isCompleted: boolean) {
  const res = await fetch(`${API_BASE}/research/${researchId}/tasks/${taskId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ is_completed: isCompleted }),
  });
  if (!res.ok) throw new Error("Failed to update task progress");
  return res.json();
}

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/documents/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Failed to upload document");
  return res.json();
}

export async function listDocuments() {
  const res = await fetch(`${API_BASE}/documents`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to list documents");
  return res.json();
}

export async function deleteDocument(id: string) {
  const res = await fetch(`${API_BASE}/documents/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete document");
  return res.json();
}

export async function searchKnowledge(query: string, topK: number = 5) {
  const res = await fetch(`${API_BASE}/documents/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, top_k: topK }),
  });
  if (!res.ok) throw new Error("Failed to search knowledge base");
  return res.json();
}

export async function getSettings() {
  const res = await fetch(`${API_BASE}/settings`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch settings");
  return res.json();
}

export async function updateSettings(data: { llm_provider: string; search_provider: string; demo_mode: boolean }) {
  const res = await fetch(`${API_BASE}/settings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update settings");
  return res.json();
}
