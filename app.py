
import streamlit as st
from datetime import date, time
from difflib import SequenceMatcher

st.set_page_config(
    page_title="RSS Lost & Found",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Persistent-for-session demo data
# -----------------------------
if "reports" not in st.session_state:
    st.session_state.reports = [
        {
            "id": 1, "type": "Found", "name": "Black Water Bottle",
            "description": "Black reusable water bottle with a silver cap.",
            "building": "Girls Building", "floor": "2nd Floor",
            "location": "Classroom 10K", "grade": "Grade 10",
            "date": "September 28, 2026", "time": "10:30 AM",
            "status": "Found", "reporter": "RSS Lost & Found", "photo": None,
        },
        {
            "id": 2, "type": "Lost", "name": "Blue Pencil Case",
            "description": "Small blue pencil case with school supplies inside.",
            "building": "Girls Building", "floor": "1st Floor",
            "location": "Library", "grade": "Grade 9",
            "date": "September 28, 2026", "time": "9:15 AM",
            "status": "Lost", "reporter": "Student", "photo": None,
        },
    ]

# -----------------------------
# Tech Expo design
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.stApp { background:#f6f8fc; font-family:'Inter',sans-serif; }
.block-container { max-width:1250px; padding-top:2rem; padding-bottom:3rem; }
[data-testid="stSidebar"] { background:#111827; }
[data-testid="stSidebar"] * { color:white !important; }

.hero {
    background:linear-gradient(135deg,#111827,#1e3a8a 55%,#2563eb);
    padding:38px 42px; border-radius:24px; color:white;
    margin-bottom:25px; box-shadow:0 12px 35px rgba(30,58,138,.18);
}
.hero h1 { font-size:44px; font-weight:800; margin:0; letter-spacing:-1px; }
.hero p { font-size:17px; margin:10px 0 0; opacity:.88; }

.feature-card {
    background:white; padding:25px; border-radius:18px;
    border:1px solid #e5e7eb; min-height:155px;
    box-shadow:0 5px 18px rgba(15,23,42,.05);
}
.feature-icon { font-size:28px; }
.feature-title { font-size:19px; font-weight:700; margin-top:10px; }
.feature-text { color:#64748b; line-height:1.5; margin-top:7px; }

.section-title { font-size:28px; font-weight:800; color:#111827; margin-top:20px; }
.stat-card {
    background:white; padding:20px; border-radius:18px;
    border:1px solid #e5e7eb; text-align:center;
    box-shadow:0 5px 18px rgba(15,23,42,.04);
}
.stat-number { font-size:32px; font-weight:800; color:#111827; }
.stat-label { color:#64748b; font-size:14px; margin-top:3px; }

.item-title { font-size:21px; font-weight:750; color:#111827; }
.item-description { color:#475569; margin-top:5px; }

.status-lost { background:#fee2e2; color:#b91c1c; padding:5px 11px; border-radius:999px; font-weight:700; font-size:13px; }
.status-found { background:#dbeafe; color:#1d4ed8; padding:5px 11px; border-radius:999px; font-weight:700; font-size:13px; }
.status-returned { background:#dcfce7; color:#15803d; padding:5px 11px; border-radius:999px; font-weight:700; font-size:13px; }

.info-box {
    background:#eff6ff; border-left:5px solid #2563eb;
    padding:16px 18px; border-radius:12px; color:#1e3a8a; margin:15px 0;
}
div.stButton > button { border-radius:10px; font-weight:600; }
div[data-testid="stForm"] {
    background:white; padding:25px; border-radius:18px;
    border:1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def status_class(status):
    return {"Lost": "status-lost", "Found": "status-found",
            "Returned": "status-returned"}.get(status, "status-found")

def find_matches(report):
    opposite = "Found" if report["type"] == "Lost" else "Lost"
    matches = []
    for other in st.session_state.reports:
        if other["id"] == report["id"] or other["type"] != opposite:
            continue
        if other["status"] == "Returned":
            continue

        name_score = similarity(report["name"], other["name"])
        desc_score = similarity(report["description"], other["description"])
        location_score = 0
        if report["building"] == other["building"]:
            location_score += .25
        if report["floor"] == other["floor"]:
            location_score += .15
        if report["location"].lower() == other["location"].lower():
            location_score += .20

        score = name_score * .45 + desc_score * .15 + location_score
        if score >= .40:
            matches.append((score, other))
    return sorted(matches, key=lambda x: x[0], reverse=True)

def display_report(report):
    with st.container(border=True):
        left, right = st.columns([5, 1])
        with left:
            st.markdown(f'<div class="item-title">{report["name"]}</div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div class="item-description">{report["description"]}</div>',
                        unsafe_allow_html=True)
            st.write(f'📍 **{report["building"]}** → {report["floor"]} → {report["location"]}')
            st.caption(f'🏫 {report["grade"]}  •  📅 {report["date"]}  •  🕐 {report["time"]}')
            st.caption(f'Reported by: {report["reporter"]}')
        with right:
            st.markdown(f'<span class="{status_class(report["status"])}">{report["status"]}</span>',
                        unsafe_allow_html=True)
            if report["photo"]:
                st.image(report["photo"], width=130)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("## 🔎 RSS")
    st.markdown("### Lost & Found")
    st.caption("School-wide Tech Expo Project")
    st.divider()
    page = st.radio("MENU", [
        "🏠 Home", "➕ Report an Item", "🔍 Find an Item", "🤖 Smart Match"
    ])
    st.divider()
    st.markdown("**RSS School Coverage**")
    st.caption("✓ Both buildings")
    st.caption("✓ KG to Grade 12")
    st.caption("✓ Classrooms & shared spaces")
    st.caption("✓ Students & staff")
    st.divider()
    st.caption("Built with Python + Streamlit")

# -----------------------------
# Home
# -----------------------------
if page == "🏠 Home":
    st.markdown("""
    <div class="hero">
        <h1>🔎 RSS Lost & Found</h1>
        <p>One simple place to report, search, and reconnect lost belongings across the entire school.</p>
    </div>
    """, unsafe_allow_html=True)

    total = len(st.session_state.reports)
    lost = sum(r["status"] == "Lost" for r in st.session_state.reports)
    found = sum(r["status"] == "Found" for r in st.session_state.reports)
    returned = sum(r["status"] == "Returned" for r in st.session_state.reports)

    for col, number, label in zip(
        st.columns(4),
        [total, lost, found, returned],
        ["Total Reports", "Lost Items", "Found Items", "Returned"]
    ):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">How it works</div>', unsafe_allow_html=True)
    cards = [
        ("📝", "Report", "Add the item, building, class, location, date, and time."),
        ("🔍", "Find", "Search the whole school using simple filters."),
        ("🤖", "Match", "Smart Match looks for similar lost and found reports."),
    ]
    for col, (icon, title, text) in zip(st.columns(3), cards):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <b>🏫 Made for the whole RSS community</b><br>
        Designed to cover both school buildings, from KG through high school,
        including classrooms and shared school spaces.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Recent Reports</div>', unsafe_allow_html=True)
    for report in reversed(st.session_state.reports[-4:]):
        display_report(report)

# -----------------------------
# Report
# -----------------------------
elif page == "➕ Report an Item":
    st.markdown('<div class="section-title">➕ Report an Item</div>', unsafe_allow_html=True)
    st.write("Tell us where the item was lost or found so it can be easier to locate.")

    with st.form("report_form", clear_on_submit=True):
        item_type = st.radio("Report type", ["Lost", "Found"], horizontal=True)
        st.subheader("Item Details")
        name = st.text_input("Item name *", placeholder="Example: Black water bottle")
        description = st.text_area("Description *",
            placeholder="Color, brand, stickers, size, or anything that helps identify it.")

        st.subheader("Where and when?")
        c1, c2 = st.columns(2)
        with c1:
            building = st.selectbox("Building *",
                ["Girls Building", "Boys Building", "KG / Elementary Building"])
            floor = st.selectbox("Floor",
                ["Ground Floor", "1st Floor", "2nd Floor", "3rd Floor", "Other"])
            location = st.text_input("Specific location *",
                placeholder="Example: Classroom 10K, cafeteria, playground")
        with c2:
            grade = st.selectbox("Grade", [
                "KG", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5",
                "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10",
                "Grade 11", "Grade 12", "Staff", "Unknown"
            ])
            report_date = st.date_input("Date", value=date.today())
            report_time = st.time_input("Approximate time", value=time(12, 0))

        reporter = st.text_input("Your name", placeholder="Optional")
        photo = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("🚀 Submit Report", use_container_width=True)

        if submitted:
            if not name.strip() or not description.strip() or not location.strip():
                st.error("Please complete all required fields marked with *.")
            else:
                new_id = max((r["id"] for r in st.session_state.reports), default=0) + 1
                new_report = {
                    "id": new_id, "type": item_type, "name": name.strip(),
                    "description": description.strip(), "building": building,
                    "floor": floor, "location": location.strip(), "grade": grade,
                    "date": report_date.strftime("%B %d, %Y"),
                    "time": report_time.strftime("%I:%M %p"),
                    "status": item_type,
                    "reporter": reporter.strip() or "Anonymous",
                    "photo": photo.getvalue() if photo else None,
                }
                st.session_state.reports.append(new_report)
                st.success("✅ Report submitted successfully!")
                if find_matches(new_report):
                    st.info("🤖 Smart Match found possible matches. Check the Smart Match page.")

# -----------------------------
# Search
# -----------------------------
elif page == "🔍 Find an Item":
    st.markdown('<div class="section-title">🔍 Find an Item</div>', unsafe_allow_html=True)
    st.write("Search across the RSS Lost & Found reports.")

    c1, c2, c3 = st.columns(3)
    with c1:
        search = st.text_input("Search by item or location",
                               placeholder="calculator, bottle, library...")
    with c2:
        status_filter = st.selectbox("Status", ["All", "Lost", "Found", "Returned"])
    with c3:
        building_filter = st.selectbox("Building",
            ["All", "Girls Building", "Boys Building", "KG / Elementary Building"])

    c4, c5 = st.columns(2)
    with c4:
        floor_filter = st.selectbox("Floor",
            ["All", "Ground Floor", "1st Floor", "2nd Floor", "3rd Floor", "Other"])
    with c5:
        grade_filter = st.selectbox("Grade", [
            "All", "KG", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5",
            "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11",
            "Grade 12", "Staff", "Unknown"
        ])

    results = []
    for report in st.session_state.reports:
        if search:
            searchable = " ".join([
                report["name"], report["description"],
                report["location"], report["grade"]
            ]).lower()
            if search.lower() not in searchable:
                continue
        if status_filter != "All" and report["status"] != status_filter:
            continue
        if building_filter != "All" and report["building"] != building_filter:
            continue
        if floor_filter != "All" and report["floor"] != floor_filter:
            continue
        if grade_filter != "All" and report["grade"] != grade_filter:
            continue
        results.append(report)

    st.write(f"### {len(results)} report(s) found")
    if not results:
        st.info("No reports matched your search.")
    else:
        for report in reversed(results):
            with st.container(border=True):
                left, right = st.columns([5, 1])
                with left:
                    st.markdown(f'<div class="item-title">{report["name"]}</div>',
                                unsafe_allow_html=True)
                    st.write(report["description"])
                    st.write(f'📍 **{report["building"]}** → {report["floor"]} → {report["location"]}')
                    st.caption(f'🏫 {report["grade"]}  •  📅 {report["date"]}  •  🕐 {report["time"]}')
                with right:
                    st.markdown(f'<span class="{status_class(report["status"])}">{report["status"]}</span>',
                                unsafe_allow_html=True)
                    if report["photo"]:
                        st.image(report["photo"], width=120)

                if report["status"] != "Returned":
                    if st.button("✅ Mark as Returned", key=f"return_{report['id']}"):
                        report["status"] = "Returned"
                        st.success("Item marked as returned!")
                        st.rerun()

# -----------------------------
# Smart Match
# -----------------------------
elif page == "🤖 Smart Match":
    st.markdown('<div class="section-title">🤖 Smart Match</div>', unsafe_allow_html=True)
    st.write("Smart Match compares item names, descriptions, buildings, floors, and locations.")

    lost_reports = [
        r for r in st.session_state.reports
        if r["type"] == "Lost" and r["status"] == "Lost"
    ]

    if not lost_reports:
        st.info("There are currently no active lost-item reports.")
    else:
        for lost_report in lost_reports:
            matches = find_matches(lost_report)
            with st.container(border=True):
                st.markdown(f'<div class="item-title">🔴 Lost: {lost_report["name"]}</div>',
                            unsafe_allow_html=True)
                st.caption(f'{lost_report["building"]} • {lost_report["floor"]} • {lost_report["location"]}')

                if not matches:
                    st.write("No possible matches found yet.")
                else:
                    st.write("### Possible Matches")
                    for score, found_report in matches[:3]:
                        pct = min(round(score * 100), 99)
                        st.markdown(f'**🔵 {found_report["name"]}** — Match: **{pct}%**')
                        st.write(f'📍 {found_report["building"]} • {found_report["floor"]} • {found_report["location"]}')
                        st.caption(found_report["description"])
                        if found_report["photo"]:
                            st.image(found_report["photo"], width=120)
                        st.divider()

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.markdown("""
<div style="text-align:center;color:#64748b;padding:15px;">
<b>RSS Lost & Found</b> · Tech Expo Project<br>
Built with Python · Streamlit · GitHub
</div>
""", unsafe_allow_html=True)
