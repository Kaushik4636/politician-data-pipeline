import streamlit as st
import pandas as pd
from pipeline import run_pipeline

st.set_page_config(page_title="Political Intelligence", layout="wide")

st.title("🏛️ Political Data Pipeline")
st.markdown("Upload your messy CSV to clean, impute, and score data automatically.")

uploaded_file = st.file_uploader("Upload Raw CSV Dataset", type="csv")

if uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file)
    
    with st.spinner('🚀 Processing data...'):
        # This calls the code in pipeline.py
        clean_df = run_pipeline(raw_df)
    
    st.success("Pipeline executed successfully!")

    # Tabs
    tab1, tab2 = st.tabs(["📋 Processed Data", "📊 Performance Rankings"])
    
    with tab1:
        st.dataframe(clean_df, use_container_width=True)
        csv = clean_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Clean CSV", data=csv, file_name="cleaned_politician_data.csv")

    with tab2:
        st.subheader("Top Performers")
        top_10 = clean_df.nlargest(10, 'performance_score')[['name', 'party', 'performance_score']]
        st.table(top_10)