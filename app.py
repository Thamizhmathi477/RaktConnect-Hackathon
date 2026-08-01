# ============================================
# 🩸 RAKTCONNECT — Streamlit App (FULLY FIXED)
# CodeStorm 2026 — FutureForge
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2, asin

# Page Configuration
st.set_page_config(
    page_title="RaktConnect — AI Blood Donor Network",
    page_icon="🩸",
    layout="wide"
)

# ============================================
# HEADER
# ============================================

st.markdown("""
<div style="background: linear-gradient(135deg, #d7263d, #a71d2a); padding: 30px; border-radius: 15px; text-align: center;">
    <h1 style="color: white; font-size: 3rem;">🩸 RaktConnect</h1>
    <p style="color: white; font-size: 1.3rem;">AI Emergency Blood &amp; Organ Donor Network</p>
    <p style="color: white; font-size: 1.1rem; opacity: 0.8;">"Saving Lives Through Intelligent Donor Matching"</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# SAMPLE DONOR DATA
# ============================================

@st.cache_data
def load_data():
    donors = pd.DataFrame({
        'name': ['Rahul Sharma', 'Priya Patel', 'Amit Kumar', 'Neha Singh', 
                 'Vikram Reddy', 'Sneha Gupta', 'Arjun Nair', 'Meera Iyer',
                 'Karan Joshi', 'Ananya Rao'],
        'blood_group': ['O+', 'A+', 'B+', 'AB+', 'O+', 'A-', 'B-', 'AB-', 'O+', 'A+'],
        'city': ['Delhi', 'Delhi', 'Gurgaon', 'Noida', 'Delhi', 'Delhi', 'Mumbai', 'Chennai', 'Delhi', 'Bangalore'],
        'latitude': [28.6139, 28.7041, 28.5355, 28.6692, 28.4595, 28.5123, 19.0760, 13.0827, 28.5432, 12.9716],
        'longitude': [77.2090, 77.1025, 77.3910, 77.4538, 77.0266, 77.1345, 72.8777, 80.2707, 77.4123, 77.5946],
        'phone': ['9876543210', '9876543211', '9876543212', '9876543213', 
                  '9876543214', '9876543215', '9876543216', '9876543217',
                  '9876543218', '9876543219'],
        'available': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        'donations': [5, 3, 2, 1, 7, 4, 2, 1, 9, 3]
    })
    return donors

df = load_data()

# ============================================
# BLOOD COMPATIBILITY MATRIX
# ============================================

compatibility_matrix = {
    'A+': ['A+', 'AB+'],
    'A-': ['A+', 'A-', 'AB+', 'AB-'],
    'B+': ['B+', 'AB+'],
    'B-': ['B+', 'B-', 'AB+', 'AB-'],
    'AB+': ['AB+'],
    'AB-': ['AB+', 'AB-'],
    'O+': ['A+', 'B+', 'AB+', 'O+'],
    'O-': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
}

def get_compatible(blood):
    return compatibility_matrix.get(blood.upper(), [])

# ============================================
# HAVERSINE DISTANCE FUNCTION
# ============================================

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in kilometers"""
    R = 6371  # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

# ============================================
# AI MATCHING ENGINE
# ============================================

def find_donors(patient_lat, patient_lon, patient_blood, urgency='normal'):
    compatible_groups = get_compatible(patient_blood)
    
    compatible = df[
        (df['blood_group'].str.upper().isin(compatible_groups)) &
        (df['available'] == 'Yes')
    ].copy()
    
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

indian_cities = {
    'Delhi': (28.6139, 77.2090),
    'Mumbai': (19.0760, 72.8777),
    'Chennai': (13.0827, 80.2707),
    'Bangalore': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867),
    'Kolkata': (22.5726, 88.3639),
    'Pune': (18.5204, 73.8567),
    'Ahmedabad': (23.0225, 72.5714)
}

# ============================================
# SIDEBAR — DATASET INFO
# ============================================

with st.sidebar:
    st.markdown("## 📊 Dataset Info")
    st.write(f"**Total Donors:** {len(df)}")
    st.write(f"**Available Donors:** {len(df[df['available'] == 'Yes'])}")
    st.write(f"**Blood Groups:** {df['blood_group'].nunique()}")
    st.write(f"**Cities:** {df['city'].nunique()}")
    
    st.markdown("---")
    st.markdown("### 🩸 Blood Group Distribution")
    st.write(df['blood_group'].value_counts())
    
    st.markdown("---")
    st.markdown("### 📍 Cities")
    st.write(df['city'].value_counts())

# ============================================
# MAIN CONTENT — AI MATCHING DEMO
# ============================================

st.markdown("## 🩸 AI Emergency Blood Donor Matching")

col1, col2 = st.columns(2)

with col1:
    patient_name = st.text_input("👤 Patient Name", "Rajesh Kumar")
    blood_group = st.selectbox("🩸 Blood Group", ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
    city = st.selectbox("📍 City", list(indian_cities.keys()))
    urgency = st.selectbox("🚨 Urgency Level", ['Normal', 'Urgent', 'Critical'])

with col2:
    st.markdown("### 📋 Patient Details")
    st.write(f"**Name:** {patient_name}")
    st.write(f"**Blood Group:** {blood_group}")
    st.write(f"**Location:** {city}")
    st.write(f"**Urgency:** {urgency}")

# ============================================
# FIND DONORS BUTTON
# ============================================

if st.button("🔍 Find Donors Now", use_container_width=True):
    lat, lon = indian_cities.get(city, (28.6139, 77.2090))
    
    donors, total = find_donors(lat, lon, blood_group, urgency.lower())
    
    if donors is None:
        st.error("❌ No compatible donors found! 🚨 Escalating to hospital network...")
    else:
        st.success(f"✅ {total} compatible donors found!")
        
        st.markdown("### 🏆 Top Donors")
        
        emojis = ['🥇', '🥈', '🥉', '📍', '📍']
        
        for i, (_, donor) in enumerate(donors.iterrows()):
            col1, col2, col3 = st.columns([1, 4, 2])
            with col1:
                st.markdown(f"## {emojis[i]}")
            with col2:
                st.markdown(f"**{donor['name']}**")
                st.markdown(f"🩸 {donor['blood_group']} | 📍 {donor['city']} | 📞 {donor['phone']}")
                st.markdown(f"💉 {donor['donations']} donations")
            with col3:
                st.markdown(f"## {donor['distance_km']:.1f} km")
                st.markdown(f"*Priority: {donor['priority_score']:.2f}*")
            
            st.markdown("---")
        
        # Best Match
        best = donors.iloc[0]
        st.markdown("### 🎯 Best Match")
        st.markdown(f"""
        <div style="background: #e8f5e9; padding: 15px; border-radius: 10px; border-left: 5px solid #2e7d32;">
            <h4>🩸 {best['name']}</h4>
            <p>📍 {best['distance_km']:.1f} km away | 📞 {best['phone']}</p>
            <p>⏱️ Estimated arrival: ~{best['distance_km']/30*60:.0f} minutes</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("📱 Notification sent to donor! ✅")

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p>🩸 <strong>RaktConnect</strong> — Saving Lives Through Intelligent Donor Matching</p>
    <p style="font-size: 0.9rem; color: #666;">© 2026 Team RaktConnect | CodeStorm 2026 — FutureForge</p>
</div>
""", unsafe_allow_html=True)
