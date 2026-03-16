# AI Exposure of the Australian Job Market

Analysing how susceptible every occupation in the Australian economy is to AI and automation, using official data from [Jobs and Skills Australia](https://www.jobsandskills.gov.au/).

**Live dashboard: [0xtreme.github.io/aus-jobs](https://0xtreme.github.io/aus-jobs/)**

## Background

[Andrej Karpathy](https://github.com/karpathy) built a project scoring every job in America on AI replacement risk (0–10), using data from the Bureau of Labor Statistics. It went viral — Elon replied, news outlets picked it up — and was then deleted.

[Josh Kale](https://github.com/JoshKale/jobs) cloned the entire repo before it went down and brought it back to life. The original pipeline scraped all 342 BLS occupations, fed each to an LLM with a scoring rubric, and built an interactive treemap visualisation. Average AI exposure across the US economy: **5.3/10**.

This project applies the same methodology to Australia, using real Australian Government data instead of BLS. **No US data. No sample data. No fabrication.** Every number comes from official Australian sources you can verify yourself.

## How this differs from the US version

| | US (Karpathy/JoshKale) | Australia (this repo) |
|---|---|---|
| **Occupations** | 342 (BLS Occupational Outlook Handbook) | 358 (ANZSCO 4-digit unit groups) |
| **Data source** | US Bureau of Labor Statistics | Jobs and Skills Australia + ABS |
| **Classification** | SOC codes | ANZSCO codes |
| **Currency** | USD | AUD |
| **Pay data** | BLS median annual pay | ABS median weekly earnings (annualised) |
| **Projections** | BLS 10-year (2024–2034) | JSA/Victoria University 5-year (2024–2029) |
| **Education levels** | US system (High school, Associate's, Bachelor's, etc.) | Australian system (Year 12, Cert III/IV, Diploma, Bachelor, Postgrad) |
| **Categories** | BLS occupation groups | 8 ANZSCO major groups |
| **Avg. exposure** | 5.3/10 | 4.4/10 (job-weighted) |
| **Total employment** | ~160M | ~14.2M |
| **Scoring method** | Gemini Flash via OpenRouter | Same rubric, adapted for AU context |

**Why is Australia's average lower (4.4 vs 5.3)?** Australia's economy is more weighted toward physical trades, healthcare, mining, and agriculture. The largest occupations — sales assistants (554K), aged care workers (361K), registered nurses (345K) — are hands-on jobs with natural barriers to AI disruption.

## Data sources

All data is from official Australian Government sources:

| Source | What it provides | Link |
|--------|-----------------|------|
| **Jobs and Skills Australia — Occupation Profiles** (Feb 2025) | Employment, median earnings, education, descriptions, tasks for 358 occupations at ANZSCO 4-digit level | [jobsandskills.gov.au/data/occupation-and-industry-profiles](https://www.jobsandskills.gov.au/data/occupation-and-industry-profiles) |
| **Jobs and Skills Australia — Employment Projections** (May 2024–2034) | 5-year and 10-year employment growth projections by occupation, produced by Victoria University (VUEF model) | [jobsandskills.gov.au/data/employment-projections](https://www.jobsandskills.gov.au/data/employment-projections) |

Underlying data is sourced from:
- **ABS Labour Force Survey** (2024, annual average) — employment counts
- **ABS Employee Earnings and Hours** (May 2023) — median earnings
- **Australian Treasury** macroeconomic forecasts — projection calibration

The Excel files are downloaded directly from the JSA website by the pipeline. You can verify any number against the source.

## AI exposure scoring

Each occupation is scored on a single **AI Exposure** axis from 0 to 10, measuring how much AI will reshape that occupation. The scoring rubric is identical to the original Karpathy project, adapted with Australian occupation examples.

| Score | Meaning | Australian examples |
|-------|---------|-------------------|
| 0–1 | Minimal | Concreters, farm workers, cleaners, roof tilers |
| 2–3 | Low | Electricians, plumbers, paramedics, aged care workers |
| 4–5 | Moderate | Registered nurses, police, GPs, school teachers |
| 6–7 | High | Civil engineers, architects, managers, university lecturers |
| 8–9 | Very high | Software developers, accountants, solicitors, graphic designers |
| 10 | Maximum | Keyboard operators, switchboard operators |

## Visualisation

The main visualisation is an interactive **treemap** where:
- **Area** of each rectangle is proportional to employment (number of jobs)
- **Colour** indicates AI exposure on a green (safe) to red (exposed) scale
- **Layout** groups occupations by ANZSCO major group (Managers, Professionals, Technicians & Trades, Community & Personal Service, Clerical & Admin, Sales, Machinery Operators & Drivers, Labourers)
- **Hover** shows detailed tooltip with ANZSCO code, median pay (AUD), employment, 5-year growth outlook, education level, AI exposure score, and rationale
- **Click** opens the occupation's page on Jobs and Skills Australia

## Data pipeline

1. **Extract** (`extract_data.py`) — Downloads official JSA Excel files and produces `occupations.json`, `occupations.csv`, and Markdown pages in `pages/`.
2. **Score** (`generate_scores.py` or `score.py`) — Assigns AI exposure scores (0–10) with rationales. `score.py` uses an LLM via OpenRouter for automated scoring.
3. **Build site data** (`build_site_data.py`) — Merges CSV stats and AI exposure scores into `site/data.json`.
4. **Website** (`site/index.html`) — Single-file interactive treemap visualisation.

## Key files

| File | Description |
|------|-------------|
| `occupations.json` | Master list of 358 occupations with title, ANZSCO code, category, slug |
| `occupations.csv` | Summary stats: pay (AUD), education, job count, growth projections |
| `scores.json` | AI exposure scores (0–10) with rationales for all 358 occupations |
| `pages/` | Markdown descriptions for each occupation (generated from JSA data) |
| `site/` | Static website (treemap visualisation) |

## Usage

```bash
# Step 1: Download JSA data and extract occupations
python3 extract_data.py

# Step 2: Generate AI exposure scores
python3 generate_scores.py

# Step 3: Build website data
python3 build_site_data.py

# Step 4: Serve the site locally
cd site && python -m http.server 8000
```

To use LLM-based scoring instead (requires [OpenRouter](https://openrouter.ai/) API key in `.env`):
```bash
OPENROUTER_API_KEY=your_key_here
python3 score.py
```

## Credits

- Original concept and pipeline by [Andrej Karpathy](https://github.com/karpathy)
- US version preserved by [Josh Kale](https://github.com/JoshKale/jobs)
- Australian adaptation using official [Jobs and Skills Australia](https://www.jobsandskills.gov.au/) data
