# 🛡️ Risk Register Automation Tool

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ISO 27005](https://img.shields.io/badge/Methodology-ISO%2027005-orange)](https://www.iso.org/standard/75281.html)

A lightweight Python CLI tool that automates the generation of an **ISO/IEC 27005-aligned risk register** from a simple CSV input. Built for security analysts, GRC professionals, and students who need to quickly turn a list of identified risks into a properly formatted, prioritized risk register report.

## Why This Tool?

Manually maintaining a risk register in Excel is slow and error-prone — recalculating scores, re-sorting by priority, and reformatting tables every time a risk changes. This tool automates that entire workflow:

- Input a simple CSV of assets, threats, and likelihood/impact ratings
- Get back a fully sorted, color-coded, ISO 27005-aligned risk register
- Export to both **Markdown** (for documentation/GitHub/Confluence) and **CSV** (for Excel)

## Features

- ✅ Automatic risk scoring (Likelihood × Impact, 1–9 scale)
- ✅ ISO/IEC 27005-aligned risk level classification (Low / Medium / High / Critical)
- ✅ Auto-sorts findings by priority (highest risk first)
- ✅ Maps findings to ISO 27001 Annex A controls
- ✅ Clean Markdown report output with summary statistics
- ✅ CSV export for further analysis in Excel
- ✅ Zero external dependencies — pure Python standard library

## Installation

```bash
git clone https://github.com/yourusername/risk-register-tool.git
cd risk-register-tool
```

No dependencies to install — this tool uses only the Python standard library (Python 3.9+).

## Usage

```bash
python3 src/risk_register.py sample_data/sample_risks.csv -n "Your Organization Name" -o output
```

### Arguments

| Flag | Description | Default |
|------|-------------|---------|
| `input` | Path to input CSV file (required) | — |
| `-o`, `--output` | Output directory for reports | `./output` |
| `-n`, `--name` | Organization name shown in report | `Organization` |

### Input CSV Format

Your input CSV must contain these columns:

| Column | Description | Required |
|--------|-------------|----------|
| `id` | Unique risk identifier (e.g. R1, R2) | Yes |
| `asset` | The asset at risk | Yes |
| `threat` | Threat / vulnerability description | Yes |
| `likelihood` | Likelihood score (1-3) | Yes |
| `impact` | Impact score (1-3) | Yes |
| `existing_controls` | Current controls in place | No |
| `recommended_action` | Suggested remediation | No |
| `iso_control` | Mapped ISO 27001 Annex A control | No |

See [`sample_data/sample_risks.csv`](sample_data/sample_risks.csv) for a full example.

## Example Output

```
Loading risks from sample_data/sample_risks.csv...
Loaded 10 risk entries.
Markdown report written to output/risk_register_report.md
Sorted CSV written to output/risk_register_sorted.csv

Summary: 3 Critical, 5 High risk findings require priority attention.
```

The generated Markdown report includes a summary table, a fully sorted risk register, and risk level definitions — ready to paste into documentation or a client deliverable.

## Risk Scoring Methodology

This tool follows a simplified **ISO/IEC 27005** qualitative risk assessment approach:

```
Risk Score = Likelihood (1-3) × Impact (1-3)
```

| Score | Level | Action Required |
|-------|-------|------------------|
| 9 | 🔴 Critical | Immediate remediation (within 7 days) |
| 5–8 | 🟠 High | Remediation within 30 days |
| 3–4 | 🟡 Medium | Remediation within 90 days |
| 1–2 | 🟢 Low | Monitor / accept with review |

## Project Structure

```
risk-register-tool/
├── src/
│   └── risk_register.py      # Main CLI tool
├── sample_data/
│   └── sample_risks.csv      # Example input
├── output/                   # Generated reports (gitignored)
├── README.md
├── LICENSE
└── requirements.txt
```

## Roadmap

- [ ] Add HTML report export with interactive sorting
- [ ] Add support for risk treatment tracking (accept/mitigate/transfer/avoid)
- [ ] Add NIST CSF control mapping option alongside ISO 27001
- [ ] Add unit tests with pytest
- [ ] Add a simple web UI using Flask

## Author

**Muhammad Zaeem Siddiqui**

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
