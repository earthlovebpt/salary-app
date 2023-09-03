import streamlit as st
import pandas as pd
from util import *
import altair as alt
import json


@st.cache_data
def load_data():
    YEAR = 2023
    CUTOFF = 400
    YEAR_MAX = 30

    df = pd.read_csv(f"stack-overflow-developer-survey-{YEAR}/survey_results_public.csv")
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)

    # Remove NaN values.
    dropped_df = df.dropna(subset=["Salary","DevType","YearsCodePro"])

    # Select only full-time employment.
    dropped_df["full_time"] = dropped_df["Employment"].apply(lambda x: "full-time" in str(x))
    dropped_df = dropped_df[dropped_df["full_time"]]

    # Filter out countries that have less data.
    countries_dict = remove_minor_categories(df["Country"].value_counts(), CUTOFF)
    dropped_df["Country"] = dropped_df["Country"].map(countries_dict).astype("category")
    dropped_df = dropped_df[dropped_df["Country"] != "Other"]

    # Group minor types of dev into "Other".
    dev_dict = remove_minor_categories(dropped_df["DevType"].value_counts(), CUTOFF)
    dropped_df["DevType"] = dropped_df["DevType"].map(dev_dict) 
    dropped_df["DevType"] = dropped_df["DevType"].apply(lambda x: "Other" if "Other" in x else x).astype("category")  

    # Set the maximum experience.
    dropped_df["YearsCodePro"] = dropped_df["YearsCodePro"].apply(lambda x: experience2number(x, YEAR_MAX)).astype(int)      
    
    return dropped_df

df = load_data()
with open("notebooks/choices.json") as json_file:
    choice_dict = json.load(json_file)

def show_insights_page():
    st.title("Developer Salary Insights")
    st.caption("The data is based on :blue[Stack Overflow Developer Survey 2023].")
    
    # 1.Country plot
    st.write(""" #### Median Salary based on Country """)
    data = df.groupby("Country")[["Salary"]].median().sort_values(by="Salary", ascending=False).head(15).reset_index()
    bar_chart = alt.Chart(data).mark_bar().encode(
        x="Salary",
        y=alt.Y('Country').sort('-x')
    ).configure_scale(
        bandPaddingInner=0.3
        )
    st.altair_chart(bar_chart, use_container_width=True, theme="streamlit")

    # 2.DevType Plot
    st.write(""" #### Median Salary based on Developer Role """)
    data = df.groupby("DevType")[["Salary"]].median().sort_values(by="Salary", ascending=False).head(15).reset_index()
    bar_chart = alt.Chart(data).mark_bar().encode(
        x="Salary",
        y=alt.Y('DevType').sort('-x')
    ).configure_scale(
        bandPaddingInner=0.3
        )
    st.altair_chart(bar_chart, use_container_width=True, theme="streamlit")

    # 3.Salary Growth
    st.write(""" #### Salary Growth based on Experience """)
    dev_list = st.multiselect(label='Select your roles',options=choice_dict["DevType"],default=["Developer, back-end"])
    data = df.groupby(["YearsCodePro","DevType"])[["Salary"]].median().reset_index()
    data = data[data["DevType"].isin(dev_list)]
    data = data.pivot(index="YearsCodePro", columns='DevType', values='Salary')
    st.line_chart(data)
    
    # 4.Country distribution
    st.write(""" #### Country distribution """)
    data = df.groupby("Country")[["Salary"]].count().rename({"Salary":"count"}, axis=1).sort_values(by="count", ascending=False).head(10).reset_index()
    data["percent"] = data["count"]/df.shape[0]*100
    bar_chart = alt.Chart(data).mark_bar().encode(
        x="percent",
        y=alt.Y('Country').sort('-x')
    ).configure_scale(
        bandPaddingInner=0.3
        )
    st.altair_chart(bar_chart, use_container_width=True, theme="streamlit")

    # 5.DevType distribution
    st.write(""" #### Developer Role distribution """)
    data = df.groupby("DevType")[["Salary"]].count().rename({"Salary":"count"}, axis=1).sort_values(by="count", ascending=False).head(10).reset_index()
    data["percent"] = data["count"]/df.shape[0]*100
    bar_chart = alt.Chart(data).mark_bar().encode(
        x="percent",
        y=alt.Y('DevType').sort('-x')
    ).configure_scale(
        bandPaddingInner=0.3,
        )
    st.altair_chart(bar_chart, use_container_width=True, theme="streamlit")


