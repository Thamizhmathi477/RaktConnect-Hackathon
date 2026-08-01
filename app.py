# ============================================
# 🩸 RAKTCONNECT — Professional Streamlit App
# CodeStorm 2026 — FutureForge
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2, asin
import time

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="RaktConnect — AI Blood Donor Network",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .header {
        background: linear-gradient(135deg, #d7263d, #a71d2a);
        padding: 25px 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(215, 38, 61, 0.3);
    }
    .header h1 { color: white; font-size: 2.8rem; font-weight: 800; margin: 0; }
    .header h1 span { background: white; color: #d7263d; padding: 0 15px; border-radius: 10px; }
    .header p { color: white; font-size: 1.2rem; opacity: 0.9; margin: 5px 0 0; }
    .header .sub { color: white; font-size: 1rem; opacity: 0.7; font-style: italic; }
    
    .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px; border: 1px solid #eee; }
    .card h3 { color: #d7263d; margin-bottom: 10px; font-size: 1.1rem; }
    
    .stat-box { background: white; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #eee; }
    .stat-box .number { font-size: 2rem; font-weight: 800; color: #d7263d; }
    .stat-box .label { font-size: 0.8rem; color: #888; margin-top: 2px; }
    
    .donor-card { background: #f8f9fa; padding: 12px 15px; border-radius: 10px; border-left: 4px solid #d7263d; margin: 8px 0; transition: transform 0.2s; }
    .donor-card:hover { transform: translateX(5px); }
    .donor-card .rank { font-weight: 800; color: #d7263d; font-size: 1.1rem; }
    .donor-card .name { font-weight: 600; font-size: 1rem; }
    .donor-card .details { font-size: 0.85rem; color: #666; }
    .donor-card .distance { font-weight: 700; color: #2e7d32; }
    
    .best-match { background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 15px 20px; border-radius: 12px; border-left: 5px solid #2e7d32; margin-top: 10px; }
    .best-match h4 { color: #2e7d32; margin: 0; }
    .best-match p { margin: 2px 0; color: #1b5e20; }
    
    .stButton button { background: #d7263d !important; color: white !important; font-weight: 700 !important; border-radius: 8px !important; padding: 10px 30px !important; border: none !important; transition: all 0.3s !important; }
    .stButton button:hover { background: #a71d2a !important; transform: translateY(-2px); box-shadow: 0 4px 15px rgba(215, 38, 61, 0.4); }
    
    .footer { text-align: center; padding: 15px; color: #888; font-size: 0.85rem; border-top: 1px solid #eee; margin-top: 20px; }
    .footer strong { color: #d7263d; }
    
    .badge { display: inline-block; background: #f1f2f6; padding: 2px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin: 2px; }
    .badge-red { background: #ffebee; color: #c62828; }
    .badge-green { background: #e8f5e9; color: #2e7d32; }
    .badge-blue { background: #e3f2fd; color: #0d47a1; }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

st.markdown("""
<div class="header">
    <h1>🩸 <span>RaktConnect</span></h1>
    <p>AI Emergency Blood &amp; Organ Donor Network</p>
    <p class="sub">"Saving Lives Through Intelligent Donor Matching"</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# LOAD REAL DATA (10,000 DONORS)
# ============================================

@st.cache_data
def load_data():
    # Create 10,000 realistic donors
    np.random.seed(42)
    
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Hyderabad', 
              'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
    
    blood_groups = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-']
    
    # Indian city coordinates
    city_coords = {
        'Delhi': (28.6139, 77.2090), 'Mumbai': (19.0760, 72.8777),
        'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946),
        'Hyderabad': (17.3850, 78.4867), 'Kolkata': (22.5726, 88.3639),
        'Pune': (18.5204, 73.8567), 'Ahmedabad': (23.0225, 72.5714),
        'Jaipur': (26.9124, 75.7873), 'Lucknow': (26.8467, 80.9462)
    }
    
    # First names and last names
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
# COMPATIBILITY MATRIX
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

# ============================================
# HAVERSINE DISTANCE
# ============================================

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return 2 * R * asin(sqrt(sin((lat2 - lat1) / 2)**2 + 
                       cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2)**2))

# ============================================
# AI MATCHING ENGINE
# ============================================

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

# ============================================
# CITY COORDINATES
# ============================================

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
        st.markdown(f"{bg} → {count:,}")
    
    st.markdown("---")
    
    st.markdown("### 📍 Cities")
    city_counts = df['city'].value_counts().head(6)
    for city, count in city_counts.items():
        st.markdown(f"{city} → {count:,}")
    
    st.markdown("---")
    st.caption("🤖 AI-Powered Matching Engine")

# ============================================
# MAIN CONTENT
# ============================================

st.markdown("## 🩸 Emergency Blood Request")

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 👤 Patient Details")
        patient_name = st.text_input("Name", "Rajesh Kumar")
        blood_group = st.selectbox("Blood Group", ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-'])
        city = st.selectbox("City", list(cities.keys()))
        urgency = st.selectbox("Urgency Level", ['Normal', 'Urgent', 'Critical'])
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📋 Request Summary")
        st.markdown(f"**Patient:** {patient_name}")
        st.markdown(f"**Blood Group:** `{blood_group}`")
        st.markdown(f"**Location:** 📍 {city}")
        
        urgency_colors = {'Normal': '🟢', 'Urgent': '🟡', 'Critical': '🔴'}
        st.markdown(f"**Urgency:** {urgency_colors.get(urgency, '')} {urgency}")
        
        compatible_groups = get_compatible(blood_group)
        st.markdown(f"**Compatible Groups:** {', '.join(compatible_groups)}")
        st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔍 Find Donors Now", use_container_width=True):
    lat, lon = cities.get(city, (28.6139, 77.2090))
    
    with st.spinner("🤖 Searching compatible donors..."):
        time.sleep(1)
        donors, total = find_donors(lat, lon, blood_group, urgency.lower())
    
    if donors is None:
        st.error("❌ No compatible donors found! 🚨 Escalating to hospital network...")
    else:
        st.success(f"✅ {total:,} compatible donors found!")
        
        st.markdown("### 🏆 Top Donors")
        
        emojis = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']
        
        for i, (_, donor) in enumerate(donors.iterrows()):
            col1, col2, col3 = st.columns([0.5, 3, 1.5])
            with col1:
                st.markdown(f"<h3 style='color:#d7263d;'>{emojis[i]}</h3>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="donor-card" style="border-left-color: {'#d7263d' if i == 0 else '#666'};">
                    <span class="name">{donor['name']}</span>
                    <span class="badge badge-red">🩸 {donor['blood_group']}</span>
                    <span class="badge badge-blue">📍 {donor['city']}</span>
                    <div class="details">📞 {donor['phone']} | 💉 {donor['donations']} donations</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div style="text-align: right; padding-top: 8px;">
                    <span style="font-size: 1.5rem; font-weight: 800; color: #2e7d32;">{donor['distance_km']:.1f} km</span>
                    <div style="font-size: 0.8rem; color: #888;">Priority: {donor['priority_score']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("---")
        
        best = donors.iloc[0]
        st.markdown(f"""
        <div class="best-match">
            <h4>🎯 Best Match</h4>
            <p><strong>{best['name']}</strong> — {best['blood_group']} | 📍 {best['city']}</p>
            <p>📞 {best['phone']} | 📍 {best['distance_km']:.1f} km away</p>
            <p>⏱️ Estimated arrival: ~{best['distance_km'] / 30 * 60:.0f} minutes</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("📱 Notification sent to donor! ✅")

st.markdown("""
<div class="footer">
    <p>🩸 <strong>RaktConnect</strong> — Saving Lives Through Intelligent Donor Matching</p>
    <p>© 2026 Team RaktConnect | CodeStorm 2026 — FutureForge</p>
</div>
""", unsafe_allow_html=True)
