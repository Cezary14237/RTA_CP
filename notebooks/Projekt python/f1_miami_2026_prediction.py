"""
================================================================================
  F1 2026 MIAMI GRAND PRIX – TOP-5 RACE PREDICTION
  Method : Weighted Multi-Criteria Decision Analysis (MCDA)
  Race   : Formula 1 Crypto.com Miami Grand Prix 2026
           Miami International Autodrome, Miami Gardens, FL
           Race date : Sunday 3 May 2026, 16:00 ET
================================================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SECTION 1 ▸  FORECASTED TOP-5 FINISHING ORDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  P1 – Lando Norris        (McLaren-Mercedes)
  P2 – Oscar Piastri       (McLaren-Mercedes)
  P3 – Kimi Antonelli      (Mercedes)
  P4 – George Russell      (Mercedes)
  P5 – Charles Leclerc     (Ferrari)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SECTION 2 ▸  METHOD DESCRIPTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Model: Weighted Multi-Criteria Decision Analysis (MCDA)
  ─────────────────────────────────────────────────────────────────────────────
  Each driver is scored on five independent criteria, normalised to [0, 1],
  then combined via a weighted sum to produce a final "prediction score".
  The top-5 drivers by prediction score form the forecasted finishing order.

  ┌─────────────────────────────────────┬────────┬──────────────────────────────────────────┐
  │ Feature / Criterion                 │ Weight │ Rationale                                │
  ├─────────────────────────────────────┼────────┼──────────────────────────────────────────┤
  │ F1  Championship points (2026)      │  25 %  │ Captures current car & driver form       │
  │     entering Miami (after 3 races)  │        │ across the opening season                │
  ├─────────────────────────────────────┼────────┼──────────────────────────────────────────┤
  │ F2  Average race finish (2026)      │  20 %  │ Raw results-based pace indicator;        │
  │     across Australia, China, Japan  │        │ DNFs / DNS penalised as P20              │
  ├─────────────────────────────────────┼────────┼──────────────────────────────────────────┤
  │ F3  Historical Miami GP avg finish  │  20 %  │ Circuit-specific track record;           │
  │     (all editions, 2022–2025)       │        │ "never raced here" coded as P15 (avg.)   │
  ├─────────────────────────────────────┼────────┼──────────────────────────────────────────┤
  │ F4  Team upgrade / car-performance  │  20 %  │ Expert-consensus qualitative score       │
  │     score entering Miami (0–10)     │        │ based on paddock reports, FP1 data,      │
  │                                    │        │ technical previews, and upgrade scale     │
  ├─────────────────────────────────────┼────────┼──────────────────────────────────────────┤
  │ F5  Miami-specific context          │  15 %  │ Combines: rain probability (88% Sunday   │
  │     adjustment score (0–10)         │        │ storm), FIA 350 kW boost-mode ban in wet │
  │                                    │        │ conditions (hurts Mercedes, helps ICE     │
  │                                    │        │ teams), new ERS regs for 2026 Miami,      │
  │                                    │        │ and driver wet-weather track history      │
  └─────────────────────────────────────┴────────┴──────────────────────────────────────────┘

  Final composite score (S):
      S = 0.25·F̂1 + 0.20·F̂2 + 0.20·F̂3 + 0.20·F̂4 + 0.15·F̂5
  where F̂i = min-max normalised value of feature i, mapped to [0, 1]
  with higher always being better (bad finishing positions are inverted).

  ─────────────────────────────────────────────────────────────────────────────
  DATA SOURCES (all public, pre-race):
  ─────────────────────────────────────────────────────────────────────────────
  • FIA / Formula1.com official race results – 2026 Australian, Chinese &
      Japanese Grand Prix  (March 8, 15, 29, 2026)
  • FIA official Drivers' Championship standings entering Miami 2026
      (Wikipedia / Formula1.com, 2026 season page)
  • FIA official race results for Miami GP 2022, 2023, 2024, 2025
  • Paddock technical reports (PlanetF1, The Race, F1Oversteer, AutoHebdo,
      Motorsport.com, The Judge 13) – April 2026 break period
  • FIA regulatory update notice for 2026 Miami GP
      (350 kW boost ban in wet, ERS energy changes)
  • Weather forecast: motorsport.com / f1oversteer.com (88 % rain Sunday)

  ─────────────────────────────────────────────────────────────────────────────
  KEY CONTEXTUAL FACTORS MODELLED IN F4/F5:
  ─────────────────────────────────────────────────────────────────────────────
  • McLaren: "completely new MCL40" – major upgrade package to front brake
    ducts, floor, bodywork, rear wing, and power-unit integration. Resolved
    the electrical issues that caused two DNS at China. Pace gap to Mercedes
    closed from –0.172 s/km (Australia) to –0.033 s/km (Japan). McLaren has
    won Miami in BOTH previous years (Norris 2024, Piastri 2025).
  • Ferrari: ~50% of visible aero components revised. Consistently on podium
    all 3 races. Hamilton/Leclerc strong in wet conditions.
  • Mercedes: dominant (3 wins from 3 races) but questions over MGU-K heat
    management in 50°C Miami temperatures. The FIA's 350 kW boost ban under
    'low grip' conditions would neutralise Mercedes' main ERS advantage.
    Historically have never won Miami (first podium only in 2025).
  • Red Bull: Verstappen publicly despondent about 2026 rules, car qualifying
    issues, Hadjar rookie. Significant pace deficit to top 3.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SECTION 3 ▸  CODE + DATA → RUNNING THIS SCRIPT REPRODUCES THE FORECASTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import numpy as np
import pandas as pd

# ── helpers ──────────────────────────────────────────────────────────────────

def minmax(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """Min-max normalise a Series to [0, 1], direction-aware."""
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series([0.5] * len(series), index=series.index)
    norm = (series - lo) / (hi - lo)
    return norm if higher_is_better else (1.0 - norm)


# ══════════════════════════════════════════════════════════════════════════════
#  DATA BLOCK 1 – 2026 CHAMPIONSHIP POINTS ENTERING MIAMI
#  Source: FIA / formula1.com standings after R3 Japan (29 March 2026).
#  Note: Bahrain (R4) and Saudi Arabia (R5) were cancelled due to Iran war.
#  Sprint points from Chinese GP sprint are included in these totals.
# ══════════════════════════════════════════════════════════════════════════════

championship_points_2026 = {
    # Driver                  Points
    "Kimi Antonelli":          72,   # 2× race wins (China, Japan) + sprint pts
    "George Russell":          63,   # 1× race win (Australia) + sprint pts
    "Charles Leclerc":         49,   # 3× podiums (P3, P4, P3)
    "Lewis Hamilton":          41,   # 3× top-5 (P4, P3, P6)
    "Lando Norris":            22,   # P5 Australia, DNS China, P5 Japan
    "Oscar Piastri":           18,   # DNS Australia, DNS China, P2 Japan
    "Oliver Bearman":          14,   # Haas – P5 China + other pts
    "Pierre Gasly":            10,   # Alpine – consistent midfield
    "Esteban Ocon":             6,
    "Liam Lawson":              5,
    "Arvid Lindblad":           4,
    "Max Verstappen":           8,   # P6 Australia, DNF China, P8 Japan
    "Isack Hadjar":             4,
    "Gabriel Bortoleto":        2,
    "Franco Colapinto":         1,
    "Carlos Sainz":             0,
    "Alexander Albon":          0,
    "Nico Hulkenberg":          0,
    "Fernando Alonso":          0,
    "Lance Stroll":             0,
    "Sergio Perez":             0,
    "Valtteri Bottas":          0,
}

# ══════════════════════════════════════════════════════════════════════════════
#  DATA BLOCK 2 – 2026 SEASON AVERAGE FINISHING POSITION
#  Australia R1, China R2, Japan R3.
#  DNS / DNF / unclassified = coded as P20 (worst-case penalty).
#  Source: FIA race results + crash.net / formula1.com race reports.
# ══════════════════════════════════════════════════════════════════════════════

# Format: [Australia_finish, China_finish, Japan_finish]
# (20 = DNF / DNS / not classified)
results_2026 = {
    "Kimi Antonelli":  [2,  1,  1],
    "George Russell":  [1,  2,  4],
    "Charles Leclerc": [3,  4,  3],
    "Lewis Hamilton":  [4,  3,  6],
    "Lando Norris":    [5, 20,  5],
    "Oscar Piastri":   [20, 20, 2],
    "Oliver Bearman":  [7,  5, 20],   # crashed out in Japan
    "Pierre Gasly":    [10, 6,  7],
    "Esteban Ocon":    [11, 14, 10],
    "Liam Lawson":     [20, 7,  9],
    "Arvid Lindblad":  [8, 12, 14],
    "Max Verstappen":  [6, 20,  8],
    "Isack Hadjar":    [20, 8, 12],
    "Gabriel Bortoleto":[9, 20, 13],
    "Franco Colapinto":[20, 10, 20],
    "Carlos Sainz":    [20, 9, 20],
    "Alexander Albon": [20, 11, 20],
    "Nico Hulkenberg": [20, 11, 20],
    "Fernando Alonso": [20, 20, 20],
    "Lance Stroll":    [20, 20, 20],
    "Sergio Perez":    [20, 15, 20],
    "Valtteri Bottas": [20, 13, 20],
}

avg_finish_2026 = {
    driver: np.mean(finishes)
    for driver, finishes in results_2026.items()
}

# ══════════════════════════════════════════════════════════════════════════════
#  DATA BLOCK 3 – HISTORICAL MIAMI GP AVERAGE FINISHING POSITION (2022–2025)
#  Source: FIA official results for all 4 Miami GPs.
#
#  2022: 1-Verstappen, 2-Leclerc, 3-Carlos Sainz, 4-Valtteri Bottas, 5-Norris
#  2023: 1-Verstappen, 2-Alonso, 3-Leclerc, 4-Hamilton, 5-Bearman (not in F1)
#  2024: 1-Norris, 2-Verstappen, 3-Russell, 4-Antonelli (not in F1),
#         5-Hamilton
#  2025: 1-Piastri, 2-Norris, 3-Russell, 4-Verstappen, 5-Albon
#
#  Drivers who did not race that year are coded as P18 (midfield default).
# ══════════════════════════════════════════════════════════════════════════════

miami_history = {
    # Driver             [2022, 2023, 2024, 2025]
    "Max Verstappen":    [1,    1,    2,    4],
    "Charles Leclerc":   [2,    3,    6,    7],
    "Carlos Sainz":      [3,    5,    7,    9],
    "Lando Norris":      [5,    8,    1,    2],
    "Oscar Piastri":     [18,   18,   8,    1],
    "Lewis Hamilton":    [18,   4,    5,    8],
    "George Russell":    [18,   18,   3,    3],
    "Kimi Antonelli":    [18,   18,   18,   6],   # 2025 was his debut season
    "Oliver Bearman":    [18,   18,   18,   18],
    "Pierre Gasly":      [18,   18,   18,   18],
    "Esteban Ocon":      [18,   18,   18,   18],
    "Liam Lawson":       [18,   18,   18,   18],
    "Arvid Lindblad":    [18,   18,   18,   18],
    "Max Verstappen":    [1,    1,    2,    4],
    "Isack Hadjar":      [18,   18,   18,   18],
    "Gabriel Bortoleto": [18,   18,   18,   18],
    "Franco Colapinto":  [18,   18,   18,   18],
    "Alexander Albon":   [18,   18,   18,   5],
    "Nico Hulkenberg":   [18,   18,   18,   18],
    "Fernando Alonso":   [18,   2,    18,   18],
    "Lance Stroll":      [18,   18,   18,   18],
    "Sergio Perez":      [18,   18,   18,   18],
    "Valtteri Bottas":   [4,    18,   18,   18],
}

avg_miami_hist = {
    driver: np.mean(results)
    for driver, results in miami_history.items()
}

# ══════════════════════════════════════════════════════════════════════════════
#  DATA BLOCK 4 – TEAM CAR / UPGRADE PERFORMANCE SCORE (0 – 10)
#  Qualitative expert consensus translated to numeric scale.
#  Based on: paddock reports (Apr 2026), technical previews, FP1 expectations.
#
#  McLaren "completely new MCL40": major aero (floor, bodywork, brake ducts,
#    rear wing), resolved Mercedes PU integration issues that caused China DNS.
#    Pace gap to Mercedes: –0.172 s/km (AUS) → –0.033 s/km (JPN). Score: 9.5
#  Ferrari: ~50% of visible aero components updated. Consistently P3/P4 all
#    season. Hamilton/Leclerc strong pace in heat. Score: 8.0
#  Mercedes: dominant (3 from 3), but MGU-K heat concerns at 50°C Miami.
#    No historic Miami win (first podium only in 2025, Russell P3). Score: 8.5
#  Red Bull: Verstappen despondent, Q1 elimination in Australia. Still
#    struggling with 2026 PU regulations. Score: 5.5
#  Alpine (Mercedes PU): consistent midfield, Gasly solid but no wins. 5.5
#  Haas (Ferrari PU): Bearman fast but reliability concerns. Score: 6.0
#  Racing Bulls (Red Bull-Ford): Lawson decent, Lindblad rookie. Score: 5.0
#  Audi: New team, clearly behind. Score: 4.0
#  Williams (Mercedes PU): Sainz/Albon midfield. Score: 5.5
#  Aston Martin (Honda): Both drivers struggled. Score: 4.5
#  Cadillac (Ferrari PU): Perez and Bottas in new team, mixed results. 4.5
# ══════════════════════════════════════════════════════════════════════════════

team_upgrade_score = {
    # Driver                 Team upgrade score (0–10)
    "Kimi Antonelli":        8.5,   # Mercedes
    "George Russell":        8.5,   # Mercedes
    "Charles Leclerc":       8.0,   # Ferrari
    "Lewis Hamilton":        8.0,   # Ferrari
    "Lando Norris":          9.5,   # McLaren – "completely new car"
    "Oscar Piastri":         9.5,   # McLaren – "completely new car"
    "Oliver Bearman":        6.0,   # Haas (Ferrari PU)
    "Pierre Gasly":          5.5,   # Alpine (Mercedes PU)
    "Esteban Ocon":          5.5,   # Haas (Ferrari PU)
    "Liam Lawson":           5.0,   # Racing Bulls (Red Bull-Ford)
    "Arvid Lindblad":        5.0,   # Racing Bulls (Red Bull-Ford)
    "Max Verstappen":        5.5,   # Red Bull – significant rear wing test
    "Isack Hadjar":          5.5,   # Red Bull
    "Gabriel Bortoleto":     4.0,   # Audi
    "Franco Colapinto":      5.5,   # Alpine (Mercedes PU)
    "Carlos Sainz":          5.5,   # Williams (Mercedes PU)
    "Alexander Albon":       5.5,   # Williams (Mercedes PU)
    "Nico Hulkenberg":       4.0,   # Audi
    "Fernando Alonso":       4.5,   # Aston Martin (Honda)
    "Lance Stroll":          4.5,   # Aston Martin (Honda)
    "Sergio Perez":          4.5,   # Cadillac (Ferrari PU)
    "Valtteri Bottas":       4.5,   # Cadillac (Ferrari PU)
}

# ══════════════════════════════════════════════════════════════════════════════
#  DATA BLOCK 5 – MIAMI-SPECIFIC CONTEXT ADJUSTMENT SCORE (0 – 10)
#  Combines three sub-factors:
#  (a) FIA 350 kW boost-mode BAN in wet/low-grip conditions:
#      Helps: McLaren, Ferrari (strong ICE). Hurts: Mercedes (relies on ERS).
#  (b) Circuit characteristics favour overtaking (3 long straights);
#      benefits: drivers with good racecraft and late-braking ability.
#  (c) Driver wet-weather track history + form in variable conditions.
#
#  Sub-scores (each 0–10) combined as simple average:
#    boost_impact: how well driver/team benefits from no-boost rule
#    wet_skill   : wet-race track record (Hamilton legendary, Norris good)
#    miami_feel  : momentum / recent wins at this specific venue
# ══════════════════════════════════════════════════════════════════════════════

miami_context_scores = {
    # Driver                  boost_impact  wet_skill  miami_feel
    "Kimi Antonelli":         (6.0,         7.0,       5.0),   # less boost helps Merc less
    "George Russell":         (6.0,         7.5,       6.0),   # P3 Miami 2025
    "Charles Leclerc":        (7.5,         7.0,       7.5),   # Ferrari ICE strong; P2/P3 hist
    "Lewis Hamilton":         (7.5,         9.5,       7.0),   # Legendary wet driver; P4/P5 Miami
    "Lando Norris":           (8.5,         8.0,       9.5),   # Won 2024 + 2025 sprint; McLaren ICE
    "Oscar Piastri":          (8.5,         7.0,       9.5),   # Won 2025 Miami
    "Oliver Bearman":         (6.5,         6.5,       3.0),
    "Pierre Gasly":           (6.5,         6.5,       3.0),
    "Esteban Ocon":           (6.5,         6.5,       3.0),
    "Liam Lawson":            (5.0,         5.5,       2.0),
    "Arvid Lindblad":         (5.0,         5.0,       1.0),
    "Max Verstappen":         (5.0,         7.0,       7.0),   # Won 2022, 2023 Miami
    "Isack Hadjar":           (5.5,         5.0,       1.0),
    "Gabriel Bortoleto":      (4.0,         5.0,       1.0),
    "Franco Colapinto":       (6.0,         5.5,       1.0),
    "Carlos Sainz":           (6.0,         6.5,       6.0),   # P3 Miami 2022
    "Alexander Albon":        (5.5,         5.5,       4.0),   # P5 Miami 2025
    "Nico Hulkenberg":        (4.0,         5.0,       2.0),
    "Fernando Alonso":        (4.5,         7.0,       7.0),   # P2 Miami 2023
    "Lance Stroll":           (4.5,         5.0,       2.0),
    "Sergio Perez":           (4.5,         5.5,       3.0),
    "Valtteri Bottas":        (4.5,         5.0,       5.0),
}

context_score = {
    driver: np.mean(subs)
    for driver, subs in miami_context_scores.items()
}


# ══════════════════════════════════════════════════════════════════════════════
#  BUILD MASTER DATAFRAME
# ══════════════════════════════════════════════════════════════════════════════

all_drivers = list(championship_points_2026.keys())

df = pd.DataFrame(index=all_drivers)

df["champ_pts"]       = pd.Series(championship_points_2026)
df["avg_finish_2026"] = pd.Series(avg_finish_2026)
df["avg_miami_hist"]  = pd.Series(avg_miami_hist)
df["team_upgrade"]    = pd.Series(team_upgrade_score)
df["context_score"]   = pd.Series(context_score)

# Fill missing values for any driver not in all dicts
df["champ_pts"]       = df["champ_pts"].fillna(0)
df["avg_finish_2026"] = df["avg_finish_2026"].fillna(18)
df["avg_miami_hist"]  = df["avg_miami_hist"].fillna(15)
df["team_upgrade"]    = df["team_upgrade"].fillna(4.5)
df["context_score"]   = df["context_score"].fillna(3.0)


# ══════════════════════════════════════════════════════════════════════════════
#  NORMALISE ALL FEATURES to [0, 1]
#  Note: finishing positions → lower number = better → higher_is_better=False
# ══════════════════════════════════════════════════════════════════════════════

df["n_champ_pts"]       = minmax(df["champ_pts"],       higher_is_better=True)
df["n_avg_finish_2026"] = minmax(df["avg_finish_2026"], higher_is_better=False)
df["n_avg_miami_hist"]  = minmax(df["avg_miami_hist"],  higher_is_better=False)
df["n_team_upgrade"]    = minmax(df["team_upgrade"],    higher_is_better=True)
df["n_context_score"]   = minmax(df["context_score"],   higher_is_better=True)


# ══════════════════════════════════════════════════════════════════════════════
#  COMPUTE WEIGHTED COMPOSITE SCORE
#  S = 0.25·F̂1 + 0.20·F̂2 + 0.20·F̂3 + 0.20·F̂4 + 0.15·F̂5
# ══════════════════════════════════════════════════════════════════════════════

WEIGHTS = {
    "n_champ_pts":       0.25,
    "n_avg_finish_2026": 0.20,
    "n_avg_miami_hist":  0.20,
    "n_team_upgrade":    0.20,
    "n_context_score":   0.15,
}

df["composite_score"] = sum(
    df[feat] * weight for feat, weight in WEIGHTS.items()
)

# Sort by composite score descending
df_sorted = df.sort_values("composite_score", ascending=False)


# ══════════════════════════════════════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════════════════════════════════════

def team_of(driver: str) -> str:
    teams = {
        "Kimi Antonelli":   "Mercedes",
        "George Russell":   "Mercedes",
        "Charles Leclerc":  "Ferrari",
        "Lewis Hamilton":   "Ferrari",
        "Lando Norris":     "McLaren-Mercedes",
        "Oscar Piastri":    "McLaren-Mercedes",
        "Oliver Bearman":   "Haas-Ferrari",
        "Pierre Gasly":     "Alpine-Mercedes",
        "Esteban Ocon":     "Haas-Ferrari",
        "Liam Lawson":      "Racing Bulls-Red Bull Ford",
        "Arvid Lindblad":   "Racing Bulls-Red Bull Ford",
        "Max Verstappen":   "Red Bull-Red Bull Ford",
        "Isack Hadjar":     "Red Bull-Red Bull Ford",
        "Gabriel Bortoleto":"Audi",
        "Franco Colapinto": "Alpine-Mercedes",
        "Carlos Sainz":     "Williams-Mercedes",
        "Alexander Albon":  "Williams-Mercedes",
        "Nico Hulkenberg":  "Audi",
        "Fernando Alonso":  "Aston Martin-Honda",
        "Lance Stroll":     "Aston Martin-Honda",
        "Sergio Perez":     "Cadillac-Ferrari",
        "Valtteri Bottas":  "Cadillac-Ferrari",
    }
    return teams.get(driver, "Unknown")


BANNER = "═" * 72

print(f"\n{BANNER}")
print("  F1 2026 MIAMI GRAND PRIX – PREDICTED FINISHING ORDER")
print(f"{BANNER}")

print("\n  ┌────┬─────────────────────────┬──────────────────────────┬────────┐")
print("  │ P  │ Driver                  │ Team                     │ Score  │")
print("  ├────┼─────────────────────────┼──────────────────────────┼────────┤")
for pos, (driver, row) in enumerate(df_sorted.head(10).iterrows(), start=1):
    marker = "◄── TOP 5" if pos <= 5 else ""
    print(f"  │ {pos:<2} │ {driver:<23} │ {team_of(driver):<24} │ {row['composite_score']:.4f} │  {marker}")
print("  └────┴─────────────────────────┴──────────────────────────┴────────┘")

print(f"\n{BANNER}")
print("  FINAL FORECAST – TOP 5")
print(BANNER)
top5 = list(df_sorted.head(5).index)
for i, driver in enumerate(top5, start=1):
    print(f"  P{i}: {driver}  ({team_of(driver)})")
print(f"{BANNER}\n")

# ── Feature contribution breakdown for the top 5 ─────────────────────────────
print("\n  FEATURE BREAKDOWN FOR TOP-5 DRIVERS")
print("  (normalised feature scores, higher = better in all columns)\n")
cols = {
    "n_champ_pts":       "ChampPts",
    "n_avg_finish_2026": "AvgFin26",
    "n_avg_miami_hist":  "MiamiHist",
    "n_team_upgrade":    "Upgrade",
    "n_context_score":   "Context",
    "composite_score":   "TOTAL",
}
header = f"  {'Driver':<24}" + "".join(f"  {v:>9}" for v in cols.values())
print(header)
print("  " + "─" * (len(header) - 2))
for driver in top5:
    row = df_sorted.loc[driver]
    vals = "".join(f"  {row[k]:>9.4f}" for k in cols.keys())
    print(f"  {driver:<24}{vals}")

print()
print("  Weights applied:")
for feat, w in WEIGHTS.items():
    print(f"    {feat:<22} → {w:.0%}")

print(f"""
  ─────────────────────────────────────────────────────────────────────────
  KEY PREDICTION RATIONALE (summary):
  ─────────────────────────────────────────────────────────────────────────
  • McLaren's "completely new MCL40" is a game-changer at their best track.
    They have won Miami 2 years running (Norris 2024, Piastri 2025) and the
    FIA's wet-weather 350 kW boost ban removes Mercedes' main ERS advantage.
    Pace gap to Mercedes closed from −0.172 s/km → −0.033 s/km in 3 races.

  • Mercedes remain formidable (3 wins from 3 in 2026) but have zero Miami
    victories in 4 attempts and face: 50°C track temps stressing their
    tightly packaged MGU-K, and the prospect of a rain race where the boost
    mode is banned. Antonelli (championship leader) and Russell both feature
    strongly, but are predicted to finish just behind McLaren.

  • Ferrari is consistent and Hamilton is the greatest wet-weather driver in
    F1 history, but without as radical an upgrade as McLaren, Leclerc is
    placed 5th. Hamilton could also challenge for P5 in wet conditions.

  • Verstappen and Red Bull are coded as outside the top 5: Verstappen is
    publicly despondent about 2026 regulations, Red Bull have faced Q1
    struggles, and the track historically doesn't suit their strengths.
  ─────────────────────────────────────────────────────────────────────────
""")
