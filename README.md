# 🏆 India Runs Hackathon — Intelligent Candidate Ranking
### Track 1: Data & AI Challenge by Redrob AI

> **Built by a 2nd semester engineering student**  
> A working AI-powered candidate ranking system that ranked 100,000 profiles
> intelligently — going far beyond keyword matching.

---

## What this system does

Given a job description for a **Senior AI Engineer at Redrob AI**, this system
reads 100,000 candidate profiles and outputs a ranked shortlist of the top 100
best-fit candidates — with a score and human-readable explanation for each rank.

**Key result:** All 100 shortlisted candidates were open to work, active on the
platform, and in genuine AI/ML engineering roles. The system correctly rejected
keyword stuffers and unreachable candidates.

---

## The problem with keyword matching (and why we didn't use it)

Most basic systems count how many job keywords appear in a candidate's skills
list and rank by that count. This fails in two ways:

1. **Keyword stuffers** — A "Marketing Manager" who lists every AI skill gets
   ranked #1, even though they've never done AI engineering work.
2. **Hidden gems** — A strong ML engineer who describes their work as "built a
   retrieval pipeline" instead of "vector database" gets missed entirely.

We solve both problems with a 5-signal approach.

---

## Our approach — 5 signals + behavioral multiplier

### The formula
```
Final Score = (Semantic × 0.45 + Skill Match × 0.25 + Role Relevance × 0.20
              + Profile Quality × 0.10) × Behavioral Multiplier
```

### Signal 1 — Semantic similarity (45%)
We use the `all-MiniLM-L6-v2` sentence-transformer model to convert both the
job description and each candidate's full profile (headline + summary + career
history descriptions + skills) into 384-dimensional vectors. We then compute
cosine similarity between the job vector and each candidate vector.

**Why 45%?** Semantic understanding is the hardest problem to solve and the
most valuable signal. The AI catches meaning — "retrieval pipeline" matches
"vector database" even without identical keywords. This is the core innovation.

**Why career history descriptions?** This is where hidden gems live. A
candidate who built vector search infrastructure but doesn't list "FAISS" as
a skill will still surface through semantic matching of their job descriptions.

### Signal 2 — Skill keyword match (25%)
We extract 43 required AI/ML skills from the job description and check how many
appear in each candidate's skills list. We also weight by proficiency level —
expert/advanced skills count more than beginner-level claims.

**Why 25%?** Explicit skill overlap still matters — it's fast verification of
the semantic match. But we deliberately weighted it lower than semantics to
avoid over-rewarding keyword stuffers.

### Signal 3 — Role relevance (20%)
We check whether the candidate is actually working in AI/engineering by
matching their current job title and career history titles against a list of
18 good engineering roles (ML Engineer, Data Scientist, Backend Engineer, etc.).

**The trap detection:** The job description explicitly warns that candidates
with all the right AI skills but non-engineering titles are poor fits. Our
system penalizes non-engineering titles and gives partial credit for past
(but not current) engineering roles.

**Consulting firm penalty:** The JD says pure consulting backgrounds (TCS,
Infosys, Wipro, Accenture, Cognizant, etc.) are a poor fit. If a candidate's
entire career history is at consulting firms, we apply a 50% score reduction
on their role relevance score.

### Signal 4 — Behavioral availability (multiplier: 0.3–1.0)
This is our key innovation. Instead of treating availability as just another
score, we use it as a **multiplier** on the entire final score.

A perfect-on-paper candidate who is unreachable is worthless to a recruiter.
So we designed the system to ensure that unavailable/inactive candidates
always rank lower than slightly-weaker-but-reachable ones.

The multiplier combines 6 behavioral signals from the Redrob platform:
- `open_to_work_flag` — Most important: actively looking?
- `last_active_date` — Active this month? This quarter? 6+ months ago?
- `recruiter_response_rate` — Will they actually reply?
- `notice_period_days` — JD wants sub-30 days
- `interview_completion_rate` — Do they ghost interviews?
- Location match — Pune/Noida preferred; willing to relocate?

### Signal 5 — Profile quality (10%)
Combines: profile completeness score, GitHub activity score (JD explicitly
values this), verified skill assessment scores (verified > self-claimed),
verified email/phone, LinkedIn connection, and saved-by-recruiters count.

---

## Results from 100,000 candidates

| Metric | Value |
|--------|-------|
| Total candidates processed | 100,000 |
| Final shortlist | 100 candidates |
| Open to work (top 100) | **100/100 (100%)** |
| Avg semantic score (top 100) | 0.6898 |
| Avg skill match score (top 100) | 0.9890 |
| Avg role relevance (top 100) | 0.9690 |
| Avg behavioral availability (top 100) | 0.8537 |
| Top score | 0.7876 |
| Score range (top 100) | 0.7876 → 0.6593 |

### Top job titles in final shortlist
| Title | Count |
|-------|-------|
| AI Research Engineer | 16 |
| ML Engineer | 15 |
| Junior ML Engineer | 13 |
| Data Scientist | 11 |
| Senior Software Engineer (ML) | 11 |
| Machine Learning Engineer | 5 |
| Senior Data Scientist | 5 |
| AI Engineer | 5 |
| Senior Machine Learning Engineer | 3 |
| NLP Engineer | 3 |

**Every candidate in the top 100 is in a genuine AI/ML engineering role.**

### Sample top 5 with reasoning
```
Rank 1: CAND_0046132 | Score: 0.7876
  AI Research Engineer | 4.3 yrs exp | 7 AI skills matched
  strong semantic match | open to work | active this month | response rate 94%

Rank 2: CAND_0018499 | Score: 0.7825
  Senior Machine Learning Engineer | 7.2 yrs exp | 10 AI skills matched
  strong semantic match | open to work | active this month | response rate 61%

Rank 3: CAND_0039754 | Score: 0.7767
  Senior Applied Scientist | 16.2 yrs exp | 13 AI skills matched
  strong semantic match | open to work | active this month | response rate 81%

Rank 4: CAND_0011687 | Score: 0.7662
  Senior NLP Engineer | 7.8 yrs exp | 10 AI skills matched
  strong semantic match | open to work | active this month | response rate 89%

Rank 5: CAND_0046525 | Score: 0.7660
  Senior Machine Learning Engineer | 6.1 yrs exp | 11 AI skills matched
  strong semantic match | open to work | active this month | response rate 88%
```

---

## How to run

### Requirements
```
pandas
sentence-transformers
scikit-learn
numpy
tqdm
```

### Steps
1. Upload dataset files to Google Drive in a folder called `hackathon_data`
2. Open `india_runs_candidate_ranking.ipynb` in Google Colab
3. Enable GPU: Runtime → Change runtime type → T4 GPU
4. Run cells 1–13 in order
5. Final `submission.csv` is saved to your Drive and downloaded automatically

**Estimated runtime:** ~7 minutes on T4 GPU for 100,000 candidates

---

## Files in this repository

| File | Description |
|------|-------------|
| `india_runs_candidate_ranking.ipynb` | Complete solution notebook |
| `submission.csv` | Final ranked top-100 output |
| `README.md` | This file |

---

## About the team

Built by a **2nd semester B.Tech student** participating in their first
hackathon. Prior experience: basic Python, HTML/CSS, JavaScript.

This project was built from scratch in one day — starting from zero knowledge
of machine learning, embeddings, or semantic search. Every function is
commented to explain what it does and why.

**Tools used:** Google Colab (T4 GPU), sentence-transformers, scikit-learn,
pandas, Python 3.12

**Compute:** Google Colab free tier with T4 GPU acceleration

---

## Why we think this approach works

The challenge explicitly says the dataset contains a trap — candidates with
all the right AI keywords but the wrong job backgrounds. Our system handles
this through three mechanisms:

1. **Semantic similarity catches hidden gems** — Strong engineers who describe
   their work naturally (not keyword-optimized) still surface.
2. **Role relevance catches keyword stuffers** — A Marketing Manager with
   listed AI skills scores near zero on Signal 3.
3. **Behavioral multiplier catches unreachable candidates** — A perfect
   profile that hasn't logged in for 8 months ranks below a slightly weaker
   but actively job-seeking engineer.

The combination of these three mechanisms is what makes this system behave
like a real, thoughtful recruiter — not just a search engine.
