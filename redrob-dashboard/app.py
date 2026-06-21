"""
Redrob AI Recruiter Dashboard
India Runs Hackathon — Track 1: Intelligent Candidate Discovery
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, date
import numpy as np

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Redrob AI Recruiter",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Global */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
  }
  section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  section[data-testid="stSidebar"] .stSlider > div > div > div > div {
    background: #6366f1 !important;
  }

  /* Cards */
  .metric-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    text-align: center;
    margin-bottom: 0.5rem;
  }
  .metric-card .val {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #6366f1, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
  }
  .metric-card .lbl {
    font-size: 0.75rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
  }

  /* Candidate card */
  .cand-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-left: 4px solid #6366f1;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
    transition: border-color 0.2s;
  }
  .cand-card:hover { border-left-color: #a78bfa; }
  .cand-name { font-size: 1rem; font-weight: 600; color: #f1f5f9; }
  .cand-title { font-size: 0.82rem; color: #94a3b8; margin: 2px 0; }
  .cand-score {
    font-size: 1.5rem; font-weight: 700;
    background: linear-gradient(90deg, #6366f1, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .badge {
    display: inline-block;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 999px;
    padding: 2px 10px;
    font-size: 0.72rem;
    color: #94a3b8;
    margin: 2px 2px 0 0;
  }
  .badge-green { border-color: #22c55e; color: #22c55e; }
  .badge-red   { border-color: #f87171; color: #f87171; }
  .badge-indigo{ border-color: #818cf8; color: #818cf8; }

  /* Divider */
  hr { border-color: #334155; }

  /* Section headers */
  .section-header {
    font-size: 1.05rem;
    font-weight: 600;
    color: #e2e8f0;
    border-bottom: 2px solid #334155;
    padding-bottom: 6px;
    margin: 1rem 0 0.8rem;
  }

  /* Score bar */
  .score-bar-wrap { background: #0f172a; border-radius: 999px; height: 8px; margin: 6px 0 2px; }
  .score-bar-fill { height: 8px; border-radius: 999px;
                    background: linear-gradient(90deg, #6366f1, #a78bfa); }

  /* Hide streamlit branding */
  #MainMenu, footer, header { visibility: hidden; }

  /* Plotly dark fix */
  .js-plotly-plot .plotly .modebar { background: transparent; }
</style>
""", unsafe_allow_html=True)

# ─── Data Loading ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("enriched_candidates.csv")
    df["last_active"] = pd.to_datetime(df["last_active"])
    df["days_since_active"] = (pd.Timestamp("2026-06-21") - df["last_active"]).dt.days
    df["score_pct"] = (df["score"] * 100).round(1)

    # Active label
    def active_label(days):
        if days <= 7:   return "This week"
        if days <= 30:  return "This month"
        if days <= 90:  return "This quarter"
        return "6+ months ago"
    df["active_label"] = df["days_since_active"].apply(active_label)

    # Notice tier
    def notice_tier(d):
        if d <= 15:  return "≤15 days"
        if d <= 30:  return "≤30 days"
        if d <= 60:  return "≤60 days"
        return ">60 days"
    df["notice_tier"] = df["notice_period"].apply(notice_tier)

    return df

@st.cache_data
def load_full_profiles():
    try:
        submission_ids = set(pd.read_csv("enriched_candidates.csv")["candidate_id"].tolist())
        profiles = {}
        with open("candidates.jsonl") as f:
            for line in f:
                c = json.loads(line)
                if c["candidate_id"] in submission_ids:
                    profiles[c["candidate_id"]] = c
        return profiles
    except FileNotFoundError:
        return {}


df = load_data()
profiles = load_full_profiles()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎯 Redrob AI")
    st.markdown("**Recruiter Dashboard**")
    st.markdown("---")

    st.markdown("### 🔍 Filters")

    min_score, max_score = float(df["score"].min()), float(df["score"].max())
    score_range = st.slider(
        "Match Score",
        min_value=min_score, max_value=max_score,
        value=(min_score, max_score),
        step=0.001, format="%.3f"
    )

    all_titles = sorted(df["title"].unique())
    sel_titles = st.multiselect("Job Title", all_titles)

    all_locations = sorted(df["location"].unique())
    sel_locs = st.multiselect("Location", all_locations)

    notice_opts = ["≤15 days", "≤30 days", "≤60 days", ">60 days"]
    sel_notice = st.multiselect("Notice Period", notice_opts)

    open_only = st.checkbox("Open to work only", value=True)
    verified_only = st.checkbox("Verified email/phone", value=False)

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
**India Runs Hackathon**  
Track 1 · Data & AI Challenge

5-Signal Ranking Model:
- 🧠 Semantic (45%)
- 🛠 Skills (25%)
- 💼 Role (20%)
- ✅ Quality (10%)
- ⚡ Behavioral ×

Built by a 2nd sem B.Tech student.
    """)

# ─── Apply filters ────────────────────────────────────────────────────────────
fdf = df.copy()
fdf = fdf[(fdf["score"] >= score_range[0]) & (fdf["score"] <= score_range[1])]
if sel_titles:
    fdf = fdf[fdf["title"].isin(sel_titles)]
if sel_locs:
    fdf = fdf[fdf["location"].isin(sel_locs)]
if sel_notice:
    fdf = fdf[fdf["notice_tier"].isin(sel_notice)]
if open_only:
    fdf = fdf[fdf["open_to_work"] == True]
if verified_only:
    fdf = fdf[(fdf["verified_email"] == True) & (fdf["verified_phone"] == True)]

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("# 🎯 Redrob AI Recruiter Dashboard")
st.markdown(
    "**Senior AI Engineer** · Ranked shortlist from 100,000 profiles · "
    f"*Showing {len(fdf)} of 100 candidates*"
)
st.markdown("---")

# ─── KPI Row ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    (len(fdf), "Shortlisted"),
    (f"{fdf['score'].mean():.3f}" if len(fdf) else "—", "Avg Score"),
    (f"{(fdf['open_to_work'].sum()/len(fdf)*100):.0f}%" if len(fdf) else "—", "Open to Work"),
    (f"{fdf['response_rate'].mean()*100:.0f}%" if len(fdf) else "—", "Avg Response Rate"),
    (f"{fdf['notice_period'].mean():.0f}d" if len(fdf) else "—", "Avg Notice Period"),
]
for col, (val, lbl) in zip([k1, k2, k3, k4, k5], kpis):
    col.markdown(
        f'<div class="metric-card"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>',
        unsafe_allow_html=True
    )

st.markdown("")

# ─── Tabs ────────────────────────────────────────────────────────────────────
tab_list, tab_analytics, tab_profile = st.tabs(
    ["📋 Candidate List", "📊 Analytics", "🔎 Deep Profile"]
)

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — CANDIDATE LIST
# ════════════════════════════════════════════════════════════════════════════
with tab_list:
    if fdf.empty:
        st.warning("No candidates match the current filters.")
    else:
        sort_col = st.selectbox(
            "Sort by",
            ["rank", "score", "years_exp", "response_rate", "github_score"],
            index=0,
            key="sort_list"
        )
        sort_asc = sort_col == "rank"
        fdf_sorted = fdf.sort_values(sort_col, ascending=sort_asc)

        for _, row in fdf_sorted.iterrows():
            with st.container():
                col_main, col_score = st.columns([4, 1])
                with col_main:
                    # Badges
                    badges = ""
                    if row["open_to_work"]:
                        badges += '<span class="badge badge-green">✓ Open to Work</span>'
                    if row["active_label"] in ("This week", "This month"):
                        badges += f'<span class="badge badge-indigo">⚡ {row["active_label"]}</span>'
                    if row["notice_period"] <= 30:
                        badges += f'<span class="badge badge-green">⏱ {int(row["notice_period"])}d notice</span>'
                    if row["verified_email"]:
                        badges += '<span class="badge">✉ Verified</span>'
                    badges += f'<span class="badge">{row["location"]}</span>'
                    badges += f'<span class="badge">{row["years_exp"]:.1f} yrs exp</span>'

                    st.markdown(
                        f"""
                        <div class="cand-card">
                          <div style="display:flex;justify-content:space-between;align-items:flex-start">
                            <div>
                              <div class="cand-name">#{int(row["rank"])} &nbsp; {row["name"]}</div>
                              <div class="cand-title">{row["title"]} · {row["company"]}</div>
                              <div style="margin-top:6px">{badges}</div>
                            </div>
                            <div style="text-align:right">
                              <div class="cand-score">{row['score']:.4f}</div>
                              <div style="font-size:0.72rem;color:#64748b">match score</div>
                            </div>
                          </div>
                          <div style="margin-top:8px;font-size:0.78rem;color:#94a3b8">
                            {row['reasoning']}
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        st.markdown("---")
        st.download_button(
            "⬇️ Download Filtered Shortlist (CSV)",
            data=fdf_sorted[[
                "rank", "candidate_id", "name", "title", "company", "location",
                "score", "years_exp", "response_rate", "notice_period", "reasoning"
            ]].to_csv(index=False),
            file_name="redrob_shortlist.csv",
            mime="text/csv"
        )

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — ANALYTICS
# ════════════════════════════════════════════════════════════════════════════
with tab_analytics:
    if fdf.empty:
        st.warning("No data to plot with current filters.")
    else:
        PLOT_BG  = "#0f172a"
        GRID_CLR = "#1e293b"
        TEXT_CLR = "#94a3b8"
        FONT     = dict(family="Inter", color=TEXT_CLR, size=12)
        PALETTE  = ["#6366f1", "#a78bfa", "#38bdf8", "#34d399", "#fb923c", "#f472b6"]

        def style(fig, title=""):
            fig.update_layout(
                title=dict(text=title, font=dict(color="#e2e8f0", size=14)),
                paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
                font=FONT, margin=dict(l=20, r=20, t=40, b=20),
                legend=dict(bgcolor=PLOT_BG, bordercolor=GRID_CLR, font=FONT)
            )
            fig.update_xaxes(gridcolor=GRID_CLR, zeroline=False, color=TEXT_CLR)
            fig.update_yaxes(gridcolor=GRID_CLR, zeroline=False, color=TEXT_CLR)
            return fig

        # Row 1
        r1c1, r1c2 = st.columns(2)

        with r1c1:
            score_hist = px.histogram(
                fdf, x="score", nbins=20,
                color_discrete_sequence=[PALETTE[0]],
                labels={"score": "Match Score", "count": "Candidates"},
            )
            score_hist.update_traces(marker_line_width=0)
            st.plotly_chart(style(score_hist, "Score Distribution"), use_container_width=True)

        with r1c2:
            title_counts = fdf["title"].value_counts().head(10).reset_index()
            title_counts.columns = ["title", "count"]
            bar = px.bar(
                title_counts, x="count", y="title", orientation="h",
                color="count", color_continuous_scale=["#6366f1", "#a78bfa"],
                labels={"count": "Candidates", "title": ""},
            )
            bar.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
            st.plotly_chart(style(bar, "Top Job Titles"), use_container_width=True)

        # Row 2
        r2c1, r2c2 = st.columns(2)

        with r2c1:
            loc_counts = fdf["location"].value_counts().head(12).reset_index()
            loc_counts.columns = ["location", "count"]
            bubble = px.scatter(
                loc_counts, x="location", y="count", size="count",
                color="count", color_continuous_scale=["#6366f1", "#a78bfa"],
                labels={"count": "Candidates", "location": "City"},
            )
            bubble.update_layout(coloraxis_showscale=False,
                                 xaxis_tickangle=-40)
            st.plotly_chart(style(bubble, "Candidate Locations"), use_container_width=True)

        with r2c2:
            scatter = px.scatter(
                fdf, x="years_exp", y="score",
                color="response_rate",
                color_continuous_scale=["#6366f1", "#a78bfa", "#34d399"],
                hover_data=["name", "title", "location"],
                labels={
                    "years_exp": "Years of Experience",
                    "score": "Match Score",
                    "response_rate": "Response Rate"
                },
                size_max=12
            )
            st.plotly_chart(style(scatter, "Score vs Experience (color = Response Rate)"),
                            use_container_width=True)

        # Row 3
        r3c1, r3c2 = st.columns(2)

        with r3c1:
            avail = fdf["active_label"].value_counts().reset_index()
            avail.columns = ["label", "count"]
            order = ["This week", "This month", "This quarter", "6+ months ago"]
            avail["label"] = pd.Categorical(avail["label"], categories=order, ordered=True)
            avail = avail.sort_values("label")
            pie = px.pie(
                avail, names="label", values="count",
                color_discrete_sequence=PALETTE,
                hole=0.45
            )
            pie.update_traces(textposition="inside", textinfo="percent+label",
                              marker=dict(line=dict(color=PLOT_BG, width=2)))
            st.plotly_chart(style(pie, "Last Active Breakdown"), use_container_width=True)

        with r3c2:
            notice_order = ["≤15 days", "≤30 days", "≤60 days", ">60 days"]
            notice_counts = fdf["notice_tier"].value_counts().reset_index()
            notice_counts.columns = ["tier", "count"]
            notice_counts["tier"] = pd.Categorical(
                notice_counts["tier"], categories=notice_order, ordered=True)
            notice_counts = notice_counts.sort_values("tier")
            nb = px.bar(
                notice_counts, x="tier", y="count",
                color="count", color_continuous_scale=["#6366f1", "#a78bfa"],
                labels={"tier": "Notice Period", "count": "Candidates"},
                text="count"
            )
            nb.update_traces(textposition="outside")
            nb.update_layout(coloraxis_showscale=False)
            st.plotly_chart(style(nb, "Notice Period Distribution"), use_container_width=True)

        # Row 4 — Signal radar for avg top-10 vs avg bottom-10
        st.markdown('<div class="section-header">🎯 Signal Radar — Top 10 vs Bottom 10</div>',
                    unsafe_allow_html=True)
        fdf_sorted_score = fdf.sort_values("score", ascending=False)
        top10 = fdf_sorted_score.head(10)
        bot10 = fdf_sorted_score.tail(10)

        categories = ["Score", "Response Rate", "GitHub Score",
                      "Profile Complete", "Interview Rate"]
        top_vals = [
            top10["score"].mean() / fdf["score"].max(),
            top10["response_rate"].mean(),
            top10["github_score"].mean() / 100,
            top10["profile_completeness"].mean() / 100,
            top10["interview_completion"].mean(),
        ]
        bot_vals = [
            bot10["score"].mean() / fdf["score"].max(),
            bot10["response_rate"].mean(),
            bot10["github_score"].mean() / 100,
            bot10["profile_completeness"].mean() / 100,
            bot10["interview_completion"].mean(),
        ]

        radar = go.Figure()
        for vals, name, color in [
            (top_vals, "Top 10", "#6366f1"),
            (bot_vals, "Bottom 10", "#f87171")
        ]:
            radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=categories + [categories[0]],
                fill="toself", name=name,
                line=dict(color=color),
                fillcolor=color,
                opacity=0.35
            ))
        radar.update_layout(
            polar=dict(
                bgcolor=GRID_CLR,
                radialaxis=dict(visible=True, range=[0, 1], color=TEXT_CLR,
                                gridcolor=GRID_CLR),
                angularaxis=dict(color=TEXT_CLR)
            ),
            paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG, font=FONT,
            margin=dict(l=50, r=50, t=30, b=30),
            legend=dict(bgcolor=PLOT_BG)
        )
        st.plotly_chart(radar, use_container_width=True)

        # Salary heatmap
        st.markdown('<div class="section-header">💰 Expected Salary vs Score</div>',
                    unsafe_allow_html=True)
        sal_fig = px.scatter(
            fdf, x="salary_min", y="salary_max",
            size="score", color="score",
            color_continuous_scale=["#6366f1", "#a78bfa"],
            hover_data=["name", "title", "score"],
            labels={"salary_min": "Min Salary (LPA)", "salary_max": "Max Salary (LPA)",
                    "score": "Score"}
        )
        st.plotly_chart(style(sal_fig, ""), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — DEEP PROFILE
# ════════════════════════════════════════════════════════════════════════════
with tab_profile:
    st.markdown("### Select a candidate to explore their full profile")

    if not profiles:
        st.markdown("### 🔒 Deep Profile — Local Only")
        st.info(
            "This tab requires the organizer-provided `candidates.jsonl` dataset.  \n"
            "**Candidate List** and **Analytics** tabs are fully available above.  \n\n"
            "To unlock locally:  \n"
            "```bash\n"
            "python build_data.py --submission submission.csv --jsonl candidates.jsonl\n"
            "streamlit run app.py\n"
            "```"
        )
        st.stop()

    if fdf.empty:
        st.warning("No candidates match current filters.")
    else:
        fdf_sorted2 = fdf.sort_values("rank")
        options = [
            f"#{int(r['rank'])} · {r['name']} · {r['title']} · Score: {r['score']:.4f}"
            for _, r in fdf_sorted2.iterrows()
        ]
        id_map = {opt: cid for opt, cid in zip(options, fdf_sorted2["candidate_id"])}

        selected_opt = st.selectbox("Choose candidate", options)
        selected_id  = id_map[selected_opt]
        row = fdf[fdf["candidate_id"] == selected_id].iloc[0]
        profile = profiles[selected_id]

        # Header block
        c_left, c_right = st.columns([3, 1])
        with c_left:
            st.markdown(f"## {row['name']}")
            st.markdown(f"**{row['title']}** at {row['company']}  \n📍 {row['location']}")
            st.markdown(f"*{row['headline']}*")
        with c_right:
            st.markdown(
                f'<div class="metric-card"><div class="val">{row["score"]:.4f}</div>'
                f'<div class="lbl">Match Score · Rank #{int(row["rank"])}</div></div>',
                unsafe_allow_html=True
            )

        # Score breakdown bars
        st.markdown('<div class="section-header">📊 Score Breakdown</div>', unsafe_allow_html=True)
        signals = {
            "Semantic Similarity": 0.45,
            "Skill Match": 0.25,
            "Role Relevance": 0.20,
            "Profile Quality": 0.10,
        }
        # Estimate individual contributions proportionally from final score
        total_weight = sum(signals.values())
        for sig, weight in signals.items():
            contrib = row["score"] * weight / total_weight
            pct = min(contrib / 0.45, 1.0)  # normalise to max observable
            bar_w = int(pct * 100)
            st.markdown(
                f"""
                <div style="margin-bottom:10px">
                  <div style="display:flex;justify-content:space-between;
                              font-size:0.82rem;color:#94a3b8;margin-bottom:3px">
                    <span>{sig}</span>
                    <span style="color:#e2e8f0">{weight*100:.0f}% weight · {contrib:.4f}</span>
                  </div>
                  <div class="score-bar-wrap">
                    <div class="score-bar-fill" style="width:{bar_w}%"></div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Quick stats
        st.markdown('<div class="section-header">⚡ Behavioral Signals</div>', unsafe_allow_html=True)
        bs1, bs2, bs3, bs4 = st.columns(4)
        bs1.metric("Response Rate", f"{row['response_rate']*100:.0f}%")
        bs2.metric("Notice Period", f"{int(row['notice_period'])} days")
        bs3.metric("GitHub Score", f"{row['github_score']:.1f}/100")
        bs4.metric("Interview Rate", f"{row['interview_completion']*100:.0f}%")

        brow = profile["redrob_signals"]
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Last Active", row["active_label"])
        b2.metric("Profile Complete", f"{row['profile_completeness']:.0f}%")
        b3.metric("Open to Work", "✅ Yes" if row["open_to_work"] else "❌ No")
        b4.metric("Willing to Relocate", "✅ Yes" if row["willing_to_relocate"] else "❌ No")

        # Summary
        if row["summary"]:
            st.markdown('<div class="section-header">📝 Summary</div>', unsafe_allow_html=True)
            st.markdown(f"> {row['summary'][:600]}{'...' if len(row['summary']) > 600 else ''}")

        # Skills
        st.markdown('<div class="section-header">🛠 Skills</div>', unsafe_allow_html=True)
        skills = profile["skills"]
        skill_cols = st.columns(3)
        for i, skill in enumerate(skills):
            lvl_color = {
                "expert": "#22c55e",
                "advanced": "#6366f1",
                "intermediate": "#fb923c",
                "beginner": "#64748b"
            }.get(skill.get("proficiency", ""), "#64748b")
            skill_cols[i % 3].markdown(
                f"""<div style="background:#1e293b;border:1px solid #334155;
                    border-left:3px solid {lvl_color};border-radius:6px;
                    padding:6px 10px;margin-bottom:6px;font-size:0.82rem">
                  <span style="color:#f1f5f9;font-weight:500">{skill['name']}</span>
                  <span style="color:{lvl_color};float:right">{skill.get('proficiency','').title()}</span>
                  <div style="color:#64748b;font-size:0.72rem">
                    {skill.get('endorsements',0)} endorsements · {skill.get('duration_months',0)} months
                  </div>
                </div>""",
                unsafe_allow_html=True
            )

        # Career history
        st.markdown('<div class="section-header">💼 Career History</div>', unsafe_allow_html=True)
        for job in profile["career_history"]:
            is_current = job.get("is_current", False)
            badge = '<span style="color:#22c55e;font-size:0.72rem">● Current</span>' if is_current else ""
            st.markdown(
                f"""<div style="background:#1e293b;border:1px solid #334155;
                    border-radius:8px;padding:12px 16px;margin-bottom:8px">
                  <div style="display:flex;justify-content:space-between">
                    <div>
                      <span style="font-weight:600;color:#f1f5f9">{job['title']}</span>
                      <span style="color:#94a3b8"> at {job['company']}</span>
                    </div>
                    <div>{badge} <span style="color:#64748b;font-size:0.78rem">
                      {job.get('duration_months',0)} months</span>
                    </div>
                  </div>
                  <div style="color:#64748b;font-size:0.75rem;margin:4px 0">
                    {job.get('industry','')} · {job.get('company_size','')}
                  </div>
                  <div style="color:#94a3b8;font-size:0.8rem;margin-top:6px">
                    {job.get('description','')[:400]}
                    {'...' if len(job.get('description','')) > 400 else ''}
                  </div>
                </div>""",
                unsafe_allow_html=True
            )

        # Education
        if profile.get("education"):
            st.markdown('<div class="section-header">🎓 Education</div>', unsafe_allow_html=True)
            for edu in profile["education"]:
                st.markdown(
                    f"""<div style="background:#1e293b;border:1px solid #334155;
                        border-radius:8px;padding:10px 14px;margin-bottom:6px;font-size:0.85rem">
                      <span style="font-weight:600;color:#f1f5f9">{edu.get('degree','')} 
                        in {edu.get('field_of_study','')}</span>
                      <span style="color:#94a3b8"> · {edu.get('institution','')}</span>
                      <span style="color:#64748b;float:right">
                        {edu.get('start_year','')}–{edu.get('end_year','')}
                      </span>
                      {f"<div style='color:#6366f1;font-size:0.75rem'>{edu.get('grade','')}</div>" if edu.get('grade') else ""}
                    </div>""",
                    unsafe_allow_html=True
                )

        # Certifications
        if profile.get("certifications"):
            st.markdown('<div class="section-header">🏅 Certifications</div>', unsafe_allow_html=True)
            for cert in profile["certifications"]:
                st.markdown(
                    f"""<div style="background:#1e293b;border:1px solid #334155;border-radius:6px;
                        padding:8px 12px;margin-bottom:4px;font-size:0.82rem">
                      <span style="color:#f1f5f9;font-weight:500">{cert.get('name','')}</span>
                      <span style="color:#94a3b8"> · {cert.get('issuer','')}</span>
                      <span style="color:#64748b;float:right">{cert.get('year','')}</span>
                    </div>""",
                    unsafe_allow_html=True
                )

        # AI-generated reasoning
        st.markdown('<div class="section-header">🤖 AI Ranking Reasoning</div>', unsafe_allow_html=True)
        st.info(row["reasoning"])

        # Salary expectation
        st.markdown('<div class="section-header">💰 Salary Expectation</div>', unsafe_allow_html=True)
        st.markdown(
            f"**₹{row['salary_min']:.1f} – ₹{row['salary_max']:.1f} LPA**"
        )

        # Skill assessment scores
        skill_assessments = brow.get("skill_assessment_scores", {})
        if skill_assessments:
            st.markdown('<div class="section-header">📈 Verified Skill Scores</div>',
                        unsafe_allow_html=True)
            sa_df = pd.DataFrame(
                list(skill_assessments.items()), columns=["Skill", "Score"]
            ).sort_values("Score", ascending=False)
            sa_fig = px.bar(
                sa_df, x="Skill", y="Score",
                color="Score",
                color_continuous_scale=["#6366f1", "#a78bfa", "#34d399"],
                range_y=[0, 100],
                labels={"Score": "Assessment Score (/100)"}
            )
            sa_fig.update_layout(
                paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
                font=dict(color="#94a3b8"), margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_showscale=False
            )
            sa_fig.update_xaxes(gridcolor="#1e293b")
            sa_fig.update_yaxes(gridcolor="#1e293b")
            st.plotly_chart(sa_fig, use_container_width=True)
