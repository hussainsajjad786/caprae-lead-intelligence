const BASE = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '');
export function queryString(filters) {
  return new URLSearchParams(Object.entries(filters).filter(([, value]) => value !== '' && value !== null && value !== undefined)).toString();
}
export async function api(path, signal) {
  const response = await fetch(`${BASE}/api${path}`, { signal });
  if (!response.ok) throw new Error(`Request failed (${response.status}). Check that the API is running and try again.`);
  return response.json();
}
export async function exportCSV(filters) {
  const response = await fetch(`${BASE}/api/leads/export?${queryString(filters)}`);
  if (!response.ok) throw new Error('Export failed. Please try again.');
  const url = URL.createObjectURL(await response.blob());
  const link = document.createElement('a');
  link.href = url; link.download = 'qualified-demo-leads.csv'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
