import streamlit as st
import requests
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="PhishPrint V2",
    page_icon="",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Consolas&family=Segoe+UI:wght@400;600;700&display=swap');

[data-testid="stAppViewContainer"] { background-color: #1E1E1E; }
[data-testid="stHeader"] { background-color: #1E1E1E; }
section[data-testid="stMain"] > div { padding-top: 1.5rem; }
[data-testid="stDecoration"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

* { font-family: 'Segoe UI', sans-serif !important; }

/* Input */
input[type="text"] {
    background-color: #3C3C3C !important;
    border: 1px solid #555555 !important;
    border-radius: 4px !important;
    color: #D4D4D4 !important;
    font-family: 'Consolas', monospace !important;
    font-size: 0.9rem !important;
}
input[type="text"]:focus {
    border-color: #007ACC !important;
    outline: none !important;
}

/* Button */
.stButton > button {
    background-color: #0E639C !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 2px !important;
    width: 100% !important;
    padding: 0.55rem !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    background-color: #1177BB !important;
}

/* Spinner */
.stSpinner > div { border-top-color: #CE9178 !important; }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="border-bottom: 1px solid #3C3C3C; padding-bottom: 1rem; margin-bottom: 1.5rem;">
    <p style="font-size: 0.72rem; color: #858585; font-family: Consolas, monospace;
              letter-spacing: 1px; text-transform: uppercase; margin: 0 0 0.3rem 0;">
        PHISHPRINT / V2
    </p>
    <h1 style="font-size: 1.6rem; font-weight: 700; color: #D4D4D4;
               margin: 0 0 0.2rem 0; letter-spacing: -0.3px;">
        Phishing URL Detector
    </h1>
    <p style="color: #858585; font-size: 0.82rem; margin: 0; font-family: Consolas, monospace;">
        XGBoost &nbsp;&nbsp;|&nbsp;&nbsp; 30+ features &nbsp;&nbsp;|&nbsp;&nbsp; 97.97% accuracy
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="color: #9CDCFE; font-size: 0.8rem; font-family: Consolas, monospace;
          margin-bottom: 0.4rem;">
  &gt; enter_url
</p>
""", unsafe_allow_html=True)

url_input = st.text_input("url", placeholder="https://example.com",
                           label_visibility="collapsed")
analyse = st.button("Run Analysis")

st.markdown("""
<p style="color: #555555; font-size: 0.78rem; font-family: Consolas, monospace;
          margin-top: 0.6rem;">
// try: &nbsp;
<span style="color:#CE9178;">https://www.google.com</span>
&nbsp;&nbsp;
<span style="color:#CE9178;">http://paypa1-verify.tk/login</span>
</p>
""", unsafe_allow_html=True)

if analyse:
    if not url_input.strip():
        st.warning("Please enter a URL.")
    elif not url_input.startswith("http"):
        st.error("URL must start with http:// or https://")
    else:
        with st.spinner("Analysing..."):
            try:
                resp = requests.post(API_URL, json={"url": url_input}, timeout=15)
                data = resp.json()

                verdict    = data["verdict"]
                confidence = data["confidence"]
                top_feats  = data["top_features"]

                st.markdown('<hr style="border:none; border-top:1px solid #3C3C3C; margin:1.5rem 0;">',
                            unsafe_allow_html=True)

                if verdict == "phishing":
                    st.markdown(f"""
                    <div style="background:#2D1A1A; border-left: 3px solid #F44747;
                                border-radius: 2px; padding: 1rem 1.25rem; margin-bottom: 1.25rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <p style="font-size:0.72rem; color:#858585; font-family:Consolas,monospace;
                                          letter-spacing:1px; text-transform:uppercase; margin:0 0 0.2rem 0;">
                                    VERDICT
                                </p>
                                <p style="font-size:1.4rem; font-weight:700; color:#F44747; margin:0;">
                                    PHISHING
                                </p>
                                <p style="color:#6A6A6A; font-size:0.78rem; font-family:Consolas,monospace;
                                          margin:0.3rem 0 0 0; word-break:break-all;">
                                    {url_input}
                                </p>
                            </div>
                            <div style="text-align:right; padding-left:1rem;">
                                <p style="font-size:2rem; font-weight:700; color:#F44747;
                                          font-family:Consolas,monospace; margin:0; line-height:1.1;">
                                    {confidence}%
                                </p>
                                <p style="color:#6A6A6A; font-size:0.72rem;
                                          font-family:Consolas,monospace; margin:0.2rem 0 0 0;">
                                    confidence
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background:#1A2D1E; border-left: 3px solid #4EC9B0;
                                border-radius: 2px; padding: 1rem 1.25rem; margin-bottom: 1.25rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <p style="font-size:0.72rem; color:#858585; font-family:Consolas,monospace;
                                          letter-spacing:1px; text-transform:uppercase; margin:0 0 0.2rem 0;">
                                    VERDICT
                                </p>
                                <p style="font-size:1.4rem; font-weight:700; color:#4EC9B0; margin:0;">
                                    LEGITIMATE
                                </p>
                                <p style="color:#6A6A6A; font-size:0.78rem; font-family:Consolas,monospace;
                                          margin:0.3rem 0 0 0; word-break:break-all;">
                                    {url_input}
                                </p>
                            </div>
                            <div style="text-align:right; padding-left:1rem;">
                                <p style="font-size:2rem; font-weight:700; color:#4EC9B0;
                                          font-family:Consolas,monospace; margin:0; line-height:1.1;">
                                    {confidence}%
                                </p>
                                <p style="color:#6A6A6A; font-size:0.72rem;
                                          font-family:Consolas,monospace; margin:0.2rem 0 0 0;">
                                    confidence
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("""
                <p style="font-size:0.72rem; color:#858585; font-family:Consolas,monospace;
                          letter-spacing:1px; text-transform:uppercase; margin: 0 0 0.6rem 0;">
                    FEATURE WEIGHTS
                </p>
                """, unsafe_allow_html=True)

                feats  = list(top_feats.keys())
                vals   = list(top_feats.values())
                colors = ["#F44747" if v > 0 else "#1AEF28" for v in vals]

                fig, ax = plt.subplots(figsize=(7, 2.6))
                fig.patch.set_facecolor("#252526")
                ax.set_facecolor("#252526")
                ax.barh(feats, vals, color=colors, height=0.45)
                ax.axvline(0, color="#555555", linewidth=0.8)
                ax.tick_params(colors="#858585", labelsize=8)
                for spine in ax.spines.values():
                    spine.set_color("#3C3C3C")
                for label in ax.get_yticklabels():
                    label.set_color("#CE9178")
                    label.set_fontfamily("monospace")
                ax.set_xlabel("weight", color="#858585", fontsize=7.5,
                              fontfamily="monospace")
                plt.tight_layout(pad=0.8)
                st.pyplot(fig)
                plt.close()

                st.markdown("""
                <p style="color:#555555; font-size:0.76rem; font-family:Consolas,monospace;
                          margin-top:0.3rem;">
                // red = toward phishing &nbsp;&nbsp; green = toward legitimate
                </p>
                """, unsafe_allow_html=True)

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API. Start FastAPI on port 8000.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("""
<div style="border-top:1px solid #3C3C3C; margin-top:2.5rem; padding-top:0.75rem;">
    <p style="color:#555555; font-size:0.75rem; font-family:Consolas,monospace; margin:0;">
        PhishPrint V2 &nbsp;|&nbsp; RV University, Bengaluru
    </p>
</div>
""", unsafe_allow_html=True)