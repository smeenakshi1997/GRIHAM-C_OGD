
#######################

# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import pickle
import torch
import json
import csv
import datetime

########################

# Page configuration
st.set_page_config(
    page_title="GRIHAM-C: DEMO",
    page_icon="/content/drive/MyDrive/problem_statement_1_and_2/OIG.jpeg",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################

# CSS styling

st.markdown("""
<style>
[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

#######################

# Load data
with open('/content/drive/MyDrive/problem_statement_1_and_2/classification_report.json', 'r') as f:  #/content/drive/MyDrive/problem_statement_1_and_2/classification_report_hindi (2).json
     # Load JSON data from file
     json_cluster_dat = json.load(f)    # Your JSON data

cluster_df = json_cluster_dat

with open('/content/drive/MyDrive/problem_statement_1_and_2/CategoryCode_Mapping_v2.json', 'r') as c:
     # Load JSON data from file
     json_dat = json.load(c)    # Your JSON data

json_data = json_dat

#######################

#Initialize

sequence_to_classify = ""
summary = ""
trans = ""
org_code = ""
org_code_items = []
org_code_gri_id_items = []

result = {}
best_item_result = {}

#######################

# Sidebar
with st.sidebar:
    st.image('/content/drive/MyDrive/problem_statement_1_and_2/OIG.jpeg', width=200)
    st.title('GRIHAM-C: Demo')
    st.write('_This page is demo only.\nThe proposed trained model code can be viewed in GRIHAMC-ReportGen.ipynb, which is the backend_')

    for i in range(len(cluster_df)):
       if cluster_df[i]['org_code'] not in org_code_items and cluster_df[i]['grievance_id'] not in org_code_gri_id_items:
          org_code_items.append(cluster_df[i]['org_code'])

    selected_code = st.selectbox('Select an OrgCode', org_code_items)

    st.text("(And)")

    for i in range(len(cluster_df)):
        if cluster_df[i]['org_code'] == selected_code:
           org_code_gri_id_items.append(cluster_df[i]['grievance_id'])

    gr_id = st.selectbox('Select the Grievance Id', org_code_gri_id_items)

    if(st.button("Enter", key='orgid')):
      st.text(gr_id)
      for i in range(len(cluster_df)):
          if cluster_df[i]['grievance_id'] == gr_id:
             org_code = cluster_df[i]['org_code']
             sequence_to_classify = cluster_df[i]['grievance_text']
             result = cluster_df[i]['classification_result']
             best_item_result = cluster_df[i]['best_items_dict']
             summary = cluster_df[i]['summary_result']
             trans = cluster_df[i]['translated_text']
             break


#######################
    #lang_list = ["hi_IN", "ta_IN", "ml_IN" , "mr_IN", "bn_IN", "te_IN"]

    #selected_lang = st.selectbox('Select the language to be translated to Eng', lang_list)

    #gr_id="MEAPD/E/2023/0000002" #"GOVUP/E/2023/0000051" #"MEAPD/E/2023/0000002" #"CBODT/E/2023/0000001" #"MOLBR/E/2023/0000004" #"MORLY/E/2023/0000001" #"MOLBR/E/2023/0000003"
#######################

#Textbox for text input

st.title('GRIHAM- :blue[Clustering]')
st.subheader('_Grievance Hierarchical Analytics Monitoring_ :blue[Clustering]', divider='blue')
st.write('_Make sure classification_report.json file is generated and in path_')

text = sequence_to_classify

user_input = st.text_area("Grievance Text appears here:", value=text , key = 'before_classify')

col1, col2 = st.columns(2)

with col1:
    if st.button("Show Classification"):
       st.write("Generating classification!")
       st.write("Classification:")
       for i in range(len(cluster_df)):
          if cluster_df[i]['grievance_id'] == gr_id:
             result = cluster_df[i]['classification_result']

with col2:
    if st.button("Show Summary"):
       st.write("Generating Summary")
       for i in range(len(cluster_df)):
          if cluster_df[i]['grievance_id'] == gr_id:
             summary = cluster_df[i]['summary_result']


st.dataframe(data = result, use_container_width=True)  #append all the values in a json dic and then add values to create report
st.dataframe(data = best_item_result, use_container_width=True)
user_summary = st.text_area("Grievance Summary appears here:", summary, key = 'summary')
user_translation = st.text_area("Grievance translation (if any) appears here:", trans, key = 'translation')

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
org_code = selected_code


if st.button("Add to report"):
       existing_json_file_path = f'/content/classification_{org_code}_{current_date}.json'
       try:
          with open(existing_json_file_path, 'r') as file:
               final_update = json.load(file)
       except FileNotFoundError:
            final_update = []

       for i in range(len(cluster_df)):
           if cluster_df[i]['grievance_id'] == gr_id:
              final_update.append(cluster_df[i])

       with open(existing_json_file_path, 'w') as file:
            json.dump(final_update, file, indent=2)

       st.write("Classification added!")

if st.button("Generate Final report for the Org Code"):
       existing_json_file_path = f'/content/classification_{org_code}_{current_date}.json'
       new_csv_file_name = f'/content/classification_report_{org_code}_{current_date}.csv'

       with open(existing_json_file_path, 'r') as file:
               final_update = json.load(file)

       with open(new_csv_file_name, 'w', newline='') as file:
            fieldnames = ["grievance_id","org_code","grievance_text","classification_result",
                           "best_items_dict", "summary_result", "remarks_text", "translated_text"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(final_update)
       st.write("CSV file created Successfully!")

