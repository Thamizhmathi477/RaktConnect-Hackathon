# ============================================
# 🩸 RAKTCONNECT — Professional Edition
# CodeStorm 2026 — FutureForge
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, asin
import time

st.set_page_config(
    page_title="RaktConnect — Emergency Blood Donor Network",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# PROFESSIONAL STYLE — Corporate Blue + Trust Colors
# ============================================

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+Pro:wght@600;700&display=swap" rel="stylesheet">
<style>
    :root{
        --navy:#0A1628;
        --navy-light:#1A2A4A;
        --blue:#1A5C9A;
        --blue-light:#E8F0FE;
        --blue-mid:#4A8BC2;
        --red:#C0392B;
        --red-light:#FDF2F1;
        --ink:#1A1A2E;
        --muted:#5A6A7A;
        --bg:#F5F7FA;
        --card:#FFFFFF;
        --line:#E2E8F0;
        --green:#27AE60;
        --green-light:#E8F8F0;
    }

    .stApp { background-color: var(--bg) !important; font-family: 'Inter', sans-serif; }
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
        color: var(--ink);
        font-family: 'Inter', sans-serif;
    }

    .block-container { max-width: 1200px; padding-top: 1.5rem; padding-bottom: 3rem; }

    /* ---- Top Bar ---- */
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 0 16px 0;
        border-bottom: 3px solid var(--navy);
        margin-bottom: 24px;
    }
    .topbar .brand { display: flex; align-items: baseline; gap: 12px; }
    .topbar .mark {
        font-family: 'Source Serif Pro', serif !important;
        font-size: 1.8rem; font-weight: 700; color: var(--navy) !important;
    }
    .topbar .mark span { color: var(--blue) !important; }
    .topbar .desc { font-size: 0.85rem; color: var(--muted) !important; font-weight: 400; }
    .topbar .badge {
        background: var(--navy);
        color: white !important;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    /* ---- Cards ---- */
    .card {
        background: var(--card);
        padding: 24px 28px;
        border-radius: 8px;
        border: 1px solid var(--line);
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .card h3 {
        font-family: 'Source Serif Pro', serif !important;
        color: var(--navy) !important;
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0 0 14px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--line);
    }
    .card, .card p, .card div, .card span, .card label, .card strong {
        color: var(--ink) !important;
    }

    /* ---- Stat Tiles ---- */
    .stat {
        background: var(--card);
        padding: 16px 18px;
        border-radius: 8px;
        border: 1px solid var(--line);
        border-top: 4px solid var(--blue);
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    .stat .label {
        font-size: 0.7rem;
        color: var(--muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .stat .number {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--navy) !important;
        font-family: 'Source Serif Pro', serif;
        line-height: 1.1;
    }

    /* ---- Donor List ---- */
    .donor {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 6px;
        padding: 14px 18px;
        margin: 6px 0;
        transition: all 0.2s;
    }
    .donor:hover { border-color: var(--blue); box-shadow: 0 2px 8px rgba(26, 92, 154, 0.08); }
    .donor.top { border-color: var(--blue); background: var(--blue-light); border-left: 4px solid var(--blue); }
    .donor .left { flex: 1; }
    .donor .name-row { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
    .donor .name { font-size: 0.98rem; font-weight: 700; color: var(--navy) !important; }
    .donor .flag {
        font-size: 0.65rem;
        font-weight: 700;
        color: var(--blue) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        background: var(--blue-light);
        padding: 2px 12px;
        border-radius: 12px;
    }
    .donor .meta { font-size: 0.82rem; color: var(--muted) !important; }
    .donor .right { text-align: right; flex-shrink: 0; padding-left: 16px; }
    .donor .dist { font-size: 1.1rem; font-weight: 700; color: var(--navy) !important; }
    .donor .bg-chip {
        display: inline-block;
        background: var(--navy);
        color: #fff !important;
        padding: 2px 10px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-top: 4px;
    }
    .donor .wa {
        display: inline-block;
        margin-top: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--blue) !important;
        text-decoration: none;
        border-bottom: 2px solid var(--blue);
    }
    .donor .wa:hover { color: var(--navy) !important; border-color: var(--navy) !important; }

    /* ---- Best Match ---- */
    .best-match {
        background: var(--blue-light);
        border: 2px solid var(--blue);
        padding: 20px 24px;
        border-radius: 8px;
        margin-top: 14px;
    }
    .best-match, .best-match * { color: var(--ink) !important; }
    .best-match .label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--blue) !important;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .best-match .phone { font-size: 1.2rem; font-weight: 700; color: var(--navy) !important; }
    .best-match .wa {
        display: inline-block;
        margin-top: 8px;
        font-weight: 700;
        color: var(--blue) !important;
        text-decoration: none;
        border-bottom: 2px solid var(--blue);
    }

    /* ---- Shortage Alert ---- */
    .shortage-note {
        background: #FEF9E7;
        border: 1px solid #F39C12;
        border-left: 4px solid #F39C12;
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 0.9rem;
        color: var(--ink) !important;
        margin: 8px 0;
    }

    /* ---- Buttons ---- */
    .stButton button {
        background: var(--navy) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 12px 28px !important;
        border: none !important;
        border-radius: 6px !important;
        width: 100% !important;
        transition: all 0.3s !important;
    }
    .stButton button:hover {
        background: var(--blue) !important;
        box-shadow: 0 4px 16px rgba(26, 92, 154, 0.3) !important;
    }

    /* ---- Inputs ---- */
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        color: var(--muted) !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .stSelectbox div[data-baseweb="select"] * { color: var(--ink) !important; }
    .stTextInput input, .stNumberInput input {
        color: var(--ink) !important;
        background: #FFFFFF !important;
        border: 2px solid var(--line) !important;
        border-radius: 6px !important;
        padding: 10px 14px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus { border-color: var(--blue) !important; }

    /* ---- Tabs ---- */
    .stTabs [data-baseweb="tab-list"] { border-bottom: 2px solid var(--line); gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        color: var(--muted) !important;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        color: var(--navy) !important;
        border-bottom: 3px solid var(--blue) !important;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid var(--line);
        padding-top: 20px;
    }
    section[data-testid="stSidebar"] * { color: var(--ink) !important; }
    section[data-testid="stSidebar"] h2 {
        font-family: 'Source Serif Pro', serif !important;
        font-size: 0.95rem !important;
        color: var(--navy) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 2px solid var(--line);
        padding-bottom: 10px;
    }

    /* ---- Footer ---- */
    .footer {
        text-align: center;
        padding: 20px;
        background: var(--navy);
        border-radius: 8px;
        margin-top: 32px;
    }
    .footer p { color: #DCE8F0 !important; font-size: 0.85rem; margin: 3px 0; }
    .footer .brand { color: #FFFFFF !important; font-weight: 700; }

    .map-box { background: var(--card); padding: 16px; border-radius: 8px; border: 1px solid var(--line); }

    /* ---- Thank You Message ---- */
    .thank-you {
        background: linear-gradient(135deg, var(--green-light), #D5F5E3);
        border: 2px solid var(--green);
        padding: 30px 35px;
        border-radius: 12px;
        text-align: center;
        margin: 15px 0;
    }
    .thank-you h2 {
        color: #1A6E34 !important;
        font-family: 'Source Serif Pro', serif !important;
        font-size: 1.8rem;
        margin: 0;
    }
    .thank-you .sub {
        color: #1A4A2A !important;
        font-size: 1.1rem;
        margin: 8px 0;
    }
    .thank-you .details {
        background: white;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 12px 0;
        border: 1px solid #A9DFBF;
    }
    .thank-you .details p { margin: 4px 0; color: var(--ink) !important; }

    /* ---- Browse Table ---- */
    .browse-table {
        background: var(--card);
        border-radius: 8px;
        border: 1px solid var(--line);
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# TOP BAR
# ============================================

st.markdown("""
<div class="topbar">
    <div class="brand">
        <span class="mark">Rakt<span>Connect</span></span>
        <span class="desc">Emergency Blood Donor Network</span>
    </div>
    <span class="badge">CodeStorm 2026</span>
</div>
""", unsafe_allow_html=True)

# ============================================
# DATA
# ============================================

@st.cache_data
def load_data():
    np.random.seed(42)
    city_coords = {
        'Delhi': (28.6139, 77.2090), 'Mumbai': (19.0760, 72.8777),
        'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946),
        'Hyderabad': (17.3850, 78.4867), 'Kolkata': (22.5726, 88.3639),
        'Pune': (18.5204, 73.8567), 'Ahmedabad': (23.0225, 72.5714),
        'Jaipur': (26.9124, 75.7873), 'Lucknow': (26.8467, 80.9462)
    }
    blood_groups = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-']
    first_names = ['Rahul','Priya','Amit','Neha','Vikram','Sneha','Arjun','Meera','Karan','Ananya',
                   'Rohan','Pooja','Suresh','Lakshmi','Manoj','Divya','Naveen','Kavya','Srinivas','Anjali',
                   'Rajesh','Sangeeta','Vijay','Shreya','Ajay','Anita','Sunil','Deepa','Ravi','Sonia']
    last_names = ['Sharma','Patel','Kumar','Singh','Reddy','Gupta','Nair','Iyer','Joshi','Rao',
                  'Verma','Malhotra','Srinivasan','Menon','Shetty','Pillai','Naidu','Das','Ganguly','Bose']

    donors = []
    for i in range(10000):
        city = np.random.choice(list(city_coords.keys()))
        lat, lon = city_coords[city]
        lat += np.random.uniform(-0.5, 0.5)
        lon += np.random.uniform(-0.5, 0.5)
        donors.append({
            'name': f"{np.random.choice(first_names)} {np.random.choice(last_names)}",
            'blood_group': np.random.choice(blood_groups, p=[0.30,0.25,0.20,0.10,0.06,0.04,0.03,0.02]),
            'city': city, 'latitude': lat, 'longitude': lon,
            'phone': f"9{np.random.randint(100000000, 999999999)}",
            'available': np.random.choice(['Yes','Yes','Yes','No'], p=[0.75,0.10,0.10,0.05]),
            'donations': np.random.randint(1, 20)
        })
    return pd.DataFrame(donors)

if 'donors_df' not in st.session_state:
    st.session_state.donors_df = load_data()
if 'registration_success' not in st.session_state:
    st.session_state.registration_success = False
if 'new_donor_name' not in st.session_state:
    st.session_state.new_donor_name = ""
if 'new_donor_details' not in st.session_state:
    st.session_state.new_donor_details = {}

df = st.session_state.donors_df

cities = {
    'Delhi': (28.6139, 77.2090), 'Mumbai': (19.0760, 72.8777),
    'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867), 'Kolkata': (22.5726, 88.3639),
    'Pune': (18.5204, 73.8567), 'Ahmedabad': (23.0225, 72.5714),
    'Jaipur': (26.9124, 75.7873), 'Lucknow': (26.8467, 80.9462)
}

# ============================================
# COMPATIBILITY & MATCHING
# ============================================

compatibility = {
    'O+': ['O+','O-'], 'O-': ['O-'],
    'A+': ['A+','A-','O+','O-'], 'A-': ['A-','O-'],
    'B+': ['B+','B-','O+','O-'], 'B-': ['B-','O-'],
    'AB+': ['A+','A-','B+','B-','AB+','AB-','O+','O-'],
    'AB-': ['A-','B-','AB-','O-'],
}

def get_compatible(patient_blood):
    return compatibility.get(patient_blood.upper(), [])

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return 2 * R * asin(sqrt(sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2))

def find_donors(patient_lat, patient_lon, patient_blood, urgency='normal'):
    eligible = get_compatible(patient_blood)
    result = df[(df['blood_group'].str.upper().isin(eligible)) & (df['available']=='Yes')].copy()
    if len(result) == 0:
        return None, 0
    result['distance_km'] = result.apply(
        lambda r: haversine(patient_lat, patient_lon, r['latitude'], r['longitude']), axis=1
    )
    urgency_w = {'critical': 0.3, 'urgent': 0.6, 'normal': 1.0}
    result['score'] = result['distance_km'] / 5 * urgency_w.get(urgency.lower(), 1.0)
    result = result.sort_values('score')
    return result.head(5), len(result)

def badge(donations):
    if donations >= 15: return 'Gold donor'
    if donations >= 10: return 'Silver donor'
    if donations >= 5: return 'Bronze donor'
    return 'New donor'

# ============================================
# NATIONWIDE SUMMARY
# ============================================

total_donors = len(df)
total_available = len(df[df['available'] == 'Yes'])
total_cities = df['city'].nunique()
avg_donations = df['donations'].mean()

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(f'<div class="stat"><div class="label">Total Donors</div><div class="number">{total_donors:,}</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown(f'<div class="stat"><div class="label">Available Now</div><div class="number">{total_available:,}</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown(f'<div class="stat"><div class="label">Cities Covered</div><div class="number">{total_cities}</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown(f'<div class="stat"><div class="label">Avg. Donations</div><div class="number">{avg_donations:.1f}</div></div>', unsafe_allow_html=True)

st.write("")

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("## Top Contributors")
    for _, row in df.nlargest(5, 'donations')[['name','donations']].iterrows():
        st.markdown(f"<div style='font-size:0.85rem; padding:5px 0; border-bottom:1px solid #E2E8F0; display:flex; justify-content:space-between;'><span>{row['name']}</span><span style='color:#5A6A7A;'>{row['donations']}</span></div>", unsafe_allow_html=True)

# ============================================
# TABS
# ============================================

tab1, tab2, tab3, tab4 = st.tabs(["🔍 Find Donors", "📋 Browse All Donors", "📝 Register", "🗺️ Map"])

# ---- TAB 1: FIND DONORS ----
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>Patient Details</h3>', unsafe_allow_html=True)
        patient_name = st.text_input("Patient Name", "Rajesh Kumar")
        patient_blood = st.selectbox("Patient Blood Group", ['O+','A+','B+','AB+','O-','A-','B-','AB-'])
        patient_city = st.selectbox("Patient City", list(cities.keys()))
        urgency = st.selectbox("Urgency Level", ['Normal','Urgent','Critical'])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><h3>Request Summary</h3>', unsafe_allow_html=True)
        st.markdown(f"**Patient** — {patient_name}")
        st.markdown(f"**Blood group** — {patient_blood}")
        st.markdown(f"**Location** — {patient_city}")
        st.markdown(f"**Urgency** — {urgency}")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Find Compatible Donors"):
        lat, lon = cities.get(patient_city, (28.6139, 77.2090))
        with st.spinner("Matching against network..."):
            time.sleep(0.6)
            donors, total = find_donors(lat, lon, patient_blood, urgency.lower())

        if donors is None:
            st.error("No compatible donors found in the network.")
        else:
            st.markdown(f"**{total:,} compatible donors found**, ranked by distance and urgency.")
            if len(donors) < 3:
                st.markdown('<div class="shortage-note">⚠️ Shortage alert — fewer than 3 compatible donors nearby.</div>', unsafe_allow_html=True)

            st.write("")
            for i, (_, donor) in enumerate(donors.iterrows()):
                row_class = "donor top" if i == 0 else "donor"
                wa_link = f"https://wa.me/91{donor['phone']}?text=Hi%20{donor['name'].split()[0]}%2C%20I%20need%20emergency%20blood%20donation."
                flag = '<span class="flag">Best Match</span>' if i == 0 else ''
                st.markdown(f'''
                <div class="{row_class}">
                    <div class="left">
                        <div class="name-row"><span class="name">{donor["name"]}</span>{flag}</div>
                        <span class="meta">{donor["city"]} · {badge(donor["donations"])} · 📞 {donor["phone"]}</span>
                        <a class="wa" href="{wa_link}" target="_blank">💬 Contact on WhatsApp →</a>
                    </div>
                    <div class="right">
                        <div class="dist">{donor["distance_km"]:.1f} km</div>
                        <span class="bg-chip">{donor["blood_group"]}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

            best = donors.iloc[0]
            wa_link = f"https://wa.me/91{best['phone']}?text=Hi%20{best['name'].split()[0]}%2C%20I%20need%20emergency%20blood%20donation."
            st.markdown(f'''
            <div class="best-match">
                <div class="label">🎯 Recommended Contact</div>
                <p style="font-weight:700; font-size:1.05rem; margin:0;">{best["name"]} — {best["blood_group"]}</p>
                <p class="phone">📞 {best["phone"]}</p>
                <p style="margin:2px 0; color:#5A6A7A;">📍 {best["distance_km"]:.1f} km away · approx. {best["distance_km"]/30*60:.0f} min</p>
                <a class="wa" href="{wa_link}" target="_blank">💬 Contact on WhatsApp →</a>
            </div>
            ''', unsafe_allow_html=True)

# ---- TAB 2: BROWSE ALL DONORS ----
with tab2:
    st.markdown('<div class="card"><h3>All Registered Donors</h3>', unsafe_allow_html=True)
    st.markdown(f"Showing all **{len(df):,}** registered donors in the network.")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        filter_blood = st.selectbox("Filter by Blood Group", ['All'] + ['O+','A+','B+','AB+','O-','A-','B-','AB-'])
    with col2:
        filter_city = st.selectbox("Filter by City", ['All'] + list(cities.keys()))
    
    # Apply filters
    filtered_df = df.copy()
    if filter_blood != 'All':
        filtered_df = filtered_df[filtered_df['blood_group'] == filter_blood]
    if filter_city != 'All':
        filtered_df = filtered_df[filtered_df['city'] == filter_city]
    
    st.markdown(f"**{len(filtered_df):,} donors** found")
    
    # Display donors in a table-like format
    display_df = filtered_df[['name', 'blood_group', 'city', 'phone', 'donations', 'available']].head(100)
    st.dataframe(
        display_df,
        column_config={
            "name": "Name",
            "blood_group": "Blood Group",
            "city": "City",
            "phone": "Phone",
            "donations": "Donations",
            "available": "Available"
        },
        use_container_width=True,
        height=400
    )
    
    if len(filtered_df) > 100:
        st.caption(f"Showing first 100 of {len(filtered_df):,} donors")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---- TAB 3: REGISTER ----
with tab3:
    st.markdown('<div class="card"><h3>Donor Registration</h3>', unsafe_allow_html=True)
    
    # Check if registration was successful
    if st.session_state.registration_success:
        # Professional Thank You Message
        st.markdown(f'''
        <div class="thank-you">
            <h2>🎉 Thank You, {st.session_state.new_donor_name}!</h2>
            <p class="sub">You are now registered as a life-saving blood donor!</p>
            <div class="details">
                <p><strong>🩸 Blood Group:</strong> {st.session_state.new_donor_details.get('blood', 'N/A')}</p>
                <p><strong>📍 City:</strong> {st.session_state.new_donor_details.get('city', 'N/A')}</p>
                <p><strong>📞 Phone:</strong> {st.session_state.new_donor_details.get('phone', 'N/A')}</p>
                <p><strong>💉 Total Donations:</strong> {st.session_state.new_donor_details.get('donations', 0)}</p>
            </div>
            <p style="color: #1A4A2A; font-weight: 600;">You are now part of a network of {len(df):,} donors across India.</p>
            <p style="color: #1A4A2A; font-size: 0.9rem;">Your registration helps save lives in emergency situations. 🩸❤️</p>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("📝 Register Another Donor", key="register_another"):
            st.session_state.registration_success = False
            st.rerun()
    
    else:
        st.markdown("Join the donor network. Takes under a minute.")
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Full Name", placeholder="Enter your full name", key="reg_name")
            new_blood = st.selectbox("Blood Group", ['O+','A+','B+','AB+','O-','A-','B-','AB-'], key="reg_blood")
            new_city = st.selectbox("City", list(cities.keys()), key="reg_city")
        with col2:
            new_phone = st.text_input("Phone Number", placeholder="9XXXXXXXXX", key="reg_phone")
            new_available = st.selectbox("Availability", ['Yes','No'], key="reg_available")
            new_donations = st.number_input("Total Past Donations", min_value=0, max_value=50, value=0, key="reg_donations")

        if st.button("✅ Register as Donor"):
            if not new_name or not new_phone:
                st.error("Please complete all fields.")
            elif len(new_phone) < 10:
                st.error("Please enter a valid 10-digit phone number.")
            else:
                lat, lon = cities.get(new_city, (28.6139, 77.2090))
                lat += np.random.uniform(-0.3, 0.3)
                lon += np.random.uniform(-0.3, 0.3)
                new_donor = pd.DataFrame({
                    'name':[new_name], 'blood_group':[new_blood], 'city':[new_city],
                    'latitude':[lat], 'longitude':[lon], 'phone':[new_phone],
                    'available':[new_available], 'donations':[new_donations]
                })
                st.session_state.donors_df = pd.concat([st.session_state.donors_df, new_donor], ignore_index=True)
                df = st.session_state.donors_df
                
                # Set session state for thank you message
                st.session_state.registration_success = True
                st.session_state.new_donor_name = new_name
                st.session_state.new_donor_details = {
                    'blood': new_blood,
                    'city': new_city,
                    'phone': new_phone,
                    'donations': new_donations
                }
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---- TAB 4: MAP ----
with tab4:
    st.markdown('<div class="map-box">', unsafe_allow_html=True)
    map_df = df[['latitude','longitude']].dropna()
    if len(map_df) > 0:
        st.map(map_df, zoom=4)
        st.caption(f"📍 {len(map_df):,} donor locations across India")
    else:
        st.warning("No donor location data available.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:20px;">Donors by City</div>', unsafe_allow_html=True)
    st.bar_chart(df['city'].value_counts())

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
    <p><span class="brand">🩸 RaktConnect</span> — Saving lives through intelligent donor matching</p>
    <p>Built for CodeStorm 2026: FutureForge</p>
</div>
""", unsafe_allow_html=True)
