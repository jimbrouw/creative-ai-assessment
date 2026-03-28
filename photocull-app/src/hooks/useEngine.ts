import { invoke } from "@tauri-apps/api/core";
import { listen, UnlistenFn } from "@tauri-apps/api/event";
import { useEffect, useRef } from "react";

export interface EngineEvent {
  event: string;
  total?: number;
  done?: number;
  file?: string;
  batch?: Result[];
  summary?: Summary;
  count?: number;
  output_dir?: string;
  path?: string;
  message?: string;
}

export interface Result {
  path: string;
  sharpness_score: number;
  exposure_score: number;
  combined_score: number;
  face_count: number;
  eyes_open: boolean;
  stars: number;
  category: "selected" | "maybe" | "rejected";
  is_blurry: boolean;
  is_duplicate: boolean;
  duplicate_group_id: number | null;
  duplicate_rank: number;
  error?: string;
}

export interface Summary {
  total: number;
  selected: number;
  maybe: number;
  rejected: number;
  cull_ratio: number;
}

export interface AnalysisParams {
  input_dir: string;
  mode: string;
  keep_duplicates: number;
  output_dir: string;
  workers: number;
}

export function useEngine(onEvent: (e: EngineEvent) => void) {
  const unlistenRef = useRef<UnlistenFn | null>(null);

  useEffect(() => {
    let active = true;
    listen<EngineEvent>("engine-event", (event) => {
      if (active) onEvent(event.payload);
    }).then((unlisten) => {
      unlistenRef.current = unlisten;
    });
    return () => {
      active = false;
      unlistenRef.current?.();
    };
  }, [onEvent]);

  async function startAnalysis(params: AnalysisParams) {
    return invoke("run_analysis", params);
  }

  async function runExports(params: {
    input_dir: string;
    mode: string;
    keep_duplicates: number;
    output_dir: string;
    write_xmp: boolean;
    write_html: boolean;
  }) {
    return invoke("run_exports", params);
  }

  return { startAnalysis, runExports };
}
