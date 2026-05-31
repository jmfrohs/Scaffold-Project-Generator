#!/usr/bin/env python3
"""Convert coverage data to JSON for live updates."""

import json
import subprocess
from pathlib import Path
from datetime import datetime

def coverage_to_json(output_path="htmlcov/coverage.json"):
    """Convert coverage.json report to live-friendly format."""
    
    json_report = Path("coverage.json")
    
    if not json_report.exists():
        print("[INFO] coverage.json not found. Running coverage report...")
        subprocess.run(["coverage", "json"], check=False)
    
    try:
        with open(json_report) as f:
            data = json.load(f)
        
        # Transform coverage data for live updates
        coverage_data = {
            "timestamp": datetime.now().isoformat(),
            "files": {},
            "overall": {
                "statements": 0,
                "executed": 0,
                "missing": 0,
                "coverage": "0%"
            }
        }
        
        if "files" in data:
            for file_path, file_data in data["files"].items():
                summary = file_data.get("summary", {})
                statements = summary.get("num_statements", 0)
                missing = summary.get("missing_lines", 0)
                executed = statements - missing
                
                coverage_pct = int(100 * executed / statements) if statements > 0 else 0
                
                coverage_data["files"][file_path] = {
                    "statements": statements,
                    "executed": executed,
                    "missing": missing,
                    "coverage": f"{coverage_pct}%"
                }
                
                coverage_data["overall"]["statements"] += statements
                coverage_data["overall"]["executed"] += executed
                coverage_data["overall"]["missing"] += missing
        
        # Calculate overall coverage
        total_stmts = coverage_data["overall"]["statements"]
        if total_stmts > 0:
            overall_pct = int(100 * coverage_data["overall"]["executed"] / total_stmts)
            coverage_data["overall"]["coverage"] = f"{overall_pct}%"
        
        # Write JSON
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(coverage_data, f, indent=2)
        
        print(f"[OK] Coverage data saved to {output_path}")
        
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    coverage_to_json()
