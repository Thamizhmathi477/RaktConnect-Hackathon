# ============================================
# RaktConnect — AI Emergency Blood Donor Network
# CodeStorm 2026 — FutureForge
# Professional edition
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, asin
import time

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="RaktConnect — Emergency Blood Donor Network",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# STYLE — clinical, professional palette
# Primary: deep teal (trust, medical) | Accent: muted crimson (urgency, used sparingly)
# ============================================

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+Pro:wght@600;700&display=swap" rel="stylesheet">
<style>
    :root{
        --ink:#1C2530;
        --muted:#5B6675;
        --teal:#0E5C56;
        --teal-dark:#0A423E;
        --crimson:#A6303C;
        --bg:#F6F5F2;
        --card:#FFFFFF;
        --line:#E3E1DB;
        --amber:#B8862E;
    }

    .stApp { background-color: var(--bg) !important; font-family: 'Inter', sans-serif; }
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
        color: var(--ink);
        font-family: 'Inter', sans-serif;
    }

    /* ---- Header ---- */
    .hdr{
        background: var(--teal);
        padding: 34px 36px;
        border-radius: 4px;
        margin-bottom: 28px;
        border-left: 6px solid var(--crimson);
    }
    .hdr .eyebrow{
        color: #B7D9D5 !important;
        font-size: 0.72rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .hdr h1{
        font-family: 'Source Serif Pro', serif !important;
        color: #FFFFFF !important;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.01em;
    }
    .hdr .tagline{
        color: #DCEAE8 !important;
        font-size: 1rem;
        margin-top: 8px;
        font-weight: 400;
    }

    /* ---- Cards ---- */
    .card{
        background: var(--card);
        padding: 26px 28px;
        border-radius: 4px;
        border: 1px solid var(--line);
        margin-bottom: 18px;
    }
    .card h3{
        font-family: 'Source Serif Pro', serif !important;
        color: var(--teal-dark) !important;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 16px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--line);
    }
    .card, .card p, .card div, .card span, .card label, .card strong{
        color: var(--ink) !important;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"]{ background-color: #FFFFFF !important; border-right: 1px solid var(--line); }
    section[data-testid="stSidebar"] *{ color: var(--ink) !important; }
    section[data-testid="stSidebar"] h2{
        font-family: 'Source Serif Pro', serif !important;
        font-size: 1.05rem !important;
        color: var(--teal-dark) !important;
    }

    /* ---- Inputs ---- */
    .stSelectbox label, .stTextInput label, .stNumberInput label{
        color: var(--muted) !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .stSelectbox div[data-baseweb="select"] *{ color: var(--ink) !important; }
    .stTextInput input, .stNumberInput input{
        color: var(--ink) !important;
        background: #FFFFFF !important;
        border: 1px solid var(--line) !important;
        border-radius: 3px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus{
        border-color: var(--teal) !important;
    }

    /* ---- Tabs ---- */
    .stTabs [data-baseweb="tab-list"]{ border-bottom: 1px solid var(--line); gap: 4px; }
    .stTabs [data-baseweb="tab"]{
        color: var(--muted) !important;
        font-weight: 600;
        font-size: 0.92rem;
    }
    .stTabs [aria-selected="true"]{ color: var(--teal-dark) !important; }

    /* ---- Stat blocks ---- */
    .stat{
        background: #FFFFFF;
        padding: 16px 18px;
        border-radius: 4px;
        border: 1px solid var(--line);
        border-top: 3px solid var(--teal);
    }
    .stat .number{ font-size: 1.9rem; font-weight: 700; color: var(--teal-dark) !important; font-family: 'Source Serif Pro', serif; }
    .stat .label{ font-size: 0.74rem; color: var(--muted) !important; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 600; }

    /* ---- Donor row ---- */
    .donor-row{
        background: #FFFFFF;
        padding: 16px 20px;
        border-radius: 3px;
        border: 1px solid var(--line);
        border-left: 3px solid var(--teal);
        margin: 8px 0;
    }
    .donor-row.rank1{ border-left: 3px solid var(--crimson); background: #FBF3F2; }
    .donor-row, .donor-row *{ color: var(--ink) !important; }
    .donor-row .name{ font-size: 1.02rem; font-weight: 700; }
    .donor-row .meta{ font-size: 0.86rem; color: var(--muted) !important; }
    .donor-row .bg-tag{
        display: inline-block; background: var(--teal); color: #fff !important;
        padding: 2px 9px; border-radius: 3px; font-size: 0.78rem; font-weight: 700;
    }

    .wa-link{
        display: inline-block;
        margin-top: 8px;
        color: var(--teal-dark) !important;
        font-size: 0.85rem;
        font-weight: 600;
        text-decoration: none;
        border-bottom: 1px solid var(--teal-dark);
    }

    .best-match{
        background: #FFFFFF;
        border: 1px solid var(--crimson);
        border-top: 4px solid var(--crimson);
        padding: 20px 24px;
        border-radius: 4px;
        margin-top: 14px;
    }
    .best-match, .best-match *{ color: var(--ink) !important; }
    .best-match .label{
        font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em;
        color: var(--crimson) !important; font-weight: 700; margin-bottom: 6px;
    }
    .best-match .phone{ font-size: 1.15rem; font-weight: 700; color: var(--teal-dark) !important; }

    .stButton button{
        background: var(--teal) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 11px 28px !important;
        border: none !important;
        border-radius: 3px !important;
        width: 100% !important;
        letter-spacing: 0.01em;
    }
    .stButton button:hover{ background: var(--teal-dark) !important; }

    .footer{
        text-align: center; padding: 20px; background: var(--teal-dark);
        border-radius: 4px; margin-top: 28px;
    }
    .footer, .footer p{ color: #DCEAE8 !important; font-size: 0.85rem; margin: 3px 0; }
    .footer .brand{ color: #FFFFFF !important; font-weight: 700; }

    .map-box{ background: #FFFFFF; padding: 16px; border-radius: 4px; border: 1px solid var(--line); }

    .shortage-note{
        background: #FBF3E7; border: 1px solid var(--amber); border-left: 4px solid var(--amber);
        padding: 12px 16px; border-radius: 3px; font-size: 0.9rem; color: var(--ink) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

st.markdown("""
<div class="hdr">
    <div class="eyebrow">Prototype · Emergency Response</div>
    <h1>RaktConnect</h1>
    <p class="tagline">Matching patients to the nearest medically compatible blood donor.</p>
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
df = st.session_state.donors_df

cities = {
    'Delhi': (28.6139, 77.2090), 'Mumbai': (19.0760, 72.8777),
    'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867), 'Kolkata': (22.5726, 88.3639),
    'Pune': (18.5204, 73.8567), 'Ahmedabad': (23.0225, 72.5714),
    'Jaipur': (26.9124, 75.7873), 'Lucknow': (26.8467, 80.9462)
}

# ============================================
# COMPATIBILITY & MATCHING (medically correct: key = patient, value = eligible donors)
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
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("## Network Overview")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="stat"><div class="number">{len(df):,}</div><div class="label">Total Donors</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat"><div class="number">{len(df[df["available"]=="Yes"]):,}</div><div class="label">Available</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Top contributors**")
    for _, row in df.nlargest(5, 'donations')[['name','donations']].iterrows():
        st.markdown(f"<span style='font-size:0.88rem'>{row['name']} — {row['donations']} donations</span>", unsafe_allow_html=True)

# ============================================
# TABS
# ============================================

tab1, tab2, tab3 = st.tabs(["Find Donors", "Register as Donor", "Donor Map"])

# ---- TAB 1 ----
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

    if st.button("Find Compatible Donors"):
        lat, lon = cities.get(patient_city, (28.6139, 77.2090))
        with st.spinner("Matching against network..."):
            time.sleep(0.6)
            donors, total = find_donors(lat, lon, patient_blood, urgency.lower())

        if donors is None:
            st.error("No compatible donors found in the network.")
        else:
            st.markdown(f"**{total:,} compatible donors found**, ranked by distance and urgency.")
            if len(donors) < 3:
                st.markdown('<div class="shortage-note">Shortage alert — fewer than 3 compatible donors nearby.</div>', unsafe_allow_html=True)

            st.write("")
            for i, (_, donor) in enumerate(donors.iterrows()):
                row_class = "donor-row rank1" if i == 0 else "donor-row"
                wa_link = f"https://wa.me/91{donor['phone']}?text=Hi%20{donor['name'].split()[0]}%2C%20I%20need%20emergency%20blood%20donation."
                st.markdown(f"""
                <div class="{row_class}">
                    <span class="name">{donor['name']}</span>
                    {' <span style="color:var(--crimson);font-size:0.8rem;font-weight:700;">· BEST MATCH</span>' if i==0 else ''}
                    <span class="bg-tag" style="margin-left:8px;">{donor['blood_group']}</span><br>
                    <span class="meta">{donor['city']} · {donor['distance_km']:.1f} km away · {badge(donor['donations'])}</span><br>
                    <span class="meta">{donor['phone']}</span>
                    <a class="wa-link" href="{wa_link}" target="_blank">Contact on WhatsApp →</a>
                </div>
                """, unsafe_allow_html=True)

            best = donors.iloc[0]
            wa_link = f"https://wa.me/91{best['phone']}?text=Hi%20{best['name'].split()[0]}%2C%20I%20need%20emergency%20blood%20donation."
            st.markdown(f"""
            <div class="best-match">
                <div class="label">Recommended Contact</div>
                <p style="font-weight:700; font-size:1.05rem; margin:0;">{best['name']} — {best['blood_group']}</p>
                <p class="phone">{best['phone']}</p>
                <p style="margin:2px 0;">{best['distance_km']:.1f} km away · approx. {best['distance_km']/30*60:.0f} min</p>
                <a class="wa-link" href="{wa_link}" target="_blank">Contact on WhatsApp →</a>
            </div>
            """, unsafe_allow_html=True)

# ---- TAB 2 ----
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

    if st.button("Register as Donor"):
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
            st.success(f"Thank you, {new_name} — you're now registered.")
            st.info(f"{new_name} · {new_blood} · {new_city} · {new_phone}")
    st.markdown('</div>', unsafe_allow_html=True)

# ---- TAB 3 ----
with tab3:
    st.markdown('<div class="map-box">', unsafe_allow_html=True)
    map_df = df[['latitude','longitude']].dropna()
    if len(map_df) > 0:
        st.map(map_df, zoom=4)
        st.caption(f"{len(map_df)} donor locations across India")
    else:
        st.warning("No donor location data available.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>**Donors by city**", unsafe_allow_html=True)
    st.bar_chart(df['city'].value_counts())

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
    <p class="brand">RaktConnect</p>
    <p>Built for CodeStorm 2026: FutureForge</p>
</div>
""", unsafe_allow_html=True)
