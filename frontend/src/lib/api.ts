const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type FileItem = {
  id: string;
  title: string;
  original_name: string;
  mime_type: string;
  size: number;
  processing_status: string;
  scan_status: string | null;
  scan_details: string | null;
  metadata_json: Record<string, unknown> | null;
  requires_attention: boolean;
  created_at: string;
  updated_at: string;
};

export type AlertItem = {
  id: number;
  file_id: string;
  level: string;
  message: string;
  created_at: string;
};

export type PagedResponse<T> = {
  items: T[];
  total: number;
  page: number;
  page_size: number;
};

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { cache: "no-store", ...init });
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(text || `Request failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export function getDownloadUrl(fileId: string) {
  return `${API_BASE}/files/${fileId}/download`;
}

export async function fetchFiles(page: number, pageSize: number): Promise<PagedResponse<FileItem>> {
  return apiFetch(`/files?page=${page}&page_size=${pageSize}`);
}

export async function fetchAlerts(page: number, pageSize: number): Promise<PagedResponse<AlertItem>> {
  return apiFetch(`/alerts?page=${page}&page_size=${pageSize}`);
}

export async function uploadFile(title: string, file: File): Promise<FileItem> {
  const formData = new FormData();
  formData.append("title", title.trim());
  formData.append("file", file);
  return apiFetch("/files", { method: "POST", body: formData });
}
