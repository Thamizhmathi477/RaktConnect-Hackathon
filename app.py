# ============================================
# 🩸 RAKTCONNECT — Complete App
# CodeStorm 2026 — FutureForge
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2, asin
import time
import random
from datetime import datetime

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
# CUSTOM CSS — DARK TEXT ON LIGHT BACKGROUND
# ============================================

st.markdown("""
<style>
    /* All text is dark on light background */
    .stApp {
        background-color: #f5f7fa;
    }
    
    /* Header — Dark text on red background */
    .main-header {
        background: #c0392b;
        padding: 30px 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        border: 3px solid #922b21;
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
    }
    .main-header h1 span {
        background: #ffffff;
        color: #c0392b;
        padding: 0 20px;
        border-radius: 15px;
    }
    .main-header .tagline {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 8px;
    }
    .main-header .sub {
        color: #f5b7b1;
        font-size: 1.1rem;
        font-style: italic;
    }
    
    /* Cards — White background, dark text */
    .big-card {
        background: #ffffff;
        padding: 22px 25px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 18px;
        border: 1px solid #e0e0e0;
    }
    .big-card h3 {
        color: #c0392b;
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 12px;
    }
    .big-card label {
        color: #1a1a2e !important;
        font-weight: 700 !important;
    }
    .big-card p, .big-card div {
        color: #1a1a2e;
    }
    
    /* Stats */
    .stat-box {
        background: #ffffff;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .stat-box .number {
        font-size: 2.5rem;
        font-weight: 900;
        color: #c0392b;
    }
    .stat-box .label {
        font-size: 0.9rem;
        color: #555;
        font-weight: 600;
    }
    
    /* Donor Cards — Light background, dark text */
    .donor-card {
        background: #f8f9fa;
        padding: 15px 20px;
        border-radius: 10px;
        border-left: 6px solid #c0392b;
        margin: 10px 0;
        border: 1px solid #e0e0e0;
    }
    .donor-card .rank {
        font-size: 1.3rem;
        font-weight: 900;
        color: #c0392b;
    }
    .donor-card .name {
        font-size: 1.2rem;
        font-weight: 800;
        color: #1a1a2e;
    }
    .donor-card .details {
        font-size: 0.95rem;
        color: #333;
    }
    .donor-card .distance {
        font-size: 1.3rem;
        font-weight: 900;
        color: #27ae60;
    }
    
    /* WhatsApp Button */
    .whatsapp-btn {
        display: inline-block;
        background: #25D366;
        color: white !important;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .whatsapp-btn:hover {
        background: #1da851;
    }
    
    /* Best Match */
    .best-match {
        background: #d5f5e3;
        padding: 18px 22px;
        border-radius: 12px;
        border-left: 8px solid #27ae60;
        margin-top: 12px;
        border: 2px solid #27ae60;
    }
    .best-match h4 {
        color: #1a6e34;
        font-size: 1.3rem;
        margin: 0;
    }
    .best-match p {
        color: #1a4a2a;
        font-size: 1rem;
        margin: 4px 0;
    }
    .best-match .big-phone {
        font-size: 1.2rem;
        font-weight: 800;
        color: #1a5276;
    }
    
    /* Buttons */
    .stButton button {
        background: #c0392b !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        padding: 12px 35px !important;
        border: none !important;
        border-radius: 10px !important;
        width: 100% !important;
    }
    .stButton button:hover {
        background: #922b21 !important;
        box-shadow: 0 4px 15px rgba(192, 57, 43, 0.4);
    }
    
    /* Inputs — Dark text */
    .stTextInput input, .stSelectbox select {
        color: #1a1a2e !important;
        font-size: 1.1rem !important;
        padding: 10px 15px !important;
        border-radius: 8px !important;
        border: 2px solid #d5d8dc !important;
        background: #ffffff !important;
    }
    .stTextInput input::placeholder {
        color: #888 !important;
    }
    
    /* Alerts */
    .stAlert {
        font-size: 1.1rem !important;
        padding: 14px !important;
        border-radius: 10px !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f0f2f6;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 18px;
        background: #2c3e50;
        border-radius: 12px;
        margin-top: 25px;
    }
    .footer p {
        color: #ffffff;
        font-size: 1rem;
        margin: 4px 0;
    }
    .footer .red-text {
        color: #e74c3c;
        font-weight: 800;
    }
    
    /* Badge System */
    .badge-gold {
        background: #f1c40f;
        color: #1a1a2e;
        padding: 3px 12px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .badge-silver {
        background: #bdc3c7;
        color: #1a1a2e;
        padding: 3px 12px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .badge-bronze {
        background: #e67e22;
        color: white;
        padding: 3px 12px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    
    /* Map Container */
    .map-container {
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

st.markdown("""
<div class="main-header">
    <h1>🩸 <span>RaktConnect</span></h1>
    <p class="tagline">AI Emergency Blood &amp; Organ Donor Network</p>
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
        # Add random jitter for realistic distances
        lat += np.random.uniform(-0.5, 0.5)
        lon += np.random.uniform(-0.5, 0.5)
        blood = np.random.choice(blood_groups, p=[0.30, 0.25, 0.20, 0.10, 0.06, 0.04, 0.03, 0.02])
        
        donors.append({
            'name': f"{first} {last}",
            'blood_group': blood,
            'city': city,
            'latitude': lat,
            'longitude': lon,
            'phone': f"9{np.random.randint(100000000, 999999999)}",
            'available': np.random.choice(['Yes', 'Yes', 'Yes', 'No'], p=[0.75, 0.10, 0.10, 0.05]),
            'donations': np.random.randint(1, 20)
        })
    
    return pd.DataFrame(donors)

# Initialize session state for new donors
if 'donors_df' not in st.session_state:
    st.session_state.donors_df = load_data()

df = st.session_state.donors_df

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

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return 2 * R * asin(sqrt(sin((lat2 - lat1) / 2)**2 + 
                       cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2)**2))

def get_badge(donations):
    if donations >= 15:
        return '🥇 Gold'
    elif donations >= 10:
        return '🥈 Silver'
    elif donations >= 5:
        return '🥉 Bronze'
    else:
        return '⭐ New'

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
    
    # Check for shortage
    compatible['shortage'] = len(compatible) < 3
    
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
    
    # Top Donors Leaderboard
    st.markdown("### 🏆 Top Donors")
    top_donors = df.nlargest(5, 'donations')[['name', 'donations']]
    for _, row in top_donors.iterrows():
        st.markdown(f"**{row['name']}** — {row['donations']} donations")

# ============================================
# TABS
# ============================================

tab1, tab2, tab3 = st.tabs(["🩸 Find Donors", "📝 Register as Donor", "🗺️ Donor Map"])

# ============================================
# TAB 1: FIND DONORS
# ============================================

with tab1:
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
        
        with st.spinner("🤖 Searching for compatible donors..."):
            time.sleep(1)
            donors, total = find_donors(lat, lon, blood_group, urgency.lower())
        
        if donors is None:
            st.error("❌ No compatible donors found!")
        else:
            st.success(f"✅ {total:,} compatible donors found!")
            
            # Shortage Alert
            if len(donors) < 3:
                st.warning("⚠️ Blood shortage alert! Fewer than 3 compatible donors nearby.")
            
            st.markdown("### 🏆 Top Donors")
            
            emojis = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']
            
            for i, (_, donor) in enumerate(donors.iterrows()):
                badge = get_badge(donor['donations'])
                col1, col2, col3 = st.columns([0.5, 3, 1.5])
                with col1:
                    st.markdown(f"<h3 style='color:#c0392b;'>{emojis[i]}</h3>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="donor-card" style="border-left-color: {'#c0392b' if i == 0 else '#666'};">
                        <span class="name">{donor['name']}</span>
                        <span style="margin-left: 10px; font-size: 0.8rem;">{badge}</span><br>
                        <span class="details">🩸 {donor['blood_group']} | 📍 {donor['city']}</span><br>
                        <span class="details">📞 {donor['phone']} | 💉 {donor['donations']} donations</span>
                    </div>
                    """, unsafe_allow_html=True)
                    # WhatsApp Link
                    wa_link = f"https://wa.me/91{donor['phone']}?text=Hi%20{donor['name'].split()[0]}%2C%20I%20need%20emergency%20blood%20donation."
                    st.markdown(f'<a href="{wa_link}" target="_blank" class="whatsapp-btn">💬 WhatsApp</a>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div style="text-align: right; padding-top: 8px;">
                        <span style="font-size: 1.3rem; font-weight: 900; color: #27ae60;">{donor['distance_km']:.1f} km</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("---")
            
            best = donors.iloc[0]
            wa_link = f"https://wa.me/91{best['phone']}?text=Hi%20{best['name'].split()[0]}%2C%20I%20need%20emergency%20blood%20donation."
            st.markdown(f"""
            <div class="best-match">
                <h4>🎯 Best Match</h4>
                <p><strong>{best['name']}</strong> — {best['blood_group']} | 📍 {best['city']}</p>
                <p class="big-phone">📞 {best['phone']}</p>
                <p>📍 {best['distance_km']:.1f} km away</p>
                <p>⏱️ ~{best['distance_km'] / 30 * 60:.0f} minutes</p>
                <a href="{wa_link}" target="_blank" class="whatsapp-btn" style="margin-top: 10px;">💬 Contact on WhatsApp</a>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("📱 Notification sent to donor! ✅")

# ============================================
# TAB 2: REGISTER AS DONOR
# ============================================

with tab2:
    st.markdown("## 📝 Register as a Blood Donor")
    
    st.markdown('<div class="big-card">', unsafe_allow_html=True)
    st.markdown("### 🩸 Donor Registration Form")
    st.markdown("Join our network and help save lives!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_name = st.text_input("Full Name", placeholder="Enter your full name")
        new_blood = st.selectbox("Blood Group", ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-'])
        new_city = st.selectbox("City", list(cities.keys()))
    
    with col2:
        new_phone = st.text_input("Phone Number", placeholder="9XXXXXXXXX")
        new_available = st.selectbox("Availability", ['Yes', 'No'])
        new_donations = st.number_input("Total Donations", min_value=0, max_value=50, value=0)
    
    if st.button("✅ Register as Donor"):
        if not new_name or not new_phone:
            st.error("❌ Please fill in all fields!")
        elif len(new_phone) < 10:
            st.error("❌ Please enter a valid 10-digit phone number!")
        else:
            # Add new donor to dataframe
            lat, lon = cities.get(new_city, (28.6139, 77.2090))
            lat += np.random.uniform(-0.3, 0.3)
            lon += np.random.uniform(-0.3, 0.3)
            
            new_donor = pd.DataFrame({
                'name': [new_name],
                'blood_group': [new_blood],
                'city': [new_city],
                'latitude': [lat],
                'longitude': [lon],
                'phone': [new_phone],
                'available': [new_available],
                'donations': [new_donations]
            })
            
            # Append to session state
            st.session_state.donors_df = pd.concat([st.session_state.donors_df, new_donor], ignore_index=True)
            df = st.session_state.donors_df
            
            st.success(f"✅ Thank you {new_name}! You're now registered as a donor!")
            st.balloons()
            st.info(f"🩸 Your details: {new_name} | {new_blood} | 📍 {new_city} | 📞 {new_phone}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# TAB 3: DONOR MAP
# ============================================

with tab3:
    st.markdown("## 🗺️ Donor Locations")
    
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    
    # Filter donors for map
    map_df = df[['latitude', 'longitude']].dropna()
    if len(map_df) > 0:
        st.map(map_df, zoom=4)
        st.caption(f"📍 Showing {len(map_df)} donor locations across India")
    else:
        st.warning("No donor location data available.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # City-wise donor count
    st.markdown("### 📊 Donors by City")
    city_counts = df['city'].value_counts()
    st.bar_chart(city_counts)

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
    <p>🩸 <span class="red-text">RaktConnect</span> — Saving Lives Through Intelligent Donor Matching</p>
    <p style="font-size: 0.85rem; opacity: 0.8;">© 2026 Team RaktConnect | CodeStorm 2026 — FutureForge</p>
</div>
""", unsafe_allow_html=True)
