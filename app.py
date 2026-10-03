import streamlit as st
import pandas as pd
from datetime import date, datetime
from pathlib import Path
import uuid

st.set_page_config(page_title="RSS Lost & Found", layout="centered")

BASE_DIR = Path(__file__).parent
LOGO_DATA = "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"
DATA_FILE = BASE_DIR / "rss_reports.csv"
IMAGE_DIR = BASE_DIR / "rss_item_images"
IMAGE_DIR.mkdir(exist_ok=True)

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
/* Keep Streamlit Material icons as icons. Without this, the upload icon renders as the word “upload”, creating “uploadUpload”. */
span[data-testid="stIconMaterial"],
span[class*="material-symbols"],
.material-symbols-rounded,
.material-symbols-outlined {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined" !important;
    font-weight: normal !important;
    font-style: normal !important;
}
.stApp { background:#fff; color:#172033; }
[data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p,
.stSelectbox label, .stTextInput label, .stTextArea label,
.stDateInput label, .stFileUploader label, .stRadio label {
    color:var(--navy) !important; opacity:1 !important; font-weight:700 !important;
}
/* ALL FORM FIELDS: light grey background, navy text. */
input,
textarea,
[data-baseweb="input"],
[data-baseweb="input"] > div,
[data-baseweb="base-input"],
[data-baseweb="base-input"] > div,
[data-baseweb="select"],
[data-baseweb="select"] > div,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stDateInput"] input,
[data-testid="stSelectbox"] [role="combobox"] {
    background:#EEF2F6 !important;
    background-color:#EEF2F6 !important;
    color:#102a52 !important;
    -webkit-text-fill-color:#102a52 !important;
}

.block-container { max-width:800px; padding-top:2rem; padding-bottom:3rem; }
#MainMenu, footer, header { visibility:hidden; }
.rss-header { text-align:center; margin-bottom:24px; }
.rss-title { color:var(--navy); font-size:2.4rem; font-weight:700; margin:8px 0 4px; }
.rss-subtitle { color:#667085; font-size:1.05rem; margin:0 auto; max-width:560px; }
.contact-box { background:#eef0f3; color:#172033; border:1px solid #d5d9df; border-radius:14px; padding:18px; margin:12px 0; }
.contact-box a { color:#102a52 !important; font-weight:700; text-decoration:underline; }
.choice-title { text-align:center; color:var(--navy); font-size:1.55rem; font-weight:700; margin:30px 0 15px; }
.helper { text-align:center; color:#667085; margin:-6px auto 20px; max-width:620px; }
.success-box { padding:28px; border:1px solid #d8e7dd; border-radius:18px; text-align:center; background:#fbfefc; }
.item-card { border:1px solid var(--line); border-radius:16px; padding:18px; margin:12px 0; background:#fff; }
.item-name { color:var(--navy); font-size:1.3rem; font-weight:700; margin-bottom:4px; }
.item-meta { color:#667085; font-size:.95rem; margin-bottom:8px; }
div.stButton > button { min-height:58px; border-radius:14px; font-size:1.05rem; font-weight:700; border:1px solid #102A52; background:#102A52 !important; color:#FFFFFF !important; }
div.stButton > button p, div.stButton > button span { color:#FFFFFF !important; -webkit-text-fill-color:#FFFFFF !important; }
div.stButton > button:hover { background:#183B6B !important; border-color:#183B6B !important; color:#FFFFFF !important; }
div.stForm { border:1px solid var(--line); border-radius:18px; padding:22px; background:#fff; }
div.stFormSubmitButton > button { background:#102A52 !important; color:#FFFFFF !important; border-color:#102A52 !important; min-height:48px; }
div.stFormSubmitButton > button p, div.stFormSubmitButton > button span { color:#FFFFFF !important; -webkit-text-fill-color:#FFFFFF !important; }

/* SELECT BOXES — override Streamlit/BaseWeb dark-theme backgrounds at EVERY nested level. */
div[data-testid="stSelectbox"] div[data-baseweb="select"],
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background:#EEF2F6 !important;
    background-color:#EEF2F6 !important;
    border-color:#b9bec7 !important;
    box-shadow:none !important;
}

/* Force every nested select layer transparent so the grey parent always shows after interaction. */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div,
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div > div,
div[data-testid="stSelectbox"] div[data-baseweb="select"] [role="combobox"] {
    background:transparent !important;
    background-color:transparent !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] *,
div[data-testid="stSelectbox"] div[data-baseweb="select"] input {
    color:#102a52 !important;
    -webkit-text-fill-color:#102a52 !important;
    opacity:1 !important;
    caret-color:#102a52 !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] svg,
div[data-testid="stSelectbox"] div[data-baseweb="select"] svg * {
    color:#102a52 !important;
    fill:#102a52 !important;
    stroke:#102a52 !important;
}

/* OPEN DROPDOWN — also remove Streamlit's dark popup background. */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] [role="listbox"],
div[data-baseweb="popover"] [role="option"],
ul[role="listbox"],
li[role="option"] {
    background:#EEF2F6 !important;
    background-color:#EEF2F6 !important;
}

div[data-baseweb="popover"] [role="option"] *,
ul[role="listbox"] *,
li[role="option"] * {
    color:#102a52 !important;
    -webkit-text-fill-color:#102a52 !important;
}

div[data-baseweb="popover"] [role="option"]:hover,
div[data-baseweb="popover"] [role="option"][aria-selected="true"],
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background:#c4c9d1 !important;
    background-color:#c4c9d1 !important;
}
/* FINAL OVERRIDE: these are the actual Streamlit/BaseWeb field surfaces. */
.stApp div[data-baseweb="select"] > div,
.stApp div[data-baseweb="input"],
.stApp div[data-baseweb="input"] > div,
.stApp div[data-baseweb="base-input"],
.stApp div[data-baseweb="base-input"] > div,
.stApp input,
.stApp textarea,
.stApp [role="combobox"] {
    background:#EEF2F6 !important;
    background-color:#EEF2F6 !important;
    color:#102a52 !important;
    -webkit-text-fill-color:#102a52 !important;
}
.stApp div[data-baseweb="select"] *,
.stApp div[data-baseweb="input"] *,
.stApp div[data-baseweb="base-input"] * {
    color:#102a52 !important;
    -webkit-text-fill-color:#102a52 !important;
}

/* FINAL FIELD-SURFACE FIX: remove the remaining dark Streamlit pieces. */
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stSelectbox"] [data-baseweb="select"] div,
[data-testid="stSelectbox"] [role="combobox"],
[data-testid="stDateInput"] > div,
[data-testid="stDateInput"] > div > div,
[data-testid="stDateInput"] [data-baseweb="input"],
[data-testid="stDateInput"] [data-baseweb="input"] div,
[data-testid="stDateInput"] input,
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploaderDropzone"] > div,
[data-testid="stFileUploaderDropzone"] section,
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] section > div,
[data-testid="stFileUploader"] button {
    background: #EEF2F6 !important;
    background-color: #EEF2F6 !important;
    color: #102A52 !important;
    -webkit-text-fill-color: #102A52 !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] svg,
[data-testid="stDateInput"] svg,
[data-testid="stFileUploader"] svg {
    color: #102A52 !important;
    fill: #102A52 !important;
}

/* The open select menu is grey too. */
[data-baseweb="popover"],
[data-baseweb="popover"] div,
[data-baseweb="popover"] ul,
[data-baseweb="popover"] li {
    background-color: #EEF2F6 !important;
    color: #102A52 !important;
    -webkit-text-fill-color: #102A52 !important;
}

/* COLOR BALANCE: keep the upload area neutral grey while form fields use blue-grey. */
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploaderDropzone"] > div,
[data-testid="stFileUploaderDropzone"] section,
[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] section > div,
[data-testid="stFileUploader"] button {
    background:#D1D5DB !important;
    background-color:#D1D5DB !important;
    color:#102A52 !important;
    -webkit-text-fill-color:#102A52 !important;
}

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

    # Remove the old water-bottle demonstration record from the visible dataset.
    item = df["ItemName"].astype(str).str.strip().str.lower()
    building = df["Building"].astype(str).str.strip().str.lower()
    location = df["Location"].astype(str).str.strip().str.lower()
    class_name = df["Class"].astype(str).str.strip().str.lower()
    description = df["Description"].astype(str).str.strip().str.lower()
    legacy_test = (
        item.eq("water bottle")
        & building.eq("girls building")
        & (location.eq("11k") | class_name.eq("11k"))
    )
    if legacy_test.any():
        df = df.loc[~legacy_test].copy()
        # Also clean the CSV when it is writable, so the test record stays gone.
        try:
            df[REPORT_COLUMNS].to_csv(DATA_FILE, index=False)
        except OSError:
            pass

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


def resolve_report(report_id):
    """Remove a resolved report from the active listings and delete its saved photo."""
    if not DATA_FILE.exists():
        return False
    try:
        df = pd.read_csv(DATA_FILE, dtype=str).fillna("")
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return False
    if "ID" not in df.columns:
        return False

    match = df["ID"].astype(str) == str(report_id)
    if not match.any():
        return False

    if "Photo" in df.columns:
        for photo_path in df.loc[match, "Photo"].astype(str):
            if photo_path:
                try:
                    photo = Path(photo_path)
                    if photo.exists() and photo.is_file():
                        photo.unlink()
                except OSError:
                    pass

    df = df.loc[~match].copy()
    for column in REPORT_COLUMNS:
        if column not in df.columns:
            df[column] = ""
    df[REPORT_COLUMNS].to_csv(DATA_FILE, index=False)
    return True


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

st.markdown(f"""
<div class="rss-header">
    <img src="data:image/jpeg;base64,{LOGO_DATA}" style="max-width:220px;width:42%;height:auto;margin:0 auto 10px;display:block;">
    <div class="rss-title">Rawd Al Saleheen School Lost & Found</div>
</div>
""", unsafe_allow_html=True)

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
    if st.button("BROWSE MISSING ITEMS", use_container_width=True):
        st.session_state.page = "missing_items"
        st.rerun()

elif st.session_state.page == "found_items":
    st.markdown('<div class="choice-title">Found Items</div>', unsafe_allow_html=True)
    st.markdown('<div class="helper">Look through items that have already been found before submitting a lost-item report.</div>', unsafe_allow_html=True)
    reports = load_reports()
    found = reports[reports["Type"].str.lower() == "found"].copy() if not reports.empty else reports
    search = st.text_input("Search found items")
    if search and not found.empty:
        mask = (found["ItemName"] + " " + found["Description"] + " " + found["Location"]).str.contains(search, case=False, na=False)
        found = found[mask]
    if found.empty:
        st.info("No found items match your search yet.")
    else:
        found = found.sort_values("SubmittedAt", ascending=False)
        for _, row in found.iterrows():
            st.markdown(f'<div class="item-card"><div class="item-name">{row["ItemName"]}</div><div class="item-meta">{row["Building"]} | {row["Location"]}</div><div>{row["Description"]}</div></div>', unsafe_allow_html=True)
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

elif st.session_state.page == "missing_items":
    st.markdown('<div class="choice-title">Missing Items</div>', unsafe_allow_html=True)
    st.markdown('<div class="helper">These are items students have reported missing. If you recognize or found one, open the report to contact the student.</div>', unsafe_allow_html=True)
    reports = load_reports()
    missing = reports[reports["Type"].str.lower() == "lost"].copy() if not reports.empty else reports
    search = st.text_input("Search missing items")
    if search and not missing.empty:
        mask = (missing["ItemName"] + " " + missing["Description"] + " " + missing["Location"]).str.contains(search, case=False, na=False)
        missing = missing[mask]
    if missing.empty:
        st.info("No missing items match your search yet.")
    else:
        missing = missing.sort_values("SubmittedAt", ascending=False)
        for _, row in missing.iterrows():
            st.markdown(f'<div class="item-card"><div class="item-name">{row["ItemName"]}</div><div class="item-meta">{row["Building"]} | {row["Location"]}</div><div>{row["Description"]}</div></div>', unsafe_allow_html=True)
            if st.button("View Missing Item / I Found This", key=f'missing_{row["ID"]}', use_container_width=True):
                st.session_state.selected_item = row.to_dict()
                st.session_state.page = "item_detail"
                st.rerun()
    st.write("")
    if st.button("Back to Home", use_container_width=True, key="missing_back_home"):
        go_home()
        st.rerun()

elif st.session_state.page == "item_detail":
    item = st.session_state.selected_item
    if not item:
        st.session_state.page = "found_items"
        st.rerun()
    contact_email = str(item.get("Email", "")).strip()
    is_lost_item = str(item.get("Type", "")).strip().lower() == "lost"
    if contact_email:
        st.markdown(f'<div class="choice-title">{item["ItemName"]}</div>', unsafe_allow_html=True)
        photo_path = item.get("Photo", "")
        if photo_path and Path(photo_path).exists():
            st.image(photo_path, use_container_width=True)
        st.write(f'**Building:** {item["Building"]}')
        if item.get("GradeLevel"):
            st.write(f'**Grade Level:** {item["GradeLevel"]}')
        if item.get("Class"):
            st.write(f'**Class:** {item["Class"]}')
        place_label = "Last seen at" if is_lost_item else "Found at"
        date_label = "Date lost" if is_lost_item else "Date found"
        st.write(f'**{place_label}:** {item["Location"]}')
        st.write(f'**{date_label}:** {item["EventDate"]}')
        st.write(f'**Description:** {item["Description"]}')
        if is_lost_item:
            st.markdown("### I Found This Item")
            st.markdown(f'<div class="contact-box"><strong>Contact the student:</strong><br><a href="mailto:{contact_email}">{contact_email}</a><br><span>Click the email address to contact the student through Outlook or your email app.</span></div>', unsafe_allow_html=True)
        else:
            st.markdown("### Contact the finder")
            st.markdown(f'<div class="contact-box"><strong>Finder email:</strong><br><a href="mailto:{contact_email}">{contact_email}</a><br><span>Click the email address to contact the finder through Outlook or your email app.</span></div>', unsafe_allow_html=True)

    if contact_email:
        st.markdown("### Item returned?")
        item_id = str(item.get("ID", ""))
        confirm_key = f"confirm_resolve_{item_id}"

        if not st.session_state.get(confirm_key, False):
            st.markdown('<div class="helper">If this item has been returned to its owner, mark the report as resolved to remove it from the active listings.</div>', unsafe_allow_html=True)
            if st.button("MARK AS RESOLVED", use_container_width=True, key=f"resolve_start_{item_id}"):
                st.session_state[confirm_key] = True
                st.rerun()
        else:
            st.markdown('<div style="background:#D1D5DB; color:#FFFFFF; padding:0.85rem 1rem; border-radius:8px; font-weight:700; margin:0.5rem 0 1rem 0;">Are you sure this item has been returned to its owner?</div>', unsafe_allow_html=True)
            confirm_col, cancel_col = st.columns(2)
            with confirm_col:
                if st.button("YES, MARK AS RESOLVED", use_container_width=True, key=f"resolve_yes_{item_id}"):
                    if resolve_report(item_id):
                        st.session_state.pop(confirm_key, None)
                        st.session_state.selected_item = None
                        st.session_state.page = "resolved"
                        st.rerun()
                    else:
                        st.error("This report could not be removed. Please try again.")
            with cancel_col:
                if st.button("CANCEL", use_container_width=True, key=f"resolve_cancel_{item_id}"):
                    st.session_state.pop(confirm_key, None)
                    st.rerun()

    back_label = "Back to Missing Items" if is_lost_item else "Back to Found Items"
    if st.button(back_label, use_container_width=True):
        st.session_state.page = "missing_items" if is_lost_item else "found_items"
        st.rerun()

elif st.session_state.page == "resolved":
    st.markdown("""
    <div class="success-box">
        <h2 style="color:#102a52;margin-top:0;">Item Resolved</h2>
        <p style="color:#667085;margin-bottom:0;">The report has been removed from the active Lost & Found listings.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Back to Home", use_container_width=True, key="resolved_home"):
        go_home()
        st.rerun()

elif st.session_state.page == "form":
    report_type = st.session_state.report_type
    action = "lost" if report_type == "Lost" else "found"
    st.markdown(f'<div class="choice-title">Report a {report_type} Item</div>', unsafe_allow_html=True)

    building = st.selectbox("Building *", BUILDINGS, help="Choose the school building where the item was lost or found.")

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
        item_name = st.text_input("Item name *", placeholder="What item was lost or found?")
        description = st.text_area("Description *", placeholder="Describe the item: color, brand, size, or any detail that can help identify it.", height=100)
        location = st.selectbox("Place *", location_options, help="Choose the exact place where the item was lost or found.")
        event_date = st.date_input(f"Date it was {action} *", value=date.today(), max_value=date.today())
        email = st.text_input("Your RSS email *", placeholder="Email e.g. 1730@rawdalsaleheen.edu.kw", help="Write your RSS email here. It is required so someone can contact you through Outlook. Your name is not displayed.")
        photo = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"], help="Upload a clear photo of the item if you have one.")
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
                    "ItemCategory": "",
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
