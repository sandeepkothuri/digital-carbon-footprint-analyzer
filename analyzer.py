"""
Digital Carbon Footprint Analyzer
------------------------------------
Analyzed digital app usage and quantified CO2 emissions using
publicly available environmental metrics (IEA 2023, Carbon Trust).

Built Power BI and Tableau dashboards to visualize per-app carbon
footprint and support what-if user behavior analysis.

Identified high-emission digital activities and recommended usage
reductions to promote sustainable tech habits.

Author : Sandeep K | CSULB M.S. Information Systems
Period : Feb 2025 - Mar 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import os, warnings
warnings.filterwarnings("ignore")

os.makedirs("outputs", exist_ok=True)

# ── 1. Load Data ───────────────────────────────────────────────────────────────
df = pd.read_csv("data/usage_data.csv")
print(f"Dataset loaded: {len(df)} apps tracked")
print(f"Total daily CO2:  {df['daily_co2_grams'].sum()/1000:.4f} kg")
print(f"Total annual CO2: {df['annual_co2_kg'].sum():.2f} kg\n")

# ── 2. Summary ─────────────────────────────────────────────────────────────────
print("── Top 5 CO2 Emitters (Annual) ─────────────────")
top5 = df.nlargest(5, "annual_co2_kg")[["app", "category", "device", "annual_co2_kg"]]
print(top5.to_string(index=False))

print("\n── Emissions by Category ───────────────────────")
cat = df.groupby("category")["annual_co2_kg"].sum().sort_values(ascending=False)
for name, val in cat.items():
    print(f"  {name:<20} {val:.2f} kg/yr")

# ── 3. What-If Scenario Analysis ──────────────────────────────────────────────
# Resume: "support what-if user behavior analysis"
scenarios = {
    "Switch YouTube/Netflix HD → SD":       {"apps": ["YouTube (HD Streaming)", "Netflix (HD Streaming)"], "reduction": 0.60},
    "Reduce TikTok/Reels by 30 min/day":    {"apps": ["TikTok", "Instagram (Reels/Video)"],              "new_minutes": 20},
    "Replace Gaming Console with Laptop":   {"apps": ["Online Gaming"],                                   "new_device": "Laptop"},
    "Cut AI Tool usage by 50%":             {"apps": ["ChatGPT / AI Tools"],                              "reduction": 0.50},
    "Use Smartphone instead of Smart TV":   {"apps": ["YouTube (HD Streaming)"],                          "new_device": "Smartphone"},
}

DEVICE_MULTIPLIERS = {"Smartphone":0.4,"Laptop":1.0,"Desktop PC":2.2,"Smart TV":1.8,"Gaming Console":2.5}
baseline = df["annual_co2_kg"].sum()
scenario_results = []

for name, params in scenarios.items():
    mod = df.copy()
    for app in params["apps"]:
        mask = mod["app"] == app
        if "reduction" in params:
            mod.loc[mask, "minutes_per_day"] *= (1 - params["reduction"])
        if "new_minutes" in params:
            mod.loc[mask, "minutes_per_day"] = params["new_minutes"]
        if "new_device" in params:
            mod.loc[mask, "device"] = params["new_device"]
            mod.loc[mask, "device_energy_multiplier"] = DEVICE_MULTIPLIERS[params["new_device"]]
    mod["annual_co2_kg"] = mod["minutes_per_day"] * mod["emission_factor_g_per_min"] * mod["device_energy_multiplier"] * 365 / 1000
    saving = baseline - mod["annual_co2_kg"].sum()
    scenario_results.append({"scenario": name, "saving_kg": round(saving, 2), "saving_pct": round(saving/baseline*100, 1)})

sc_df = pd.DataFrame(scenario_results).sort_values("saving_kg", ascending=False)
print("\n── What-If Scenario Savings ────────────────────")
print(sc_df.to_string(index=False))

# ── 4. Dashboard ───────────────────────────────────────────────────────────────
BG    = "#0d1117"
PANEL = "#161b22"
WHITE = "#f0f6fc"
GRAY  = "#8b949e"
GREEN = "#2ecc71"

CAT_COLORS = {
    "Entertainment": "#e74c3c",
    "Social Media":  "#9b59b6",
    "Productivity":  "#3498db",
}

fig = plt.figure(figsize=(18, 12))
fig.patch.set_facecolor(BG)
gs = GridSpec(2, 3, figure=fig, hspace=0.50, wspace=0.35)
ax1 = fig.add_subplot(gs[0, :2])
ax2 = fig.add_subplot(gs[0, 2])
ax3 = fig.add_subplot(gs[1, :2])
ax4 = fig.add_subplot(gs[1, 2])

for ax in [ax1, ax2, ax3, ax4]:
    ax.set_facecolor(PANEL)
    for spine in ax.spines.values():
        spine.set_edgecolor("#30363d")

# Panel 1 – Per-app annual CO2
sdf    = df.sort_values("annual_co2_kg", ascending=True)
colors = [CAT_COLORS.get(c, GRAY) for c in sdf["category"]]
bars   = ax1.barh(sdf["app"], sdf["annual_co2_kg"], color=colors, edgecolor=BG, linewidth=0.5)
ax1.set_title("Annual CO₂ Emissions by App (kg)", color=WHITE, fontsize=12, fontweight="bold", pad=10)
ax1.set_xlabel("kg CO₂ / year", color=GRAY, fontsize=10)
ax1.tick_params(colors=GRAY)
for bar, val in zip(bars, sdf["annual_co2_kg"]):
    ax1.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
             f"{val:.2f}", va="center", color=GRAY, fontsize=9)
patches = [mpatches.Patch(color=c, label=l) for l, c in CAT_COLORS.items()]
ax1.legend(handles=patches, facecolor=PANEL, labelcolor=GRAY, edgecolor="#30363d", fontsize=9)

# Panel 2 – Category pie
cat_totals = df.groupby("category")["annual_co2_kg"].sum()
ax2.pie(cat_totals.values,
        labels=cat_totals.index,
        colors=[CAT_COLORS.get(c, GRAY) for c in cat_totals.index],
        autopct="%1.0f%%", startangle=140,
        textprops={"color": GRAY, "fontsize": 10},
        wedgeprops={"edgecolor": BG, "linewidth": 1.5})
ax2.set_title("Emissions by Category", color=WHITE, fontsize=12, fontweight="bold", pad=10)

# Panel 3 – What-if scenario savings
sc_sorted = sc_df.sort_values("saving_kg")
bar_sc = ax3.barh(sc_sorted["scenario"], sc_sorted["saving_kg"], color=GREEN, alpha=0.85, edgecolor=BG)
ax3.set_title("Annual CO₂ Savings per Behaviour Change (kg)", color=WHITE, fontsize=12, fontweight="bold", pad=10)
ax3.set_xlabel("kg CO₂ saved / year", color=GRAY, fontsize=10)
ax3.tick_params(colors=GRAY)
for bar, val, pct in zip(bar_sc, sc_sorted["saving_kg"], sc_sorted["saving_pct"]):
    ax3.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2,
             f"{val:.2f} kg  ({pct}%)", va="center", color=GRAY, fontsize=9)

# Panel 4 – Key stats
top_app    = df.loc[df["annual_co2_kg"].idxmax(), "app"]
best_action = sc_df.iloc[0]["scenario"]
best_save   = sc_df.iloc[0]["saving_kg"]
ax4.axis("off")
summary = (
    f"  Apps tracked:      {len(df)}\n\n"
    f"  Annual CO2:        {df['annual_co2_kg'].sum():.2f} kg\n\n"
    f"  Top emitter:\n"
    f"  {top_app}\n\n"
    f"  Best action:\n"
    f"  {best_action[:30]}\n"
    f"  saves {best_save:.2f} kg/yr\n\n"
    f"  Equivalent to:\n"
    f"  {df['annual_co2_kg'].sum()/0.12:.0f} km driven"
)
ax4.text(0.08, 0.95, "Key Stats", fontsize=13, fontweight="bold",
         color=WHITE, transform=ax4.transAxes, va="top")
ax4.text(0.08, 0.78, summary, fontsize=10, color=GRAY,
         transform=ax4.transAxes, va="top", linespacing=1.6, family="monospace")

fig.suptitle("Digital Carbon Footprint Analyzer — Dashboard",
             fontsize=15, fontweight="bold", color=WHITE, y=0.98)

plt.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("\nDashboard saved → outputs/dashboard.png")
print("✅  Analysis complete.")
