import streamlit as st
import requests
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="PhishPrint V2",
    page_icon=None,
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

[data-testid="stAppViewContainer"] { background-color: #1E1E1E; }
[data-testid="stHeader"] { background-color: #1E1E1E; }
section[data-testid="stMain"] > div { padding-top: 2rem; }
[data-testid="stDecoration"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

* { font-family: 'JetBrains Mono', monospace !important; }

input[type="text"] {
    background-color: #2D2D2D !important;
    border: 1px solid #454545 !important;
    border-radius: 3px !important;
    color: #D4D4D4 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 0.8rem !important;
}
input[type="text"]:focus {
    border-color: #569CD6 !important;
    box-shadow: none !important;
}
.stButton > button {
    background-color: #0E639C !important;
    color: #FFFFFF !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500 !important;
    border: none !important;
    border-radius: 3px !important;
    width: 100% !important;
    padding: 0.55rem !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px !important;
}
.stButton > button:hover { background-color: #1177BB !important; }

/* stat card */
.stat-card {
    background-color: #252526;
    border: 1px solid #3C3C3C;
    border-radius: 3px;
    padding: 1rem 1.25rem;
    height: 100%;
}
.stat-label {
    color: #858585;
    font-size: 0.7rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 0 0 0.4rem 0;
}
.stat-value {
    color: #D4D4D4;
    font-size: 1.3rem;
    font-weight: 600;
    margin: 0;
}
.stat-sub {
    color: #6A6A6A;
    font-size: 0.7rem;
    margin: 0.2rem 0 0 0;
}

/* how it works */
.how-card {
    background-color: #252526;
    border: 1px solid #3C3C3C;
    border-radius: 3px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.6rem;
}
.how-step {
    color: #569CD6;
    font-size: 0.72rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 0 0 0.2rem 0;
}
.how-desc {
    color: #858585;
    font-size: 0.78rem;
    margin: 0;
    line-height: 1.5;
}

/* verdict */
.verdict-phish {
    background-color: #2D1A1A;
    border-left: 3px solid #F44747;
    border-radius: 3px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.25rem;
}
.verdict-legit {
    background-color: #1A2D1E;
    border-left: 3px solid #4EC9B0;
    border-radius: 3px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.25rem;
}
.verdict-tag {
    font-size: 0.68rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #858585;
    margin: 0 0 0.3rem 0;
}
.verdict-main {
    font-size: 1.35rem;
    font-weight: 600;
    margin: 0 0 0.25rem 0;
}
.verdict-url {
    color: #6A6A6A;
    font-size: 0.75rem;
    margin: 0;
    word-break: break-all;
}
.verdict-conf {
    font-size: 1.8rem;
    font-weight: 600;
    margin: 0;
    line-height: 1.1;
}
.verdict-conf-label {
    color: #6A6A6A;
    font-size: 0.68rem;
    margin: 0.15rem 0 0 0;
}

.section-label {
    color: #858585;
    font-size: 0.68rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 0 0 0.6rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-bottom: 1px solid #3C3C3C; padding-bottom: 1rem; margin-bottom: 1.5rem;">
    <p style="font-size: 0.68rem; color: #569CD6; letter-spacing: 2px;
              text-transform: uppercase; margin: 0 0 0.3rem 0;">
        PHISHPRINT / V2
    </p>
    <h1 style="font-size: 1.5rem; font-weight: 600; color: #D4D4D4;
               margin: 0 0 0.25rem 0; letter-spacing: -0.3px;">
        Phishing URL Detector
    </h1>
    <p style="color: #6A6A6A; font-size: 0.75rem; margin: 0;">
        XGBoost &nbsp;&mdash;&nbsp; 30+ real features &nbsp;&mdash;&nbsp; 97.97% accuracy &nbsp;&mdash;&nbsp; RV University
    </p>
</div>
""", unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────
st.markdown("""
<p style="color: #4EC9B0; font-size: 0.75rem; margin-bottom: 0.4rem; letter-spacing: 0.5px;">
&gt; enter_url
</p>
""", unsafe_allow_html=True)

url_input = st.text_input("url", placeholder="https://example.com",
                           label_visibility="collapsed")
analyse = st.button("Run Analysis")

st.markdown("""
<p style="color: #454545; font-size: 0.75rem; margin-top: 0.5rem; font-style: italic;">
// try:
<span style="color:#CE9178; font-style:normal;">https://www.google.com</span>
&nbsp;&nbsp;
<span style="color:#CE9178; font-style:normal;">http://paypa1-verify.tk/login</span>
</p>
""", unsafe_allow_html=True)

# ── Results or Info ────────────────────────────────────────────────────────
if not analyse or not url_input.strip():
    st.markdown('<hr style="border:none;border-top:1px solid #3C3C3C;margin:1.5rem 0;">',
                unsafe_allow_html=True)

    # Stat cards
    st.markdown('<p class="section-label">Model Stats</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="stat-card">
            <p class="stat-label">Accuracy</p>
            <p class="stat-value" style="color:#4EC9B0;">97.97%</p>
            <p class="stat-sub">on 6,000 test URLs</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="stat-card">
            <p class="stat-label">Dataset</p>
            <p class="stat-value" style="color:#569CD6;">30,000</p>
            <p class="stat-sub">balanced URLs</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="stat-card">
            <p class="stat-label">Features</p>
            <p class="stat-value" style="color:#CE9178;">30+</p>
            <p class="stat-sub">extracted live per URL</p>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr style="border:none;border-top:1px solid #3C3C3C;margin:1.5rem 0;">',
                unsafe_allow_html=True)

    # How it works
    st.markdown('<p class="section-label">How It Works</p>', unsafe_allow_html=True)

    steps = [
        ("01 — Lexical Analysis",
         "Parses the raw URL string — length, subdomains, special characters, digit ratio, suspicious TLD, phishing keywords, brand similarity score."),
        ("02 — Webpage Inspection",
         "Fetches the live page and checks for login forms, iframes, external favicons, hyperlink ratios."),
        ("03 — XGBoost Inference",
         "30 selected features are passed through a trained XGBoost classifier. Trained on OpenPhish + Majestic Million data."),
        ("04 — SHAP Explainability",
         "Feature weights are computed per prediction so you can see exactly which signals drove the verdict."),
    ]
    for title, desc in steps:
        st.markdown(f"""
        <div class="how-card">
            <p class="how-step">{title}</p>
            <p class="how-desc">{desc}</p>
        </div>""", unsafe_allow_html=True)

else:
    if not url_input.startswith("http"):
        st.error("URL must start with http:// or https://")
    else:
        with st.spinner("Analysing..."):
            try:
                resp = requests.post(API_URL, json={"url": url_input}, timeout=15)
                data = resp.json()

                verdict    = data["verdict"]
                confidence = data["confidence"]
                top_feats  = data["top_features"]

                st.markdown('<hr style="border:none;border-top:1px solid #3C3C3C;margin:1.5rem 0;">',
                            unsafe_allow_html=True)

                left, right = st.columns([1.2, 1])

                with left:
                    if verdict == "phishing":
                        st.markdown(f"""
                        <div class="verdict-phish">
                            <p class="verdict-tag">Verdict</p>
                            <p class="verdict-main" style="color:#F44747;">Phishing Detected</p>
                            <p class="verdict-url">{url_input}</p>
                        </div>""", unsafe_allow_html=True)
                        conf_color = "#F44747"
                    else:
                        st.markdown(f"""
                        <div class="verdict-legit">
                            <p class="verdict-tag">Verdict</p>
                            <p class="verdict-main" style="color:#4EC9B0;">Legitimate</p>
                            <p class="verdict-url">{url_input}</p>
                        </div>""", unsafe_allow_html=True)
                        conf_color = "#4EC9B0"

                    st.markdown(f"""
                    <div style="background:#252526; border:1px solid #3C3C3C;
                                border-radius:3px; padding:0.9rem 1.25rem;">
                        <p class="verdict-tag">Confidence</p>
                        <p class="verdict-conf" style="color:{conf_color};">{confidence}%</p>
                        <p class="verdict-conf-label">model confidence score</p>
                    </div>""", unsafe_allow_html=True)

                with right:
                    st.markdown('<p class="section-label" style="margin-top:0;">Feature Weights</p>',
                                unsafe_allow_html=True)

                    feats  = list(top_feats.keys())
                    vals   = list(top_feats.values())
                    colors = ["#F44747" if v > 0 else "#4EC9B0" for v in vals]

                    fig, ax = plt.subplots(figsize=(5, 2.8))
                    fig.patch.set_facecolor("#252526")
                    ax.set_facecolor("#252526")
                    ax.barh(feats, vals, color=colors, height=0.45)
                    ax.axvline(0, color="#454545", linewidth=0.8)
                    ax.tick_params(colors="#858585", labelsize=7.5)
                    for spine in ax.spines.values():
                        spine.set_color("#3C3C3C")
                    for label in ax.get_yticklabels():
                        label.set_color("#CE9178")
                        label.set_fontfamily("monospace")
                        label.set_fontsize(7.5)
                    ax.set_xlabel("weight", color="#6A6A6A", fontsize=7,
                                  fontfamily="monospace")
                    plt.tight_layout(pad=0.8)
                    st.pyplot(fig)
                    plt.close()

                    st.markdown("""
                    <p style="color:#454545; font-size:0.72rem; margin-top:0.2rem;">
                    // red = toward phishing &nbsp; teal = toward legitimate
                    </p>""", unsafe_allow_html=True)

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API. Start FastAPI on port 8000.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #3C3C3C; margin-top:2rem; padding-top:0.75rem;">
    <p style="color:#454545; font-size:0.72rem; margin:0;">
        PhishPrint V2 &nbsp;|&nbsp; XGBoost &nbsp;|&nbsp; RV University, Bengaluru
    </p>
</div>
""", unsafe_allow_html=True)