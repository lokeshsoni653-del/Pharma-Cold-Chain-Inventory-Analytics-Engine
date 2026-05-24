"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     CCL PHARMACEUTICALS — PHARMA COLD-CHAIN & INVENTORY ANALYTICS ENGINE    ║
║     Digital Transformation Internship — Portfolio Flagship Project           ║
║     Stack: Streamlit · Pandas · NumPy · Plotly · Folium                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import random

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION — must be the very first Streamlit call
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CCL Pharma | Cold-Chain Analytics",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — Premium Corporate Medical Aesthetic
# Deep medical blues, pure whites, strict alert reds, elevated KPI cards
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Root Variables ── */
:root {
    --blue-deep:    #004C97;
    --blue-mid:     #0068C9;
    --blue-light:   #E8F1FB;
    --blue-accent:  #00A3E0;
    --red-alert:    #D32F2F;
    --red-soft:     #FFEBEE;
    --green-ok:     #2E7D32;
    --green-soft:   #E8F5E9;
    --amber:        #F57C00;
    --amber-soft:   #FFF3E0;
    --white:        #FFFFFF;
    --grey-50:      #F8FAFC;
    --grey-100:     #F1F5F9;
    --grey-200:     #E2E8F0;
    --grey-400:     #94A3B8;
    --grey-700:     #334155;
    --grey-900:     #0F172A;
    --shadow-sm:    0 1px 3px rgba(0,76,151,0.08), 0 1px 2px rgba(0,76,151,0.06);
    --shadow-md:    0 4px 16px rgba(0,76,151,0.10), 0 2px 6px rgba(0,76,151,0.08);
    --shadow-lg:    0 8px 32px rgba(0,76,151,0.14), 0 4px 12px rgba(0,76,151,0.10);
    --radius:       12px;
    --radius-sm:    8px;
}

/* ── Base Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--grey-700);
}

/* ── Main Background ── */
.stApp {
    background: linear-gradient(160deg, #F0F6FF 0%, #F8FAFC 50%, #EEF4FF 100%);
    min-height: 100vh;
}

/* ── Remove Streamlit Default Padding & Margins ── */
.block-container {
    padding: 1.5rem 2rem 2rem 2rem !important;
    max-width: 1600px;
}

/* ── Header Banner ── */
.ccl-header {
    background: linear-gradient(135deg, var(--blue-deep) 0%, #003070 60%, #001F4E 100%);
    border-radius: var(--radius);
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}
.ccl-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(0,163,224,0.12);
}
.ccl-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 160px; height: 160px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
}
.ccl-header h1 {
    color: var(--white) !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    margin: 0 0 0.35rem 0 !important;
    letter-spacing: -0.02em;
}
.ccl-header p {
    color: rgba(255,255,255,0.72) !important;
    font-size: 0.875rem !important;
    margin: 0 !important;
    font-weight: 400;
}
.ccl-header .badge {
    display: inline-block;
    background: rgba(0,163,224,0.25);
    border: 1px solid rgba(0,163,224,0.4);
    color: #7DD3F8;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.25rem 0.65rem;
    border-radius: 20px;
    margin-bottom: 0.65rem;
}

/* ── Filter Strip ── */
.filter-strip {
    background: var(--white);
    border-radius: var(--radius-sm);
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--grey-200);
    display: flex;
    align-items: center;
    gap: 1rem;
}
.filter-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--grey-400);
    white-space: nowrap;
}

/* ── Streamlit Select Widgets Override ── */
.stSelectbox > div > div {
    border-radius: var(--radius-sm) !important;
    border-color: var(--grey-200) !important;
    font-size: 0.875rem !important;
}
.stSelectbox > div > div:focus-within {
    border-color: var(--blue-mid) !important;
    box-shadow: 0 0 0 2px rgba(0,104,201,0.15) !important;
}

/* ── KPI Cards ── */
.kpi-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.4rem 1.5rem;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--grey-200);
    border-top: 3px solid var(--blue-mid);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}
.kpi-card.alert {
    border-top-color: var(--red-alert);
    background: linear-gradient(180deg, var(--red-soft) 0%, var(--white) 100%);
}
.kpi-card.warn {
    border-top-color: var(--amber);
    background: linear-gradient(180deg, var(--amber-soft) 0%, var(--white) 100%);
}
.kpi-card.good {
    border-top-color: var(--green-ok);
    background: linear-gradient(180deg, var(--green-soft) 0%, var(--white) 100%);
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--grey-400);
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.35rem;
    font-variant-numeric: tabular-nums;
    color: var(--grey-900);
}
.kpi-value.alert-text { color: var(--red-alert); }
.kpi-value.warn-text  { color: var(--amber); }
.kpi-value.good-text  { color: var(--green-ok); }
.kpi-sub {
    font-size: 0.78rem;
    color: var(--grey-400);
    display: flex;
    align-items: center;
    gap: 0.3rem;
}
.kpi-icon {
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
}

/* ── Section Headers ── */
.section-header {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--blue-deep);
    border-left: 3px solid var(--blue-accent);
    padding-left: 0.65rem;
    margin: 1.5rem 0 0.85rem 0;
}

/* ── Chart Panels ── */
.chart-panel {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.25rem;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--grey-200);
    margin-bottom: 1rem;
}
.chart-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--grey-900);
    margin-bottom: 0.25rem;
}
.chart-subtitle {
    font-size: 0.72rem;
    color: var(--grey-400);
    margin-bottom: 0.75rem;
}

/* ── Map Container ── */
.map-panel {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.25rem;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--grey-200);
    margin-bottom: 1.5rem;
}

/* ── Status Pills ── */
.pill {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.pill-green  { background: var(--green-soft);  color: var(--green-ok); }
.pill-red    { background: var(--red-soft);    color: var(--red-alert); }
.pill-amber  { background: var(--amber-soft);  color: var(--amber); }
.pill-blue   { background: var(--blue-light);  color: var(--blue-deep); }

/* ── Data Table ── */
.stDataFrame { border-radius: var(--radius-sm); overflow: hidden; }

/* ── Footer ── */
.ccl-footer {
    text-align: center;
    padding: 1.5rem 0 0.5rem 0;
    color: var(--grey-400);
    font-size: 0.72rem;
}

/* ── Divider ── */
hr { border-color: var(--grey-200) !important; margin: 1.5rem 0 !important; }

/* ── Mono Font for IDs ── */
.mono { font-family: 'DM Mono', monospace; font-size: 0.82rem; }

/* Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS — Geographic Coordinates & Config
# ─────────────────────────────────────────────────────────────────────────────
LAHORE_HUB = {"name": "Lahore (Manufacturing Hub)", "lat": 31.5204, "lon": 74.3587}

DISTRIBUTION_CENTERS = [
    {"name": "Karachi DC",    "lat": 24.8607, "lon": 67.0011, "region": "South"},
    {"name": "Islamabad DC",  "lat": 33.6844, "lon": 73.0479, "region": "North"},
    {"name": "Multan DC",     "lat": 30.1575, "lon": 71.5249, "region": "Central"},
    {"name": "Peshawar DC",   "lat": 34.0151, "lon": 71.5249, "region": "KPK"},
    {"name": "Quetta DC",     "lat": 30.1798, "lon": 66.9750, "region": "Balochistan"},
    {"name": "Faisalabad DC", "lat": 31.4180, "lon": 73.0790, "region": "Punjab"},
]

PRODUCT_CATEGORIES = ["Vaccines", "Antibiotics", "Biologics", "Oncology", "Plasma Derivatives"]
TRANSIT_STATUSES   = ["In Transit", "Delivered", "Alert"]

# Temperature requirements per category (min_C, max_C)
TEMP_REQUIREMENTS = {
    "Vaccines":           (2.0,  8.0),
    "Antibiotics":        (15.0, 25.0),
    "Biologics":          (2.0,  8.0),
    "Oncology":           (2.0,  8.0),
    "Plasma Derivatives": (-20.0, -15.0),
}


# ─────────────────────────────────────────────────────────────────────────────
# DATA GENERATION — Cached for performance
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)  # Cache for 5 minutes
def generate_shipment_data(n_shipments: int = 48) -> pd.DataFrame:
    """
    Generate highly realistic synthetic pharmaceutical shipment data.
    Each row represents one active batch shipment from the Lahore hub.
    """
    np.random.seed(42)
    random.seed(42)

    today = datetime.now()
    records = []

    for i in range(n_shipments):
        category    = random.choice(PRODUCT_CATEGORIES)
        destination = random.choice(DISTRIBUTION_CENTERS)
        temp_min, temp_max = TEMP_REQUIREMENTS[category]

        # Manufacture & expiry dates (more realistic distribution)
        mfg_date    = today - timedelta(days=random.randint(10, 300))
        shelf_life  = random.randint(90, 730)   # days
        expiry_date = mfg_date + timedelta(days=shelf_life)
        days_to_exp = (expiry_date - today).days

        # Current temperature — introduce realistic variance + some breaches
        temp_center = (temp_min + temp_max) / 2
        temp_std    = (temp_max - temp_min) * 0.35
        current_temp = round(np.random.normal(temp_center, temp_std), 1)

        # Determine if there's a breach
        is_breach = current_temp < temp_min or current_temp > temp_max

        # Bias transit status: alerts correlate with breaches
        if is_breach:
            status = "Alert"
        elif random.random() < 0.35:
            status = "Delivered"
        else:
            status = "In Transit"

        # Shipment volume (units)
        units = random.randint(500, 25000)

        # Batch ID
        batch_id = f"CCL-{category[:3].upper()}-{1000 + i:04d}"

        records.append({
            "batch_id":       batch_id,
            "category":       category,
            "destination":    destination["name"],
            "dest_lat":       destination["lat"],
            "dest_lon":       destination["lon"],
            "region":         destination["region"],
            "status":         status,
            "current_temp":   current_temp,
            "temp_min":       temp_min,
            "temp_max":       temp_max,
            "is_breach":      is_breach,
            "mfg_date":       mfg_date.date(),
            "expiry_date":    expiry_date.date(),
            "days_to_expiry": days_to_exp,
            "units":          units,
            "dispatch_date":  (today - timedelta(days=random.randint(1, 14))).date(),
        })

    df = pd.DataFrame(records)
    return df


@st.cache_data(ttl=300)
def generate_temperature_timeline(df: pd.DataFrame, n_points: int = 50) -> pd.DataFrame:
    """
    Simulate a time-series temperature log for currently active shipments.
    Returns melted DataFrame suitable for a multi-line Plotly chart.
    """
    np.random.seed(99)
    active = df[df["status"] == "In Transit"].head(6)  # show up to 6 shipments
    timestamps = pd.date_range(end=datetime.now(), periods=n_points, freq="30min")
    rows = []

    for _, row in active.iterrows():
        mid   = (row["temp_min"] + row["temp_max"]) / 2
        noise = (row["temp_max"] - row["temp_min"]) * 0.4
        temps = np.cumsum(np.random.randn(n_points) * 0.3) + mid
        # Inject a realistic drift toward end
        temps += np.linspace(0, noise * random.choice([-1, 1]), n_points)
        for ts, t in zip(timestamps, temps):
            rows.append({
                "timestamp":  ts,
                "batch_id":   row["batch_id"],
                "category":   row["category"],
                "temp":       round(t, 2),
                "temp_min":   row["temp_min"],
                "temp_max":   row["temp_max"],
            })

    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
df_all     = generate_shipment_data(n_shipments=48)
df_temp_ts = generate_temperature_timeline(df_all)


# ─────────────────────────────────────────────────────────────────────────────
# HEADER BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ccl-header">
    <div class="badge">🔬 Digital Transformation Initiative</div>
    <h1>Pharma Cold-Chain &amp; Inventory Analytics Engine</h1>
    <p>Real-time batch tracking · Temperature integrity monitoring · FIFO expiry management · Pakistan distribution network</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL FILTERS — control row
# ─────────────────────────────────────────────────────────────────────────────
f_col1, f_col2, f_col3, f_col4 = st.columns([1, 2, 2, 5])

with f_col1:
    st.markdown('<div class="filter-label">🔽 Filters</div>', unsafe_allow_html=True)

with f_col2:
    sel_category = st.selectbox(
        "Product Category",
        options=["All Categories"] + PRODUCT_CATEGORIES,
        label_visibility="collapsed",
    )

with f_col3:
    sel_status = st.selectbox(
        "Transit Status",
        options=["All Statuses"] + TRANSIT_STATUSES,
        label_visibility="collapsed",
    )

with f_col4:
    st.markdown(
        f'<div style="font-size:0.75rem; color:#94A3B8; padding-top:0.6rem;">'
        f'Last refreshed: {datetime.now().strftime("%d %b %Y, %H:%M:%S")} PKT &nbsp;|&nbsp; '
        f'Hub: Lahore Manufacturing Facility &nbsp;|&nbsp; '
        f'Distribution Centers: {len(DISTRIBUTION_CENTERS)}</div>',
        unsafe_allow_html=True,
    )

# Apply filters
df = df_all.copy()
if sel_category != "All Categories":
    df = df[df["category"] == sel_category]
if sel_status != "All Statuses":
    df = df[df["status"] == sel_status]


# ─────────────────────────────────────────────────────────────────────────────
# KPI ROW — 4 elevated cards
# ─────────────────────────────────────────────────────────────────────────────
total_active   = len(df[df["status"] == "In Transit"])
temp_alerts    = len(df[df["is_breach"] == True])
expiring_soon  = len(df[df["days_to_expiry"] <= 30])
integrity_pct  = round((1 - temp_alerts / max(len(df), 1)) * 100, 1)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🚚</div>
        <div class="kpi-label">Total Active Shipments</div>
        <div class="kpi-value">{total_active}</div>
        <div class="kpi-sub">📦 {len(df)} batches in current view</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    alert_class = "alert" if temp_alerts > 0 else "good"
    val_class   = "alert-text" if temp_alerts > 0 else "good-text"
    st.markdown(f"""
    <div class="kpi-card {alert_class}">
        <div class="kpi-icon">🌡️</div>
        <div class="kpi-label">Critical Temperature Alerts</div>
        <div class="kpi-value {val_class}">{temp_alerts}</div>
        <div class="kpi-sub">{'⚠️ Immediate action required' if temp_alerts > 0 else '✅ All within safe range'}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    warn_class = "warn" if expiring_soon > 0 else "good"
    val_class2 = "warn-text" if expiring_soon > 0 else "good-text"
    st.markdown(f"""
    <div class="kpi-card {warn_class}">
        <div class="kpi-icon">⏳</div>
        <div class="kpi-label">Batches Expiring &lt; 30 Days</div>
        <div class="kpi-value {val_class2}">{expiring_soon}</div>
        <div class="kpi-sub">{'⚡ FIFO priority required' if expiring_soon > 0 else '✅ Stock rotation healthy'}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    integrity_class = "good" if integrity_pct >= 90 else ("warn" if integrity_pct >= 75 else "alert")
    int_val_class   = "good-text" if integrity_pct >= 90 else ("warn-text" if integrity_pct >= 75 else "alert-text")
    st.markdown(f"""
    <div class="kpi-card {integrity_class}">
        <div class="kpi-icon">🛡️</div>
        <div class="kpi-label">Cold-Chain Integrity Score</div>
        <div class="kpi-value {int_val_class}">{integrity_pct}%</div>
        <div class="kpi-sub">{'🏆 Excellent' if integrity_pct >= 90 else ('⚠️ Needs attention' if integrity_pct >= 75 else '🚨 Critical')}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# GEOSPATIAL MAP — Folium with route lines & colour-coded markers
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🗺️ GEOSPATIAL DISTRIBUTION NETWORK</div>', unsafe_allow_html=True)

st.markdown('<div class="map-panel">', unsafe_allow_html=True)
mc1, mc2 = st.columns([3, 1])

with mc2:
    st.markdown("""
    <div style="padding: 0.5rem;">
        <div style="font-size:0.78rem; font-weight:600; color:#334155; margin-bottom:0.75rem;">MAP LEGEND</div>
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem; font-size:0.75rem;">
            <div style="width:14px;height:14px;border-radius:50%;background:#004C97;flex-shrink:0;"></div>
            Lahore Hub (Origin)
        </div>
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem; font-size:0.75rem;">
            <div style="width:14px;height:14px;border-radius:50%;background:#2E7D32;flex-shrink:0;"></div>
            In Transit (OK)
        </div>
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem; font-size:0.75rem;">
            <div style="width:14px;height:14px;border-radius:50%;background:#D32F2F;flex-shrink:0;"></div>
            Temperature Alert
        </div>
        <div style="display:flex; align-items:center; gap:0.5rem; font-size:0.75rem;">
            <div style="width:14px;height:14px;border-radius:50%;background:#94A3B8;flex-shrink:0;"></div>
            Delivered
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Summary stats per destination
    if not df.empty:
        dest_summary = df.groupby("destination").agg(
            Shipments=("batch_id", "count"),
            Alerts=("is_breach", "sum"),
        ).reset_index()
        st.markdown(
            '<div style="font-size:0.78rem; font-weight:600; color:#334155; margin:1rem 0 0.5rem 0;">DC SHIPMENT LOAD</div>',
            unsafe_allow_html=True
        )
        for _, row in dest_summary.iterrows():
            dc_name = row["destination"].replace(" DC", "").replace(" (Manufacturing Hub)", "")
            alert_badge = f'<span style="color:#D32F2F; font-size:0.68rem;">⚠ {int(row["Alerts"])}</span>' if row["Alerts"] > 0 else ""
            st.markdown(
                f'<div style="font-size:0.73rem; display:flex; justify-content:space-between; padding:0.3rem 0; border-bottom:1px solid #E2E8F0;">'
                f'<span>{dc_name}</span>'
                f'<span style="font-weight:600;">{int(row["Shipments"])} {alert_badge}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

with mc1:
    # Build Folium map centred on Pakistan
    m = folium.Map(
        location=[30.0, 70.5],
        zoom_start=6,
        tiles="CartoDB Positron",
    )

    # Hub marker (Lahore)
    folium.CircleMarker(
        location=[LAHORE_HUB["lat"], LAHORE_HUB["lon"]],
        radius=14,
        color="#004C97",
        fill=True,
        fill_color="#004C97",
        fill_opacity=0.9,
        popup=folium.Popup(
            f"<b>🏭 {LAHORE_HUB['name']}</b><br>Manufacturing & Dispatch Hub",
            max_width=220
        ),
        tooltip="Lahore — CCL Manufacturing Hub",
    ).add_to(m)

    # Draw route lines & destination markers per shipment
    if not df.empty:
        # Aggregate by destination for marker sizing
        dest_groups = df.groupby(["destination", "dest_lat", "dest_lon"])

        for (dest, dlat, dlon), grp in dest_groups:
            has_alert   = grp["is_breach"].any()
            delivered   = (grp["status"] == "Delivered").all()
            n_shipments = len(grp)
            n_alerts    = grp["is_breach"].sum()

            # Colour logic
            if has_alert:
                colour = "#D32F2F"
            elif delivered:
                colour = "#94A3B8"
            else:
                colour = "#2E7D32"

            # Route line from Lahore to DC
            folium.PolyLine(
                locations=[
                    [LAHORE_HUB["lat"], LAHORE_HUB["lon"]],
                    [dlat, dlon],
                ],
                color=colour,
                weight=2.5,
                opacity=0.55,
                dash_array="6 4" if delivered else None,
            ).add_to(m)

            # Popup content
            sample    = grp.iloc[0]
            popup_html = f"""
            <div style="font-family:sans-serif; font-size:12px; min-width:200px;">
                <b style="color:#004C97;">{dest}</b><br>
                <hr style="margin:4px 0; border-color:#E2E8F0;">
                <b>Shipments:</b> {n_shipments}<br>
                <b>Alerts:</b> <span style="color:#D32F2F;">{n_alerts}</span><br>
                <b>Sample Batch:</b> {sample['batch_id']}<br>
                <b>Category:</b> {sample['category']}<br>
                <b>Temp:</b> {sample['current_temp']}°C
                  (range: {sample['temp_min']}–{sample['temp_max']}°C)<br>
                <b>Status:</b> {sample['status']}
            </div>
            """
            # Circle size by shipment count
            radius = 8 + n_shipments * 1.2

            folium.CircleMarker(
                location=[dlat, dlon],
                radius=radius,
                color=colour,
                fill=True,
                fill_color=colour,
                fill_opacity=0.75,
                popup=folium.Popup(popup_html, max_width=260),
                tooltip=f"{dest} — {n_shipments} shipments | {n_alerts} alerts",
            ).add_to(m)

    st_folium(m, width="100%", height=440, returned_objects=[])

st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DIAGNOSTIC ANALYTICS — Two-column chart section
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📊 DIAGNOSTIC ANALYTICS</div>', unsafe_allow_html=True)

chart_left, chart_right = st.columns(2)

# ── LEFT: Cold-Chain Live Temperature Feed ──────────────────────────────────
with chart_left:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🌡️ Cold-Chain Live Temperature Feed</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Simulated 25-hour temperature log for active In-Transit shipments (30-min intervals)</div>', unsafe_allow_html=True)

    if df_temp_ts.empty:
        st.info("No In-Transit shipments match the current filter.")
    else:
        # Filter temp timeline to selected category
        ts_df = df_temp_ts.copy()
        if sel_category != "All Categories":
            ts_df = ts_df[ts_df["category"] == sel_category]

        if ts_df.empty:
            st.info("No temperature data for selected filters.")
        else:
            fig_temp = go.Figure()

            # Shade the safe zone band (first batch's range as reference)
            ref = ts_df.iloc[0]
            fig_temp.add_hrect(
                y0=ref["temp_min"], y1=ref["temp_max"],
                fillcolor="rgba(0, 163, 224, 0.07)",
                line_width=0,
                annotation_text="Safe Zone",
                annotation_position="right",
                annotation_font_size=10,
                annotation_font_color="#00A3E0",
            )
            # Danger lines
            fig_temp.add_hline(y=ref["temp_max"], line_dash="dot",
                               line_color="#D32F2F", line_width=1.2,
                               annotation_text=f"Max {ref['temp_max']}°C", annotation_position="right",
                               annotation_font_color="#D32F2F", annotation_font_size=10)
            fig_temp.add_hline(y=ref["temp_min"], line_dash="dot",
                               line_color="#D32F2F", line_width=1.2,
                               annotation_text=f"Min {ref['temp_min']}°C", annotation_position="right",
                               annotation_font_color="#D32F2F", annotation_font_size=10)

            # One line per batch
            palette = ["#0068C9", "#00A3E0", "#2E7D32", "#F57C00", "#6A1B9A", "#00838F"]
            for idx, (batch_id, grp) in enumerate(ts_df.groupby("batch_id")):
                colour = palette[idx % len(palette)]
                fig_temp.add_trace(go.Scatter(
                    x=grp["timestamp"], y=grp["temp"],
                    mode="lines",
                    name=batch_id,
                    line=dict(color=colour, width=1.8),
                    hovertemplate=(
                        f"<b>{batch_id}</b><br>"
                        "Time: %{x|%H:%M}<br>"
                        "Temp: %{y:.1f}°C<extra></extra>"
                    ),
                ))

            fig_temp.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=60, t=10, b=0),
                height=340,
                font=dict(family="DM Sans", size=11, color="#334155"),
                legend=dict(
                    orientation="h", yanchor="bottom", y=-0.28, xanchor="left", x=0,
                    font=dict(size=10),
                ),
                xaxis=dict(
                    showgrid=True, gridcolor="rgba(148,163,184,0.15)",
                    showline=False, zeroline=False,
                    tickformat="%H:%M",
                ),
                yaxis=dict(
                    showgrid=True, gridcolor="rgba(148,163,184,0.15)",
                    showline=False, zeroline=False,
                    title="Temperature (°C)",
                    title_font=dict(size=10),
                ),
                hovermode="x unified",
            )

            st.plotly_chart(fig_temp, use_container_width=True, config={"displayModeBar": False})

    st.markdown('</div>', unsafe_allow_html=True)

# ── RIGHT: Expiry & FIFO Tracker ────────────────────────────────────────────
with chart_right:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">⏳ Expiry & FIFO Priority Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Batches sorted by days remaining — shortest first. Distribute top items immediately.</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("No data matches the current filters.")
    else:
        # Take top 16 soonest-expiring batches
        fifo_df = df.sort_values("days_to_expiry").head(16).copy()
        fifo_df["days_to_expiry_disp"] = fifo_df["days_to_expiry"].clip(lower=0)

        # Colour each bar by urgency
        def urgency_colour(d):
            if d <= 0:   return "#D32F2F"   # expired
            if d <= 30:  return "#F57C00"   # urgent
            if d <= 90:  return "#0068C9"   # watch
            return "#2E7D32"                # ok

        bar_colours = fifo_df["days_to_expiry"].apply(urgency_colour).tolist()

        fig_fifo = go.Figure(go.Bar(
            x=fifo_df["days_to_expiry_disp"],
            y=fifo_df["batch_id"],
            orientation="h",
            marker_color=bar_colours,
            marker_line_width=0,
            customdata=np.stack([
                fifo_df["category"],
                fifo_df["destination"],
                fifo_df["expiry_date"].astype(str),
                fifo_df["units"],
                fifo_df["days_to_expiry"],
            ], axis=-1),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Category: %{customdata[0]}<br>"
                "Destination: %{customdata[1]}<br>"
                "Expiry: %{customdata[2]}<br>"
                "Units: %{customdata[3]:,}<br>"
                "Days Left: <b>%{customdata[4]}</b><extra></extra>"
            ),
            text=fifo_df["days_to_expiry_disp"].apply(lambda d: f"{d}d"),
            textposition="outside",
            textfont=dict(size=9, color="#334155"),
        ))

        fig_fifo.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=40, t=10, b=0),
            height=340,
            font=dict(family="DM Sans", size=10, color="#334155"),
            xaxis=dict(
                title="Days to Expiry",
                title_font=dict(size=10),
                showgrid=True, gridcolor="rgba(148,163,184,0.15)",
                showline=False, zeroline=False,
            ),
            yaxis=dict(
                showgrid=False, showline=False, zeroline=False,
                tickfont=dict(family="DM Mono, monospace", size=9),
                autorange="reversed",  # shortest at top (FIFO priority)
            ),
        )
        # Add 30-day urgency marker
        fig_fifo.add_vline(x=30, line_dash="dot", line_color="#D32F2F",
                           line_width=1.5, annotation_text="30-day threshold",
                           annotation_position="top", annotation_font_color="#D32F2F",
                           annotation_font_size=9)

        st.plotly_chart(fig_fifo, use_container_width=True, config={"displayModeBar": False})

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECONDARY ANALYTICS ROW — Category Breakdown + Status Distribution
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 FLEET OVERVIEW</div>', unsafe_allow_html=True)
a1, a2, a3 = st.columns(3)

# Category Treemap
with a1:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Shipments by Product Category</div>', unsafe_allow_html=True)
    if not df.empty:
        cat_df = df.groupby("category").agg(count=("batch_id", "count"), alerts=("is_breach","sum")).reset_index()
        fig_cat = px.bar(
            cat_df, x="count", y="category", orientation="h",
            color="category",
            color_discrete_sequence=["#004C97","#0068C9","#00A3E0","#2E7D32","#F57C00"],
            text="count",
        )
        fig_cat.update_traces(textposition="outside", textfont_size=11, marker_line_width=0)
        fig_cat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=30, t=5, b=0), height=230,
            showlegend=False,
            font=dict(family="DM Sans", size=11, color="#334155"),
            xaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)", showline=False, zeroline=False, title=""),
            yaxis=dict(showgrid=False, showline=False, zeroline=False, title=""),
        )
        st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# Status Donut
with a2:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Transit Status Distribution</div>', unsafe_allow_html=True)
    if not df.empty:
        status_df = df["status"].value_counts().reset_index()
        status_df.columns = ["status", "count"]
        colour_map = {"In Transit": "#0068C9", "Delivered": "#2E7D32", "Alert": "#D32F2F"}
        fig_status = go.Figure(go.Pie(
            labels=status_df["status"],
            values=status_df["count"],
            hole=0.62,
            marker_colors=[colour_map.get(s, "#94A3B8") for s in status_df["status"]],
            textfont_size=11,
            hovertemplate="<b>%{label}</b><br>%{value} batches<br>%{percent}<extra></extra>",
        ))
        fig_status.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=5, b=0), height=230,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=10)),
            font=dict(family="DM Sans"),
            annotations=[dict(text=f"<b>{len(df)}</b><br>Total", x=0.5, y=0.5,
                              font_size=14, showarrow=False, font=dict(color="#334155"))],
        )
        st.plotly_chart(fig_status, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# Temperature Gauge — overall fleet
with a3:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Fleet Cold-Chain Integrity Gauge</div>', unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=integrity_pct,
        delta={"reference": 95, "valueformat": ".1f", "suffix": "%"},
        number={"suffix": "%", "font": {"size": 32, "family": "DM Sans", "color": "#334155"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94A3B8", "tickfont": {"size": 9}},
            "bar": {"color": "#0068C9"},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 75],  "color": "rgba(211,47,47,0.12)"},
                {"range": [75, 90], "color": "rgba(245,124,0,0.12)"},
                {"range": [90, 100],"color": "rgba(46,125,50,0.12)"},
            ],
            "threshold": {
                "line": {"color": "#D32F2F", "width": 2},
                "thickness": 0.75,
                "value": 90,
            },
        },
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=10), height=230,
        font=dict(family="DM Sans"),
    )
    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# ALERT DETAIL TABLE — shows only breached shipments
# ─────────────────────────────────────────────────────────────────────────────
alert_df = df[df["is_breach"] == True].copy()
if not alert_df.empty:
    st.markdown('<div class="section-header">🚨 ACTIVE TEMPERATURE BREACH LOG</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)

    display_cols = ["batch_id", "category", "destination", "current_temp", "temp_min", "temp_max", "status", "days_to_expiry", "units"]
    alert_display = alert_df[display_cols].copy()
    alert_display.columns = ["Batch ID", "Category", "Destination", "Current °C", "Min °C", "Max °C", "Status", "Days to Expiry", "Units"]

    # Colour the temp column red
    def highlight_temp(val):
        return "color: #D32F2F; font-weight: 600;"

    st.dataframe(
        alert_display.style.map(highlight_temp, subset=["Current °C"]),
        use_container_width=True,
        hide_index=True,
        height=min(len(alert_display) * 38 + 38, 320),
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FULL SHIPMENT TABLE (collapsed by default)
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("📋 Full Shipment Register", expanded=False):
    if df.empty:
        st.info("No records match the current filters.")
    else:
        show_cols = ["batch_id","category","destination","status","current_temp",
                     "temp_min","temp_max","is_breach","expiry_date","days_to_expiry","units","dispatch_date"]
        st.dataframe(df[show_cols].sort_values("days_to_expiry"), use_container_width=True,
                     hide_index=True, height=350)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="ccl-footer">
    <hr>
    <b>CCL Pharmaceuticals</b> · Pharma Cold-Chain & Inventory Analytics Engine ·
    Digital Transformation Internship Portfolio &nbsp;|&nbsp;
    Data refreshed: {datetime.now().strftime('%d %b %Y %H:%M')} PKT &nbsp;|&nbsp;
    Synthetic data for demonstration purposes only
</div>
""", unsafe_allow_html=True)
