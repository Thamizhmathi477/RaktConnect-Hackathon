# ============================================
# RaktConnect — AI Emergency Blood Donor Network
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
# SESSION STATE FOR DARK MODE
# ============================================

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# ============================================
# STYLE — corporate slate/indigo palette, single accent color
# ============================================

def apply_css(dark_mode):
    if dark_mode:
        bg_main = "#0e1117"
        bg_card = "#1e1e1e"
        border_color = "#333333"
        text_color = "#fafafa"
        header_bg = "#1a1a2e"
        stat_bg = "#1e1e1e"
        footer_bg = "#1a1a2e"
        primary = "#4a8bc2"
        primary_dark = "#3a7baf"
    else:
        bg_main = "#F4F5F7"
        bg_card = "#FFFFFF"
        border_color = "#DFE2E7"
        text_color = "#161B22"
        header_bg = "#FFFFFF"
        stat_bg = "#FFFFFF"
        footer_bg = "#FFFFFF"
        primary = "#1F3A5F"
        primary_dark = "#152A45"

    return f"""
    <style>
        :root{{
            --ink:{text_color};
            --muted:#5B6472;
            --primary:{primary};
            --primary-dark:{primary_dark};
            --primary-pale:#EEF2F6;
            --accent:#B3261E;
            --accent-pale:#FBEDEC;
            --bg:{bg_main};
            --card:{bg_card};
            --line:{border_color};
            --success:#1E7B4D;
        }}
        .stApp {{ background-color: var(--bg) !important; font-family: 'Inter', sans-serif; }}
        .stApp, .stApp p, .stApp span, .stApp div, .stApp label,
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {{
            color: var(--ink);
            font-family: 'Inter', sans-serif;
        }}
        .block-container{{ max-width: 1100px; padding-top: 1.5rem; padding-bottom: 3rem; }}
        .topbar{{
            display: flex; align-items: baseline; justify-content: space-between;
            padding: 0 0 16px 0; border-bottom: 2px solid var(--primary); margin-bottom: 24px;
        }}
        .topbar .brand{{ display: flex; align-items: baseline; gap: 10px; }}
        .topbar .mark{{ font-size: 1.4rem; font-weight: 800; color: var(--primary-dark) !important; letter-spacing: -0.01em; }}
        .topbar .mark span{{ color: var(--accent) !important; }}
        .topbar .desc{{ font-size: 0.83rem; color: var(--muted) !important; }}
        .topbar .eyebrow{{ font-size: 0.66rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted) !important; font-weight: 700; }}
        .card{{ background: var(--card); padding: 22px 24px; border-radius: 6px; border: 1px solid var(--line); margin-bottom: 16px; }}
        .card h3{{
            color: var(--primary-dark) !important; font-size: 0.98rem; font-weight: 700;
            margin: 0 0 14px 0; padding-bottom: 10px; border-bottom: 1px solid var(--line);
            text-transform: uppercase; letter-spacing: 0.04em;
        }}
        .card, .card p, .card div, .card span, .card label, .card strong{{ color: var(--ink) !important; }}
        .section-label{{
            font-size: 0.7rem; letter-spacing: 0.09em; text-transform: uppercase;
            color: var(--muted) !important; font-weight: 700; margin: 4px 0 10px 0;
        }}
        section[data-testid="stSidebar"]{{ background-color: var(--card) !important; border-right: 1px solid var(--line); }}
        section[data-testid="stSidebar"] *{{ color: var(--ink) !important; }}
        section[data-testid="stSidebar"] h2{{
            font-size: 0.9rem !important; color: var(--primary-dark) !important;
            text-transform: uppercase; letter-spacing: 0.04em; font-weight: 700;
        }}
        .stSelectbox label, .stTextInput label, .stNumberInput label{{
            color: var(--muted) !important; font-weight: 600 !important; font-size: 0.76rem !important;
            text-transform: uppercase; letter-spacing: 0.04em;
        }}
        .stSelectbox div[data-baseweb="select"] *{{ color: var(--ink) !important; }}
        .stTextInput input, .stNumberInput input{{
            color: var(--ink) !important; background: var(--card) !important;
            border: 1px solid var(--line) !important; border-radius: 4px !important;
        }}
        .stTextInput input:focus, .stNumberInput input:focus{{ border-color: var(--primary) !important; }}
        .stTabs [data-baseweb="tab-list"]{{ border-bottom: 1px solid var(--line); gap: 6px; }}
        .stTabs [data-baseweb="tab"]{{ color: var(--muted) !important; font-weight: 600; font-size: 0.88rem; }}
        .stTabs [aria-selected="true"]{{ color: var(--primary-dark) !important; }}
        .stat{{ background: var(--card); padding: 14px 16px; border-radius: 6px; border: 1px solid var(--line); }}
        .stat .label{{ font-size: 0.66rem; color: var(--muted) !important; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; margin-bottom: 4px; }}
        .stat .number{{ font-size: 1.55rem; font-weight: 800; color: var(--primary-dark) !important; line-height: 1.1; }}
        .donor{{
            display: flex; justify-content: space-between; align-items: flex-start;
            background: var(--card); border: 1px solid var(--line); border-radius: 5px;
            padding: 13px 16px; margin: 6px 0;
        }}
        .donor.top{{ border-color: var(--accent); background: var(--accent-pale); }}
        .donor, .donor *{{ color: var(--ink) !important; }}
        .donor .left{{ flex: 1; }}
        .donor .name-row{{ display: flex; align-items: center; gap: 8px; margin-bottom: 2px; }}
        .donor .name{{ font-size: 0.94rem; font-weight: 700; }}
        .donor .flag{{ font-size: 0.64rem; font-weight: 700; color: var(--accent) !important; text-transform: uppercase; letter-spacing: 0.04em; }}
        .donor .meta{{ font-size: 0.8rem; color: var(--muted) !important; }}
        .donor .right{{ text-align: right; flex-shrink: 0; padding-left: 14px; }}
        .donor .dist{{ font-size: 1rem; font-weight: 700; color: var(--primary-dark) !important; }}
        .donor .bg-chip{{
            display: inline-block; background: var(--primary); color: #fff !important;
            padding: 2px 8px; border-radius: 3px; font-size: 0.7rem; font-weight: 700; margin-top: 3px;
        }}
        .donor .wa{{
            display: block; margin-top: 5px; font-size: 0.76rem; font-weight: 600;
            color: var(--primary-dark) !important; text-decoration: none; border-bottom: 1px solid var(--primary-dark);
        }}
        .best-match{{
            background: var(--card); border: 1px solid var(--line); border-left: 4px solid var(--accent);
            padding: 16px 20px; border-radius: 6px; margin-top: 12px;
        }}
        .best-match, .best-match *{{ color: var(--ink) !important; }}
        .best-match .label{{ font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--accent) !important; font-weight: 700; margin-bottom: 6px; }}
        .best-match .phone{{ font-size: 1.05rem; font-weight: 700; color: var(--primary-dark) !important; }}
        .shortage-note{{
            background: #FDF3E3; border: 1px solid #C99A2E; border-left: 4px solid #C99A2E;
            padding: 10px 14px; border-radius: 4px; font-size: 0.84rem; color: var(--ink) !important; margin: 8px 0;
        }}
        .confirm{{
            background: var(--card); border: 1px solid var(--line); border-left: 4px solid var(--success);
            border-radius: 6px; padding: 20px 24px; margin-top: 14px;
        }}
        .confirm, .confirm *{{ color: var(--ink) !important; }}
        .confirm .check{{
            display: inline-flex; align-items: center; justify-content: center;
            width: 22px; height: 22px; border-radius: 50%; background: var(--success);
            color: #fff !important; font-size: 0.78rem; font-weight: 800; margin-right: 8px;
        }}
        .confirm .title{{ font-size: 1rem; font-weight: 700; color: var(--success) !important; display: flex; align-items: center; margin-bottom: 10px; }}
        .confirm .row{{ display: flex; gap: 8px; font-size: 0.88rem; padding: 3px 0; }}
        .confirm .row .k{{ color: var(--muted) !important; min-width: 90px; }}
        .confirm .row .v{{ font-weight: 600; }}
        .stButton button{{
            background: var(--primary) !important; color: #FFFFFF !important;
            font-weight: 600 !important; font-size: 0.88rem !important;
            padding: 10px 22px !important; border: none !important;
            border-radius: 4px !important; width: 100% !important;
        }}
        .stButton button:hover{{ background: var(--primary-dark) !important; }}
        .footer{{ text-align: center; padding: 16px; border-top: 1px solid var(--line); margin-top: 30px; }}
        .footer p{{ color: var(--muted) !important; font-size: 0.78rem; margin: 2px 0; }}
        .footer .brand{{ color: var(--primary-dark) !important; font-weight: 700; }}
        .map-box{{ background: var(--card); padding: 16px; border-radius: 6px; border: 1px solid var(--line); }}
        div[data-testid="stDataFrame"]{{ border: 1px solid var(--line); border-radius: 6px; overflow: hidden; }}
        .stDataFrame thead th{{ background: var(--card) !important; color: var(--ink) !important; }}
        .stDataFrame tbody td{{ background: var(--card) !important; color: var(--ink) !important; }}
    </style>
    """

st.markdown(apply_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ============================================
# TOP BAR
# ============================================

st.markdown("""
<div class="topbar">
    <div class="brand">
        <span class="mark">Rakt<span>Connect</span></span>
        <span class="desc">Emergency Blood Donor Network</span>
    </div>
    <span class="eyebrow">Prototype · CodeStorm 2026</span>
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

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("## Top Contributors")
    for _, row in df.nlargest(5, 'donations')[['name','donations']].iterrows():
        st.markdown(f"<div style='font-size:0.85rem; padding:4px 0; border-bottom:1px solid var(--line);'>{row['name']} <span style='color:var(--muted);float:right;'>{row['donations']}</span></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Dark Mode Toggle ---
    dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="dark_mode_toggle")
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()

# ============================================
# TABS
# ============================================

tab1, tab2, tab3, tab4 = st.tabs(["🔍 Find Donors", "📋 Browse Directory", "📝 Register", "🗺️ Map"])

# ---- TAB 1: FIND DONORS ----
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>Patient Details</h3>', unsafe_allow_html=True)
        patient_name = st.text_input("Patient Name", "Rajesh Kumar", key="patient_name")
        patient_blood = st.selectbox("Patient Blood Group", ['O+','A+','B+','AB+','O-','A-','B-','AB-'], key="patient_blood")
        patient_city = st.selectbox("Patient City", list(cities.keys()), key="patient_city")
        urgency = st.selectbox("Urgency Level", ['Normal','Urgent','Critical'], key="urgency")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><h3>Request Summary</h3>', unsafe_allow_html=True)
        st.markdown(f"**Patient** — {patient_name}")
        st.markdown(f"**Blood group** — {patient_blood}")
        st.markdown(f"**Location** — {patient_city}")
        st.markdown(f"**Urgency** — {urgency}")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Find Compatible Donors", key="find_donors_btn"):
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
                row_html = (
                    f'<div class="{row_class}">'
                    f'<div class="left">'
                    f'<div class="name-row"><span class="name">{donor["name"]}</span>{flag}</div>'
                    f'<span class="meta">{donor["city"]} · {badge(donor["donations"])} · {donor["phone"]}</span>'
                    f'<a class="wa" href="{wa_link}" target="_blank">Contact on WhatsApp →</a>'
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
                f'<p style="font-weight:700; font-size:1rem; margin:0;">{best["name"]} — {best["blood_group"]}</p>'
                f'<p class="phone">{best["phone"]}</p>'
                f'<p style="margin:2px 0; color:var(--muted);">{best["distance_km"]:.1f} km away · approx. {best["distance_km"]/30*60:.0f} min</p>'
                f'<a class="wa" href="{wa_link}" target="_blank">Contact on WhatsApp →</a>'
                f'</div>'
            )
            st.markdown(best_html, unsafe_allow_html=True)

# ---- TAB 2: BROWSE DIRECTORY (with Search, Rows Slider, CSV Download) ----
with tab2:
    st.markdown('<div class="card"><h3>Filter Directory</h3>', unsafe_allow_html=True)
    
    # --- Search by Name (NEW) ---
    search_name = st.text_input("🔍 Search by Name", placeholder="Type donor name...", key="search_name_dir")
    
    f1, f2, f3 = st.columns(3)
    with f1:
        filter_bg = st.selectbox("Blood Group", ['All'] + ['O+','A+','B+','AB+','O-','A-','B-','AB-'], key="dir_filter_bg")
    with f2:
        filter_city = st.selectbox("City", ['All'] + list(cities.keys()), key="dir_filter_city")
    with f3:
        filter_avail = st.selectbox("Availability", ['All', 'Available only'], key="dir_filter_avail")
    st.markdown('</div>', unsafe_allow_html=True)

    view = df.copy()
    if filter_bg != 'All':
        view = view[view['blood_group'] == filter_bg]
    if filter_city != 'All':
        view = view[view['city'] == filter_city]
    if filter_avail == 'Available only':
        view = view[view['available'] == 'Yes']
    if search_name:
        view = view[view['name'].str.contains(search_name, case=False)]

    st.markdown(f'<div class="section-label">{len(view):,} donors match your filters</div>', unsafe_allow_html=True)

    # --- Rows Slider (NEW) ---
    rows_to_show = st.slider("Rows to display", min_value=10, max_value=500, value=100, step=10, key="rows_slider")

    display_df = view[['name', 'blood_group', 'city', 'phone', 'available', 'donations']].rename(columns={
        'name': 'Name', 'blood_group': 'Blood Group', 'city': 'City',
        'phone': 'Phone', 'available': 'Available', 'donations': 'Donations'
    }).head(rows_to_show)

    st.dataframe(display_df, use_container_width=True, height=460, hide_index=True)
    if len(view) > rows_to_show:
        st.caption(f"Showing first {rows_to_show} of {len(view):,} donors. Adjust the slider to see more.")

    # --- CSV Download (NEW) ---
    csv = view.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="raktconnect_donors.csv",
        mime="text/csv",
        key="download_csv"
    )

# ---- TAB 3: REGISTER AS DONOR ----
with tab3:
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

    if st.button("Register as Donor", key="register_btn"):
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

            donor_id = f"RC-{len(st.session_state.donors_df):06d}"
            confirm_html = (
                f'<div class="confirm">'
                f'<div class="title"><span class="check">✓</span>Registration Confirmed</div>'
                f'<div class="row"><span class="k">Donor ID</span><span class="v">{donor_id}</span></div>'
                f'<div class="row"><span class="k">Name</span><span class="v">{new_name}</span></div>'
                f'<div class="row"><span class="k">Blood Group</span><span class="v">{new_blood}</span></div>'
                f'<div class="row"><span class="k">City</span><span class="v">{new_city}</span></div>'
                f'<div class="row"><span class="k">Phone</span><span class="v">{new_phone}</span></div>'
                f'<div class="row"><span class="k">Status</span><span class="v">{"Available" if new_available == "Yes" else "Not available"}</span></div>'
                f'<p style="margin-top:12px; font-size:0.85rem; color:var(--muted);">Thank you for registering, {new_name.split()[0]}. You may be contacted when a compatible patient nearby needs your blood group.</p>'
                f'</div>'
            )
            st.markdown(confirm_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---- TAB 4: DONOR MAP ----
with tab4:
    st.markdown('<div class="map-box">', unsafe_allow_html=True)
    map_df = df[['latitude','longitude']].dropna()
    if len(map_df) > 0:
        st.map(map_df, zoom=4)
        st.caption(f"📍 {len(map_df)} donor locations across India")
    else:
        st.warning("No donor location data available.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:20px;">Donors by City</div>', unsafe_allow_html=True)
    st.bar_chart(df['city'].value_counts())

    st.markdown('<div class="section-label" style="margin-top:20px;">Available Donors by Blood Group — All India</div>', unsafe_allow_html=True)
    bg_available = df[df['available'] == 'Yes']['blood_group'].value_counts()
    st.bar_chart(bg_available)

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
    <p><span class="brand">RaktConnect</span> — Saving lives through intelligent donor matching</p>
    <p>Built for CodeStorm 2026: FutureForge</p>
</div>
""", unsafe_allow_html=True)
