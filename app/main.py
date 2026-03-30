import streamlit as st
import requests
import time

API_URL = "http://localhost:5000"

st.set_page_config(page_title="🔐 SecureApp", layout="centered")
st.title("🔐 Security Assistant")
st.caption("Check password strength, generate secure passwords, and track history.")

tab1, tab2, tab3 = st.tabs(["Check Password", "Generate Password", "History"])

with tab1:
    st.subheader("Password strength checker")
    password = st.text_input("Enter password", type="password", key="pw_input")

    if st.button("Check strength", key="check_btn"):
        if not password:
            st.warning("Please enter a password.")
        else:
            with st.spinner("Checking..."):
                try:
                    res = requests.post(f"{API_URL}/check", json={"password": password}, timeout=5)
                    data = res.json()
                    strength = data.get("strength", "Unknown")
                    score = data.get("score", 0)
                    reasons = data.get("reasons", [])

                    color = {"Strong": "green", "Medium": "orange", "Weak": "red"}.get(strength, "gray")
                    st.markdown(f"**Strength:** :{color}[{strength}]")
                    st.progress(score / 10)
                    st.caption(f"Score: {score}/10")

                    if reasons:
                        st.info("Suggestions: " + " | ".join(reasons))
                except Exception as e:
                    st.error(f"API error: {e}")

with tab2:
    st.subheader("Secure password generator")
    length = st.slider("Password length", 8, 32, 12)

    if st.button("Generate", key="gen_btn"):
        try:
            res = requests.get(f"{API_URL}/generate", params={"length": length}, timeout=5)
            pw = res.json().get("password", "")
            st.code(pw, language=None)
            st.success("Copy the password above!")
        except Exception as e:
            st.error(f"API error: {e}")

with tab3:
    st.subheader("Recent checks")
    try:
        res = requests.get(f"{API_URL}/history", timeout=5)
        rows = res.json()
        if rows:
            st.table(rows)
        else:
            st.info("No history yet.")
    except Exception as e:
        st.error(f"API error: {e}")