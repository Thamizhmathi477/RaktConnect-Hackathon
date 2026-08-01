import streamlit as st
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

st.set_page_config(page_title="RaktConnect", page_icon="🩸")

# ===== HEADER =====
st.markdown("""
<div style="background: #d7263d; padding: 30px; border-radius: 15px; text-align: center;">
    <h1 style="color: white;">🩸 RaktConnect</h1>
    <p style="color: white;">AI Emergency Blood Donor Network</p>
    <p style="color: white; opacity: 0.8;">"Saving Lives Through Intelligent Donor Matching"</p>
</div>
""", unsafe_allow_html=True)

# ===== SAMPLE DATA =====
df = pd.DataFrame({
    'name': ['Rahul Sharma', 'Priya Patel', 'Amit Kumar', 'Vikram Reddy', 'Karan Joshi', 'Sneha Gupta'],
    'blood_group': ['O+', 'A+', 'B+', 'O+', 'O+', 'A-'],
    'city': ['Delhi', 'Delhi', 'Gurgaon', 'Delhi', 'Delhi', 'Delhi'],
    'latitude': [28.6139, 28.7041, 28.5355, 28.4595, 28.5432, 28.5123],
    'longitude': [77.2090, 77.1025, 77.3910, 77.0266, 77.4123, 77.1345],
    'phone': ['9876543210', '9876543211', '9876543212', '9876543214', '9876543218', '9876543215'],
    'available': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes']
})

# ===== COMPATIBILITY =====
compatibility = {
    'A+': ['A+', 'AB+'], 'A-': ['A+', 'A-', 'AB+', 'AB-'],
    'B+': ['B+', 'AB+'], 'B-': ['B+', 'B-', 'AB+', 'AB-'],
    'AB+': ['AB+'], 'AB-': ['AB+', 'AB-'],
    'O+': ['A+', 'B+', 'AB+', 'O+'],
    'O-': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
}

def get_compatible(blood):
    return compatibility.get(blood.upper(), [])

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return 2 * R * asin(sqrt(sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2))

def find_donors(lat, lon, blood, urgency='normal'):
    compatible_groups = get_compatible(blood)
    compatible = df[(df['blood_group'].str.upper().isin(compatible_groups)) & (df['available'] == 'Yes')].copy()
    if len(compatible) == 0:
        return None, 0
    compatible['distance'] = compatible.apply(lambda row: haversine(lat, lon, row['latitude'], row['longitude']), axis=1)
    compatible = compatible.sort_values('distance')
    urgency_multiplier = {'critical': 0.3, 'urgent': 0.6, 'normal': 1.0}
    compatible['priority'] = compatible['distance'] / 5 * urgency_multiplier.get(urgency.lower(), 1.0)
    compatible = compatible.sort_values('priority')
    return compatible.head(5), len(compatible)

cities = {
    'Delhi': (28.6139, 77.2090), 'Mumbai': (19.0760, 72.8777),
    'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946)
}

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("## 📊 Dataset Info")
    st.write(f"**Total Donors:** {len(df)}")
    st.write(f"**Available:** {len(df[df['available'] == 'Yes'])}")
    st.write("**Blood Groups:**", list(df['blood_group'].unique()))

# ===== MAIN =====
st.markdown("## 🩸 Emergency Blood Request")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("👤 Patient Name", "Rajesh Kumar")
    blood = st.selectbox("🩸 Blood Group", ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-'])
    city = st.selectbox("📍 City", list(cities.keys()))
    urgency = st.selectbox("🚨 Urgency", ['Normal', 'Urgent', 'Critical'])

if st.button("🔍 Find Donors", use_container_width=True):
    lat, lon = cities.get(city, (28.6139, 77.2090))
    donors, total = find_donors(lat, lon, blood, urgency.lower())
    
    if donors is None:
        st.error("❌ No compatible donors found! 🚨 Escalating to hospitals...")
    else:
        st.success(f"✅ {total} compatible donors found!")
        st.markdown("### 🏆 Top Donors")
        for _, d in donors.iterrows():
            st.markdown(f"""
            <div style="background: #f0f2f6; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #d7263d;">
                <b>🩸 {d['name']}</b><br>
                📍 {d['city']} | 📞 {d['phone']} | {d['distance']:.1f} km
            </div>
            """, unsafe_allow_html=True)
        
        best = donors.iloc[0]
        st.markdown(f"""
        <div style="background: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 10px; border-left: 5px solid #2e7d32;">
            <b>🎯 Best Match: {best['name']}</b><br>
            📍 {best['distance']:.1f} km away | 📞 {best['phone']}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 10px;">
    <p>🩸 RaktConnect — CodeStorm 2026</p>
</div>
""", unsafe_allow_html=True)
