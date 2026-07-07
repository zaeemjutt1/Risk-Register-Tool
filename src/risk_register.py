#!/usr/bin/env python3
"""
Risk Register Automation Tool
==============================
Automates the generation of an ISO 27005-aligned risk register from a simple
CSV input. Calculates risk scores (Likelihood x Impact), classifies risk
levels, sorts findings by priority, and exports a formatted report in
Markdown, CSV, and optionally HTML.

Author: Affan Bin Adnan
License: MIT
"""

import csv
import argparse
import sys
from pathlib import Path
from datetime import datetime


# ── Risk scoring configuration (ISO 27005-aligned) ──────────────────────────

RISK_LEVELS = {
    range(1, 3): "Low",
    range(3, 5): "Medium",
    range(5, 9): "High",      # NOTE: 5,6,7,8
    range(9, 10): "Critical", # 9
}


def classify_risk(score: int) -> str:
    """Map a numeric risk score (Likelihood x Impact, 1-9) to a risk level."""
    for score_range, level in RISK_LEVELS.items():
        if score in score_range:
            return level
    return "Unknown"


def risk_color(level: str) -> str:
    """Return a markdown-friendly emoji indicator for the risk level."""
    return {
        "Critical": "🔴",
        "High": "🟠",
        "Medium": "🟡",
        "Low": "🟢",
    }.get(level, "⚪")


# ── Core data handling ───────────────────────────────────────────────────────

class RiskItem:
    """Represents a single risk entry from the input CSV."""

    def __init__(self, row: dict):
        self.id = row.get("id", "").strip()
        self.asset = row.get("asset", "").strip()
        self.threat = row.get("threat", "").strip()
        self.existing_controls = row.get("existing_controls", "").strip()
        self.likelihood = int(row.get("likelihood", 0))
        self.impact = int(row.get("impact", 0))
        self.recommended_action = row.get("recommended_action", "").strip()
        self.iso_control = row.get("iso_control", "").strip()

        self.score = self.likelihood * self.impact
        self.level = classify_risk(self.score)

    def to_dict(self) -> dict:
        return {
            "ID": self.id,
            "Asset": self.asset,
            "Threat / Vulnerability": self.threat,
            "Existing Controls": self.existing_controls,
            "Likelihood": self.likelihood,
            "Impact": self.impact,
            "Risk Score": self.score,
            "Risk Level": self.level,
            "Recommended Action": self.recommended_action,
            "ISO 27001 Control": self.iso_control,
        }


def load_risks(csv_path: Path) -> list[RiskItem]:
    """Load and parse risk entries from a CSV file."""
    if not csv_path.exists():
        sys.exit(f"Error: input file not found: {csv_path}")

    risks = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"id", "asset", "threat", "likelihood", "impact"}
        if not required.issubset(set(reader.fieldnames or [])):
            missing = required - set(reader.fieldnames or [])
            sys.exit(f"Error: CSV is missing required columns: {missing}")

        for row in reader:
            try:
                risks.append(RiskItem(row))
            except ValueError:
                print(f"Warning: skipping malformed row: {row}", file=sys.stderr)

    return risks


# ── Report generation ────────────────────────────────────────────────────────

def generate_markdown_report(risks: list[RiskItem], org_name: str) -> str:
    """Generate a formatted Markdown risk register report."""
    risks_sorted = sorted(risks, key=lambda r: r.score, reverse=True)

    total = len(risks_sorted)
    critical = sum(1 for r in risks_sorted if r.level == "Critical")
    high = sum(1 for r in risks_sorted if r.level == "High")
    medium = sum(1 for r in risks_sorted if r.level == "Medium")
    low = sum(1 for r in risks_sorted if r.level == "Low")

    lines = []
    lines.append(f"# Risk Register Report — {org_name}")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Methodology:** ISO/IEC 27005 — Likelihood x Impact (1-9 scale)")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Total Risks | 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low |")
    lines.append(f"|---|---|---|---|---|")
    lines.append(f"| {total} | {critical} | {high} | {medium} | {low} |")
    lines.append("")
    lines.append("## Risk Register (sorted by priority)")
    lines.append("")
    lines.append("| ID | Asset | Threat / Vulnerability | Likelihood | Impact | Score | Level | Recommended Action | ISO Control |")
    lines.append("|---|---|---|---|---|---|---|---|---|")

    for r in risks_sorted:
        lines.append(
            f"| {r.id} | {r.asset} | {r.threat} | {r.likelihood} | {r.impact} "
            f"| {r.score} | {risk_color(r.level)} {r.level} | {r.recommended_action} | {r.iso_control} |"
        )

    lines.append("")
    lines.append("## Risk Level Definitions")
    lines.append("")
    lines.append("| Score Range | Level | Action Required |")
    lines.append("|---|---|---|")
    lines.append("| 9 | 🔴 Critical | Immediate remediation (within 7 days) |")
    lines.append("| 5-8 | 🟠 High | Remediation within 30 days |")
    lines.append("| 3-4 | 🟡 Medium | Remediation within 90 days |")
    lines.append("| 1-2 | 🟢 Low | Monitor / accept with review |")
    lines.append("")
    lines.append("---")
    lines.append("*Generated by [risk-register-tool](https://github.com/) — an open-source ISO 27005-aligned risk register automation tool.*")

    return "\n".join(lines)


def export_csv(risks: list[RiskItem], output_path: Path):
    """Export the sorted risk register back to CSV."""
    risks_sorted = sorted(risks, key=lambda r: r.score, reverse=True)
    fieldnames = list(risks_sorted[0].to_dict().keys()) if risks_sorted else []

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in risks_sorted:
            writer.writerow(r.to_dict())


# ── CLI entry point ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate an ISO 27005-aligned risk register report from a CSV of assets and risks."
    )
    parser.add_argument("input", type=Path, help="Path to input CSV file")
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("output"),
        help="Output directory (default: ./output)"
    )
    parser.add_argument(
        "-n", "--name", type=str, default="Organization",
        help="Organization name to display in the report"
    )
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    print(f"Loading risks from {args.input}...")
    risks = load_risks(args.input)
    print(f"Loaded {len(risks)} risk entries.")

    if not risks:
        sys.exit("No valid risk entries found. Exiting.")

    md_report = generate_markdown_report(risks, args.name)
    md_path = args.output / "risk_register_report.md"
    md_path.write_text(md_report, encoding="utf-8")
    print(f"Markdown report written to {md_path}")

    csv_path = args.output / "risk_register_sorted.csv"
    export_csv(risks, csv_path)
    print(f"Sorted CSV written to {csv_path}")

    critical_count = sum(1 for r in risks if r.level == "Critical")
    high_count = sum(1 for r in risks if r.level == "High")
    print(f"\nSummary: {critical_count} Critical, {high_count} High risk findings require priority attention.")


if __name__ == "__main__":
    main()
