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
GIRLS_MIDDLE_SCHOOL = ["5K", "5L", "6K", "6L", "7K", "7L", "8K", "8L"]
GIRLS_ELEMENTARY = ["1K", "1L", "2K", "2L", "3K", "3L", "4K", "4L"]
BOYS_HIGH_SCHOOL = ["9H", "9G", "10H", "10G", "11H", "11G", "12H", "12G"]
BOYS_MIDDLE_SCHOOL = ["5H", "5G", "6H", "6G", "7H", "7G", "8H", "8G"]
BOYS_ELEMENTARY = ["1H", "1G", "2H", "2G", "3H", "3G", "4H", "4G"]
GIRLS_SPECIAL_LOCATIONS = ["Computer Lab", "Art Room", "Theatre Room"]
BOYS_SPECIAL_LOCATIONS = ["Computer Lab", "Art Room", "Ghaneema's Auditorium"]
ADMIN_LOCATIONS = ["Library", "Ms Razan Room", "Ms Heba Alodaid Room", "Lobby"]
REPORT_COLUMNS = [
    "ID", "Type", "Building", "ItemCategory", "GradeLevel", "Class", "ItemName",
    "Description", "Location", "EventDate", "Email", "Photo", "SubmittedAt"
]

st.markdown("""
<style>
:root { --navy:#102a52; --gray:#747987; --line:#e6e9ef; }
html, body, [class*="css"], .stApp, button, input, textarea, select, label, p, div, span, h1, h2, h3 {
    font-family: "Times New Roman", Times, serif !important;
}
.stApp { background:#fff; color:#172033; }
.block-container { max-width:800px; padding-top:2rem; padding-bottom:3rem; }
#MainMenu, footer, header { visibility:hidden; }
.rss-header { text-align:center; margin-bottom:24px; }
.rss-title { color:var(--navy); font-size:2.4rem; font-weight:700; margin:8px 0 4px; }
.rss-subtitle { color:#667085; font-size:1.05rem; margin:0 auto; max-width:560px; }
.choice-title { text-align:center; color:var(--navy); font-size:1.55rem; font-weight:700; margin:30px 0 15px; }
.helper { text-align:center; color:#667085; margin:-6px auto 20px; max-width:620px; }
.success-box { padding:28px; border:1px solid #d8e7dd; border-radius:18px; text-align:center; background:#fbfefc; }
.item-card { border:1px solid var(--line); border-radius:16px; padding:18px; margin:12px 0; background:#fff; }
.item-name { color:var(--navy); font-size:1.3rem; font-weight:700; margin-bottom:4px; }
.item-meta { color:#667085; font-size:.95rem; margin-bottom:8px; }
div.stButton > button { min-height:58px; border-radius:14px; font-size:1.05rem; font-weight:700; border:1px solid #d9dee8; background:#fff; color:var(--navy); }
div.stButton > button:hover { border-color:var(--navy); color:var(--navy); }
div.stForm { border:1px solid var(--line); border-radius:18px; padding:22px; background:#fff; }
div.stFormSubmitButton > button { background:var(--navy); color:white; border-color:var(--navy); min-height:48px; }
</style>
""", unsafe_allow_html=True)


def load_reports():
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=REPORT_COLUMNS)
    try:
        df = pd.read_csv(DATA_FILE, dtype=str).fillna("")
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame(columns=REPORT_COLUMNS)
    for column in REPORT_COLUMNS:
        if column not in df.columns:
            df[column] = ""
    return df[REPORT_COLUMNS]


def save_report(report, uploaded_photo):
    if uploaded_photo is not None:
        ext = Path(uploaded_photo.name).suffix.lower()
        image_name = f"{uuid.uuid4().hex}{ext}"
        image_path = IMAGE_DIR / image_name
        image_path.write_bytes(uploaded_photo.getbuffer())
        report["Photo"] = str(image_path)
    else:
        report["Photo"] = ""
    pd.DataFrame([report], columns=REPORT_COLUMNS).to_csv(
        DATA_FILE, mode="a", header=not DATA_FILE.exists(), index=False
    )


def valid_rss_email(email):
    email = email.strip().lower()
    return email.endswith("@rawdalsaleheen.edu.kw") and len(email.split("@", 1)[0]) > 0


def go_home():
    st.session_state.page = "home"
    st.session_state.report_type = None
    st.session_state.selected_item = None


if "page" not in st.session_state:
    st.session_state.page = "home"
if "report_type" not in st.session_state:
    st.session_state.report_type = None
if "selected_item" not in st.session_state:
    st.session_state.selected_item = None

st.markdown('<div class="rss-header">', unsafe_allow_html=True)
if LOGO_PATH.exists():
    c1, c2, c3 = st.columns([1, 1.25, 1])
    with c2:
        st.image(str(LOGO_PATH), use_container_width=True)
st.markdown('<div class="rss-title">RSS Lost & Found</div>', unsafe_allow_html=True)
st.markdown('<div class="rss-subtitle">Rawd Al Saleheen School Lost & Found</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown('<div class="choice-title">What would you like to do?</div>', unsafe_allow_html=True)
    st.markdown('<div class="helper">If you lost something, check the found items first. Someone may have already reported it.</div>', unsafe_allow_html=True)
    if st.button("I LOST AN ITEM", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()
    if st.button("I FOUND AN ITEM", use_container_width=True):
        st.session_state.report_type = "Found"
        st.session_state.page = "form"
        st.rerun()
    if st.button("BROWSE FOUND ITEMS", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()

elif st.session_state.page == "found_items":
    st.markdown('<div class="choice-title">Found Items</div>', unsafe_allow_html=True)
    st.markdown('<div class="helper">Look through items that have already been found before submitting a lost-item report.</div>', unsafe_allow_html=True)
    reports = load_reports()
    found = reports[reports["Type"].str.lower() == "found"].copy() if not reports.empty else reports
    search = st.text_input("Search found items")
    category = st.selectbox("Category", ["All"] + ITEM_CATEGORIES)
    if search and not found.empty:
        mask = (found["ItemName"] + " " + found["Description"] + " " + found["Location"]).str.contains(search, case=False, na=False)
        found = found[mask]
    if category != "All" and not found.empty:
        found = found[found["ItemCategory"] == category]
    if found.empty:
        st.info("No found items match your search yet.")
    else:
        found = found.sort_values("SubmittedAt", ascending=False)
        for _, row in found.iterrows():
            st.markdown(f'<div class="item-card"><div class="item-name">{row["ItemName"]}</div><div class="item-meta">{row["ItemCategory"]} | {row["Building"]} | {row["Location"]}</div><div>{row["Description"]}</div></div>', unsafe_allow_html=True)
            if st.button("View Item / Contact Finder", key=f'view_{row["ID"]}', use_container_width=True):
                st.session_state.selected_item = row.to_dict()
                st.session_state.page = "item_detail"
                st.rerun()
    st.write("")
    if st.button("I DID NOT FIND MY ITEM - REPORT IT", use_container_width=True):
        st.session_state.report_type = "Lost"
        st.session_state.page = "form"
        st.rerun()
    if st.button("Back to Home", use_container_width=True):
        go_home()
        st.rerun()

elif st.session_state.page == "item_detail":
    item = st.session_state.selected_item
    if not item:
        st.session_state.page = "found_items"
        st.rerun()
    st.markdown(f'<div class="choice-title">{item["ItemName"]}</div>', unsafe_allow_html=True)
    photo_path = item.get("Photo", "")
    if photo_path and Path(photo_path).exists():
        st.image(photo_path, use_container_width=True)
    st.write(f'**Category:** {item["ItemCategory"]}')
    st.write(f'**Building:** {item["Building"]}')
    if item.get("GradeLevel"):
        st.write(f'**Grade Level:** {item["GradeLevel"]}')
    if item.get("Class"):
        st.write(f'**Class:** {item["Class"]}')
    st.write(f'**Found at:** {item["Location"]}')
    st.write(f'**Date found:** {item["EventDate"]}')
    st.write(f'**Description:** {item["Description"]}')
    st.markdown("### Contact the finder")
    st.write(item.get("Email", "No contact email provided."))
    if st.button("Back to Found Items", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()

elif st.session_state.page == "form":
    report_type = st.session_state.report_type
    action = "lost" if report_type == "Lost" else "found"
    st.markdown(f'<div class="choice-title">Report a {report_type} Item</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        building = st.selectbox("Building *", BUILDINGS)
    with col2:
        item_category = st.selectbox("Item Category *", ITEM_CATEGORIES)

    grade_level = ""
    class_name = ""
    if building in ["Girls Building", "Boys Building"]:
        grade_level = st.selectbox("Grade Level *", GRADE_LEVELS)
        if building == "Girls Building":
            class_map = {
                "High School": GIRLS_HIGH_SCHOOL,
                "Middle School": GIRLS_MIDDLE_SCHOOL,
                "Elementary School": GIRLS_ELEMENTARY,
            }
        else:
            class_map = {
                "High School": BOYS_HIGH_SCHOOL,
                "Middle School": BOYS_MIDDLE_SCHOOL,
                "Elementary School": BOYS_ELEMENTARY,
            }
        class_name = st.selectbox("Class *", class_map[grade_level])

    if building == "Girls Building":
        location_options = ["Classroom"] + GIRLS_SPECIAL_LOCATIONS
    elif building == "Boys Building":
        location_options = ["Classroom"] + BOYS_SPECIAL_LOCATIONS
    else:
        location_options = ADMIN_LOCATIONS

    with st.form("rss_report_form", clear_on_submit=False):
        item_name = st.text_input("Item name *")
        description = st.text_area("Description *", height=100)
        location = st.selectbox("Where was it lost/found? *", location_options)
        event_date = st.date_input(f"Date it was {action} *", value=date.today(), max_value=date.today())
        email = st.text_input("RSS Email Address *", placeholder="1730@rawdalsaleheen.edu.kw")
        photo = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Submit Report", use_container_width=True)

        if submitted:
            missing_school_info = building in ["Girls Building", "Boys Building"] and (not grade_level or not class_name.strip())
            if not item_name.strip() or not description.strip() or not location.strip() or missing_school_info:
                st.error("Please complete all required fields.")
            elif not valid_rss_email(email):
                st.error("Please enter a valid RSS email ending with @rawdalsaleheen.edu.kw.")
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
                    "Email": email.strip().lower(),
                    "Photo": "",
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
        <p style="color:#667085;margin-bottom:0;">Your report has been recorded.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Back to Home", use_container_width=True):
        go_home()
        st.rerun()
<style>
:root { --navy:#102a52; --gray:#747987; --line:#e6e9ef; }
html, body, [class*="css"], .stApp, button, input, textarea, select, label, p, div, span, h1, h2, h3 {
    font-family: "Times New Roman", Times, serif !important;
}
.stApp { background:#fff; color:#172033; }
.block-container { max-width:800px; padding-top:2rem; padding-bottom:3rem; }
#MainMenu, footer, header { visibility:hidden; }
.rss-header { text-align:center; margin-bottom:24px; }
.rss-title { color:var(--navy); font-size:2.4rem; font-weight:700; margin:8px 0 4px; }
.rss-subtitle { color:#667085; font-size:1.05rem; margin:0 auto; max-width:560px; }
.choice-title { text-align:center; color:var(--navy); font-size:1.55rem; font-weight:700; margin:30px 0 15px; }
.helper { text-align:center; color:#667085; margin:-6px auto 20px; max-width:620px; }
.success-box { padding:28px; border:1px solid #d8e7dd; border-radius:18px; text-align:center; background:#fbfefc; }
.item-card { border:1px solid var(--line); border-radius:16px; padding:18px; margin:12px 0; background:#fff; }
.item-name { color:var(--navy); font-size:1.3rem; font-weight:700; margin-bottom:4px; }
.item-meta { color:#667085; font-size:.95rem; margin-bottom:8px; }
div.stButton > button { min-height:58px; border-radius:14px; font-size:1.05rem; font-weight:700; border:1px solid #d9dee8; background:#fff; color:var(--navy); }
div.stButton > button:hover { border-color:var(--navy); color:var(--navy); }
div.stForm { border:1px solid var(--line); border-radius:18px; padding:22px; background:#fff; }
div.stFormSubmitButton > button { background:var(--navy); color:white; border-color:var(--navy); min-height:48px; }
</style>
""", unsafe_allow_html=True)


def load_reports():
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=REPORT_COLUMNS)
    try:
        df = pd.read_csv(DATA_FILE, dtype=str).fillna("")
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame(columns=REPORT_COLUMNS)
    for column in REPORT_COLUMNS:
        if column not in df.columns:
            df[column] = ""
    return df[REPORT_COLUMNS]


def save_report(report, uploaded_photo):
    if uploaded_photo is not None:
        ext = Path(uploaded_photo.name).suffix.lower()
        image_name = f"{uuid.uuid4().hex}{ext}"
        image_path = IMAGE_DIR / image_name
        image_path.write_bytes(uploaded_photo.getbuffer())
        report["Photo"] = str(image_path)
    else:
        report["Photo"] = ""
    pd.DataFrame([report], columns=REPORT_COLUMNS).to_csv(
        DATA_FILE, mode="a", header=not DATA_FILE.exists(), index=False
    )


def valid_rss_email(email):
    email = email.strip().lower()
    return email.endswith("@rawdalsaleheen.edu.kw") and len(email.split("@", 1)[0]) > 0


def go_home():
    st.session_state.page = "home"
    st.session_state.report_type = None
    st.session_state.selected_item = None


if "page" not in st.session_state:
    st.session_state.page = "home"
if "report_type" not in st.session_state:
    st.session_state.report_type = None
if "selected_item" not in st.session_state:
    st.session_state.selected_item = None

st.markdown('<div class="rss-header">', unsafe_allow_html=True)
if LOGO_PATH.exists():
    c1, c2, c3 = st.columns([1, 1.25, 1])
    with c2:
        st.image(str(LOGO_PATH), use_container_width=True)
st.markdown('<div class="rss-title">RSS Lost & Found</div>', unsafe_allow_html=True)
st.markdown('<div class="rss-subtitle">Rawd Al Saleheen School Lost & Found</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown('<div class="choice-title">What would you like to do?</div>', unsafe_allow_html=True)
    st.markdown('<div class="helper">If you lost something, check the found items first. Someone may have already reported it.</div>', unsafe_allow_html=True)
    if st.button("I LOST AN ITEM", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()
    if st.button("I FOUND AN ITEM", use_container_width=True):
        st.session_state.report_type = "Found"
        st.session_state.page = "form"
        st.rerun()
    if st.button("BROWSE FOUND ITEMS", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()

elif st.session_state.page == "found_items":
    st.markdown('<div class="choice-title">Found Items</div>', unsafe_allow_html=True)
    st.markdown('<div class="helper">Look through items that have already been found before submitting a lost-item report.</div>', unsafe_allow_html=True)
    reports = load_reports()
    found = reports[reports["Type"].str.lower() == "found"].copy() if not reports.empty else reports
    search = st.text_input("Search found items")
    category = st.selectbox("Category", ["All"] + ITEM_CATEGORIES)
    if search and not found.empty:
        mask = (found["ItemName"] + " " + found["Description"] + " " + found["Location"]).str.contains(search, case=False, na=False)
        found = found[mask]
    if category != "All" and not found.empty:
        found = found[found["ItemCategory"] == category]
    if found.empty:
        st.info("No found items match your search yet.")
    else:
        found = found.sort_values("SubmittedAt", ascending=False)
        for _, row in found.iterrows():
            st.markdown(f'<div class="item-card"><div class="item-name">{row["ItemName"]}</div><div class="item-meta">{row["ItemCategory"]} | {row["Building"]} | {row["Location"]}</div><div>{row["Description"]}</div></div>', unsafe_allow_html=True)
            if st.button("View Item / Contact Finder", key=f'view_{row["ID"]}', use_container_width=True):
                st.session_state.selected_item = row.to_dict()
                st.session_state.page = "item_detail"
                st.rerun()
    st.write("")
    if st.button("I DID NOT FIND MY ITEM - REPORT IT", use_container_width=True):
        st.session_state.report_type = "Lost"
        st.session_state.page = "form"
        st.rerun()
    if st.button("Back to Home", use_container_width=True):
        go_home()
        st.rerun()

elif st.session_state.page == "item_detail":
    item = st.session_state.selected_item
    if not item:
        st.session_state.page = "found_items"
        st.rerun()
    st.markdown(f'<div class="choice-title">{item["ItemName"]}</div>', unsafe_allow_html=True)
    photo_path = item.get("Photo", "")
    if photo_path and Path(photo_path).exists():
        st.image(photo_path, use_container_width=True)
    st.write(f'**Category:** {item["ItemCategory"]}')
    st.write(f'**Building:** {item["Building"]}')
    if item.get("GradeLevel"):
        st.write(f'**Grade Level:** {item["GradeLevel"]}')
    if item.get("Class"):
        st.write(f'**Class:** {item["Class"]}')
    st.write(f'**Found at:** {item["Location"]}')
    st.write(f'**Date found:** {item["EventDate"]}')
    st.write(f'**Description:** {item["Description"]}')
    st.markdown("### Contact the finder")
    st.write(item.get("Email", "No contact email provided."))
    if st.button("Back to Found Items", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()

elif st.session_state.page == "form":
    report_type = st.session_state.report_type
    action = "lost" if report_type == "Lost" else "found"
    st.markdown(f'<div class="choice-title">Report a {report_type} Item</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        building = st.selectbox("Building *", BUILDINGS)
    with col2:
        item_category = st.selectbox("Item Category *", ITEM_CATEGORIES)

    grade_level = ""
    class_name = ""
    if building in ["Girls Building", "Boys Building"]:
        grade_level = st.selectbox("Grade Level *", GRADE_LEVELS)
        if building == "Girls Building":
            class_map = {
                "High School": GIRLS_HIGH_SCHOOL,
                "Middle School": GIRLS_MIDDLE_SCHOOL,
                "Elementary School": GIRLS_ELEMENTARY,
            }
        else:
            class_map = {
                "High School": BOYS_HIGH_SCHOOL,
                "Middle School": BOYS_MIDDLE_SCHOOL,
                "Elementary School": BOYS_ELEMENTARY,
            }
        class_name = st.selectbox("Class *", class_map[grade_level])

    if building == "Girls Building":
        location_options = ["Classroom"] + GIRLS_SPECIAL_LOCATIONS
    elif building == "Boys Building":
        location_options = ["Classroom"] + BOYS_SPECIAL_LOCATIONS
    else:
        location_options = ADMIN_LOCATIONS

    with st.form("rss_report_form", clear_on_submit=False):
        item_name = st.text_input("Item name *")
        description = st.text_area("Description *", height=100)
        location = st.selectbox("Where was it lost/found? *", location_options)
        event_date = st.date_input(f"Date it was {action} *", value=date.today(), max_value=date.today())
        email = st.text_input("RSS Email Address *", placeholder="1730@rawdalsaleheen.edu.kw")
        photo = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Submit Report", use_container_width=True)

        if submitted:
            missing_school_info = building in ["Girls Building", "Boys Building"] and (not grade_level or not class_name.strip())
            if not item_name.strip() or not description.strip() or not location.strip() or missing_school_info:
                st.error("Please complete all required fields.")
            elif not valid_rss_email(email):
                st.error("Please enter a valid RSS email ending with @rawdalsaleheen.edu.kw.")
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
                    "Email": email.strip().lower(),
                    "Photo": "",
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
        <p style="color:#667085;margin-bottom:0;">Your report has been recorded.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Back to Home", use_container_width=True):
        go_home()
        st.rerun()
<style>
:root { --navy:#102a52; --gray:#747987; --line:#e6e9ef; }
html, body, [class*="css"], .stApp, button, input, textarea, select, label, p, div, span, h1, h2, h3 {
    font-family: "Times New Roman", Times, serif !important;
}
.stApp { background:#fff; color:#172033; }
.block-container { max-width:800px; padding-top:2rem; padding-bottom:3rem; }
#MainMenu, footer, header { visibility:hidden; }
.rss-header { text-align:center; margin-bottom:24px; }
.rss-title { color:var(--navy); font-size:2.4rem; font-weight:700; margin:8px 0 4px; }
.rss-subtitle { color:#667085; font-size:1.05rem; margin:0 auto; max-width:560px; }
.choice-title { text-align:center; color:var(--navy); font-size:1.55rem; font-weight:700; margin:30px 0 15px; }
.helper { text-align:center; color:#667085; margin:-6px auto 20px; max-width:620px; }
.success-box { padding:28px; border:1px solid #d8e7dd; border-radius:18px; text-align:center; background:#fbfefc; }
.item-card { border:1px solid var(--line); border-radius:16px; padding:18px; margin:12px 0; background:#fff; }
.item-name { color:var(--navy); font-size:1.3rem; font-weight:700; margin-bottom:4px; }
.item-meta { color:#667085; font-size:.95rem; margin-bottom:8px; }
div.stButton > button { min-height:58px; border-radius:14px; font-size:1.05rem; font-weight:700; border:1px solid #d9dee8; background:#fff; color:var(--navy); }
div.stButton > button:hover { border-color:var(--navy); color:var(--navy); }
div.stForm { border:1px solid var(--line); border-radius:18px; padding:22px; background:#fff; }
div.stFormSubmitButton > button { background:var(--navy); color:white; border-color:var(--navy); min-height:48px; }
</style>
""", unsafe_allow_html=True)


def load_reports():
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=REPORT_COLUMNS)
    try:
        df = pd.read_csv(DATA_FILE, dtype=str).fillna("")
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame(columns=REPORT_COLUMNS)
    for column in REPORT_COLUMNS:
        if column not in df.columns:
            df[column] = ""
    return df[REPORT_COLUMNS]


def save_report(report, uploaded_photo):
    if uploaded_photo is not None:
        ext = Path(uploaded_photo.name).suffix.lower()
        image_name = f"{uuid.uuid4().hex}{ext}"
        image_path = IMAGE_DIR / image_name
        image_path.write_bytes(uploaded_photo.getbuffer())
        report["Photo"] = str(image_path)
    else:
        report["Photo"] = ""
    pd.DataFrame([report], columns=REPORT_COLUMNS).to_csv(
        DATA_FILE, mode="a", header=not DATA_FILE.exists(), index=False
    )


def valid_rss_email(email):
    email = email.strip().lower()
    return email.endswith("@rawdalsaleheen.edu.kw") and len(email.split("@", 1)[0]) > 0


def go_home():
    st.session_state.page = "home"
    st.session_state.report_type = None
    st.session_state.selected_item = None


if "page" not in st.session_state:
    st.session_state.page = "home"
if "report_type" not in st.session_state:
    st.session_state.report_type = None
if "selected_item" not in st.session_state:
    st.session_state.selected_item = None

st.markdown('<div class="rss-header">', unsafe_allow_html=True)
if LOGO_PATH.exists():
    c1, c2, c3 = st.columns([1, 1.25, 1])
    with c2:
        st.image(str(LOGO_PATH), use_container_width=True)
st.markdown('<div class="rss-title">RSS Lost & Found</div>', unsafe_allow_html=True)
st.markdown('<div class="rss-subtitle">Rawd Al Saleheen School Lost & Found</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown('<div class="choice-title">What would you like to do?</div>', unsafe_allow_html=True)
    st.markdown('<div class="helper">If you lost something, check the found items first. Someone may have already reported it.</div>', unsafe_allow_html=True)
    if st.button("I LOST AN ITEM", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()
    if st.button("I FOUND AN ITEM", use_container_width=True):
        st.session_state.report_type = "Found"
        st.session_state.page = "form"
        st.rerun()
    if st.button("BROWSE FOUND ITEMS", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()

elif st.session_state.page == "found_items":
    st.markdown('<div class="choice-title">Found Items</div>', unsafe_allow_html=True)
    st.markdown('<div class="helper">Look through items that have already been found before submitting a lost-item report.</div>', unsafe_allow_html=True)
    reports = load_reports()
    found = reports[reports["Type"].str.lower() == "found"].copy() if not reports.empty else reports
    search = st.text_input("Search found items")
    category = st.selectbox("Category", ["All"] + ITEM_CATEGORIES)
    if search and not found.empty:
        mask = (found["ItemName"] + " " + found["Description"] + " " + found["Location"]).str.contains(search, case=False, na=False)
        found = found[mask]
    if category != "All" and not found.empty:
        found = found[found["ItemCategory"] == category]
    if found.empty:
        st.info("No found items match your search yet.")
    else:
        found = found.sort_values("SubmittedAt", ascending=False)
        for _, row in found.iterrows():
            st.markdown(f'<div class="item-card"><div class="item-name">{row["ItemName"]}</div><div class="item-meta">{row["ItemCategory"]} | {row["Building"]} | {row["Location"]}</div><div>{row["Description"]}</div></div>', unsafe_allow_html=True)
            if st.button("View Item / Contact Finder", key=f'view_{row["ID"]}', use_container_width=True):
                st.session_state.selected_item = row.to_dict()
                st.session_state.page = "item_detail"
                st.rerun()
    st.write("")
    if st.button("I DID NOT FIND MY ITEM - REPORT IT", use_container_width=True):
        st.session_state.report_type = "Lost"
        st.session_state.page = "form"
        st.rerun()
    if st.button("Back to Home", use_container_width=True):
        go_home()
        st.rerun()

elif st.session_state.page == "item_detail":
    item = st.session_state.selected_item
    if not item:
        st.session_state.page = "found_items"
        st.rerun()
    st.markdown(f'<div class="choice-title">{item["ItemName"]}</div>', unsafe_allow_html=True)
    photo_path = item.get("Photo", "")
    if photo_path and Path(photo_path).exists():
        st.image(photo_path, use_container_width=True)
    st.write(f'**Category:** {item["ItemCategory"]}')
    st.write(f'**Building:** {item["Building"]}')
    if item.get("GradeLevel"):
        st.write(f'**Grade Level:** {item["GradeLevel"]}')
    if item.get("Class"):
        st.write(f'**Class:** {item["Class"]}')
    st.write(f'**Found at:** {item["Location"]}')
    st.write(f'**Date found:** {item["EventDate"]}')
    st.write(f'**Description:** {item["Description"]}')
    st.markdown("### Contact the finder")
    st.write(item.get("Email", "No contact email provided."))
    if st.button("Back to Found Items", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()

elif st.session_state.page == "form":
    report_type = st.session_state.report_type
    action = "lost" if report_type == "Lost" else "found"
    st.markdown(f'<div class="choice-title">Report a {report_type} Item</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        building = st.selectbox("Building *", BUILDINGS)
    with col2:
        item_category = st.selectbox("Item Category *", ITEM_CATEGORIES)

    grade_level = ""
    class_name = ""
    if building in ["Girls Building", "Boys Building"]:
        grade_level = st.selectbox("Grade Level *", GRADE_LEVELS)
        if building == "Girls Building":
            class_map = {
                "High School": GIRLS_HIGH_SCHOOL,
                "Middle School": GIRLS_MIDDLE_SCHOOL,
                "Elementary School": GIRLS_ELEMENTARY,
            }
        else:
            class_map = {
                "High School": BOYS_HIGH_SCHOOL,
                "Middle School": BOYS_MIDDLE_SCHOOL,
                "Elementary School": BOYS_ELEMENTARY,
            }
        class_name = st.selectbox("Class *", class_map[grade_level])

    if building == "Girls Building":
        location_options = ["Classroom"] + GIRLS_SPECIAL_LOCATIONS
    elif building == "Boys Building":
        location_options = ["Classroom"] + BOYS_SPECIAL_LOCATIONS
    else:
        location_options = ADMIN_LOCATIONS

    with st.form("rss_report_form", clear_on_submit=False):
        item_name = st.text_input("Item name *")
        description = st.text_area("Description *", height=100)
        location = st.selectbox("Where was it lost/found? *", location_options)
        event_date = st.date_input(f"Date it was {action} *", value=date.today(), max_value=date.today())
        email = st.text_input("RSS Email Address *", placeholder="1730@rawdalsaleheen.edu.kw")
        photo = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Submit Report", use_container_width=True)

        if submitted:
            missing_school_info = building in ["Girls Building", "Boys Building"] and (not grade_level or not class_name.strip())
            if not item_name.strip() or not description.strip() or not location.strip() or missing_school_info:
                st.error("Please complete all required fields.")
            elif not valid_rss_email(email):
                st.error("Please enter a valid RSS email ending with @rawdalsaleheen.edu.kw.")
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
                    "Email": email.strip().lower(),
                    "Photo": "",
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
        <p style="color:#667085;margin-bottom:0;">Your report has been recorded.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Back to Home", use_container_width=True):
        go_home()
        st.rerun()
#MainMenu, footer, header { visibility:hidden; }
.rss-header { text-align:center; margin-bottom:24px; }
.rss-title { color:var(--navy); font-size:2.4rem; font-weight:700; margin:8px 0 4px; }
.rss-subtitle { color:#667085; font-size:1.05rem; margin:0 auto; max-width:560px; }
.choice-title { text-align:center; color:var(--navy); font-size:1.55rem; font-weight:700; margin:30px 0 15px; }
.helper { text-align:center; color:#667085; margin:-6px auto 20px; max-width:620px; }
.success-box { padding:28px; border:1px solid #d8e7dd; border-radius:18px; text-align:center; background:#fbfefc; }
.item-card { border:1px solid var(--line); border-radius:16px; padding:18px; margin:12px 0; background:#fff; }
.item-name { color:var(--navy); font-size:1.3rem; font-weight:700; margin-bottom:4px; }
.item-meta { color:#667085; font-size:.95rem; margin-bottom:8px; }
div.stButton > button { min-height:58px; border-radius:14px; font-size:1.05rem; font-weight:700; border:1px solid #d9dee8; background:#fff; color:var(--navy); }
div.stButton > button:hover { border-color:var(--navy); color:var(--navy); }
div.stForm { border:1px solid var(--line); border-radius:18px; padding:22px; background:#fff; }
div.stFormSubmitButton > button { background:var(--navy); color:white; border-color:var(--navy); min-height:48px; }
</style>
""", unsafe_allow_html=True)


def load_reports():
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=REPORT_COLUMNS)
    try:
        df = pd.read_csv(DATA_FILE, dtype=str).fillna("")
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame(columns=REPORT_COLUMNS)
    for column in REPORT_COLUMNS:
        if column not in df.columns:
            df[column] = ""
    return df[REPORT_COLUMNS]


def save_report(report, uploaded_photo):
    if uploaded_photo is not None:
        ext = Path(uploaded_photo.name).suffix.lower()
        image_name = f"{uuid.uuid4().hex}{ext}"
        image_path = IMAGE_DIR / image_name
        image_path.write_bytes(uploaded_photo.getbuffer())
        report["Photo"] = str(image_path)
    else:
        report["Photo"] = ""
    pd.DataFrame([report], columns=REPORT_COLUMNS).to_csv(
        DATA_FILE, mode="a", header=not DATA_FILE.exists(), index=False
    )


def valid_rss_email(email):
    email = email.strip().lower()
    return email.endswith("@rawdalsaleheen.edu.kw") and len(email.split("@", 1)[0]) > 0


def go_home():
    st.session_state.page = "home"
    st.session_state.report_type = None
    st.session_state.selected_item = None


if "page" not in st.session_state:
    st.session_state.page = "home"
if "report_type" not in st.session_state:
    st.session_state.report_type = None
if "selected_item" not in st.session_state:
    st.session_state.selected_item = None

st.markdown('<div class="rss-header">', unsafe_allow_html=True)
if LOGO_PATH.exists():
    c1, c2, c3 = st.columns([1, 1.25, 1])
    with c2:
        st.image(str(LOGO_PATH), use_container_width=True)
st.markdown('<div class="rss-title">RSS Lost & Found</div>', unsafe_allow_html=True)
st.markdown('<div class="rss-subtitle">Rawd Al Saleheen School Lost & Found</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown('<div class="choice-title">What would you like to do?</div>', unsafe_allow_html=True)
    st.markdown('<div class="helper">If you lost something, check the found items first. Someone may have already reported it.</div>', unsafe_allow_html=True)
    if st.button("I LOST AN ITEM", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()
    if st.button("I FOUND AN ITEM", use_container_width=True):
        st.session_state.report_type = "Found"
        st.session_state.page = "form"
        st.rerun()
    if st.button("BROWSE FOUND ITEMS", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()

elif st.session_state.page == "found_items":
    st.markdown('<div class="choice-title">Found Items</div>', unsafe_allow_html=True)
    st.markdown('<div class="helper">Look through items that have already been found before submitting a lost-item report.</div>', unsafe_allow_html=True)
    reports = load_reports()
    found = reports[reports["Type"].str.lower() == "found"].copy() if not reports.empty else reports
    search = st.text_input("Search found items")
    category = st.selectbox("Category", ["All"] + ITEM_CATEGORIES)
    if search and not found.empty:
        mask = (found["ItemName"] + " " + found["Description"] + " " + found["Location"]).str.contains(search, case=False, na=False)
        found = found[mask]
    if category != "All" and not found.empty:
        found = found[found["ItemCategory"] == category]
    if found.empty:
        st.info("No found items match your search yet.")
    else:
        found = found.sort_values("SubmittedAt", ascending=False)
        for _, row in found.iterrows():
            st.markdown(f'<div class="item-card"><div class="item-name">{row["ItemName"]}</div><div class="item-meta">{row["ItemCategory"]} | {row["Building"]} | {row["Location"]}</div><div>{row["Description"]}</div></div>', unsafe_allow_html=True)
            if st.button("View Item / Contact Finder", key=f'view_{row["ID"]}', use_container_width=True):
                st.session_state.selected_item = row.to_dict()
                st.session_state.page = "item_detail"
                st.rerun()
    st.write("")
    if st.button("I DID NOT FIND MY ITEM - REPORT IT", use_container_width=True):
        st.session_state.report_type = "Lost"
        st.session_state.page = "form"
        st.rerun()
    if st.button("Back to Home", use_container_width=True):
        go_home()
        st.rerun()

elif st.session_state.page == "item_detail":
    item = st.session_state.selected_item
    if not item:
        st.session_state.page = "found_items"
        st.rerun()
    st.markdown(f'<div class="choice-title">{item["ItemName"]}</div>', unsafe_allow_html=True)
    photo_path = item.get("Photo", "")
    if photo_path and Path(photo_path).exists():
        st.image(photo_path, use_container_width=True)
    st.write(f'**Category:** {item["ItemCategory"]}')
    st.write(f'**Building:** {item["Building"]}')
    if item.get("GradeLevel"):
        st.write(f'**Grade Level:** {item["GradeLevel"]}')
    if item.get("Class"):
        st.write(f'**Class:** {item["Class"]}')
    st.write(f'**Found at:** {item["Location"]}')
    st.write(f'**Date found:** {item["EventDate"]}')
    st.write(f'**Description:** {item["Description"]}')
    st.markdown("### Contact the finder")
    st.write(item.get("Email", "No contact email provided."))
    if st.button("Back to Found Items", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()

elif st.session_state.page == "form":
    report_type = st.session_state.report_type
    action = "lost" if report_type == "Lost" else "found"
    st.markdown(f'<div class="choice-title">Report a {report_type} Item</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        building = st.selectbox("Building *", BUILDINGS)
    with col2:
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
        email = st.text_input("RSS Email Address *", placeholder="1730@rawdalsaleheen.edu.kw")
        photo = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Submit Report", use_container_width=True)

        if submitted:
            missing_school_info = building in ["Girls Building", "Boys Building"] and (not grade_level or not class_name.strip())
            if not item_name.strip() or not description.strip() or not location.strip() or missing_school_info:
                st.error("Please complete all required fields.")
            elif not valid_rss_email(email):
                st.error("Please enter a valid RSS email ending with @rawdalsaleheen.edu.kw.")
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
                    "Email": email.strip().lower(),
                    "Photo": "",
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
        <p style="color:#667085;margin-bottom:0;">Your report has been recorded.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Back to Home", use_container_width=True):
        go_home()
        st.rerun()
