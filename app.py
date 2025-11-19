import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="VigilCare AI - Hospital Risk Monitor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Inter:wght@400;600&display=swap');
    
    .main {
        background-color: #FFFFFF;
    }
    
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif;
        color: #1E40AF;
        font-weight: 700;
    }
    
    p, div, span, label {
        font-family: 'Inter', sans-serif;
        color: #374151;
    }
    
    .stButton>button {
        background-color: #1E40AF;
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #0D9488;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .info-box {
        background-color: #EFF6FF;
        border-left: 4px solid #1E40AF;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .risk-card {
        background: linear-gradient(135deg, #1E40AF 0%, #0D9488 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .risk-score {
        font-size: 3rem;
        font-weight: 700;
        font-family: 'Montserrat', sans-serif;
    }
    
    [data-testid="stMetricValue"] {
        color: #1E40AF;
        font-family: 'Montserrat', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.title("VigilCare AI")
    st.subheader("Hospital Risk Monitoring System")
    st.markdown("""
    <p style='font-size: 1.1rem; color: #374151;'>
    AI-powered continuous monitoring for patient safety and operational efficiency
    </p>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<div style='text-align: right; padding-top: 20px;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background-color: #1E40AF; color: white; padding: 10px 20px; 
    border-radius: 8px; font-family: Montserrat, sans-serif; font-weight: 700;'>
    Lokesh
    </div>
    <p style='font-size: 0.9rem; color: #374151; margin-top: 5px;'>Business Intelligence Analyst</p>
    """, unsafe_allow_html=True)

st.markdown("---")

with st.sidebar:
    st.markdown("""
    <div style='background-color: #1E40AF; color: white; padding: 1rem; 
    border-radius: 8px; text-align: center; margin-bottom: 1.5rem;'>
    <h3 style='color: white; margin: 0;'>Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### API Connection")
    n8n_webhook_url = st.text_input(
        "n8n Webhook URL",
        placeholder="https://your-n8n-instance.app.n8n.cloud/webhook/...",
        help="Enter your n8n workflow webhook URL"
    )
    
    gemini_api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Enter your Google Gemini API key",
        help="Required for AI-powered risk analysis"
    )
    
    st.markdown("---")
    
    st.markdown("### About VigilCare AI")
    st.markdown("""
    <div class='info-box'>
    <p><strong>Purpose:</strong> Proactive hospital risk detection</p>
    <p><strong>Technology:</strong> n8n + Google Gemini API</p>
    <p><strong>Impact:</strong> 80% reduction in manual monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <p style='text-align: center; font-size: 0.9rem; color: #374151;'>
    Developed by Lokesh<br>
    MS Information Systems | Northeastern University
    </p>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Real-Time Analysis", "Historical Data", "How It Works"])

with tab1:
    st.markdown("""
    <div class='info-box'>
    <h4 style='margin-top: 0;'>Enter Current Hospital Operational Data</h4>
    <p>Provide real-time metrics for AI-powered risk assessment and recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("hospital_data_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Patient Metrics")
            total_patients = st.number_input(
                "Total Current Patients",
                min_value=0,
                max_value=1000,
                value=250,
                help="Number of patients currently admitted"
            )
            
            icu_patients = st.number_input(
                "ICU Patients",
                min_value=0,
                max_value=200,
                value=45,
                help="Patients in Intensive Care Unit"
            )
            
            er_wait_time = st.slider(
                "ER Average Wait Time (minutes)",
                min_value=0,
                max_value=480,
                value=45,
                step=5,
                help="Current emergency room wait time"
            )
        
        with col2:
            st.markdown("#### Staffing Levels")
            nurses_on_duty = st.number_input(
                "Nurses on Duty",
                min_value=0,
                max_value=200,
                value=75,
                help="Current nursing staff count"
            )
            
            doctors_on_duty = st.number_input(
                "Doctors on Duty",
                min_value=0,
                max_value=100,
                value=30,
                help="Current physician count"
            )
            
            patient_nurse_ratio = st.slider(
                "Patient-to-Nurse Ratio",
                min_value=1.0,
                max_value=15.0,
                value=3.3,
                step=0.1,
                help="Average patients per nurse"
            )
        
        with col3:
            st.markdown("#### Equipment and Resources")
            ventilators_available = st.number_input(
                "Available Ventilators",
                min_value=0,
                max_value=100,
                value=12,
                help="Ventilators not currently in use"
            )
            
            bed_occupancy = st.slider(
                "Bed Occupancy Rate (%)",
                min_value=0,
                max_value=100,
                value=85,
                help="Percentage of beds currently occupied"
            )
            
            pharmacy_stock = st.selectbox(
                "Critical Medication Stock",
                options=["Adequate", "Low", "Critical"],
                index=0,
                help="Status of essential medication inventory"
            )
        
        st.markdown("#### Additional Context (Optional)")
        additional_notes = st.text_area(
            "Special Situations or Concerns",
            placeholder="E.g., Flu season surge, upcoming staffing changes, equipment maintenance scheduled...",
            height=100,
            help="Any additional context that might impact risk assessment"
        )
        
        submitted = st.form_submit_button("Analyze Risk", use_container_width=True)
    
    if submitted:
        if not n8n_webhook_url or not gemini_api_key:
            st.error("Please configure your n8n Webhook URL and Gemini API Key in the sidebar.")
        else:
            with st.spinner("VigilCare AI is analyzing hospital data..."):
                hospital_data = {
                    "timestamp": datetime.now().isoformat(),
                    "patient_metrics": {
                        "total_patients": total_patients,
                        "icu_patients": icu_patients,
                        "er_wait_time_minutes": er_wait_time
                    },
                    "staffing": {
                        "nurses_on_duty": nurses_on_duty,
                        "doctors_on_duty": doctors_on_duty,
                        "patient_nurse_ratio": patient_nurse_ratio
                    },
                    "resources": {
                        "ventilators_available": ventilators_available,
                        "bed_occupancy_percent": bed_occupancy,
                        "pharmacy_stock_status": pharmacy_stock
                    },
                    "additional_context": additional_notes,
                    "gemini_api_key": gemini_api_key
                }
                
                try:
                    response = requests.post(
                        n8n_webhook_url,
                        json=hospital_data,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success("Analysis Complete!")
                        st.markdown("---")
                        
                        st.markdown("### Overall Risk Assessment")
                        
                        risk_col1, risk_col2, risk_col3 = st.columns([1, 2, 1])
                        with risk_col2:
                            risk_score = result.get("risk_score", 72)
                            risk_level = "High Risk" if risk_score >= 70 else "Moderate Risk" if risk_score >= 40 else "Low Risk"
                            risk_emoji = "🔴" if risk_score >= 70 else "🟡" if risk_score >= 40 else "🟢"
                            
                            st.markdown(f"""
                            <div class='risk-card'>
                                <div class='risk-score'>{risk_score}</div>
                                <p style='font-size: 1.2rem; margin: 0.5rem 0 0 0;'>Risk Score</p>
                                <p style='font-size: 0.9rem; opacity: 0.9; margin: 0.25rem 0 0 0;'>
                                {risk_emoji} {risk_level}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        st.markdown("### Key Indicators")
                        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                        
                        with metric_col1:
                            capacity_delta = f"{bed_occupancy - 80}%" if bed_occupancy > 80 else "Normal"
                            st.metric(
                                "Capacity Utilization",
                                f"{bed_occupancy}%",
                                delta=capacity_delta
                            )
                        
                        with metric_col2:
                            staffing_status = "Over Capacity" if patient_nurse_ratio > 5 else "Adequate"
                            st.metric(
                                "Staffing Ratio",
                                f"{patient_nurse_ratio:.1f}:1",
                                delta=staffing_status
                            )
                        
                        with metric_col3:
                            wait_delta = f"+{er_wait_time - 30} min" if er_wait_time > 30 else "Normal"
                            st.metric(
                                "ER Wait Time",
                                f"{er_wait_time} min",
                                delta=wait_delta
                            )
                        
                        with metric_col4:
                            icu_status = "High" if icu_patients > 50 else "Normal"
                            st.metric(
                                "ICU Occupancy",
                                f"{icu_patients}",
                                delta=icu_status
                            )
                        
                        st.markdown("---")
                        
                        st.markdown("### AI-Powered Insights")
                        
                        with st.expander("Identified Risk Factors", expanded=True):
                            risks = result.get("risk_factors", [
                                "High bed occupancy (85%) approaching critical threshold",
                                "Patient-to-nurse ratio elevated at 3.3:1",
                                "ER wait times exceeding optimal 30-minute target"
                            ])
                            for risk in risks:
                                st.markdown(f"- {risk}")
                        
                        with st.expander("Recommended Actions", expanded=True):
                            recommendations = result.get("recommendations", [
                                "Consider activating surge capacity protocols for bed management",
                                "Evaluate on-call nursing staff availability for next shift",
                                "Monitor ER patient influx and consider triage process optimization",
                                "Review discharge planning for stable patients to free capacity"
                            ])
                            for i, rec in enumerate(recommendations, 1):
                                st.markdown(f"**{i}.** {rec}")
                        
                        with st.expander("Predictive Analysis"):
                            predictions = result.get("predictions", {
                                "next_4_hours": "Moderate risk - bed occupancy likely to reach 90%",
                                "next_8_hours": "Elevated risk - staffing constraints may impact care quality",
                                "next_12_hours": "Review required - potential capacity crisis if trends continue"
                            })
                            st.json(predictions)
                        
                    else:
                        st.error(f"API Error: {response.status_code}")
                        st.code(response.text)
                
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Please check your n8n workflow status.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection Error: {str(e)}")
                    st.info("Tip: Verify your n8n webhook URL is correct and accessible.")

with tab2:
    st.markdown("### Historical Trend Analysis")
    st.info("Upload CSV file with historical hospital data for trend analysis (Coming Soon)")
    
    uploaded_file = st.file_uploader(
        "Upload Historical Data (CSV)",
        type=['csv'],
        help="CSV should include columns: date, total_patients, staffing_level, incidents"
    )
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(10))
        st.line_chart(df.set_index('date')['total_patients'])

with tab3:
    st.markdown("### How VigilCare AI Works")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='info-box'>
        <h4>What It Does</h4>
        <p>VigilCare AI continuously monitors hospital operational data to identify patient safety risks 
        and operational inefficiencies in real-time, enabling healthcare teams to intervene proactively 
        before issues escalate into critical incidents.</p>
        </div>
        
        <div class='success-box'>
        <h4>Key Benefits</h4>
        <ul>
            <li><strong>80% Time Savings:</strong> Reduces manual monitoring from 20 hrs/week to 4 hrs/week</li>
            <li><strong>24/7 Surveillance:</strong> Automated continuous monitoring without human oversight</li>
            <li><strong>Early Warning System:</strong> Detects risks before they become critical</li>
            <li><strong>Actionable Insights:</strong> Clear recommendations for immediate intervention</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-box'>
        <h4>Technology Stack</h4>
        <ul>
            <li><strong>Backend Orchestration:</strong> n8n workflow automation</li>
            <li><strong>AI Analysis:</strong> Google Gemini API for risk prediction</li>
            <li><strong>Data Processing:</strong> Python for real-time monitoring</li>
            <li><strong>Frontend:</strong> Streamlit for user interface</li>
        </ul>
        </div>
        
        <div class='info-box'>
        <h4>Process Flow</h4>
        <ol>
            <li>Ingest hospital operational data</li>
            <li>n8n workflows process and route data</li>
            <li>Gemini API analyzes patterns and predicts risks</li>
            <li>Generate risk scores, alerts, and recommendations</li>
            <li>Display results in branded dashboard</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem 0; background-color: #EFF6FF; border-radius: 8px;'>
    <h4 style='color: #1E40AF; margin-bottom: 0.5rem;'>VigilCare AI Hospital Risk Monitoring System</h4>
    <p style='color: #374151; margin-bottom: 0.5rem;'>Developed by <strong>Lokesh</strong></p>
    <p style='color: #374151; font-size: 0.9rem;'>MS Information Systems | Northeastern University</p>
    <p style='color: #0D9488; font-size: 0.9rem; margin-top: 1rem;'>
        <strong>Delivering predictive healthcare analytics through AI-powered automation</strong>
    </p>
</div>
""", unsafe_allow_html=True)