import { useCallback, useState } from "react";
import { Welcome } from "./screens/Welcome";
import { Progress } from "./screens/Progress";
import { Review } from "./screens/Review";
import { useEngine, EngineEvent, Result, Summary } from "./hooks/useEngine";

type Screen = "welcome" | "progress" | "review";

interface RunConfig {
  inputDir: string;
  outputDir: string;
  mode: string;
  keepDuplicates: number;
}

const EMPTY_SUMMARY: Summary = { total: 0, selected: 0, maybe: 0, rejected: 0, cull_ratio: 0 };

export default function App() {
  const [screen, setScreen] = useState<Screen>("welcome");
  const [config, setConfig] = useState<RunConfig>({
    inputDir: "", outputDir: "", mode: "balanced", keepDuplicates: 1,
  });

  // Progress state
  const [done, setDone] = useState(0);
  const [total, setTotal] = useState(0);
  const [currentFile, setCurrentFile] = useState("");
  const [liveSelected, setLiveSelected] = useState(0);
  const [liveMaybe, setLiveMaybe] = useState(0);
  const [liveRejected, setLiveRejected] = useState(0);

  // Review state
  const [results, setResults] = useState<Result[]>([]);
  const [summary, setSummary] = useState<Summary>(EMPTY_SUMMARY);
  const [exporting, setExporting] = useState(false);
  const [exportStatus, setExportStatus] = useState("");
  const [htmlPath, setHtmlPath] = useState("");

  const handleEvent = useCallback((e: EngineEvent) => {
    switch (e.event) {
      case "start":
        setTotal(e.total ?? 0);
        setDone(0);
        break;
      case "progress":
        setDone(e.done ?? 0);
        setCurrentFile(e.file ?? "");
        break;
      case "results":
        if (e.batch) {
          setResults((prev) => {
            const updated = [...prev, ...e.batch!];
            setLiveSelected(updated.filter((r) => r.category === "selected").length);
            setLiveMaybe(updated.filter((r) => r.category === "maybe").length);
            setLiveRejected(updated.filter((r) => r.category === "rejected").length);
            return updated;
          });
        }
        break;
      case "complete":
        if (e.summary) setSummary(e.summary);
        setScreen("review");
        break;
      case "xmp_done":
        setExporting(false);
        setExportStatus(`✅ ${e.count} XMP files written`);
        break;
      case "html_done":
        setExporting(false);
        setExportStatus("✅ HTML report ready");
        setHtmlPath(e.path ?? "");
        break;
      case "error":
        setExporting(false);
        setExportStatus(`❌ ${e.message}`);
        break;
    }
  }, []);

  const { startAnalysis, runExports } = useEngine(handleEvent);

  function handleStart(params: RunConfig) {
    setConfig(params);
    setResults([]);
    setDone(0);
    setTotal(0);
    setCurrentFile("");
    setLiveSelected(0);
    setLiveMaybe(0);
    setLiveRejected(0);
    setSummary(EMPTY_SUMMARY);
    setExportStatus("");
    setHtmlPath("");
    setScreen("progress");

    startAnalysis({
      input_dir: params.inputDir,
      output_dir: params.outputDir,
      mode: params.mode,
      keep_duplicates: params.keepDuplicates,
      workers: 4,
    }).catch((err) => {
      setExportStatus(`❌ ${err}`);
      setScreen("review");
    });
  }

  function handleExport(xmp: boolean, html: boolean) {
    setExporting(true);
    setExportStatus(xmp ? "Writing XMP files…" : "Generating HTML report…");
    runExports({
      input_dir: config.inputDir,
      output_dir: config.outputDir,
      mode: config.mode,
      keep_duplicates: config.keepDuplicates,
      write_xmp: xmp,
      write_html: html,
    }).catch((err) => {
      setExporting(false);
      setExportStatus(`❌ ${err}`);
    });
  }

  function handleReset() {
    setScreen("welcome");
  }

  return (
    <div className="app">
      {screen === "welcome" && <Welcome onStart={handleStart} />}
      {screen === "progress" && (
        <Progress
          done={done}
          total={total}
          currentFile={currentFile}
          selected={liveSelected}
          maybe={liveMaybe}
          rejected={liveRejected}
        />
      )}
      {screen === "review" && (
        <Review
          results={results}
          summary={summary}
          inputDir={config.inputDir}
          outputDir={config.outputDir}
          mode={config.mode}
          keepDuplicates={config.keepDuplicates}
          onExport={handleExport}
          exporting={exporting}
          exportStatus={exportStatus}
          htmlPath={htmlPath}
          onReset={handleReset}
        />
      )}
    </div>
  );
}
