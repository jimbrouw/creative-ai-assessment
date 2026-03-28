import { useState } from "react";
import { open } from "@tauri-apps/plugin-dialog";

interface Props {
  onStart: (params: {
    inputDir: string;
    outputDir: string;
    mode: string;
    keepDuplicates: number;
  }) => void;
}

export function Welcome({ onStart }: Props) {
  const [folder, setFolder] = useState("");
  const [mode, setMode] = useState("balanced");
  const [keepDuplicates, setKeepDuplicates] = useState(1);
  const [dragging, setDragging] = useState(false);

  async function browse() {
    const selected = await open({ directory: true, multiple: false });
    if (typeof selected === "string") setFolder(selected);
  }

  function handleDragOver(e: React.DragEvent) {
    e.preventDefault();
    setDragging(true);
  }

  function handleDragLeave() {
    setDragging(false);
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragging(false);
    const items = Array.from(e.dataTransfer.items);
    for (const item of items) {
      if (item.kind === "file") {
        const file = item.getAsFile();
        if (file) setFolder(file.path ?? "");
      }
    }
  }

  function handleStart() {
    if (!folder) return;
    onStart({ inputDir: folder, outputDir: folder, mode, keepDuplicates });
  }

  return (
    <div className="welcome">
      <div className="brand">
        <h1>PhotoCull</h1>
        <p>Free, offline photo culling</p>
      </div>

      <div
        className={`drop-zone ${dragging ? "dragging" : ""} ${folder ? "has-folder" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={browse}
      >
        {folder ? (
          <>
            <div className="drop-icon">📁</div>
            <div className="drop-folder">{folder}</div>
            <div className="drop-hint">Click to change folder</div>
          </>
        ) : (
          <>
            <div className="drop-icon">📷</div>
            <div className="drop-label">Drop a photo folder here</div>
            <div className="drop-hint">or click to browse</div>
          </>
        )}
      </div>

      <div className="settings-row">
        <div className="setting">
          <label>Mode</label>
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="strict">Strict — keep top 20%</option>
            <option value="balanced">Balanced — keep top 40%</option>
            <option value="generous">Generous — keep top 60%</option>
          </select>
        </div>
        <div className="setting">
          <label>Keep per burst group</label>
          <input
            type="number"
            min={1}
            max={5}
            value={keepDuplicates}
            onChange={(e) => setKeepDuplicates(Number(e.target.value))}
          />
        </div>
      </div>

      <button className="btn-start" disabled={!folder} onClick={handleStart}>
        Start Culling
      </button>
    </div>
  );
}
