import streamlit as st
import requests

API_URL = "http://backend:5000"  # Docker service name

st.title("🔐 Security Assistant")

menu = st.sidebar.selectbox("Choose Option", ["Check Password", "Generate Password", "History"])

# 🔹 Check Password
if menu == "Check Password":
    password = st.text_input("Enter Password", type="password")

    if st.button("Check Strength"):
        res = requests.post(f"{API_URL}/check", json={"password": password})
        if res.status_code == 200:
            data = res.json()
            st.success(f"Strength: {data['strength']}")
            st.info(f"Score: {data['score']}")

# 🔹 Generate Password
elif menu == "Generate Password":
    length = st.slider("Length", 6, 20, 12)

    if st.button("Generate"):
        res = requests.get(f"{API_URL}/generate?length={length}")
        if res.status_code == 200:
            st.success(res.json()["password"])

# 🔹 History
elif menu == "History":
    if st.button("Load History"):
        res = requests.get(f"{API_URL}/history")
        if res.status_code == 200:
            st.write(res.json())