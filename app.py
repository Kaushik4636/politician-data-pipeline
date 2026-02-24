import streamlit as st
import pandas as pd
from pipeline import run_pipeline

# Page Config
st.set_page_config(page_title="Politician Data Intelligence", layout="wide")

# Custom CSS for high-end minimal style
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ Political Data Pipeline")
st.subheader("Automated Cleaning, Imputation, and Performance Scoring")

uploaded_file = st.file_uploader("Upload Messy Politician Dataset (CSV)", type="csv")

if uploaded_file is not None:
    # Load Raw Data
    raw_df = pd.read_csv(uploaded_file)
    
    with st.spinner('⚡ Executing cleaning pipeline...'):
        # Run the Pipeline
        clean_df = run_pipeline(raw_df)
    
    st.success("Pipeline Execution Complete!")

    # Top Level Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Avg Approval", f"{clean_df['approval_rating'].mean():.1f}%")
    m2.metric("Avg Score", f"{clean_df['performance_score'].mean():.2f}")
    m3.metric("Total Profiles", len(clean_df))
    m4.metric("States Covered", clean_df['state'].nunique())

    # Data Tabs
    tab1, tab2 = st.tabs(["📋 Cleaned Dataset", "📊 Key Insights"])
    
    with tab1:
        st.dataframe(clean_df, use_container_width=True)
        
        # Download Action
        csv = clean_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Clean CSV",
            data=csv,
            file_name="cleaned_politician_data.csv",
            mime="text/csv",
        )

    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Top 5 Performers**")
            st.table(clean_df.nlargest(5, 'performance_score')[['name', 'party', 'performance_score']])
        with col_b:
            st.write("**Party Distribution**")
            st.bar_chart(clean_df['party'].value_counts())