"""
Digital Carbon Footprint Analyzer
====================================
Quantifies CO₂ emissions from digital app usage and supports
what-if behavior analysis via interactive dashboards.

Author: Sandeep K
Date: Feb–Mar 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")


# ─── 1. Emission Factors ──────────────────────────────────────────────────────
# Sources: IEA 2023, Carbon Trust Digital Footprint Report, Shift Project

EMISSION_FACTORS = {
    # App category : grams CO₂ per minute of active use
    "Video Streaming (HD)":     0.036,   # Netflix/YouTube HD
    "Video Streaming (4K)":     0.072,   # 4K content
    "Video Calls":              0.024,   # Zoom/Teams 1080p
    "Social Media (Feed)":      0.006,   # Scrolling feeds
    "Social Media (Video)":     0.018,   # TikTok/Reels
    "Music Streaming":          0.003,   # Spotify, Apple Music
    "Cloud Storage Sync":       0.002,   # Background sync
    "Email (w/ attachments)":   0.050,   # per email sent (not per minute)
    "Web Browsing":             0.004,   # Average page load
    "Online Gaming":            0.016,   # Multiplayer gaming
    "AI Assistants":            0.020,   # ChatGPT-class queries
    "Cryptocurrency":           0.180,   # Per transaction (Bitcoin avg)
}

# Device energy multipliers (relative to a standard laptop = 1.0)
DEVICE_MULTIPLIERS = {
    "Smartphone":     0.4,
    "Laptop":         1.0,
    "Desktop PC":     2.2,
    "Smart TV":       1.8,
    "Gaming Console": 2.5,
}


# ─── 2. Usage Data ────────────────────────────────────────────────────────────

def get_sample_usage_data() -> pd.DataFrame:
    """
    A realistic weekly usage profile for a typical tech-heavy user.
    Units: minutes/day for time-based apps; count/day for email/crypto.
    """
    return pd.DataFrame([
        {"app": "Video Streaming (HD)",    "minutes_per_day": 120, "device": "Smart TV",     "category": "Entertainment"},
        {"app": "Social Media (Video)",    "minutes_per_day":  90, "device": "Smartphone",   "category": "Social"},
        {"app": "Video Calls",             "minutes_per_day":  60, "device": "Laptop",       "category": "Work"},
        {"app": "Social Media (Feed)",     "minutes_per_day":  45, "device": "Smartphone",   "category": "Social"},
        {"app": "Online Gaming",           "minutes_per_day":  60, "device": "Gaming Console","category": "Entertainment"},
        {"app": "Web Browsing",            "minutes_per_day":  40, "device": "Laptop",       "category": "Productivity"},
        {"app": "AI Assistants",           "minutes_per_day":  20, "device": "Laptop",       "category": "Productivity"},
        {"app": "Music Streaming",         "minutes_per_day":  90, "device": "Smartphone",   "category": "Entertainment"},
        {"app": "Cloud Storage Sync",      "minutes_per_day":  30, "device": "Laptop",       "category": "Productivity"},
        {"app": "Email (w/ attachments)",  "minutes_per_day":  10, "device": "Laptop",       "category": "Work"},
    ])


# ─── 3. Calculate Emissions ────────────────────────────────────────────────────

def calculate_emissions(df: pd.DataFrame) -> pd.DataFrame:
    """Adds daily and annual CO₂ (grams) columns to the usage DataFrame."""
    df = df.copy()
    df["emission_factor"] = df["app"].map(EMISSION_FACTORS)
    df["device_multiplier"] = df["device"].map(DEVICE_MULTIPLIERS)

    # daily CO₂ in grams
    df["daily_co2_g"] = (
        df["minutes_per_day"]
        * df["emission_factor"]
        * df["device_multiplier"]
    )
    df["annual_co2_kg"] = (df["daily_co2_g"] * 365) / 1000

    return df


# ─── 4. What-If Scenarios ─────────────────────────────────────────────────────

REDUCTION_SCENARIOS = {
    "Switch HD → SD streaming":           {"app": "Video Streaming (HD)", "reduction_pct": 0.60},
    "Cut social video by 30 min/day":     {"app": "Social Media (Video)", "new_minutes": 60},
    "Replace gaming console with laptop": {"app": "Online Gaming",        "new_device": "Laptop"},
    "Halve AI assistant usage":           {"app": "AI Assistants",        "reduction_pct": 0.50},
    "Switch Smart TV → Laptop streaming": {"app": "Video Streaming (HD)", "new_device": "Laptop"},
}


def apply_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a summary of annual CO₂ savings per scenario."""
    baseline_annual = df["annual_co2_kg"].sum()
    records = []

    for name, params in REDUCTION_SCENARIOS.items():
        mod = df.copy()
        mask = mod["app"] == params["app"]

        if "reduction_pct" in params:
            mod.loc[mask, "minutes_per_day"] *= (1 - params["reduction_pct"])
        if "new_minutes" in params:
            mod.loc[mask, "minutes_per_day"] = params["new_minutes"]
        if "new_device" in params:
            mod.loc[mask, "device"] = params["new_device"]
            mod.loc[mask, "device_multiplier"] = DEVICE_MULTIPLIERS[params["new_device"]]

        mod["daily_co2_g"] = (
            mod["minutes_per_day"]
            * mod["emission_factor"]
            * mod["device_multiplier"]
        )
        mod["annual_co2_kg"] = (mod["daily_co2_g"] * 365) / 1000
        new_annual = mod["annual_co2_kg"].sum()

        records.append({
            "scenario":        name,
            "baseline_kg":     round(baseline_annual, 2),
            "new_annual_kg":   round(new_annual, 2),
            "saving_kg":       round(baseline_annual - new_annual, 2),
            "saving_pct":      round((baseline_annual - new_annual) / baseline_annual * 100, 1),
        })

    return pd.DataFrame(records).sort_values("saving_kg", ascending=False)


# ─── 5. Visualisation ─────────────────────────────────────────────────────────

CAT_COLORS = {
    "Entertainment": "#2ecc71",
    "Social":        "#e74c3c",
    "Work":          "#3498db",
    "Productivity":  "#f39c12",
}


def build_dashboard(df: pd.DataFrame, scenarios: pd.DataFrame):
    """Generates and saves a 4-panel dashboard."""
    fig = plt.figure(figsize=(18, 14))
    fig.patch.set_facecolor("#f8f9fa")
    gs = GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    ax1 = fig.add_subplot(gs[0, :2])   # Per-app emissions (bar)
    ax2 = fig.add_subplot(gs[0, 2])    # Category pie
    ax3 = fig.add_subplot(gs[1, :2])   # What-if scenarios
    ax4 = fig.add_subplot(gs[1, 2])    # Annual summary

    # ── Panel 1: per-app annual CO₂ ──────────────────────────────────────────
    sorted_df = df.sort_values("annual_co2_kg", ascending=True)
    bar_colors = [CAT_COLORS[c] for c in sorted_df["category"]]
    bars = ax1.barh(sorted_df["app"], sorted_df["annual_co2_kg"],
                    color=bar_colors, edgecolor="white", linewidth=0.5)
    ax1.set_title("Annual CO₂ by App (kg)", fontsize=13, fontweight="bold", pad=10)
    ax1.set_xlabel("kg CO₂ / year")
    for bar, val in zip(bars, sorted_df["annual_co2_kg"]):
        ax1.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                 f"{val:.1f}", va="center", fontsize=9)
    legend_patches = [mpatches.Patch(color=c, label=l) for l, c in CAT_COLORS.items()]
    ax1.legend(handles=legend_patches, loc="lower right", fontsize=9)
    ax1.set_facecolor("#f8f9fa")

    # ── Panel 2: category breakdown pie ──────────────────────────────────────
    cat_totals = df.groupby("category")["annual_co2_kg"].sum()
    colors_pie = [CAT_COLORS[c] for c in cat_totals.index]
    ax2.pie(cat_totals.values, labels=cat_totals.index, colors=colors_pie,
            autopct="%1.1f%%", startangle=140,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax2.set_title("Emissions by Category", fontsize=13, fontweight="bold", pad=10)

    # ── Panel 3: what-if savings ──────────────────────────────────────────────
    sc = scenarios.sort_values("saving_kg")
    bar_sc = ax3.barh(sc["scenario"], sc["saving_kg"], color="#3498db", alpha=0.85)
    ax3.set_title("Annual CO₂ Savings per Behaviour Change (kg)", fontsize=13, fontweight="bold", pad=10)
    ax3.set_xlabel("kg CO₂ saved / year")
    for bar, val, pct in zip(bar_sc, sc["saving_kg"], sc["saving_pct"]):
        ax3.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                 f"{val:.1f} kg  ({pct}%)", va="center", fontsize=9)
    ax3.set_facecolor("#f8f9fa")

    # ── Panel 4: summary stats ────────────────────────────────────────────────
    total_annual = df["annual_co2_kg"].sum()
    daily_avg    = df["daily_co2_g"].sum() / 1000
    top_emitter  = df.loc[df["annual_co2_kg"].idxmax(), "app"]
    best_saving  = scenarios.iloc[0]["saving_kg"]
    best_action  = scenarios.iloc[0]["scenario"]

    summary_text = (
        f"📅  Daily average:    {daily_avg:.2f} kg CO₂\n\n"
        f"📆  Annual total:     {total_annual:.1f} kg CO₂\n\n"
        f"🔥  Top emitter:      {top_emitter}\n\n"
        f"🌱  Best action:\n     {best_action}\n"
        f"     saves {best_saving:.1f} kg/yr\n\n"
        f"🌍  Equivalent to:\n"
        f"     {total_annual / 0.12:.0f} km driven\n"
        f"     (avg petrol car)"
    )
    ax4.axis("off")
    ax4.set_facecolor("#e8f4f8")
    ax4.text(0.05, 0.95, "Key Stats", fontsize=13, fontweight="bold",
             transform=ax4.transAxes, va="top")
    ax4.text(0.05, 0.80, summary_text, fontsize=10,
             transform=ax4.transAxes, va="top", linespacing=1.6)

    fig.suptitle("Digital Carbon Footprint Analyzer — Personal Dashboard",
                 fontsize=16, fontweight="bold", y=0.98)

    plt.savefig("outputs/carbon_dashboard.png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close()
    print("Dashboard saved → outputs/carbon_dashboard.png")


# ─── 6. Entry Point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)

    print("── Digital Carbon Footprint Analyzer ────────────────")

    usage_df   = get_sample_usage_data()
    results_df = calculate_emissions(usage_df)

    print(f"\nTotal daily CO₂:   {results_df['daily_co2_g'].sum()/1000:.3f} kg")
    print(f"Total annual CO₂:  {results_df['annual_co2_kg'].sum():.2f} kg")
    print(f"\nTop 3 emitters (annual kg CO₂):")
    print(results_df.nlargest(3, "annual_co2_kg")[["app", "annual_co2_kg"]].to_string(index=False))

    scenarios = apply_scenarios(results_df)
    print("\n── What-If Scenarios ─────────────────────────────────")
    print(scenarios[["scenario", "saving_kg", "saving_pct"]].to_string(index=False))

    build_dashboard(results_df, scenarios)
    print("\n✅  Analysis complete. Check outputs/ for the dashboard.")
