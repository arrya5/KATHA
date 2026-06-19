import { API_BASE } from "./config";
import type { SceneRender, SeasonEntry, TurnRequest } from "./types";

export async function postTurn(req: TurnRequest): Promise<SceneRender> {
  const res = await fetch(`${API_BASE}/turn`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error(`turn failed: ${res.status}`);
  return res.json();
}

export async function fetchSeason(): Promise<SeasonEntry[]> {
  const res = await fetch(`${API_BASE}/season`);
  const data = await res.json();
  return data.order as SeasonEntry[];
}
