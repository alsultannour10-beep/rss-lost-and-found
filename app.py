import streamlit as st
import pandas as pd
from datetime import date, datetime
from pathlib import Path
import uuid
import json


ITEM_TYPES = {
    "Electronics": ["iPad", "Laptop", "Calculator", "Smartwatch", "Charger", "Other"],
    "Water Bottle": ["Bottle", "Tumbler", "Other"],
    "Clothing": ["P.E Shirt", "Senior Hoodie", "School Jacket", "P.E Pants", "School Dress"],
    "Bag": ["Backpack", "Handbag", "Sports Bag", "Tote Bag", "Pouch", "Other"],
    "School Supplies": ["Pencil Case", "Pen", "Ruler", "Scissors", "Other"],
    "Book": ["Textbook", "Notebook", "Workbook", "Reading Book", "Folder"],
    "Lunch Box": ["Lunch Box"],
    "Eyewear": ["Glasses", "Sunglasses"],
    "Locker Keys": ["Locker Key"],
}

COMMON_COLORS = ["Black", "White", "Grey", "Silver", "Gold", "Red", "Orange", "Yellow", "Green", "Blue", "Navy", "Purple", "Pink", "Brown", "Beige", "Clear/Transparent", "Multicolor", "Other"]
YES_NO = ["No", "Yes"]

CATEGORY_VERIFICATION_OPTIONS = {
    "Electronics": {
        "Color": COMMON_COLORS,
        "Brand": ["Apple", "Samsung", "Microsoft", "Lenovo", "HP", "Dell", "ASUS", "Acer", "Huawei", "Xiaomi", "Sony", "JBL", "Bose", "Logitech", "Casio", "Other", "No visible brand"],
        "Case / Cover": ["No case/cover", "Black", "White", "Grey", "Clear/Transparent", "Red", "Green", "Blue", "Navy", "Purple", "Pink", "Other"],
        "Sticker / Decoration": ["None", "One sticker", "Multiple stickers", "Name label", "School label", "Other"],
        "Damage / Mark": ["None", "Scratch", "Crack", "Dent", "Chip", "Scuff", "Missing part", "Other"],
        "Name / Initials": ["No", "Yes - printed", "Yes - handwritten", "Yes - engraved", "Yes - sticker", "Yes - other"],
        "Accessory Attached": ["Nothing", "Charger/cable", "Stylus/pen", "Keyboard", "Mouse", "Strap", "Other"],
    },
    "Water Bottle": {
        "Color": COMMON_COLORS,
        "Brand": ["Stanley", "Hydro Flask", "YETI", "Contigo", "Thermos", "Nike", "Adidas", "Other", "No visible brand"],
        "Lid": ["Straw lid", "Flip lid", "Screw lid", "Spout lid", "Other"],
        "Handle": YES_NO,
        "Sticker / Decoration": ["None", "One sticker", "Multiple stickers", "Name label", "School label", "Other"],
        "Damage / Mark": ["None", "Scratch", "Dent", "Stain", "Scuff", "Other"],
        "Name / Initials": ["No", "Yes - printed", "Yes - handwritten", "Yes - engraved", "Yes - sticker", "Yes - other"],
        "Pattern / Design": ["Plain", "Striped", "Character/cartoon", "Logo/graphic", "Text", "Multicolor pattern", "Other"],
    },
    "Clothing": {
        "Color": COMMON_COLORS,
        "Brand": ["Nike", "Adidas", "Puma", "Under Armour", "New Balance", "H&M", "Zara", "Other", "No visible brand"],
        "Size": ["XS", "S", "M", "L", "XL", "XXL", "Kids size", "Other", "Unknown"],
        "Pattern / Design": ["Plain", "Striped", "Checkered", "Floral", "Character/cartoon", "Logo/graphic", "Text", "Other"],
        "Name / Initials": ["No", "Yes - printed", "Yes - handwritten", "Yes - label", "Yes - other"],
        "Damage / Mark": ["None", "Stain", "Tear", "Missing button", "Ink mark", "Other"],
    },
    "Bag": {
        "Color": COMMON_COLORS,
        "Brand": ["Nike", "Adidas", "Puma", "Under Armour", "Herschel", "JanSport", "Other", "No visible brand"],
        "Pattern / Design": ["Plain", "Striped", "Checkered", "Floral", "Character/cartoon", "Logo/graphic", "Text", "Other"],
        "Name / Initials": ["No", "Yes - printed", "Yes - handwritten", "Yes - label", "Yes - other"],
        "Keychain / Charm": ["None", "One", "More than one", "Other"],
        "Damage / Mark": ["None", "Scratch", "Tear", "Stain", "Broken zip", "Other"],
    },
    "School Supplies": {
        "Color": COMMON_COLORS,
        "Brand": ["Faber-Castell", "Staedtler", "Pilot", "BIC", "Sharpie", "Maped", "Other", "No visible brand"],
        "Pattern / Design": ["Plain", "Character/cartoon", "Logo/graphic", "Text", "Multicolor pattern", "Other"],
        "Name / Initials": ["No", "Yes - printed", "Yes - handwritten", "Yes - sticker", "Yes - other"],
        "Sticker / Decoration": ["None", "One sticker", "Multiple stickers", "Other"],
        "Damage / Mark": ["None", "Scratch", "Crack", "Ink mark", "Missing part", "Other"],
    },
    "Book": {
        "Color": COMMON_COLORS,
        "Subject": ["Arabic", "English", "Math", "Science", "Islamic", "Social Studies", "Computer", "Other"],
        "Name / Initials": ["No", "Yes - front", "Yes - inside", "Yes - back", "Yes - sticker", "Yes - other"],
        "Cover": ["No extra cover", "Clear cover", "Colored cover", "Decorated cover", "Other"],
        "Sticker / Decoration": ["None", "One sticker", "Multiple stickers", "School label", "Other"],
        "Damage / Mark": ["None", "Bent corner", "Torn page", "Writing/ink", "Stain", "Other"],
    },
    "Lunch Box": {
        "Color": COMMON_COLORS,
        "Brand": ["Sistema", "Thermos", "Bentgo", "Tupperware", "Other", "No visible brand"],
        "Pattern / Design": ["Plain", "Character/cartoon", "Logo/graphic", "Text", "Multicolor pattern", "Other"],
        "Name / Initials": ["No", "Yes - printed", "Yes - handwritten", "Yes - sticker", "Yes - other"],
        "Compartments": ["One", "Two", "Three", "Four or more", "Other"],
        "Damage / Mark": ["None", "Scratch", "Crack", "Stain", "Missing part", "Other"],
    },
    "Eyewear": {
        "Frame Color": COMMON_COLORS,
        "Brand": ["Ray-Ban", "Oakley", "Nike", "Adidas", "Other", "No visible brand"],
        "Frame Shape": ["Round", "Oval", "Square", "Rectangle", "Cat-eye", "Other"],
        "Case": ["No case", "Black", "Brown", "Blue", "Pink", "Clear/Transparent", "Other"],
        "Damage / Mark": ["None", "Scratch", "Crack", "Bent arm", "Missing part", "Other"],
        "Name / Initials": ["No", "Yes", "Other"],
    },
    "Locker Keys": {
        "Key Color": COMMON_COLORS,
        "Keychain Color": COMMON_COLORS,
        "Keychain / Charm": ["None", "Plain tag", "Character", "Letter/initial", "Logo", "Other"],
        "Label / Writing": ["None", "Name", "Number", "Word", "Other"],
        "Damage / Mark": ["None", "Scratch", "Bent", "Other"],
    },
}

# Legacy options let older reports continue to work.
LEGACY_VERIFICATION_OPTIONS = {
    "Primary color": COMMON_COLORS, "Secondary color": ["None"] + COMMON_COLORS,
    "Case or cover": ["No case/cover", "Soft case", "Hard case", "Folio/book case", "Keyboard case", "Sleeve/pouch", "Protective cover", "Other"],
    "Case/cover color": ["No case/cover"] + COMMON_COLORS,
    "Pattern/design": ["Plain", "Striped", "Checkered", "Floral", "Geometric", "Camouflage", "Character/cartoon", "Logo/graphic", "Text/quote", "Multicolor pattern", "Other"],
    "Sticker/decoration": ["None", "One sticker", "Multiple stickers", "Name label", "School label", "Keychain/charm", "Decorative tape", "Other"],
    "Visible damage/mark": ["None", "Scratch", "Crack", "Dent", "Chip", "Stain", "Tear", "Scuff", "Missing part", "Writing/ink mark", "Other"],
    "Where is the damage/mark?": ["No damage/mark", "Front", "Back", "Top", "Bottom", "Left side", "Right side", "Multiple areas", "Other"],
    "Size": ["Very small", "Small", "Medium", "Large", "Very large", "Other"],
    "Material": ["Plastic", "Metal", "Glass", "Fabric", "Leather", "Rubber", "Silicone", "Wood", "Paper/cardboard", "Mixed materials", "Other"],
    "Name/initials present": ["No", "Yes - printed label", "Yes - handwritten", "Yes - engraved", "Yes - sticker", "Yes - other"],
    "Accessory attached": ["None", "Charger/cable", "Stylus/pen", "Keyboard", "Mouse", "Strap/lanyard", "Keychain/charm", "Bottle lid/straw", "Pouch/bag", "Other"],
}

def get_verification_options(item_category, detail):
    if item_category in CATEGORY_VERIFICATION_OPTIONS and detail in CATEGORY_VERIFICATION_OPTIONS[item_category]:
        return CATEGORY_VERIFICATION_OPTIONS[item_category][detail]
    # Compatibility with the immediately previous version and older reports.
    for options in CATEGORY_VERIFICATION_OPTIONS.values():
        if detail in options:
            return options[detail]
    return LEGACY_VERIFICATION_OPTIONS.get(detail, ["Other"])

def parse_verification_data(value):
    if not value or pd.isna(value):
        return {}
    try:
        data = json.loads(str(value))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, TypeError, ValueError):
        return {}

def verification_selectors(prefix, selected_categories, item_category=""):
    """Render only the secret-detail questions selected for this item category."""
    answers = {}
    for category in selected_categories:
        options = get_verification_options(item_category, category)
        answers[category] = st.selectbox(
            category,
            ["Select an answer"] + options,
            key=f"{prefix}_{category}",
        )
    return answers

st.set_page_config(page_title="RSS Lost & Found", layout="centered")

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "rss_reports.csv"
IMAGE_DIR = BASE_DIR / "rss_item_images"

BUILDINGS = ["Girls Building", "Boys Building", "Administration Building"]
GRADE_LEVELS = ["High School", "Middle School", "Elementary School"]
GIRLS_HIGH_SCHOOL = ["9K", "9L", "10K", "10L", "11K", "11L", "12K", "12L"]
GIRLS_MIDDLE_SCHOOL = ["5K", "5L", "6K", "6L", "7K", "7L", "8K", "8L"]
GIRLS_ELEMENTARY = ["1K", "1L", "2K", "2L", "3K", "3L", "4K", "4L"]
BOYS_HIGH_SCHOOL = ["9H", "9G", "10H", "10G", "11H", "11G", "12H", "12G"]
BOYS_MIDDLE_SCHOOL = ["5H", "5G", "6H", "6G", "7H", "7G", "8H", "8G"]
BOYS_ELEMENTARY = ["1H", "1G", "2H", "2G", "3H", "3G", "4H", "4G"]
GIRLS_SPECIAL_LOCATIONS = ["Computer Lab", "Art Room", "Theatre Room", "Gym", "Cafeteria", "Break Area"]
BOYS_SPECIAL_LOCATIONS = ["Computer Lab", "Art Room", "Ghaneema's Auditorium", "Gym", "Cafeteria", "Break Area"]
ADMIN_LOCATIONS = ["Library", "Ms Razan Room", "Ms Heba Alodaid Room", "Lobby"]
REPORT_COLUMNS = [
    "ID", "Type", "Building", "ItemCategory", "ItemType", "GradeLevel", "Class", "ItemName",
    "Description", "Location", "EventDate", "Email", "Photo", "VerificationQuestion", "VerificationAnswer", "VerificationData", "SubmittedAt"
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
.item-card { border:1px solid var(--line); border-radius:16px; padding:18px; margin:12px 0; background:#fff; box-shadow:0 3px 12px rgba(16,42,82,.06); }
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


@st.cache_data(show_spinner=False, ttl=60)
def load_reports():
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=REPORT_COLUMNS)
    try:
        df = pd.read_csv(DATA_FILE, dtype=str).fillna("")
    except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError, UnicodeError):
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
        # Hide the old demo row in memory only. Do not write to disk during page loads.
        df = df.loc[~legacy_test].copy()

    return df[REPORT_COLUMNS]


def save_report(report, uploaded_photo):
    """Save a report safely, including reports created before new columns were added."""
    if uploaded_photo is not None:
        ext = Path(uploaded_photo.name).suffix.lower()
        image_name = f"{uuid.uuid4().hex}{ext}"
        image_path = IMAGE_DIR / image_name
        try:
            IMAGE_DIR.mkdir(parents=True, exist_ok=True)
            image_path.write_bytes(uploaded_photo.getbuffer())
            report["Photo"] = str(image_path)
        except OSError:
            report["Photo"] = ""
    else:
        report["Photo"] = ""

    # Rewrite the small CSV in one pass instead of appending rows with a
    # different number of columns. This keeps older reports compatible with
    # Ownership Verification and avoids CSV parser/loading problems.
    existing = load_reports()
    new_row = pd.DataFrame([report], columns=REPORT_COLUMNS)
    combined = pd.concat([existing, new_row], ignore_index=True)
    combined[REPORT_COLUMNS].to_csv(DATA_FILE, index=False)
    load_reports.clear()


def valid_rss_email(email):
    email = email.strip().lower()
    return email.endswith("@rawdalsaleheen.edu.kw") and len(email.split("@", 1)[0]) > 0


def normalize_verification_answer(value):
    """Normalize an ownership-verification answer for a simple school prototype check."""
    return " ".join(str(value).strip().lower().split())


def resolve_report(report_id):
    """Remove a resolved report from the active listings and delete its saved photo."""
    if not DATA_FILE.exists():
        return False
    try:
        df = pd.read_csv(DATA_FILE, dtype=str).fillna("")
    except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError, UnicodeError):
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
    load_reports.clear()
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
    <div class="rss-title">Rawd Al Saleheen School Lost & Found</div>
    <div style="margin-top:8px;color:#667085;font-size:15px;">Done by Nour O. Al Sultan</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown('<div class="choice-title">What would you like to do?</div>', unsafe_allow_html=True)
    st.markdown('<div class="helper">If you lost something, check the found items first. Someone may have already reported it.</div>', unsafe_allow_html=True)
    if st.button("I LOST AN ITEM", use_container_width=True):
        st.session_state.page = "found_items"
        st.rerun()
    if st.button("I FOUND AN ITEM", use_container_width=True):
        # First show missing-item reports so the finder can try to match the item
        # before creating a new found-item report.
        st.session_state.report_type = "Found"
        st.session_state.page = "missing_items"
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
        mask = (found["ItemName"] + " " + found["Description"] + " " + found["Location"]).str.contains(search, case=False, na=False, regex=False)
        found = found[mask]
    if found.empty:
        st.info("No found items match your search yet.")
    else:
        found = found.sort_values("SubmittedAt", ascending=False)
        for row in found.to_dict("records"):
            st.markdown(f'<div class="item-card"><div class="item-name">{row["ItemName"]}</div><div class="item-meta">{row["Building"]} | {row["Location"]}</div><div>{row["Description"]}</div></div>', unsafe_allow_html=True)
            if st.button("View Item / Contact Finder", key=f'view_{row["ID"]}', use_container_width=True):
                st.session_state.selected_item = row
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
        mask = (missing["ItemName"] + " " + missing["Description"] + " " + missing["Location"]).str.contains(search, case=False, na=False, regex=False)
        missing = missing[mask]
    if missing.empty:
        st.info("No missing items match your search yet.")
    else:
        missing = missing.sort_values("SubmittedAt", ascending=False)
        for row in missing.to_dict("records"):
            st.markdown(f'<div class="item-card"><div class="item-name">{row["ItemName"]}</div><div class="item-meta">{row["Building"]} | {row["Location"]}</div><div>{row["Description"]}</div></div>', unsafe_allow_html=True)
            if st.button("View Missing Item / I Found This", key=f'missing_{row["ID"]}', use_container_width=True):
                st.session_state.selected_item = row
                st.session_state.page = "item_detail"
                st.rerun()
    st.write("")
    if st.session_state.report_type == "Found":
        if st.button("I DID NOT FIND A MATCH - REPORT FOUND ITEM", use_container_width=True):
            st.session_state.report_type = "Found"
            st.session_state.page = "form"
            st.rerun()
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
        item_category = str(item.get("ItemCategory", "")).strip()
        if item_category:
            st.write(f'**Item category:** {item_category}')
        item_type = str(item.get("ItemType", "")).strip()
        if item_type:
            st.write(f'**Item type:** {item_type}')
        place_label = "Last seen at" if is_lost_item else "Found at"
        date_label = "Date lost" if is_lost_item else "Date found"
        st.write(f'**{place_label}:** {item["Location"]}')
        st.write(f'**{date_label}:** {item["EventDate"]}')
        st.write(f'**Description:** {item["Description"]}')
        if is_lost_item:
            st.markdown("### I Found This Item")
            st.markdown(f'<div class="contact-box"><strong>Contact the student:</strong><br><a href="mailto:{contact_email}">{contact_email}</a><br><span>Click the email address to contact the student through Outlook or your email app.</span></div>', unsafe_allow_html=True)
        else:
            st.markdown("### Ownership Verification")
            verification_data = parse_verification_data(item.get("VerificationData", ""))
            verification_question = str(item.get("VerificationQuestion", "")).strip()
            verification_answer = str(item.get("VerificationAnswer", "")).strip()
            verified_key = f"ownership_verified_{item.get('ID', '')}"

            if verification_data and not st.session_state.get(verified_key, False):
                item_id = str(item.get("ID", ""))
                attempts_key = f"ownership_attempts_{item_id}"
                attempts = st.session_state.get(attempts_key, 0)
                st.markdown("### This Is My Item")
                st.markdown('<div class="helper">Answer the private details chosen by the finder. All answers must match. We will not show which answer is wrong.</div>', unsafe_allow_html=True)

                if attempts >= 3:
                    st.error("You have used 3 verification attempts. Please ask a teacher or staff member for help verifying this item.")
                else:
                    with st.form(f"claim_form_{item_id}"):
                        claim_answers = verification_selectors(f"claim_{item_id}", verification_data.keys(), str(item.get("ItemCategory", "")))
                        st.caption(f"Attempts remaining: {3 - attempts}")
                        check_answers = st.form_submit_button("CHECK MY ANSWERS", use_container_width=True)
                    if check_answers:
                        unanswered = [k for k, v in claim_answers.items() if v == "Select an answer"]
                        if unanswered:
                            st.error("Please answer every question before checking your answers.")
                        else:
                            all_correct = all(claim_answers.get(k) == v for k, v in verification_data.items())
                            if all_correct:
                                st.session_state[verified_key] = True
                                st.rerun()
                            else:
                                attempts += 1
                                st.session_state[attempts_key] = attempts
                                if attempts >= 3:
                                    st.error("We couldn't verify this item. Please ask a teacher or staff member for help.")
                                else:
                                    st.error("We couldn't verify this item. Check your answers and try again, or ask a teacher for help.")
            elif verification_question and verification_answer and not st.session_state.get(verified_key, False):
                # Backward compatibility for reports created with the older question/answer system.
                st.markdown(f"**Verification question:** {verification_question}")
                claim_answer = st.text_input("Your answer *", key=f"claim_answer_{item.get('ID', '')}")
                if st.button("VERIFY OWNERSHIP", use_container_width=True, key=f"verify_{item.get('ID', '')}"):
                    if normalize_verification_answer(claim_answer) == normalize_verification_answer(verification_answer):
                        st.session_state[verified_key] = True
                        st.rerun()
                    else:
                        st.error("That answer does not match the private verification detail.")
            else:
                if verification_data or (verification_question and verification_answer):
                    st.success("Ownership verification passed.")
                else:
                    st.info("This report was created before Ownership Verification was added, so no private verification details are available.")
                st.markdown("### Contact the finder")
                st.markdown(f'<div class="contact-box"><strong>Finder email:</strong><br><a href="mailto:{contact_email}">{contact_email}</a><br><span>Click the email address to contact the finder through Outlook or your email app.</span></div>', unsafe_allow_html=True)
                st.caption("For valuable electronics, the finder or school staff should also ask the claimant to unlock the device or show another proof of ownership before it is returned.")

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

    # Start with no preselected building/place so a shared link opens cleanly.
    building = st.selectbox(
        "Building *",
        BUILDINGS,
        index=None,
        placeholder="Select a building",
        help="Choose the school building where the item was lost or found.",
    )

    grade_level = ""
    class_name = ""
    location = ""
    custom_location = ""

    # Place comes directly after Building. Grade Level and Class only appear
    # when Classroom is selected in the Girls or Boys building.
    if building == "Girls Building":
        location_options = ["Classroom"] + GIRLS_SPECIAL_LOCATIONS + ["Other"]
    elif building == "Boys Building":
        location_options = ["Classroom"] + BOYS_SPECIAL_LOCATIONS + ["Other"]
    elif building == "Administration Building":
        location_options = ADMIN_LOCATIONS + ["Other"]
    else:
        location_options = []

    if building:
        location_choice = st.selectbox(
            "Place *",
            location_options,
            index=None,
            placeholder="Select a place",
            help="Choose the exact place where the item was lost or found.",
        )

        if location_choice == "Classroom" and building in ["Girls Building", "Boys Building"]:
            grade_level = st.selectbox(
                "Grade Level *",
                GRADE_LEVELS,
                index=None,
                placeholder="Select a grade level",
            )
            if grade_level:
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
                class_name = st.selectbox(
                    "Class *",
                    class_map[grade_level],
                    index=None,
                    placeholder="Select a class",
                ) or ""

        if location_choice == "Other":
            custom_location = st.text_input(
                "Other place *",
                placeholder="Type the place",
                help="Enter the place if it is not listed above.",
            )
            location = custom_location.strip()
        else:
            location = location_choice or ""

    st.markdown("### Item Details")
    item_category = st.selectbox(
        "Item category *",
        list(ITEM_TYPES.keys()),
        index=None,
        placeholder="Select an item category",
        help="Choose what kind of item this is. The next choices will be filtered to match it.",
        key="report_item_category",
    )

    item_type = ""
    if item_category:
        item_type = st.selectbox(
            "Item type *",
            ITEM_TYPES[item_category],
            index=None,
            placeholder="Select an item type",
            key="report_item_type",
        ) or ""

    item_name = st.text_input("Item name *", placeholder="Example: Blue water bottle", key="report_item_name")
    description = st.text_area(
        "Description *",
        placeholder="Describe the item generally, but do not reveal the secret details.",
        height=100,
        key="report_description",
    )

    verification_question = ""
    verification_answer = ""
    verification_data = {}
    if report_type == "Found" and item_category:
        st.markdown("### Help Us Return It to the Right Person")
        st.caption("Choose how many secret checks to use. The questions are automatically filtered for this item category, so you will not see unrelated choices.")

        # Performance-friendly verification: instead of a large multiselect that
        # rebuilds several dependent widgets on every click, use the first 3–5
        # category-specific checks. This keeps the form simple and responsive.
        available_details = list(CATEGORY_VERIFICATION_OPTIONS[item_category].keys())
        max_checks = min(5, len(available_details))
        min_checks = min(3, max_checks)
        default_checks = min(4, max_checks)
        check_count = st.selectbox(
            "Number of secret details *",
            list(range(min_checks, max_checks + 1)),
            index=list(range(min_checks, max_checks + 1)).index(default_checks),
            help="3 minimum, 4 recommended, 5 maximum when available.",
            key="report_verification_count",
        )
        verification_categories = available_details[:check_count]
        st.caption("Secret checks: " + ", ".join(verification_categories))
        verification_data = verification_selectors(
            "finder_verification", verification_categories, item_category
        )

    event_date = st.date_input(f"Date it was {action} *", value=date.today(), max_value=date.today(), key="report_event_date")
    email = st.text_input("Your RSS email *", placeholder="Email e.g. 1730@rawdalsaleheen.edu.kw", help="Write your RSS email here. It is required so someone can contact you through Outlook. Your name is not displayed.", key="report_email")
    photo = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"], help="Upload a clear photo of the item if you have one.", key="report_photo")
    submitted = st.button("Submit Report", use_container_width=True, key="submit_report")

    if submitted:
        classroom_selected = location_choice == "Classroom" if building else False
        missing_school_info = classroom_selected and (not grade_level or not class_name.strip())
        missing_other_place = building and location_choice == "Other" and not custom_location.strip()
        verification_count = len(verification_data)
        missing_verification = report_type == "Found" and (
            verification_count < 3
            or verification_count > 5
            or any(v == "Select an answer" for v in verification_data.values())
        )
        if not building or not location or not item_category or not item_type or not item_name.strip() or not description.strip() or missing_school_info or missing_other_place or missing_verification:
            if missing_verification:
                st.error("For a found item, answer each secret detail before submitting.")
            else:
                st.error("Please complete all required fields.")
        elif not valid_rss_email(email):
            st.error("Please enter a valid RSS email ending with @rawdalsaleheen.edu.kw.")
        else:
            report = {
                "ID": uuid.uuid4().hex,
                "Type": report_type,
                "Building": building,
                "ItemCategory": item_category,
                "ItemType": item_type,
                "GradeLevel": grade_level or "",
                "Class": class_name.strip(),
                "ItemName": item_name.strip(),
                "Description": description.strip(),
                "Location": location.strip(),
                "EventDate": event_date.isoformat(),
                "Email": email.strip().lower(),
                "Photo": "",
                "VerificationQuestion": verification_question.strip(),
                "VerificationAnswer": verification_answer.strip(),
                "VerificationData": json.dumps(verification_data, ensure_ascii=False),
                "SubmittedAt": datetime.now().isoformat(timespec="seconds"),
            }
            save_report(report, photo)
            st.session_state.page = "success"
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
