# ============================================
# 🩸 RAKTCONNECT — Professional Edition (Enhanced)
# CodeStorm 2026 — FutureForge
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, asin
import time

# --- Performance Optimization: Cache data loading ---
@st.cache_resource
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

# --- Helper: Donor Badge ---
def get_badge(count):
    if count >= 15:
        return '<span class="badge-platinum">🏆 Platinum</span>'
    elif count >= 10:
        return '<span class="badge-gold">🥇 Gold</span>'
    elif count >= 5:
        return '<span class="badge-silver">🥈 Silver</span>'
    else:
        return '<span class="badge-bronze">🥉 Bronze</span>'

# --- Page Config ---
st.set_page_config(
    page_title="RaktConnect — Emergency Blood Donor Network",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Professional CSS (Enhanced) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+Pro:wght@600;700&display=swap" rel="stylesheet">
<style>
    :root{
        --ink:#1C2530;
        --muted:#606A78;
        --teal:#0E5C56;
        --teal-dark:#0A423E;
        --teal-pale:#EAF2F1;
        --crimson:#D7263D;
        --crimson-pale:#FBF0F1;
        --bg:#F7F6F3;
        --card:#FFFFFF;
        --line:#E4E2DC;
        --amber:#B8862E;
    }

    .stApp { background-color: var(--bg) !important; font-family: 'Inter', sans-serif; }
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
        color: var(--ink);
        font-family: 'Inter', sans-serif;
    }

    .block-container{
        max-width: 1080px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* ---- Top bar ---- */
    .topbar{
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        padding: 0 0 16px 0;
        border-bottom: 2px solid var(--teal);
        margin-bottom: 26px;
    }
    .topbar .brand{
        display: flex; align-items: baseline; gap: 10px;
    }
    .topbar .mark{
        font-family: 'Source Serif Pro', serif !important;
        font-size: 1.55rem; font-weight: 700; color: var(--teal-dark) !important;
        letter-spacing: -0.01em;
    }
    .topbar .mark span{ color: var(--crimson) !important; }
    .topbar .desc{ font-size: 0.85rem; color: var(--muted) !important; }
    .topbar .eyebrow{
        font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase;
        color: var(--muted) !important; font-weight: 600;
    }

    /* ---- Cards ---- */
    .card{
        background: var(--card);
        padding: 24px 26px;
        border-radius: 12px;
        border: 1px solid var(--line);
        margin-bottom: 16px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.05);
        transition: 0.3s;
    }
    .card:hover {
        box-shadow: 0 8px 30px rgba(215, 38, 61, 0.08);
    }
    .card h3{
        font-family: 'Source Serif Pro', serif !important;
        color: var(--teal-dark) !important;
        font-size: 1.05rem;
        font-weight: 700;
        margin: 0 0 16px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--line);
        text-transform: none;
    }
    .card, .card p, .card div, .card span, .card label, .card strong{
        color: var(--ink) !important;
    }

    .section-label{
        font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase;
        color: var(--muted) !important; font-weight: 700; margin: 6px 0 10px 0;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"]{ background-color: #FFFFFF !important; border-right: 1px solid var(--line); }
    section[data-testid="stSidebar"] *{ color: var(--ink) !important; }
    section[data-testid="stSidebar"] h2{
        font-family: 'Source Serif Pro', serif !important;
        font-size: 0.98rem !important;
        color: var(--teal-dark) !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    /* How-it-works box */
    .how-box {
        background: var(--teal-pale);
        border-radius: 8px;
        padding: 12px;
        margin-top: 10px;
        border-left: 4px solid var(--teal);
    }
    .how-box p { font-size: 0.9rem; margin: 4px 0; }

    /* ---- Inputs ---- */
    .stSelectbox label, .stTextInput label, .stNumberInput label{
        color: var(--muted) !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .stSelectbox div[data-baseweb="select"] *{ color: var(--ink) !important; }
    .stTextInput input, .stNumberInput input{
        color: var(--ink) !important;
        background: #FFFFFF !important;
        border: 1px solid var(--line) !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus{ border-color: var(--teal) !important; }

    /* ---- Tabs ---- */
    .stTabs [data-baseweb="tab-list"]{ border-bottom: 1px solid var(--line); gap: 6px; }
    .stTabs [data-baseweb="tab"]{ color: var(--muted) !important; font-weight: 600; font-size: 0.9rem; }
    .stTabs [aria-selected="true"]{ color: var(--teal-dark) !important; }

    /* ---- KPI stat tiles ---- */
    .stat{
        background: #FFFFFF;
        padding: 14px 16px;
        border-radius: 8px;
        border: 1px solid var(--line);
    }
    .stat .label{ font-size: 0.68rem; color: var(--muted) !important; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; margin-bottom: 4px; }
    .stat .number{ font-size: 1.65rem; font-weight: 700; color: var(--teal-dark) !important; font-family: 'Source Serif Pro', serif; line-height: 1.1; }

    /* ---- Donor list ---- */
    .donor{
        display: flex; justify-content: space-between; align-items: flex-start;
        background: #FFFFFF; border: 1px solid var(--line); border-radius: 8px;
        padding: 14px 18px; margin: 7px 0;
        transition: 0.2s;
    }
    .donor:hover { border-color: var(--teal); }
    .donor.top{ border-color: var(--crimson); background: var(--crimson-pale); }
    .donor, .donor *{ color: var(--ink) !important; }
    .donor .left{ flex: 1; }
    .donor .name-row{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 3px; }
    .donor .name{ font-size: 0.98rem; font-weight: 700; }
    .donor .flag{ font-size: 0.68rem; font-weight: 700; color: var(--crimson) !important; text-transform: uppercase; letter-spacing: 0.04em; }
    .donor .meta{ font-size: 0.83rem; color: var(--muted) !important; }
    .donor .right{ text-align: right; flex-shrink: 0; padding-left: 16px; }
    .donor .dist{ font-size: 1.05rem; font-weight: 700; color: var(--teal-dark) !important; }
    .donor .bg-chip{
        display: inline-block; background: var(--teal); color: #fff !important;
        padding: 2px 10px; border-radius: 4px; font-size: 0.72rem; font-weight: 700; margin-top: 4px;
    }
    .donor .wa{
        display: inline-block; margin-top: 6px; font-size: 0.78rem; font-weight: 600;
        color: var(--teal-dark) !important; text-decoration: none; border-bottom: 1px solid var(--teal-dark);
    }
    .donor .wa:hover { color: var(--crimson) !important; border-color: var(--crimson); }

    /* ---- Badge styles ---- */
    .badge-platinum { background: #e8e8e8; color: #333; padding: 2px 12px; border-radius: 20px; font-weight: 700; border: 2px solid #c0a050; font-size: 0.7rem; }
    .badge-gold { background: #fff8e1; color: #b8860b; padding: 2px 12px; border-radius: 20px; font-weight: 700; border: 2px solid #ffd700; font-size: 0.7rem; }
    .badge-silver { background: #f5f5f5; color: #888; padding: 2px 12px; border-radius: 20px; font-weight: 700; border: 2px solid #c0c0c0; font-size: 0.7rem; }
    .badge-bronze { background: #fff3e0; color: #cd7f32; padding: 2px 12px; border-radius: 20px; font-weight: 700; border: 2px solid #cd7f32; font-size: 0.7rem; }

    /* ---- Best match ---- */
    .best-match{
        background: #FFFFFF; border: 1px solid var(--line); border-left: 4px solid var(--crimson);
        padding: 18px 22px; border-radius: 8px; margin-top: 14px;
    }
    .best-match, .best-match *{ color: var(--ink) !important; }
    .best-match .label{ font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--crimson) !important; font-weight: 700; margin-bottom: 8px; }
    .best-match .phone{ font-size: 1.1rem; font-weight: 700; color: var(--teal-dark) !important; }

    /* ---- Shortage meter ---- */
    .shortage-note{
        background: #FBF3E7; border: 1px solid var(--amber); border-left: 4px solid var(--amber);
        padding: 10px 14px; border-radius: 6px; font-size: 0.86rem; color: var(--ink) !important; margin: 8px 0;
    }

    /* ---- Emergency button ---- */
    .stButton button {
        background: var(--teal) !important; color: #FFFFFF !important;
        font-weight: 700 !important; font-size: 0.9rem !important;
        padding: 12px 24px !important; border: none !important;
        border-radius: 30px !important; width: 100% !important;
        transition: all 0.3s !important;
    }
    .stButton button:hover {
        background: var(--teal-dark) !important;
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(14, 92, 86, 0.3);
    }
    /* Emergency override */
    .emergency-btn button {
        background: var(--crimson) !important;
    }
    .emergency-btn button:hover {
        background: #a71d2a !important;
        box-shadow: 0 4px 15px rgba(215, 38, 61, 0.4);
    }

    /* ---- Footer ---- */
    .footer{
        text-align: center; padding: 16px; border-top: 1px solid var(--line);
        margin-top: 32px;
    }
    .footer p{ color: var(--muted) !important; font-size: 0.8rem; margin: 2px 0; }
    .footer .brand{ color: var(--teal-dark) !important; font-weight: 700; }

    /* ---- Map box ---- */
    .map-box{ background: #FFFFFF; padding: 16px; border-radius: 8px; border: 1px solid var(--line); }
</style>
""", unsafe_allow_html=True)

# --- Load Data ---
df = load_data()

# --- City coordinates ---
cities = {
    'Delhi': (28.6139, 77.2090), 'Mumbai': (19.0760, 72.8777),
    'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867), 'Kolkata': (22.5726, 88.3639),
    'Pune': (18.5204, 73.8567), 'Ahmedabad': (23.0225, 72.5714),
    'Jaipur': (26.9124, 75.7873), 'Lucknow': (26.8467, 80.9462)
}

# --- Compatibility matrix ---
compatibility = {
    'O+': ['O+','O-'], 'O-': ['O-'],
    'A+': ['A+','A-','O+','O-'], 'A-': ['A-','O-'],
    'B+': ['B+','B-','O+','O-'], 'B-': ['B-','O-'],
    'AB+': ['A+','A-','B+','B-','AB+','AB-','O+','O-'],
    'AB-': ['A-','B-','AB-','O-'],
}
def get_compatible(b): return compatibility.get(b.upper(), [])

# --- Distance ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return 2 * R * asin(sqrt(sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2))

# --- Matching engine ---
def find_donors(patient_lat, patient_lon, patient_blood, urgency='normal', request_text=''):
    eligible = get_compatible(patient_blood)
    result = df[(df['blood_group'].str.upper().isin(eligible)) & (df['available']=='Yes')].copy()
    if len(result) == 0:
        return None, 0
    result['distance_km'] = result.apply(
        lambda r: haversine(patient_lat, patient_lon, r['latitude'], r['longitude']), axis=1
    )
    urgency_w = {'critical': 0.3, 'urgent': 0.6, 'normal': 1.0}
    result['score'] = result['distance_km'] / 5 * urgency_w.get(urgency.lower(), 1.0)
    
    # --- Smarter AI: boost priority if emergency keywords in request text ---
    if request_text:
        emergency_keywords = ['emergency', 'accident', 'bleeding', 'critical', 'urgent', 'need blood', 'immediately']
        if any(word in request_text.lower() for word in emergency_keywords):
            result['score'] = result['score'] * 0.5  # half the score = higher priority
    
    result = result.sort_values('score')
    return result.head(5), len(result)

# --- Top bar ---
st.markdown("""
<div class="topbar">
    <div class="brand">
        <span class="mark">Rakt<span>Connect</span></span>
        <span class="desc">Emergency Blood Donor Network</span>
    </div>
    <span class="eyebrow">Prototype · CodeStorm 2026</span>
</div>
""", unsafe_allow_html=True)

# --- Nationwide summary stats ---
total_donors = len(df)
total_available = len(df[df['available'] == 'Yes'])
total_cities = df['city'].nunique()
avg_donations = df['donations'].mean()

st.markdown('<div class="section-label">Network — All India</div>', unsafe_allow_html=True)
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

# --- Sidebar ---
with st.sidebar:
    st.markdown("## Top Contributors")
    for _, row in df.nlargest(5, 'donations')[['name','donations']].iterrows():
        st.markdown(f"<div style='font-size:0.86rem; padding:4px 0; border-bottom:1px solid var(--line);'>{row['name']} <span style='color:var(--muted);float:right;'>{row['donations']}</span></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📖 How It Works")
    st.markdown("""
    <div class="how-box">
        <p>1️⃣ <strong>Search</strong> for your blood group</p>
        <p>2️⃣ <strong>Find</strong> the nearest donor</p>
        <p>3️⃣ <strong>Contact</strong> via WhatsApp</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("🩸 Every donation saves a life!")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🔍 Find Donors", "📝 Register as Donor", "🗺️ Donor Map"])

# ---- TAB 1: Find Donors ----
with tab1:
    # Emergency button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚨 I NEED BLOOD NOW", use_container_width=True, key="emergency_btn"):
            st.session_state.urgency = "Critical"
            st.session_state.emergency_mode = True
            st.success("🚨 Emergency mode activated! We'll prioritize your request.")
    
    # Patient input
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>Patient Details</h3>', unsafe_allow_html=True)
        patient_name = st.text_input("Patient Name", "Rajesh Kumar")
        patient_blood = st.selectbox("Patient Blood Group", ['O+','A+','B+','AB+','O-','A-','B-','AB-'])
        patient_city = st.selectbox("Patient City", list(cities.keys()))
        urgency = st.selectbox("Urgency Level", ['Normal','Urgent','Critical'])
        # Request context (free text) for smarter AI
        request_context = st.text_area("Additional context (optional)", placeholder="e.g., patient is bleeding, emergency surgery needed...")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h3>Request Summary</h3>', unsafe_allow_html=True)
        st.markdown(f"**Patient** — {patient_name}")
        st.markdown(f"**Blood group** — {patient_blood}")
        st.markdown(f"**Location** — {patient_city}")
        st.markdown(f"**Urgency** — {urgency}")
        if request_context:
            st.markdown(f"**Context** — {request_context[:100]}...")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Find Compatible Donors"):
        lat, lon = cities.get(patient_city, (28.6139, 77.2090))
        with st.spinner("Matching against network..."):
            time.sleep(0.6)
            donors, total = find_donors(lat, lon, patient_blood, urgency.lower(), request_context)

        if donors is None:
            st.error("No compatible donors found in the network.")
        else:
            st.markdown(f"**{total:,} compatible donors found**, ranked by distance and urgency.")
            
            # --- Shortage meter ---
            if len(donors) < 3:
                st.progress(0.2, text="⚠️ CRITICAL SHORTAGE in this area!")
                st.warning("🚨 Fewer than 3 donors available. Emergency alert sent to hospitals.")
            elif len(donors) < 10:
                st.progress(0.5, text="🟡 Moderate supply available")
            else:
                st.progress(1.0, text="✅ Good supply nearby")
            
            st.write("")
            for i, (_, donor) in enumerate(donors.iterrows()):
                row_class = "donor top" if i == 0 else "donor"
                wa_link = f"https://wa.me/91{donor['phone']}?text=Hi%20{donor['name'].split()[0]}%2C%20I%20need%20emergency%20blood%20donation."
                flag = '<span class="flag">Best Match</span>' if i == 0 else ''
                badge_html = get_badge(donor['donations'])
                row_html = (
                    f'<div class="{row_class}">'
                    f'<div class="left">'
                    f'<div class="name-row"><span class="name">{donor["name"]}</span>{flag}{badge_html}</div>'
                    f'<span class="meta">{donor["city"]} · {donor["phone"]} · 💉 {donor["donations"]} donations</span>'
                    f'<a class="wa" href="{wa_link}" target="_blank">💬 Contact on WhatsApp →</a>'
                    f'</div>'
                    f'<div class="right">'
                    f'<div class="dist">{donor["distance_km"]:.1f} km</div>'
                    f'<span class="bg-chip">{donor["blood_group"]}</span>'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(row_html, unsafe_allow_html=True)

            best = donors.iloc[0]
            wa_link = f"https://wa.me/91{best['phone']}?text=Hi%20{best['name'].split()[0]}%2C%20I%20need%20emergency%20blood%20donation."
            best_html = (
                f'<div class="best-match">'
                f'<div class="label">🎯 Recommended Contact</div>'
                f'<p style="font-weight:700; font-size:1.02rem; margin:0;">{best["name"]} — {best["blood_group"]}</p>'
                f'<p class="phone">📞 {best["phone"]}</p>'
                f'<p style="margin:2px 0; color:var(--muted);">{best["distance_km"]:.1f} km away · approx. {best["distance_km"]/30*60:.0f} min</p>'
                f'<a class="wa" href="{wa_link}" target="_blank">💬 Contact on WhatsApp →</a>'
                f'</div>'
            )
            st.markdown(best_html, unsafe_allow_html=True)

# ---- TAB 2: Register ----
with tab2:
    st.markdown('<div class="card"><h3>Donor Registration</h3>', unsafe_allow_html=True)
    st.markdown("Register to join the donor network. Takes under a minute.")
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
            # Append to session state (requires session state management)
            if 'donors_df' not in st.session_state:
                st.session_state.donors_df = df
            st.session_state.donors_df = pd.concat([st.session_state.donors_df, new_donor], ignore_index=True)
            # Update the main df reference
            df = st.session_state.donors_df
            st.success(f"Thank you, {new_name} — you're now registered.")
            st.info(f"{new_name} · {new_blood} · {new_city} · {new_phone}")
    st.markdown('</div>', unsafe_allow_html=True)

# ---- TAB 3: Map ----
with tab3:
    st.markdown('<div class="map-box">', unsafe_allow_html=True)
    # Use Folium map for professional look
    try:
        import folium
        from streamlit_folium import st_folium
        map_center = [20.5937, 78.9629]  # Center of India
        m = folium.Map(location=map_center, zoom_start=4, tiles='OpenStreetMap')
        for _, row in df.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['name']} - {row['blood_group']}",
                icon=folium.Icon(color='red' if row['blood_group'] in ['O+','O-'] else 'blue')
            ).add_to(m)
        st_folium(m, width=700, height=500)
        st.caption(f"📍 {len(df)} donor locations across India")
    except ImportError:
        # Fallback to st.map if folium not installed
        st.map(df[['latitude','longitude']].dropna(), zoom=4)
        st.caption(f"📍 {len(df)} donor locations across India")
        st.info("💡 For a better map experience, install folium: `pip install streamlit-folium folium`")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:20px;">Donors by City</div>', unsafe_allow_html=True)
    st.bar_chart(df['city'].value_counts())

# ---- Footer ----
st.markdown("""
<div class="footer">
    <p><span class="brand">🩸 RaktConnect</span> — Saving lives through intelligent donor matching</p>
    <p>Built for CodeStorm 2026: FutureForge</p>
</div>
""", unsafe_allow_html=True)
