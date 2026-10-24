import io
import math
from typing import Optional

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="DataLab Academy",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme / helpers ----------
st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1400px;}
.hero {padding: 1.35rem 1.5rem; border-radius: 18px;
       background: linear-gradient(120deg, #102a43 0%, #1d4e67 60%, #287d80 100%);
       color: white; margin-bottom: 1rem;}
.hero h1 {color: white; margin-bottom: .25rem;}
.hero p {color: #e6f4f1; margin-bottom: 0;}
.small-muted {color: #64748b; font-size: .9rem;}
.case-card {border: 1px solid #d8e1e8; border-radius: 14px; padding: 1rem;}
</style>
""", unsafe_allow_html=True)

def make_demo_data():
    return pd.DataFrame({
        "Student": ["Alex", "Bella", "Charlie", "Dani", "Elliot", "Farah",
                    "George", "Harper", "Imani", "Jamie", "Kai", "Leah"],
        "Team": ["Blue", "Red", "Blue", "Red", "Blue", "Red",
                 "Blue", "Red", "Blue", "Red", "Blue", "Red"],
        "Sprint_Time_Seconds": [13.2, 12.8, 13.5, 12.9, 13.1, 12.7,
                                13.4, 12.6, 13.0, 12.9, 13.3, 12.8],
        "Long_Jump_Metres": [3.1, 3.3, 2.9, 3.4, 3.2, 3.5,
                             3.0, 3.6, 3.4, 3.2, 3.1, 3.5],
        "Points": [8, 10, 7, 11, 9, 12, 8, 13, 10, 9, 7, 12],
    })

def safe_numeric_columns(df):
    return df.select_dtypes(include=np.number).columns.tolist()

def stats_for(series):
    x = pd.to_numeric(series, errors="coerce").dropna()
    if x.empty:
        return None
    return {
        "Count": int(x.count()),
        "Mean": float(x.mean()),
        "Median": float(x.median()),
        "Minimum": float(x.min()),
        "Maximum": float(x.max()),
        "Range": float(x.max() - x.min()),
        "Standard deviation": float(x.std(ddof=1)) if len(x) > 1 else 0.0,
    }

def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")

if "case_completed" not in st.session_state:
    st.session_state.case_completed = False
if "case_score" not in st.session_state:
    st.session_state.case_score = 0
if "verdict_submitted" not in st.session_state:
    st.session_state.verdict_submitted = False

# ---------- Sidebar ----------
st.sidebar.markdown("## 🔎 DataLab Academy")
st.sidebar.caption("Discover data. Investigate evidence.")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "DataLab Classroom", "Data Detective Academy", "Teacher Guide"],
)
st.sidebar.divider()
student_level = st.sidebar.selectbox("Learning level", ["KS3", "KS4"])
st.sidebar.caption("Prototype v0.1 · Uses fictional demo data")

# ---------- Home ----------
if page == "Home":
    st.markdown("""
    <div class="hero">
      <h1>DataLab Academy</h1>
      <p>Learn to think with data — explore it, question it, and use evidence to solve problems.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("A combined data-analysis lab and detective challenge for KS3 and KS4 learners.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Learning spaces", "2", "Explore + Investigate")
    c2.metric("Starter case", "001", "School sports mystery")
    c3.metric("Data safety", "Demo mode", "No accounts required")
    st.subheader("Choose your learning path")
    left, right = st.columns(2)
    with left:
        st.markdown("### 📊 DataLab Classroom")
        st.write("Explore a dataset, calculate statistics, build charts and explain what the evidence shows.")
        if st.button("Open DataLab Classroom", use_container_width=True):
            st.session_state["nav_target"] = "DataLab Classroom"
            st.rerun()
    with right:
        st.markdown("### 🕵️ Data Detective Academy")
        st.write("Investigate a mystery, check the records, compare evidence and submit your verdict.")
        if st.button("Open Detective Academy", use_container_width=True):
            st.session_state["nav_target"] = "Data Detective Academy"
            st.rerun()
    st.info("Teaching principle: a chart can reveal a pattern, but a pattern alone does not prove why something happened.")
    st.subheader("Skills you will practise")
    skills = st.columns(4)
    for col, title, desc in zip(
        skills,
        ["Inspect", "Calculate", "Visualise", "Reason"],
        ["Understand columns and data quality", "Compare averages and spread", "Choose and interpret charts", "Support conclusions with evidence"],
    ):
        with col:
            st.markdown(f"**{title}**")
            st.caption(desc)

# ---------- DataLab ----------
elif page == "DataLab Classroom":
    st.title("📊 DataLab Classroom")
    st.write("Choose a dataset, explore its numerical columns and investigate patterns.")
    uploaded = st.file_uploader("Upload a CSV dataset (optional)", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            st.success(f"Loaded {len(df):,} rows and {len(df.columns)} columns.")
        except Exception as exc:
            st.error(f"Could not read this CSV: {exc}")
            df = make_demo_data()
    else:
        st.caption("Using the built-in fictional sports dataset.")
        df = make_demo_data()

    with st.expander("Preview dataset", expanded=True):
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Download current dataset as CSV", to_csv_bytes(df),
                           file_name="datalab_dataset.csv", mime="text/csv")

    numeric_cols = safe_numeric_columns(df)
    if not numeric_cols:
        st.warning("This dataset has no numerical columns. Upload a CSV containing at least one numeric column.")
    else:
        st.subheader("Statistics at a glance")
        chosen = st.selectbox("Choose a numerical variable", numeric_cols)
        summary = stats_for(df[chosen])
        if summary:
            a, b, c, d = st.columns(4)
            a.metric("Mean", f"{summary['Mean']:.2f}")
            b.metric("Median", f"{summary['Median']:.2f}")
            c.metric("Range", f"{summary['Range']:.2f}")
            d.metric("Valid values", f"{summary['Count']}")
            with st.expander("View all summary statistics"):
                stat_df = pd.DataFrame({"Statistic": list(summary.keys()),
                                        "Value": [round(v, 3) if isinstance(v, float) else v
                                                  for v in summary.values()]})
                st.dataframe(stat_df, use_container_width=True, hide_index=True)

        st.subheader("Visualisation studio")
        chart_type = st.selectbox("Choose a chart", [
            "Histogram", "Box plot", "Bar chart (count)", "Scatter plot"
        ])
        if chart_type == "Histogram":
            fig = px.histogram(df, x=chosen, nbins=10, title=f"Distribution of {chosen}",
                               labels={chosen: chosen}, template="plotly_white")
        elif chart_type == "Box plot":
            fig = px.box(df, y=chosen, points="all", title=f"Spread of {chosen}",
                         template="plotly_white")
        elif chart_type == "Bar chart (count)":
            cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()
            if cat_cols:
                cat = st.selectbox("Choose a category", cat_cols)
                counts = df[cat].astype(str).value_counts().reset_index()
                counts.columns = [cat, "Count"]
                fig = px.bar(counts, x=cat, y="Count", title=f"Count by {cat}",
                             template="plotly_white")
            else:
                st.warning("A bar count chart needs a categorical column.")
                fig = None
        else:
            if len(numeric_cols) >= 2:
                xcol, ycol = st.columns(2)
                with xcol:
                    x_var = st.selectbox("X-axis", numeric_cols, index=0)
                with ycol:
                    y_default = 1 if len(numeric_cols) > 1 else 0
                    y_var = st.selectbox("Y-axis", numeric_cols, index=y_default)
                fig = px.scatter(df, x=x_var, y=y_var, hover_data=[
                    c for c in df.columns if c not in [x_var, y_var]
                ][:2], title=f"{y_var} compared with {x_var}", template="plotly_white")
            else:
                st.warning("A scatter plot needs at least two numerical columns.")
                fig = None
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
            try:
                chart_html = fig.to_html(include_plotlyjs="cdn", full_html=True).encode("utf-8")
                st.download_button("Download interactive chart (HTML)", chart_html,
                                   file_name="datalab_chart.html", mime="text/html")
            except Exception:
                pass

        st.subheader("Check your understanding")
        if chosen in df.columns:
            question = st.radio(
                f"What does the median of **{chosen}** represent?",
                [
                    "The most common value",
                    "The middle value when the data is ordered",
                    "The difference between the largest and smallest values",
                    "The total of all values",
                ],
                key="median_question",
            )
            if st.button("Check answer", key="check_median"):
                if question == "The middle value when the data is ordered":
                    st.success("Correct. The median is the middle value after ordering the data; with an even number of values, it is the mean of the two middle values.")
                else:
                    st.error("Not quite. Think about ordering all the values from smallest to largest.")

        st.subheader("Write an evidence-based observation")
        observation = st.text_area(
            "What pattern do you notice? What can you conclude — and what can’t you conclude?",
            placeholder="I notice that... The data suggests... However, it does not prove...",
        )
        if observation.strip():
            st.caption(f"Draft length: {len(observation.split())} words. This is a reflection draft, not an automatically graded answer.")

# ---------- Detective Academy ----------
elif page == "Data Detective Academy":
    st.title("🕵️ Data Detective Academy")
    st.caption("CASE 001 · SCHOOL SPORTS DAY")
    st.markdown("""
    ### The Mystery of the Missing Winning Team
    The school sports committee has received two different versions of the sprint results.
    Your task is to inspect the records and decide what the evidence actually supports.
    """)
    st.warning("All names and results in this case are fictional and created for learning.")
    case_df = make_demo_data()
    with st.expander("Evidence file A — sprint records", expanded=True):
        st.dataframe(case_df[["Student", "Team", "Sprint_Time_Seconds", "Points"]],
                     use_container_width=True, hide_index=True)
    st.markdown("#### Clue 1: What does the sprint time tell you?")
    st.write("For sprint times, a **smaller number means a faster run**. Compare the teams using their recorded times.")
    team_stats = case_df.groupby("Team")["Sprint_Time_Seconds"].agg(["count", "mean", "median", "min", "max"]).reset_index()
    team_stats.columns = ["Team", "Number of records", "Mean time (s)", "Median time (s)", "Fastest time (s)", "Slowest time (s)"]
    st.dataframe(team_stats.round(2), use_container_width=True, hide_index=True)
    fig = px.box(case_df, x="Team", y="Sprint_Time_Seconds", color="Team",
                 points="all", title="Sprint times by team (lower is faster)",
                 labels={"Sprint_Time_Seconds": "Time (seconds)"}, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Clue 2: Submit your verdict")
    verdict = st.radio(
        "Based only on the sprint times shown, which statement is best supported?",
        [
            "The Blue team is definitely the overall sports-day winner.",
            "The Red team is definitely the overall sports-day winner.",
            "The Red team has the lower average sprint time in this dataset, but sprint times alone cannot establish the overall sports-day winner.",
            "The team with the single fastest runner must have won every event.",
        ],
        key="case_verdict",
    )
    reasoning = st.text_area(
        "Explain your reasoning using at least one piece of evidence.",
        placeholder="The average time for... is... This means... However...",
    )
    if st.button("Submit verdict", type="primary"):
        correct = verdict.startswith("The Red team has the lower average")
        has_reasoning = len(reasoning.strip().split()) >= 8
        score = (70 if correct else 0) + (30 if has_reasoning else 0)
        st.session_state.case_score = score
        st.session_state.case_completed = True
        st.session_state.verdict_submitted = True
    if st.session_state.verdict_submitted:
        score = st.session_state.case_score
        st.metric("Case score", f"{score}/100")
        if score >= 70:
            st.success("Good investigation. You identified the supported comparison. To establish the overall winner, you would also need the rules and results for the other events.")
            st.markdown("🏅 **Evidence Checker badge unlocked**")
        else:
            st.info("Review the team averages and remember: a lower sprint time is faster. Also ask whether sprint data alone can decide an entire multi-event competition.")
        st.caption("Prototype scoring checks the selected verdict and whether a written explanation has at least eight words. It does not yet evaluate the quality of the reasoning.")
        if st.button("Reset case"):
            st.session_state.case_completed = False
            st.session_state.case_score = 0
            st.session_state.verdict_submitted = False
            st.rerun()

# ---------- Teacher Guide ----------
elif page == "Teacher Guide":
    st.title("👩‍🏫 Teacher Guide")
    st.write("Use this page to introduce the learning objectives and adapt the discussion for KS3 or KS4.")
    st.subheader(f"Suggested learning objectives — {student_level}")
    if student_level == "KS3":
        st.markdown("""
        - Calculate and interpret mean, median, range and simple comparisons.
        - Read tables and select suitable charts.
        - Describe patterns using numerical evidence.
        - Recognise that a conclusion should not go beyond the data.
        """)
    else:
        st.markdown("""
        - Compare distributions using averages and spread.
        - Interpret outliers and variation between groups.
        - Evaluate the limitations of a dataset and a visualisation.
        - Distinguish a supported association from a causal claim.
        """)
    st.subheader("Suggested lesson sequence (30–45 minutes)")
    st.markdown("""
    1. **Launch (5 min):** Ask what evidence would be needed to decide the sports-day winner.
    2. **Explore (10 min):** Students inspect the table and identify relevant columns.
    3. **Analyse (10 min):** Compare team means and distributions.
    4. **Challenge (10 min):** Students submit a verdict and justify it.
    5. **Reflect (5 min):** Discuss missing evidence, fairness and the limits of conclusions.
    """)
    st.subheader("Assessment prompts")
    st.markdown("""
    - Which statistic best supports your comparison, and why?
    - How does the chart support or complicate your first impression?
    - What additional data would you need before making a final decision?
    - How could a chart mislead someone who reads it too quickly?
    """)
    st.info("For classroom pilots, use fictional or properly anonymised datasets. This prototype has no student accounts, class roster, cloud progress storage or safeguarding workflow.")
