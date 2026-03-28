import { useState } from "react";
import { convertFileSrc } from "@tauri-apps/api/core";
import { openPath } from "@tauri-apps/plugin-opener";
import { Result, Summary } from "../hooks/useEngine";

const STARS: Record<number, string> = {
  5: "★★★★★", 4: "★★★★☆", 3: "★★★☆☆", 2: "★★☆☆☆", 1: "★☆☆☆☆",
};

type Filter = "all" | "selected" | "maybe" | "rejected";

interface Props {
  results: Result[];
  summary: Summary;
  inputDir: string;
  outputDir: string;
  mode: string;
  keepDuplicates: number;
  onExport: (xmp: boolean, html: boolean) => void;
  exporting: boolean;
  exportStatus: string;
  htmlPath: string;
  onReset: () => void;
}

export function Review({
  results, summary, outputDir, onExport, exporting, exportStatus, htmlPath, onReset,
}: Props) {
  const [filter, setFilter] = useState<Filter>("all");

  const visible = filter === "all" ? results : results.filter((r) => r.category === filter);

  return (
    <div className="review-screen">
      <header className="review-header">
        <div className="review-title">
          <button className="btn-back" onClick={onReset}>← Back</button>
          <h2>Review</h2>
        </div>
        <div className="review-stats">
          <span className="stat-selected">{summary.selected} Selected</span>
          <span className="stat-maybe">{summary.maybe} Maybe</span>
          <span className="stat-rejected">{summary.rejected} Rejected</span>
          <span className="stat-cull">Cull ratio {summary.cull_ratio}%</span>
        </div>
      </header>

      <div className="filter-tabs">
        {(["all", "selected", "maybe", "rejected"] as Filter[]).map((f) => (
          <button
            key={f}
            className={`tab ${filter === f ? "active" : ""} tab-${f}`}
            onClick={() => setFilter(f)}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
            {f === "all" && ` (${results.length})`}
            {f === "selected" && ` (${summary.selected})`}
            {f === "maybe" && ` (${summary.maybe})`}
            {f === "rejected" && ` (${summary.rejected})`}
          </button>
        ))}
      </div>

      <div className="photo-grid">
        {visible.map((r) => (
          <PhotoCard key={r.path} result={r} />
        ))}
      </div>

      <div className="export-bar">
        <div className="export-status">{exportStatus}</div>
        <div className="export-buttons">
          <button
            className="btn-export"
            disabled={exporting}
            onClick={() => onExport(true, false)}
          >
            {exporting ? "Writing…" : "Write XMP"}
          </button>
          <button
            className="btn-export btn-html"
            disabled={exporting}
            onClick={() => onExport(false, true)}
          >
            {exporting ? "Generating…" : "HTML Report"}
          </button>
          {htmlPath && (
            <button
              className="btn-export btn-open"
              onClick={() => openPath(htmlPath)}
            >
              Open Report ↗
            </button>
          )}
        </div>
        <div className="export-dir">Output: {outputDir}</div>
      </div>
    </div>
  );
}

function PhotoCard({ result: r }: { result: Result }) {
  const src = convertFileSrc(r.path);
  const filename = r.path.split("/").pop() ?? r.path;

  return (
    <div className={`photo-card card-${r.category}`}>
      <div className="card-img-wrap">
        <img src={src} alt={filename} loading="lazy" />
        {r.is_duplicate && <span className="badge badge-dup">DUP</span>}
      </div>
      <div className="card-body">
        <div className="card-filename" title={filename}>{filename}</div>
        <div className="card-stars">{STARS[r.stars] ?? "★☆☆☆☆"}</div>
        <div className="card-scores">
          Score {r.combined_score?.toFixed(1)} &nbsp;·&nbsp;
          Sharp {r.sharpness_score?.toFixed(0)} &nbsp;·&nbsp;
          Exp {r.exposure_score?.toFixed(0)}
          {r.face_count > 0 && ` · 👤${r.face_count}`}
        </div>
        <div className="card-badges">
          {r.is_blurry && <span className="badge badge-blur">BLUR</span>}
          {r.face_count > 0 && !r.eyes_open && <span className="badge badge-eyes">EYES</span>}
        </div>
      </div>
    </div>
  );
}
