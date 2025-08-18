import streamlit as st
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(
    page_title="Delivery Time Predictor",
    page_icon="⏱️",
    layout="wide"
)

# --- Sidebar Navigation ---
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("Go to", ["About Me"], index=0)

# --- Page Routing ---
if page == "About Me":
    st.title("👨‍💻 About Me")

    # Profile header
    st.markdown("""
    ### Yuono Dwi Raharjo
    **Data Science and Assessment Enthusiast**  
    📍 Yogyakarta, Indonesia | 📧 yuonodwiraharjo26@gmail.com  
    🔗 [LinkedIn](https://linkedin.com/in/yuonodraharjo) | 📱 +62 812-2706-8269
    """)

    # Professional Summary
    st.markdown("""
    ## Professional Summary
    Passionate Data and Research professional with an academic background in Psychology and extensive experience in psychometrics, 
    data analysis, and research development. Combines technical expertise with psychological insights to effectively 
    support data-driven decision-making in data science, psychometrics, and business.
    """)

    # Skills
    st.markdown("## 🛠 Technical Skills")

    skills_col1, skills_col2, skills_col3 = st.columns(3)

    with skills_col1:
        st.markdown("""
        **Data Analysis & Visualization**  
        • Python (Pandas, NumPy, SciPy)  
        • SQL (BigQuery, PostgreSQL)  
        • R, Jamovi, SPSS  
        • Power BI, Tableau  
        """)

    with skills_col2:
        st.markdown("""
        **Psychological Assessment**  
        • WAIS, CFIT, BDI, BAI  
        • 16PF, Projective Tests  
        • Test Development  
        • Psychometric Analysis  
        """)

    with skills_col3:
        st.markdown("""
        **Research & Analytics**  
        • Quantitative Research  
        • Market Research  
        • People Analytics  
        • SEM, Factor Analysis  
        """)

    # Education
    st.markdown("## 🎓 Education")

    edu_col1, edu_col2 = st.columns(2)

    with edu_col1:
        st.markdown("""
        **Bootcamp Data Science**  
        *Dibimbing.id | Feb 2025-Present*  
        • Score: 98/100  
        • Python, SQL, EDA  
        • Web Scraping, Marketing Analytics  
        """)

    with edu_col2:
        st.markdown("""
        **Bachelors in Psychology**  
        *Universitas Gadjah Mada | 2021-2025*  
        • GPA: 3.85/4.00  
        • Statistics, Research Methods  
        • Psychological Measurement  
        """)

    # Work Experience
    st.markdown("## 💼 Professional Experience")

    with st.expander("**Development Staff** at UPAP Psikologi UGM (Jan-Dec 2024)", expanded=True):
        st.markdown("""
        • Developed **100+ assessment items** for academic potential and situational judgment tests  
        • Managed **test digitalization** for CAT-based assessments (4,000+ items bank)  
        • Conducted **psychometric analysis** using Jamovi, R, and Winstep  
        • Authored **10 assessment manuals** for Hak Kekayaan Intelektual registration  
        • Organized **10+ training sessions** in statistics and psychometrics  
        """)

    with st.expander("**Technical Staff Intern** at Psimetrika Indonesia (Jul-Nov 2023)"):
        st.markdown("""
        • Developed **12 cognitive test items** on digital ethics for government officials  
        • Performed **Classical Test Theory analysis** using R  
        • Conducted **Confirmatory Factor Analysis** for instrument validation  
        • Created **scoring reports** and analysis templates  
        """)
    

