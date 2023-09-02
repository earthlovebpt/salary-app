import streamlit as st
import json
import lightgbm as lgb
import pandas as pd

with open("choices.json") as json_file:
    choice_dict = json.load(json_file)

model = lgb.Booster(model_file="model.txt")


def show_predict_page():
    st.title("Developer Salary prediction")
    
    country = st.selectbox("Country", choice_dict["Country"], choice_dict["Country"].index("United States of America"))
    education = st.selectbox("Education Level", choice_dict["EdLevel"], choice_dict["EdLevel"].index("Bachelor's degree"))
    dev_type = st.selectbox("Role", choice_dict["DevType"], choice_dict["DevType"].index("Developer, back-end"))
    org_size = st.selectbox("OrgSize", choice_dict["OrgSize"], choice_dict["OrgSize"].index("100 to 499 employees"))
    age = st.selectbox("Age", choice_dict["Age"], choice_dict["Age"].index("18-24 years old"))
    experience = st.slider("Years of Experience", 0, 30, 3)

    get_prediction = st.button("Estimate Annual Salary!")
    if get_prediction:
        df = pd.DataFrame(
            {
                "Country": [country],
                "EdLevel": [education],
                "DevType": [dev_type],
                "OrgSize": [org_size],
                "Age": [age],
                "YearsCodePro": [experience],
            }
        )
        for col in df.columns:
            if col != "YearsCodePro":
                df[col] = df[col].astype("category")

        prediction = model.predict(df)
        error = 0.1
        lower, upper = prediction * (1 - error), prediction * (1 + error)
        lower = int(lower / 1000)
        upper = int(upper / 1000)
        st.subheader(f"Your estimated annual salary = {lower}k - {upper}k dollars")
