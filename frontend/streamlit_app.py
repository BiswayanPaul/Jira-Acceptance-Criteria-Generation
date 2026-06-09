import streamlit as st
import requests

st.set_page_config(
    page_title="Acceptance Criteria Agent",
    layout="wide"
)

st.title(
    "AI Acceptance Criteria Generator"
)

st.write(
    "Enter one user story per line."
)

stories_text = st.text_area(
    "Stories",
    height=300
)

if st.button("Generate"):

    stories = [
        s.strip()
        for s in stories_text.split("\n")
        if s.strip()
    ]

    response = requests.post(
        "http://localhost:8000/generate",
        json={
            "stories": stories
        }
    )

    data = response.json()

    for item in data["results"]:

        st.subheader("User Story")

        st.write(item["story"])

        st.markdown(
            item["acceptance_criteria"]
        )

        st.divider()