export interface Choice {
  id: string;
  label: string;
}

export interface SceneRender {
  scene_id: string;
  speaker: string;
  line: string;
  expression: string;
  choices: Choice[];
  ambient: string;
  voice_profile: string;
  fallback_used: boolean;
  meta: {
    intent?: string;
    trust?: number;
    dharma?: number;
    turn_no?: number;
    strikes?: number;
    advance_to?: string;
    mendicant_suspicion?: string;
    season_complete?: boolean;
    outcome?: string;
    climax_tier?: string;
  };
}

export interface TurnRequest {
  session_id: string;
  player_input?: string;
  choice_id?: string | null;
  scene_id?: string;
}

export interface SeasonEntry {
  id: string;
  title: string;
  kind: string;
}
