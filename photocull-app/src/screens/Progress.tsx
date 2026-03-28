interface Props {
  done: number;
  total: number;
  currentFile: string;
  selected: number;
  maybe: number;
  rejected: number;
}

export function Progress({ done, total, currentFile, selected, maybe, rejected }: Props) {
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  return (
    <div className="progress-screen">
      <h2>Analysing photos…</h2>

      <div className="progress-bar-wrap">
        <div className="progress-bar" style={{ width: `${pct}%` }} />
      </div>

      <div className="progress-count">
        {done} of {total} photos &nbsp;·&nbsp; {pct}%
      </div>

      {currentFile && (
        <div className="progress-file">{currentFile}</div>
      )}

      <div className="live-counters">
        <div className="counter counter-selected">
          <span className="counter-num">{selected}</span>
          <span className="counter-label">Selected</span>
        </div>
        <div className="counter counter-maybe">
          <span className="counter-num">{maybe}</span>
          <span className="counter-label">Maybe</span>
        </div>
        <div className="counter counter-rejected">
          <span className="counter-num">{rejected}</span>
          <span className="counter-label">Rejected</span>
        </div>
      </div>
    </div>
  );
}
