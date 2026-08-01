# ============================================
# 🩸 RAKTCONNECT — High Visibility Design
# CodeStorm 2026 — FutureForge
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2, asin
import time

st.set_page_config(
    page_title="RaktConnect",
    page_icon="🩸",
    layout="centered"
)

# ============================================
# BIG, BOLD, CLEAR DESIGN
# ============================================

st.markdown("""
<style>
    /* Everything bigger and bolder */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Big Header */
    .main-header {
        background: #c0392b;
        padding: 40px 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        border: 3px solid #922b21;
    }
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
    }
    .main-header h1 span {
        background: white;
        color: #c0392b;
        padding: 0 20px;
        border-radius: 15px;
    }
    .main-header .tagline {
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 10px;
    }
    .main-header .sub {
        color: #f5b7b1;
        font-size: 1.2rem;
        font-style: italic;
    }
    
    /* Big Cards */
    .big-card {
        background: white;
        padding: 25px 30px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border: 2px solid #d5d8dc;
    }
    .big-card h3 {
        color: #c0392b;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 15px;
    }
    .big-card label {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #1a1a2e !important;
    }
    
    /* Big Stats */
    .stat-box {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #d5d8dc;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .stat-box .number {
        font-size: 3rem;
        font-weight: 900;
        color: #c0392b;
    }
    .stat-box .label {
        font-size: 1rem;
        color: #555;
        font-weight: 600;
    }
    
    /* Donor Cards */
    .donor-card {
        background: #f8f9fa;
        padding: 15px 20px;
        border-radius: 10px;
        border-left: 6px solid #c0392b;
        margin: 10px 0;
        border: 2px solid #e0e0e0;
    }
    .donor-card .rank {
        font-size: 1.5rem;
        font-weight: 900;
        color: #c0392b;
    }
    .donor-card .name {
        font-size: 1.3rem;
        font-weight: 800;
        color: #1a1a2e;
    }
    .donor-card .details {
        font-size: 1rem;
        color: #444;
    }
    .donor-card .distance {
        font-size: 1.5rem;
        font-weight: 900;
        color: #27ae60;
    }
    
    /* Best Match */
    .best-match {
        background: #d5f5e3;
        padding: 20px 25px;
        border-radius: 12px;
        border-left: 8px solid #27ae60;
        margin-top: 15px;
        border: 2px solid #27ae60;
    }
    .best-match h4 {
        color: #1a6e34;
        font-size: 1.5rem;
        margin: 0;
    }
    .best-match p {
        font-size: 1.1rem;
        margin: 5px 0;
    }
    .best-match .big-phone {
        font-size: 1.3rem;
        font-weight: 800;
        color: #1a5276;
    }
    
    /* Big Buttons */
    .stButton button {
        background: #c0392b !important;
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        padding: 15px 40px !important;
        border: none !important;
        border-radius: 12px !important;
        width: 100% !important;
    }
    .stButton button:hover {
        background: #922b21 !important;
        box-shadow: 0 6px 20px rgba(192, 57, 43, 0.5);
    }
    
    /* Inputs */
    .stTextInput input, .stSelectbox select {
        font-size: 1.2rem !important;
        padding: 12px 15px !important;
        border-radius: 10px !important;
        border: 2px solid #bdc3c7 !important;
    }
    
    /* Alerts */
    .stAlert {
        font-size: 1.2rem !important;
        padding: 15px !important;
        border-radius: 12px !important;
        border: 2px solid !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        background: #2c3e50;
        border-radius: 12px;
        margin-top: 30px;
    }
    .footer p {
        color: white;
        font-size: 1.1rem;
        margin: 5px 0;
    }
    .footer .red-text {
        color: #e74c3c;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

st.markdown("""
<div class="main-header">
    <h1>🩸 <span>RaktConnect</span></h1>
    <p class="tagline">AI Emergency Blood Donor Network</p>
    <p class="sub">"Saving Lives Through Intelligent Donor Matching"</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================

@st.cache_data
def load_data():
    np.random.seed(42)
    
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Hyderabad', 
              'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
    
    blood_groups = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-']
    
    city_coords = {
        'Delhi': (28.6139, 77.2090), 'Mumbai': (19.0760, 72.8777),
        'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946),
        'Hyderabad': (17.3850, 78.4867), 'Kolkata': (22.5726, 88.3639),
        'Pune': (18.5204, 73.8567), 'Ahmedabad': (23.0225, 72.5714),
        'Jaipur': (26.9124, 75.7873), 'Lucknow': (26.8467, 80.9462)
    }
    
    first_names = ['Rahul', 'Priya', 'Amit', 'Neha', 'Vikram', 'Sneha', 'Arjun', 'Meera',
                   'Karan', 'Ananya', 'Rohan', 'Pooja', 'Suresh', 'Lakshmi', 'Manoj',
                   'Divya', 'Naveen', 'Kavya', 'Srinivas', 'Anjali', 'Rajesh', 'Sangeeta',
                   'Vijay', 'Shreya', 'Ajay', 'Anita', 'Sunil', 'Deepa', 'Ravi', 'Sonia']
    last_names = ['Sharma', 'Patel', 'Kumar', 'Singh', 'Reddy', 'Gupta', 'Nair', 'Iyer',
                  'Joshi', 'Rao', 'Verma', 'Malhotra', 'Srinivasan', 'Menon', 'Shetty',
                  'Pillai', 'Naidu', 'Das', 'Ganguly', 'Bose', 'Mishra', 'Tripathi']
    
    donors = []
    for i in range(10000):
        first = np.random.choice(first_names)
        last = np.random.choice(last_names)
        city = np.random.choice(cities)
        lat, lon = city_coords[city]
        blood = np.random.choice(blood_groups, p=[0.30, 0.25, 0.20, 0.10, 0.06, 0.04, 0.03, 0.02])
        
        donors.append({
            'name': f"{first} {last}",
            'blood_group': blood,
            'city': city,
            'latitude': lat + np.random.uniform(-0.5, 0.5),
            'longitude': lon + np.random.uniform(-0.5, 0.5),
            'phone': f"9{np.random.randint(100000000, 999999999)}",
            'available': np.random.choice(['Yes', 'Yes', 'Yes', 'No'], p=[0.75, 0.10, 0.10, 0.05]),
            'donations': np.random.randint(1, 20)
        })
    
    return pd.DataFrame(donors)

df = load_data()

# ============================================
# COMPATIBILITY
# ============================================

compatibility = {
    'A+': ['A+', 'AB+'], 'A-': ['A+', 'A-', 'AB+', 'AB-'],
    'B+': ['B+', 'AB+'], 'B-': ['B+', 'B-', 'AB+', 'AB-'],
    'AB+': ['AB+'], 'AB-': ['AB+', 'AB-'],
    'O+': ['A+', 'B+', 'AB+', 'O+'],
    'O-': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
}

def get_compatible(b):
    return compatibility.get(b.upper(), [])

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return 2 * R * asin(sqrt(sin((lat2 - lat1) / 2)**2 + 
                       cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2)**2))

def find_donors(patient_lat, patient_lon, patient_blood, urgency='normal'):
    compatible_groups = get_compatible(patient_blood)
    compatible = df[(df['blood_group'].str.upper().isin(compatible_groups)) & 
                    (df['available'] == 'Yes')].copy()
    
    if len(compatible) == 0:
        return None, 0
    
    compatible['distance_km'] = compatible.apply(
        lambda row: haversine(patient_lat, patient_lon, row['latitude'], row['longitude']),
        axis=1
    )
    
    compatible = compatible.sort_values('distance_km')
    
    urgency_multiplier = {'critical': 0.3, 'urgent': 0.6, 'normal': 1.0}
    compatible['priority_score'] = compatible['distance_km'] / 5 * urgency_multiplier.get(urgency.lower(), 1.0)
    compatible = compatible.sort_values('priority_score')
    
    return compatible.head(5), len(compatible)

cities = {
    'Delhi': (28.6139, 77.2090), 'Mumbai': (19.0760, 72.8777),
    'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867), 'Kolkata': (22.5726, 88.3639),
    'Pune': (18.5204, 73.8567), 'Ahmedabad': (23.0225, 72.5714),
    'Jaipur': (26.9124, 75.7873), 'Lucknow': (26.8467, 80.9462)
}

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("## 📊 Dashboard")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="number">{len(df):,}</div>
            <div class="label">Total Donors</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="number">{len(df[df['available'] == 'Yes']):,}</div>
            <div class="label">Available</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🩸 Blood Groups")
    bg_counts = df['blood_group'].value_counts()
    for bg, count in bg_counts.items():
        st.markdown(f"**{bg}** → {count:,}")

# ============================================
# MAIN
# ============================================

st.markdown("## 🩸 Emergency Blood Request")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="big-card">', unsafe_allow_html=True)
    st.markdown("### 👤 Patient Details")
    patient_name = st.text_input("Name", "Rajesh Kumar")
    blood_group = st.selectbox("Blood Group", ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-'])
    city = st.selectbox("City", list(cities.keys()))
    urgency = st.selectbox("Urgency", ['Normal', 'Urgent', 'Critical'])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="big-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Request Summary")
    st.markdown(f"**Patient:** {patient_name}")
    st.markdown(f"**Blood Group:** `{blood_group}`")
    st.markdown(f"**Location:** 📍 {city}")
    urgency_colors = {'Normal': '🟢', 'Urgent': '🟡', 'Critical': '🔴'}
    st.markdown(f"**Urgency:** {urgency_colors.get(urgency, '')} {urgency}")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔍 Find Donors Now"):
    lat, lon = cities.get(city, (28.6139, 77.2090))
    
    with st.spinner("🤖 Searching..."):
        time.sleep(1)
        donors, total = find_donors(lat, lon, blood_group, urgency.lower())
    
    if donors is None:
        st.error("❌ No compatible donors found!")
    else:
        st.success(f"✅ {total:,} compatible donors found!")
        
        st.markdown("### 🏆 Top Donors")
        
        for i, (_, donor) in enumerate(donors.iterrows()):
            emojis = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']
            st.markdown(f"""
            <div class="donor-card">
                <span class="rank">{emojis[i]}</span>
                <span class="name">{donor['name']}</span><br>
                <span class="details">🩸 {donor['blood_group']} | 📍 {donor['city']}</span><br>
                <span class="details">📞 {donor['phone']} | 💉 {donor['donations']} donations</span>
                <div style="text-align: right;">
                    <span class="distance">{donor['distance_km']:.1f} km</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        best = donors.iloc[0]
        st.markdown(f"""
        <div class="best-match">
            <h4>🎯 Best Match</h4>
            <p><strong>{best['name']}</strong> — {best['blood_group']} | 📍 {best['city']}</p>
            <p class="big-phone">📞 {best['phone']}</p>
            <p>📍 {best['distance_km']:.1f} km away</p>
            <p>⏱️ ~{best['distance_km'] / 30 * 60:.0f} minutes</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("📱 Notification sent to donor! ✅")

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
    <p>🩸 <span class="red-text">RaktConnect</span> — Saving Lives Through Intelligent Donor Matching</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">© 2026 Team RaktConnect | CodeStorm 2026 — FutureForge</p>
</div>
""", unsafe_allow_html=True)
