import streamlit as st
from preprocess import preprocess_input
from infer import generate_response
from postprocess import clean_output
from huggingface_hub import login
import os

token = os.getenv("HF_TOKEN")
login(token=token)


st.set_page_config(page_title="Clinical Assistant", layout="wide")

st.title("🩺 AI Clinical Assistant")
st.markdown("Provide a patient scenario and receive evidence-based clinical advice.")

# --- Collect structured inputs ---
st.header("Clinician Details")

col1, col2 = st.columns(2)
with col1:
    county = st.selectbox("County", ['Uasin Gishu', 'Kiambu', 'Kakamega', 'Elgeiyo Marakwet', 'Bungoma','unknown'])
    health_level = st.selectbox("Health Level", ['Sub-county Hospitals and Nursing Homes',
       'National Referral Hospitals', 'Health centres',
       'Dispensaries and Private Clinics', 'Health Centres',
       'County Hospitals', 'Community Health Centers', 'Health Centers','unknown'])
    nursing_competency = st.selectbox("Nursing Competency", ['Pediatric Emergency Burns', 'Child Health', 'General Emergency',
       'Critical Care', 'Adult Health', 'Maternal and Child Health',
       'Emergency Care - Mental Health', 'Sexual And Reproductive Health',
       'Emergency Care - GBV', 'Neonatal Care', 'Wound and Ostomy Care',
       'Surgical Care', 'Emergency Care - Pediatric',
       'maternal and child health', 'maternah and child health',
       'Emergency Care - Burns', 'Mental Health',
       'Emergency Care - Adult', 'Emergency Care - Rape',
       'Obstetrics Emergency', 'mayernal and child health','unknown'])

with col2:
    unknown_exp = st.checkbox("Years of experience unknown")

    if unknown_exp:
        years_experience = 'unknown'
    else:
        years_experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=1)

    st.write("Years of Experience:", years_experience)

    clinical_panel = st.selectbox("Clinical Panel", ['SURGERY', 'PAEDIATRICS', 'INTERNAL MEDICINE',
       'OBSTETRICS AND GYNAECOLOGY', 'CRITICAL CARE', 'SURGERY (ENT)',
       'SURGERY PAEDIATRICS', 'PAEDIATRIC NEUROLOGY',
       'INTERNAL MEDICINE/CARDIOLOGY', 'PSYCHIATRY',
       'INTERNAL MEDICINE/PSYCHIATRY', 'SURGERY/OPTHALMOLOGY',
       'INTERNAL MEDICINE/SURGERY', 'CRITICAL CARE/SURGERY','unknown'])

st.header("Patient Details")
col3, col4 = st.columns(2)
with col3:
    age_input = st.text_input("Years of Experience (leave blank if unknown)")

    if age_input == "":
        age = 'unknown'
    else:
        age = age_input

with col4:
    gender = st.selectbox("Patient Gender", ["Female", "Male", "Other", "unknown"])

# --- Patient Case ---
st.header("Case Description")
user_input = st.text_area("Enter patient case description below:", height=200)

# --- Generate Button ---
if st.button("Generate Response"):
    if user_input.strip() == "":
        st.warning("Please enter a patient case.")
    else:
        with st.spinner("Processing..."):
            structured_data = {
                "county": county,
                "health_level": health_level,
                "nursing_competency": nursing_competency,
                "years_experience": years_experience,
                "clinical_panel": clinical_panel,
                "age": age,
                "gender": gender,
            }

            # 👇 Combine structured data and free-text into the prompt
            prompt = preprocess_input(user_input, structured_data)

            raw_output = generate_response(prompt)
            final_response = clean_output(raw_output,prompt)

        st.markdown("### 🧠 Model Response")
        st.write(final_response)
