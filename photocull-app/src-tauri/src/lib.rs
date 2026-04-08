use std::io::BufRead;
use std::process::Stdio;
use tauri::{AppHandle, Emitter};

// Path to engine/main.py relative to this Cargo.toml's directory (src-tauri/).
// Goes up two levels: src-tauri → photocull-app → project root → engine/main.py
const ENGINE: &str = concat!(env!("CARGO_MANIFEST_DIR"), "/../../engine/main.py");

fn stream_engine(app: AppHandle, mut child: std::process::Child) -> Result<(), String> {
    let stdout = child.stdout.take().ok_or("Could not capture engine stdout")?;
    let reader = std::io::BufReader::new(stdout);
    for line in reader.lines() {
        if let Ok(line) = line {
            let line = line.trim().to_string();
            if !line.is_empty() {
                if let Ok(val) = serde_json::from_str::<serde_json::Value>(&line) {
                    app.emit("engine-event", val).ok();
                }
            }
        }
    }
    child.wait().map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn run_analysis(
    app: AppHandle,
    input_dir: String,
    mode: String,
    keep_duplicates: u32,
    output_dir: String,
    workers: u32,
) -> Result<(), String> {
    let child = std::process::Command::new("python3")
        .args([
            ENGINE,
            "--input",
            &input_dir,
            "--mode",
            &mode,
            "--keep-duplicates",
            &keep_duplicates.to_string(),
            "--output-dir",
            &output_dir,
            "--workers",
            &workers.to_string(),
        ])
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .spawn()
        .map_err(|e| format!("Failed to start Python engine: {e}"))?;

    stream_engine(app, child)
}

#[tauri::command]
fn run_exports(
    app: AppHandle,
    input_dir: String,
    mode: String,
    keep_duplicates: u32,
    output_dir: String,
    write_xmp: bool,
    write_html: bool,
) -> Result<(), String> {
    let keep_str = keep_duplicates.to_string();
    let mut args = vec![
        ENGINE,
        "--input",
        &input_dir,
        "--mode",
        &mode,
        "--keep-duplicates",
        &keep_str,
        "--output-dir",
        &output_dir,
    ];
    if write_xmp {
        args.push("--write-xmp");
    }
    if write_html {
        args.push("--write-html");
    }

    let child = std::process::Command::new("python3")
        .args(&args)
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .spawn()
        .map_err(|e| format!("Failed to start Python engine: {e}"))?;

    stream_engine(app, child)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![run_analysis, run_exports])
        .run(tauri::generate_context!())
        .expect("error while running PhotoCull");
}
