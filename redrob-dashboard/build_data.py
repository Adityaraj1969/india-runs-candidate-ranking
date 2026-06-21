"""
build_data.py
─────────────
Run once before launching the dashboard.
Merges submission.csv + candidates.jsonl → enriched_candidates.csv

Usage:
    python build_data.py
    python build_data.py --submission my_submission.csv --jsonl my_candidates.jsonl
"""

import argparse
import json
import pandas as pd
from pathlib import Path

def build(submission_path: str, jsonl_path: str, out_path: str = "enriched_candidates.csv"):
    print(f"📂  Loading submission  → {submission_path}")
    submission = pd.read_csv(submission_path)
    top_ids = set(submission["candidate_id"].tolist())
    print(f"    {len(top_ids)} candidate IDs found")

    print(f"📂  Scanning JSONL       → {jsonl_path}")
    matched = {}
    with open(jsonl_path) as f:
        for i, line in enumerate(f):
            d = json.loads(line)
            if d["candidate_id"] in top_ids:
                matched[d["candidate_id"]] = d
            if (i + 1) % 10_000 == 0:
                print(f"    … scanned {i+1:,} lines, matched {len(matched)}")
            if len(matched) == len(top_ids):
                print(f"    ✅ All {len(matched)} candidates found at line {i+1:,}")
                break

    if len(matched) < len(top_ids):
        missing = top_ids - set(matched.keys())
        print(f"⚠️  Could not find {len(missing)} IDs in JSONL: {list(missing)[:5]}")

    print("🔧  Building enriched dataset …")
    rows = []
    for _, row in submission.iterrows():
        cid = row["candidate_id"]
        if cid not in matched:
            continue
        c  = matched[cid]
        p  = c["profile"]
        rs = c["redrob_signals"]

        rows.append({
            "candidate_id":        cid,
            "rank":                int(row["rank"]),
            "score":               round(float(row["score"]), 4),
            "name":                p["anonymized_name"],
            "title":               p["current_title"],
            "company":             p["current_company"],
            "location":            p["location"],
            "years_exp":           p["years_of_experience"],
            "open_to_work":        rs["open_to_work_flag"],
            "last_active":         rs["last_active_date"],
            "response_rate":       rs["recruiter_response_rate"],
            "notice_period":       rs["notice_period_days"],
            "github_score":        rs["github_activity_score"],
            "profile_completeness":rs["profile_completeness_score"],
            "skills_count":        len(c["skills"]),
            "top_skills":          ", ".join(s["name"] for s in c["skills"][:5]),
            "willing_to_relocate": rs["willing_to_relocate"],
            "interview_completion":rs["interview_completion_rate"],
            "salary_min":          rs["expected_salary_range_inr_lpa"]["min"],
            "salary_max":          rs["expected_salary_range_inr_lpa"]["max"],
            "reasoning":           row["reasoning"],
            "verified_email":      rs["verified_email"],
            "verified_phone":      rs["verified_phone"],
            "headline":            p["headline"],
            "summary":             p.get("summary", ""),
        })

    df = pd.DataFrame(rows)
    df.to_csv(out_path, index=False)
    print(f"✅  Saved {len(df)} rows → {out_path}")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build enriched_candidates.csv")
    parser.add_argument("--submission", default="submission.csv",
                        help="Path to submission.csv (default: submission.csv)")
    parser.add_argument("--jsonl", default="candidates.jsonl",
                        help="Path to candidates.jsonl (default: candidates.jsonl)")
    parser.add_argument("--out", default="enriched_candidates.csv",
                        help="Output path (default: enriched_candidates.csv)")
    args = parser.parse_args()

    if not Path(args.submission).exists():
        print(f"❌ submission file not found: {args.submission}")
        exit(1)
    if not Path(args.jsonl).exists():
        print(f"❌ JSONL file not found: {args.jsonl}")
        exit(1)

    build(args.submission, args.jsonl, args.out)
    print("\n🚀  Now run:  streamlit run app.py")
