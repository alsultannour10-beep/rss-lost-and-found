import streamlit as st
import pandas as pd
from datetime import date, datetime
from pathlib import Path
import uuid

st.set_page_config(page_title="RSS Lost & Found", layout="centered")

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "rss_logo.jpeg"
DATA_FILE = BASE_DIR / "rss_reports.csv"
IMAGE_DIR = BASE_DIR / "rss_item_images"
IMAGE_DIR.mkdir(exist_ok=True)

ITEM_CATEGORIES = [
    "Electronics", "Bags & Wallets", "School Supplies", "Clothing & Accessories",
    "Water Bottles & Lunch Boxes", "Jewelry & Watches", "Keys & Cards",
    "Sports Items", "Other"
]
BUILDINGS = ["Girls Building", "Boys Building", "Administration Building"]
GRADE_LEVELS = ["High School", "Middle School", "Elementary School"]
GIRLS_HIGH_SCHOOL = ["9K", "9L", "10K", "10L", "11K", "11L", "12K", "12L"]
BOYS_HIGH_SCHOOL = ["9H", "9G", "10H", "10G", "11H", "11G", "12H", "12G"]

st.markdown("""
<style>
:root { --navy:#102a52; --gray:#747987; --line:#e6e9ef; }
.stApp { background:#fff; color:#172033; }
.block-container { max-width:760px; padding-top:2rem; padding-bottom:3rem; }
#MainMenu, footer, header { visibility:hidden; }
.rss-header { text-align:center; margin-bottom:24px; }
.rss-title { color:var(--navy); font-size:2.25rem; font-weight:800; margin:8px 0 4px; }
.rss-subtitle { color:#667085; font-size:1rem; margin:0 auto; max-width:560px; }
.choice-title { text-align:center; color:var(--navy); font-size:1.45rem; font-weight:750; margin:30px 0 15px; }
.small-note { text-align:center; color:#8a8f9c; font-size:.9rem; margin-top:8px; }
.success-box { padding:28px; border:1px solid #d8e7dd; border-radius:18px; text-align:center; background:#fbfefc; }
div.stButton > button { min-height:64px; border-radius:14px; font-size:1.05rem; font-weight:750; border:1px solid #d9dee8; background:#fff; color:var(--navy); }
div.stButton > button:hover { border-color:var(--navy); color:var(--navy); }
div.stForm { border:1px solid var(--line); border-radius:18px; padding:22px; background:#fff; }
div.stFormSubmitButton > button { background:var(--navy); color:white; border-color:var(--navy); min-height:48px; }
[data-testid="stFileUploader"] { border-radius:12px; }
</style>
""", unsafe_allow_html=True)


def save_report(report, uploaded_photo):
    if uploaded_photo is not None:
        ext = Path(uploaded_photo.name).suffix.lower()
        image_name = f"{uuid.uuid4().hex}{ext}"
        image_path = IMAGE_DIR / image_name
        image_path.write_bytes(uploaded_photo.getbuffer())
        report["Photo"] = str(image_path)
    else:
        report["Photo"] = ""

    new_row = pd.DataFrame([report])
    if DATA_FILE.exists():
        new_row.to_csv(DATA_FILE, mode="a", header=False, index=False)
    else:
        new_row.to_csv(DATA_FILE, index=False)


def go_home():
    st.session_state.page = "home"
    st.session_state.report_type = None


if "page" not in st.session_state:
    st.session_state.page = "home"
if "report_type" not in st.session_state:
    st.session_state.report_type = None

st.markdown('<div class="rss-header">', unsafe_allow_html=True)
if LOGO_PATH.exists():
    c1, c2, c3 = st.columns([1, 1.25, 1])
    with c2:
        st.image(str(LOGO_PATH), use_container_width=True)
st.markdown('<div class="rss-title">RSS Lost & Found</div>', unsafe_allow_html=True)
st.markdown('<div class="rss-subtitle">Rawd Al Saleheen School Lost & Found</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown('<div class="choice-title">Did you lose or find an item?</div>', unsafe_allow_html=True)
    left, right = st.columns(2, gap="medium")
    with left:
        if st.button("I LOST AN ITEM", use_container_width=True):
            st.session_state.report_type = "Lost"
            st.session_state.page = "form"
            st.rerun()
    with right:
        if st.button("I FOUND AN ITEM", use_container_width=True):
            st.session_state.report_type = "Found"
            st.session_state.page = "form"
            st.rerun()

elif st.session_state.page == "form":
    report_type = st.session_state.report_type
    action = "lost" if report_type == "Lost" else "found"
    st.markdown(f'<div class="choice-title">Report a {report_type} Item</div>', unsafe_allow_html=True)

    building = st.selectbox("Building *", BUILDINGS)
    item_category = st.selectbox("Item Category *", ITEM_CATEGORIES)

    grade_level = ""
    class_name = ""
    if building in ["Girls Building", "Boys Building"]:
        grade_level = st.selectbox("Grade Level *", GRADE_LEVELS)
        if grade_level == "High School":
            classes = GIRLS_HIGH_SCHOOL if building == "Girls Building" else BOYS_HIGH_SCHOOL
            class_name = st.selectbox("Class *", classes)
        else:
            class_name = st.text_input("Grade / Class *")

    with st.form("rss_report_form", clear_on_submit=False):
        item_name = st.text_input("Item name *")
        description = st.text_area("Description *", height=100)
        location = st.text_input("Where was it lost/found? *")
        event_date = st.date_input(f"Date it was {action} *", value=date.today(), max_value=date.today())
        reporter = st.text_input("Your name (optional)")
        photo = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Submit Report", use_container_width=True)

        if submitted:
            missing_school_info = building in ["Girls Building", "Boys Building"] and (not grade_level or not class_name.strip())
            if not item_name.strip() or not description.strip() or not location.strip() or missing_school_info:
                st.error("Please complete all required fields.")
            else:
                report = {
                    "ID": uuid.uuid4().hex,
                    "Type": report_type,
                    "Building": building,
                    "ItemCategory": item_category,
                    "GradeLevel": grade_level,
                    "Class": class_name.strip(),
                    "ItemName": item_name.strip(),
                    "Description": description.strip(),
                    "Location": location.strip(),
                    "EventDate": event_date.isoformat(),
                    "Reporter": reporter.strip() or "Anonymous",
                    "SubmittedAt": datetime.now().isoformat(timespec="seconds"),
                }
                save_report(report, photo)
                st.session_state.page = "success"
                st.rerun()

    if st.button("Back", use_container_width=True):
        go_home()
        st.rerun()

elif st.session_state.page == "success":
    st.markdown("""
    <div class="success-box">
        <h2 style="color:#102a52;margin-top:0;">Report Submitted</h2>
        <p style="color:#667085;margin-bottom:0;">Your lost and found report has been recorded.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Submit Another Report", use_container_width=True):
        go_home()
        st.rerun()
div.stButton > button:hover { border-color:var(--navy); color:var(--navy); }
div.stForm { border:1px solid var(--line); border-radius:18px; padding:22px; background:#fff; }
div.stFormSubmitButton > button { background:var(--navy); color:white; border-color:var(--navy); min-height:48px; }
[data-testid="stFileUploader"] { border-radius:12px; }
</style>
""", unsafe_allow_html=True)


def save_report(report, uploaded_photo):
    if uploaded_photo is not None:
        ext = Path(uploaded_photo.name).suffix.lower()
        image_name = f"{uuid.uuid4().hex}{ext}"
        image_path = IMAGE_DIR / image_name
        image_path.write_bytes(uploaded_photo.getbuffer())
        report["Photo"] = str(image_path)
    else:
        report["Photo"] = ""

    new_row = pd.DataFrame([report])
    if DATA_FILE.exists():
        new_row.to_csv(DATA_FILE, mode="a", header=False, index=False)
    else:
        new_row.to_csv(DATA_FILE, index=False)


def go_home():
    st.session_state.page = "home"
    st.session_state.report_type = None


if "page" not in st.session_state:
    st.session_state.page = "home"
if "report_type" not in st.session_state:
    st.session_state.report_type = None

# Header shown on every page
st.markdown('<div class="rss-header">', unsafe_allow_html=True)
if LOGO_PATH.exists():
    c1, c2, c3 = st.columns([1, 1.25, 1])
    with c2:
        st.image(str(LOGO_PATH), use_container_width=True)
st.markdown('<div class="rss-title">RSS Lost & Found</div>', unsafe_allow_html=True)
st.markdown('<div class="rss-subtitle">A simple way for the Rawd Al Saleheen community to report lost and found items.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown('<div class="choice-title">What happened?</div>', unsafe_allow_html=True)
    left, right = st.columns(2, gap="medium")
    with left:
        if st.button("🔴  I LOST AN ITEM", use_container_width=True):
            st.session_state.report_type = "Lost"
            st.session_state.page = "form"
            st.rerun()
    with right:
        if st.button("🔵  I FOUND AN ITEM", use_container_width=True):
            st.session_state.report_type = "Found"
            st.session_state.page = "form"
            st.rerun()
    st.markdown('<div class="small-note">Choose one option, fill in the short form, and submit.</div>', unsafe_allow_html=True)

elif st.session_state.page == "form":
    report_type = st.session_state.report_type
    action = "lost" if report_type == "Lost" else "found"
    st.markdown(f'<div class="choice-title">Report a {report_type} Item</div>', unsafe_allow_html=True)

    with st.form("rss_report_form", clear_on_submit=False):
        category = st.selectbox("Category *", CATEGORIES)
        item_name = st.text_input("Item name *", placeholder="Example: Black water bottle")
        description = st.text_area("Description *", placeholder="Color, brand, size, or anything that can help identify it.", height=100)

        c1, c2 = st.columns(2)
        with c1:
            building = st.selectbox("Building *", BUILDINGS)
            floor = st.selectbox("Floor *", FLOORS)
            grade = st.selectbox("Grade / Staff *", GRADES)
        with c2:
            location = st.text_input("Where was it? *", placeholder="Example: Library or Classroom 10K")
            event_date = st.date_input(f"Date it was {action} *", value=date.today(), max_value=date.today())
            reporter = st.text_input("Your name", placeholder="Optional")

        photo = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Submit Report", use_container_width=True)

        if submitted:
            if not item_name.strip() or not description.strip() or not location.strip():
                st.error("Please complete all fields marked with *.")
            else:
                report = {
                    "ID": uuid.uuid4().hex,
                    "Type": report_type,
                    "Category": category,
                    "ItemName": item_name.strip(),
                    "Description": description.strip(),
                    "Building": building,
                    "Floor": floor,
                    "Location": location.strip(),
                    "Grade": grade,
                    "EventDate": event_date.isoformat(),
                    "Reporter": reporter.strip() or "Anonymous",
                    "SubmittedAt": datetime.now().isoformat(timespec="seconds"),
                }
                save_report(report, photo)
                st.session_state.page = "success"
                st.rerun()

    if st.button("← Back", use_container_width=True):
        go_home()
        st.rerun()

elif st.session_state.page == "success":
    st.markdown("""
    <div class="success-box">
        <h2 style="color:#102a52;margin-top:0;">✓ Report Submitted</h2>
        <p style="color:#667085;margin-bottom:0;">Thank you. Your lost & found report has been recorded.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Submit Another Report", use_container_width=True):
        go_home()
        st.rerun()
