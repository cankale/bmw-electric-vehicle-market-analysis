# BMW and the German Electric Vehicle Market

An exploratory data analysis of BMW's competitive position in Germany's new-car market, electric vehicle (EV) adoption across the 16 German federal states (Bundesländer), and the relationship between charging infrastructure and regional EV adoption.

**Scope:** Germany only. **Stack:** Python, pandas, NumPy, Matplotlib, Jupyter Notebook.

---

## Questions

1. How does BMW compare with other brands in total new registrations and market share?
2. How is BMW performing in battery-electric (BEV) and plug-in hybrid (PHEV) registrations?
3. How does BEV and PHEV adoption differ across the 16 Bundesländer?
4. How does AC and DC charging infrastructure differ across the Bundesländer?
5. Is regional EV adoption associated with charging infrastructure density?
6. How might BMW registrations be distributed regionally? *(model estimate)*

---

## Data sources

| Data | Source | Content | Reference period |
|---|---|---|---|
| FZ 28.4 | Kraftfahrt-Bundesamt (KBA) | New registrations by brand and drive type | September 2026 |
| FZ 28.5 | KBA | New registrations by brand and drive type | Jan–Sep 2026 and Jan–Sep 2025 |
| FZ 28.9 | KBA | New registrations by Bundesland and drive type | Jan–Sep 2026 |
| FZ 28.2 | KBA | National monthly registrations by drive type | 2017–2026 (used as a cross-check) |
| Charging stations | Bundesnetzagentur charging station register (export) | Stations, charging ports, connector types | Snapshot = download date *(01.11.2026)* |
| 12411-0021 | Destatis | Population by Bundesland | 30.06.2026 |
| 11111-0001 | Destatis | Area by Bundesland (km²) | *(05.11.2026)* |
| FZ 2 | KBA | Passenger car stock by Bundesland | 01.01.2026 *(pending)* |

Raw files are stored unchanged in `data/raw/`. Cleaned datasets are saved to `data/processed/`.

---

## Definitions

- **Registrations, not sales.** All figures are KBA new registrations (*Neuzulassungen*). They are not retail sales and not BMW Group worldwide deliveries.
- **BMW** refers to the BMW brand only. KBA lists MINI as a separate brand.
- **BEV:** battery-electric vehicle. **PHEV:** plug-in hybrid. **FCEV:** hydrogen fuel cell vehicle. FCEVs are excluded from PHEV wherever the data allows.
- **Year-to-date PHEV** (Jan–Sep) is calculated as electric-drive total minus BEV, because FZ 28.5 has no separate PHEV column. Nationally this includes at most 11 FCEVs (2026) and 47 FCEVs (2025), which is negligible. September PHEV figures come from a dedicated PHEV column.
- **Charging port** = *Ladepunkt*: one vehicle can charge at a time. A port can have several connector types.
- **DC port:** a port with at least one DC connector (CCS or CHAdeMO). **AC-only port:** a port with no DC connector.
- **Station-level flags:** `has_AC` / `has_DC` mark stations offering at least one AC / DC connector. One station can count in both.
- **Growth** is reported in **%**. Changes in shares are reported in **percentage points (pp)**.

### Metrics

| Metric | Formula |
|---|---|
| Market share | Brand registrations / all registrations |
| BEV market share | Brand BEVs / all BEVs |
| PHEV market share | Brand PHEVs / all PHEVs |
| Internal BEV share | Brand BEVs / brand's total registrations |
| Internal PHEV share | Brand PHEVs / brand's total registrations |
| Year-over-year growth | (Jan–Sep 2026 − Jan–Sep 2025) / Jan–Sep 2025 |
| Regional BEV / PHEV share | State BEVs (PHEVs) / state total registrations |
| BEV-to-PHEV ratio | BEVs / PHEVs |

---

## Methods and validation

- All extracted brand and regional totals were reconciled with the KBA total rows ("Insgesamt" / period totals) using assertions.
- National market totals were cross-checked independently against FZ 28.2.
- Brand tables were merged on normalized brand names with outer-merge checks, so no brand is lost through spelling differences. Brands with no September registrations are filled with 0 for September only.
- Growth is left undefined (NaN) for brands with no registrations in the base year.
- "Sonstige" (registrations not assigned to a Bundesland) is kept for reconciliation and excluded from regional comparisons.
- Charging stations were assigned to Bundesländer using postal codes and city/district information, with zero missing assignments. All 118,219 charging ports in the dataset have connector information.
- Charging infrastructure is normalized three ways: per 100,000 inhabitants, per 10,000 passenger cars in stock, and per 1,000 km².

---

## Key findings so far

**BMW vs the German market, Jan–Sep 2026 vs Jan–Sep 2025**

| Category | BMW growth | Market growth | BMW share change |
|---|---|---|---|
| Total registrations | +4.25% | +5.28% | −0.08 pp |
| BEV | +42.53% | +58.07% | −0.89 pp |
| PHEV | −5.99% | +13.63% | −2.11 pp |

- BMW grew in total and BEV registrations, but more slowly than the market in all three categories.
- BMW's own lineup shifted strongly toward BEVs: the BEV share of BMW's registrations rose from about 19.0% to 25.9% (+6.96 pp).
- BMW lost ground in PHEVs on every measure.

*Regional and infrastructure findings: to be added.*

---

## Limitations

- **Registration location:** vehicles are registered at the holder's address. Company fleets, leasing and rental firms inflate registrations in some states, most visibly Hamburg.
- **Small sample:** with 16 Bundesländer, correlations are exploratory and cannot establish causality.
- **Time alignment:** the charging dataset contains no commissioning dates, so the infrastructure snapshot cannot be aligned exactly with the registration period.
- **Small brands:** growth rates for low-volume brands are volatile and can be extreme.
- **Regional BMW estimates** (if included) are model-based allocations, not observed registrations, and are not statistically validated.

---

## Repository structure

```
data/
  raw/          original source files (unchanged)
  processed/    cleaned datasets (Parquet)
src/            notebooks
README.md
```

## How to run

1. Create the environment and install dependencies with:
pip install -r requirements.txt

2. Place the source files in `data/raw/`.
3. Run the cleaning notebooks first (they write to `data/processed/`), then the analysis notebooks.