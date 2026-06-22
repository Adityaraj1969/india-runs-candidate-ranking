<div align="center">

# 🎯 India Runs Hackathon — Intelligent Candidate Ranking
### Track 1: Data & AI Challenge by Redrob AI × Hack2Skill

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aditya-redrob-ai-recruiter.streamlit.app)
&nbsp;
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
&nbsp;
![Sentence Transformers](https://img.shields.io/badge/sentence--transformers-all--MiniLM--L6--v2-orange)
&nbsp;
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B?logo=streamlit&logoColor=white)
&nbsp;
![License](https://img.shields.io/badge/license-MIT-green)

Built by a 2nd semester engineering student

[🖥️ Live Dashboard](#️-live-recruiter-dashboard) · [🚀 How to Run](#-how-to-run) · [🧠 How It Works](#-how-it-works) · [📊 Results](#-results)

</div>

---

## 🌟 What this project does

Given a job description for a **Senior AI Engineer at Redrob AI**, this system reads **100,000 candidate profiles** and outputs a ranked shortlist of the **top 100 best-fit candidates** — with a score and human-readable explanation for every rank.

**Key result:** All 100 shortlisted candidates were open to work, active on the platform, and in genuine AI/ML engineering roles. The system correctly rejected keyword stuffers and unreachable candidates.

---

## 🖥️ Live Recruiter Dashboard

> **Click below — no installation needed, works in any browser.**

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aditya-redrob-ai-recruiter.streamlit.app)

**→ [aditya-redrob-ai-recruiter.streamlit.app](https://aditya-redrob-ai-recruiter.streamlit.app)**

The dashboard has 3 tabs:

| Tab | What you see |
|-----|-------------|
| 📋 **Candidate List** | All 100 ranked candidates — scores, AI reasoning, badges, filters, CSV export |
| 📊 **Analytics** | 7 interactive charts — score distribution, title breakdown, radar chart, salary scatter |
| 🔎 **Deep Profile** | Full profile — skills, career history, education, behavioral signals, verified scores |

### Sidebar filters (live on the public URL)
- Match score range slider
- Job title multi-select
- Location multi-select
- Notice period tier (≤15 / ≤30 / ≤60 / >60 days)
- "Open to work only" toggle
- "Verified contact only" toggle

---

## 🧠 How It Works

### The problem with keyword matching

Most basic systems count how many job keywords appear in a candidate's skills list and rank by that count. This fails in two critical ways:

- **Keyword stuffers** — A Marketing Manager who lists every AI skill gets ranked #1, even though they've never done AI engineering work.
- **Hidden gems** — A strong ML engineer who describes their work as *"built a retrieval pipeline"* instead of *"vector database"* gets missed entirely.

We solve both with a **5-signal approach**.

---

### The Formula

```
Final Score = (Semantic × 0.45 + Skill Match × 0.25 + Role Relevance × 0.20
              + Profile Quality × 0.10) × Behavioral Multiplier
```

---

### Signal 1 — Semantic Similarity (45%)

We use the `all-MiniLM-L6-v2` sentence-transformer model to convert both the job description and each candidate's full profile into **384-dimensional vectors**, then compute cosine similarity.

**Why this matters:** The model catches meaning — *"retrieval pipeline"* matches *"vector database"* even without identical keywords. We embed the entire career history, not just the skills list — this is where hidden gems live.

---

### Signal 2 — Skill Keyword Match (25%)

We extract **43 required AI/ML skills** from the job description and check how many appear in each candidate's skills list. Expert/advanced proficiency counts more than beginner-level claims.

Weighted lower than semantics deliberately — to avoid over-rewarding keyword stuffers.

---

### Signal 3 — Role Relevance (20%)

We check whether the candidate is actually working in AI/engineering by matching their current and historical job titles against **18 good engineering roles**.

**Trap detection built in:**
- Non-engineering titles → penalized
- Past (but not current) engineering roles → partial credit
- Entire career at consulting firms (TCS, Infosys, Wipro, Accenture) → 50% score reduction

---

### Signal 4 — Behavioral Availability (Multiplier: 0.3–1.0)

Our key innovation. Instead of treating availability as just another score, we use it as a **multiplier on the entire final score**.

A perfect-on-paper candidate who is unreachable is worthless to a recruiter. This ensures unavailable/inactive candidates always rank below slightly-weaker-but-reachable ones.

The multiplier combines 6 platform signals:

| Signal | What it measures |
|--------|-----------------|
| `open_to_work_flag` | Actively looking? |
| `last_active_date` | Logged in this month? This quarter? |
| `recruiter_response_rate` | Will they actually reply? |
| `notice_period_days` | JD wants sub-30 days |
| `interview_completion_rate` | Do they ghost interviews? |
| Location | Pune/Noida preferred; willing to relocate? |

---

### Signal 5 — Profile Quality (10%)

Profile completeness score + GitHub activity score + verified skill assessment scores (verified > self-claimed) + verified email/phone + LinkedIn connection + saved-by-recruiters count.

---

## 📊 Results

| Metric | Value |
|--------|-------|
| Total candidates processed | 100,000 |
| Final shortlist | 100 candidates |
| Open to work (top 100) | **100/100 (100%)** |
| Avg semantic score (top 100) | 0.6898 |
| Avg skill match score (top 100) | 0.9890 |
| Avg role relevance (top 100) | 0.9690 |
| Avg behavioral availability (top 100) | 0.8537 |
| Avg recruiter response rate | **79.7%** |
| Top score | **0.7876** |
| Score range | 0.7876 → 0.6547 |

### Top job titles in final shortlist

| Title | Count |
|-------|-------|
| ML Engineer | 16 |
| AI Research Engineer | 13 |
| Junior ML Engineer | 13 |
| Senior Software Engineer (ML) | 11 |
| Data Scientist | 11 |
| AI Engineer | 7 |
| Machine Learning Engineer | 5 |
| Senior Data Scientist | 4 |
| Senior Machine Learning Engineer | 3 |
| Search Engineer | 3 |

**Every candidate in the top 100 is in a genuine AI/ML engineering role.**

### Sample Top 5

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

## 🚀 How to Run

### Option A — Live Dashboard (no setup)

Click the Streamlit badge at the top. Works instantly in any browser.

> The Candidate List and Analytics tabs are fully available on the public URL.

---

### Option B — Run the Notebook (reproduce the full 100K ranking)

**Requirements:** Google Colab with T4 GPU (free tier works)

```
pandas · sentence-transformers · scikit-learn · numpy · tqdm
```

**Steps:**
1. Upload `candidates.jsonl` (from organizer dataset) to Google Drive in a folder called `hackathon_data`
2. Open `india_runs_candidate_ranking.ipynb` in Google Colab
3. Enable GPU: Runtime → Change runtime type → T4 GPU
4. Run all cells in order
5. `submission.csv` is saved to your Drive automatically

**Estimated runtime:** ~7 minutes on T4 GPU

---

### Option C — Run the Dashboard Locally (unlocks Deep Profile tab)

```bash
cd redrob-dashboard
pip install -r requirements.txt

# Place candidates.jsonl (from organizer) in this folder, then:
python build_data.py --submission ../submission.csv --jsonl candidates.jsonl

streamlit run app.py
# Opens at http://localhost:8501
```

**On Windows CMD (one line each):**
```cmd
pip install -r requirements.txt
python build_data.py --submission ..\submission.csv --jsonl candidates.jsonl
python -m streamlit run app.py
```

---

## 📁 Repository Structure

```
india-runs-candidate-ranking/
│
├── 📓 india_runs_candidate_ranking.ipynb   # Complete ML pipeline
├── 📊 submission.csv                        # Final top-100 ranked output
├── 📄 README.md                             # This file
│
└── 📂 redrob-dashboard/                     # Interactive demo
    ├── .streamlit/                          # interactive Redrob AI Recruiter Dashboard
    ├── config.toml                          # lock the theme to dark mode permanently
    ├── app.py                               # Streamlit app (3 tabs)
    ├── build_data.py                        # Data prep script
    ├── requirements.txt                     # Dependencies
    ├── enriched_candidates.csv              # Pre-built for cloud deploy
    └── DASHBOARD_README.md                  # Dashboard setup guide
```

> `candidates.jsonl` is the organizer-provided dataset (100K profiles).
> It is not included in this repo — participants receive it separately.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Semantic embeddings | `sentence-transformers` · `all-MiniLM-L6-v2` |
| Vector similarity | `scikit-learn` cosine similarity |
| Data processing | `pandas` · `numpy` |
| Compute | Google Colab T4 GPU (free tier) |
| Dashboard | `Streamlit` |
| Charts | `Plotly` |
| Deploy | Streamlit Community Cloud |

---

## 👤 About

Built by a **2nd semester engineering student** in their first hackathon.
Prior experience: basic Python, HTML/CSS, JavaScript.

This project was built from scratch in one day — starting from zero knowledge of machine learning, embeddings, or semantic search. Every function in the notebook is commented to explain what it does and why.

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
