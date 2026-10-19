import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="PhishPrint V2",
    page_icon="",
    layout="centered"
)

st.title(" PhishPrint V2")
st.markdown("#### Real-Time Phishing URL Detection")
st.markdown("---")

url_input = st.text_input("Enter a URL to check:", placeholder="https://example.com")

if st.button(" Analyse URL", use_container_width=True):
    if not url_input.strip():
        st.warning("Please enter a URL.")
    elif not url_input.startswith("http"):
        st.error("URL must start with http:// or https://")
    else:
        with st.spinner("Extracting features and analysing..."):
            try:
                response = requests.post(API_URL, json={"url": url_input}, timeout=15)
                data = response.json()

                verdict = data["verdict"]
                confidence = data["confidence"]
                top_features = data["top_features"]

                st.markdown("---")
                if verdict == "phishing":
                    st.error(f" **PHISHING** — {confidence}% confidence")
                else:
                    st.success(f" **LEGITIMATE** — {confidence}% confidence")

                st.progress(int(confidence))

                st.markdown("#### Top Contributing Features")
                for feat, val in top_features.items():
                    col1, col2 = st.columns([3, 1])
                    col1.write(f"`{feat}`")
                    col2.write(f"{val:.4f}")

            except requests.exceptions.ConnectionError:
                st.error(" Could not connect to API. Make sure FastAPI is running on port 8000.")
            except Exception as e:
                st.error(f" Error: {str(e)}")

st.markdown("---")
st.caption("PhishPrint V2 | XGBoost | 97.97% Accuracy | RV University")