# 🌍 Digital Carbon Footprint Analyzer

> Quantify, visualize, and reduce the CO₂ emissions from your everyday digital habits.

![Dashboard](assets/dashboard.png)

## Overview

Every app you use has an environmental cost. This tool analyzes **daily digital app usage** and translates it into measurable CO₂ emissions using publicly available environmental metrics from the IEA and Carbon Trust. It generates dashboards and **what-if scenario analyses** to help identify which behavioral changes would have the greatest environmental impact.

---

## Features

- Per-app CO₂ quantification using IEA 2023 + Carbon Trust emission factors
- Device energy multipliers (smartphone vs. laptop vs. gaming console)
- Category breakdown: Entertainment, Work, Social, Productivity
- What-if scenarios modeling emission reductions from specific behavior changes
- Dark-themed 4-panel dashboard export

---

## Sample Results (Typical Tech-Heavy User)

| Metric | Value |
|---|---|
| Daily CO₂ | ~0.80 kg |
| Annual CO₂ | ~290 kg |
| Top emitter | Video Streaming (HD) |
| Best single action | Switch HD → SD saves ~1.7 kg/yr |

---

## What-If Scenarios

| Action | Annual Saving |
|---|---|
| Switch HD → SD Streaming | 1.70 kg |
| Smart TV → Laptop Streaming | 1.26 kg |
| Console → Laptop Gaming | 0.53 kg |
| Cut Social Video -30 min/day | 0.08 kg |
| Halve AI Assistant Usage | 0.07 kg |

---

## Setup & Run

```bash
git clone https://github.com/sandeepkothuri/digital-carbon-footprint-analyzer.git
cd digital-carbon-footprint-analyzer
pip install -r requirements.txt
python analyzer.py
```

---

## Data Sources

- [IEA – Digitisation and Energy (2023)](https://www.iea.org/reports/digitisation-and-energy)
- [Carbon Trust – Carbon Impact of Video Streaming](https://www.carbontrust.com)
- [The Shift Project – Lean ICT Report](https://theshiftproject.org)

---

## Tech Stack

`Python` `pandas` `numpy` `matplotlib` `Power BI` `Tableau` `Excel`

---

## Author

**Sandeep K** · [LinkedIn](https://www.linkedin.com/in/sandeep-kothuri-9b99142b6/) · [GitHub](https://github.com/sandeepkothuri) · [Portfolio](https://sandeepkothuri.github.io)

*CSULB – M.S. Information Systems | Feb–Mar 2025*
