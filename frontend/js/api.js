import { API_BASE_URL } from "./config.js";

async function fetchJson(path) {
  const url = `${API_BASE_URL}${path}`;
  const response = await fetch(url);
  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = await response.json();
      detail = body.detail ?? body.message ?? detail;
    } catch {
      /* ignore */
    }
    throw new Error(`API error ${response.status}: ${detail}`);
  }
  return response.json();
}

export function fetchTeams() {
  return fetchJson("/api/teams");
}

export function fetchMatches() {
  return fetchJson("/api/v1/matches");
}
