"""
Build a compact JSON for the website by merging CSV stats with AI exposure scores.

Reads occupations.csv (for stats) and scores.json (for AI exposure).
Writes site/data.json.

Usage:
    uv run python build_site_data.py
"""

import csv
import json
import os


def main():
    # Load AI exposure scores
    with open("scores.json") as f:
        scores_list = json.load(f)
    scores = {s["slug"]: s for s in scores_list}

    # Load CSV stats
    with open("occupations.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Merge
    data = []
    for row in rows:
        slug = row["slug"]
        score = scores.get(slug, {})
        data.append({
            "title": row["title"],
            "slug": slug,
            "anzsco": row["anzsco"],
            "category": row["category"],
            "category_name": row["category_name"],
            "pay": int(row["median_pay_annual"]) if row["median_pay_annual"] else None,
            "pay_weekly": int(row["median_pay_weekly"]) if row["median_pay_weekly"] else None,
            "jobs": int(row["employed"]) if row["employed"] else None,
            "outlook": float(row["outlook_pct"]) if row["outlook_pct"] else None,
            "outlook_desc": row["outlook_desc"],
            "education": row["entry_education"],
            "exposure": score.get("exposure"),
            "exposure_rationale": score.get("rationale"),
            "url": row.get("url", ""),
        })

    os.makedirs("site", exist_ok=True)
    with open("site/data.json", "w") as f:
        json.dump(data, f)

    print(f"Wrote {len(data)} occupations to site/data.json")
    total_jobs = sum(d["jobs"] for d in data if d["jobs"])
    scored = sum(1 for d in data if d["exposure"] is not None)
    print(f"Total jobs represented: {total_jobs:,}")
    print(f"Occupations with AI exposure scores: {scored}")


if __name__ == "__main__":
    main()
