# 🌍 Digital Carbon Footprint Analyzer

> Quantify, visualize, and reduce the CO₂ emissions from your everyday digital habits.

## Overview

Every app you use has an environmental cost. This tool analyzes **daily digital app usage** and translates it into measurable CO₂ emissions using publicly available environmental metrics. It then generates interactive dashboards and **what-if scenario analyses** to help you understand which behavioral changes would have the greatest environmental impact.

Built with Python, Excel, Power BI, and Tableau.

---

## Features

- **Per-app CO₂ quantification** using IEA 2023 + Carbon Trust emission factors
- **Device energy multipliers** (smartphone vs. laptop vs. gaming console)
- **Category breakdown** (Entertainment, Work, Social, Productivity)
- **What-if scenarios** to model emission reductions from specific behavior changes
- **Dashboard export** as high-resolution PNG (Power BI / Tableau compatible data also included)

---

## Project Structure

```
digital-carbon-footprint-analyzer/
├── analyzer.py              # Main analysis + visualization script
├── requirements.txt         # Python dependencies
├── data/
│   └── usage_data.csv       # Your personal usage profile (editable)
├── outputs/
│   └── carbon_dashboard.png # Auto-generated 4-panel dashboard
├── excel/
│   └── carbon_footprint_model.xlsx  # Excel what-if model
└── README.md
```

---

## Emission Factors Reference

| Activity | CO₂ per Minute | Source |
|---|---|---|
| Video Streaming (HD) | 0.036 g | IEA 2023 |
| Video Streaming (4K) | 0.072 g | Carbon Trust |
| Video Calls (1080p) | 0.024 g | Shift Project |
| Social Media (Video) | 0.018 g | IEA 2023 |
| Online Gaming | 0.016 g | Carbon Trust |
| AI Assistants | 0.020 g | Estimated |
| Music Streaming | 0.003 g | IEA 2023 |

---

## Sample Results

For a typical tech-heavy user profile:

| Metric | Value |
|---|---|
| Daily CO₂ | ~0.8 kg |
| Annual CO₂ | ~290 kg |
| Top emitter | Video Streaming |
| Best single action | Switch HD → SD (saves ~35 kg/yr) |

---

## What-If Scenarios

The analyzer models 5 key behavioral changes and their annual CO₂ savings:

1. Switch HD streaming to SD
2. Reduce social video usage by 30 min/day
3. Replace gaming console with laptop for gaming
4. Halve AI assistant usage
5. Watch streaming on laptop instead of Smart TV

---

## Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/sandeepkothuri/digital-carbon-footprint-analyzer.git
cd digital-carbon-footprint-analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Edit your usage profile
# Open data/usage_data.csv and update minutes_per_day values

# 4. Run the analyzer
python analyzer.py
```

---

## Customize Your Profile

Edit `analyzer.py` → `get_sample_usage_data()` to reflect your actual usage, or modify `data/usage_data.csv`. The analyzer automatically recalculates all emissions and scenarios.

---

## Tech Stack

- **Python 3.10+** (pandas, numpy, matplotlib)
- **Excel** — original data modeling and what-if analysis
- **Power BI** — enterprise dashboard version
- **Tableau** — per-app carbon footprint visualization

---

## Data Sources

- [IEA – Digitisation and Energy (2023)](https://www.iea.org/reports/digitisation-and-energy)
- [Carbon Trust – Carbon Impact of Video Streaming](https://www.carbontrust.com/our-work-and-impact/guides-reports-and-tools/carbon-impact-of-video-streaming)
- [The Shift Project – Lean ICT Report](https://theshiftproject.org/en/lean-ict-2/)

---

## Author

**Sandeep K** · [LinkedIn](https://www.linkedin.com/in/sandeep-kothuri-9b99142b6/) · [GitHub](https://github.com/sandeepkothuri)

*CSULB – Master of Science in Information Systems | Feb–Mar 2025*
