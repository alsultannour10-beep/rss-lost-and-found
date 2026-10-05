import json
import uuid
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="RSS Lost & Found", layout="centered")

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "rss_reports.csv"
IMAGE_DIR = BASE_DIR / "rss_item_images"

ITEM_TYPES = {
    "Electronics": ["Tablet", "Phone", "Laptop", "Headphones", "Calculator", "Smartwatch", "Charger", "Other"],
    "Water Bottle": ["Bottle", "Tumbler", "Flask", "Other"],
    "Clothing": ["Shirt", "T-Shirt", "Hoodie", "Sweater", "Jacket", "Pants", "Dress", "Uniform", "Other"],
    "Bag": ["Backpack", "Handbag", "Sports Bag", "Tote Bag", "Pouch", "Other"],
    "School Supplies": ["Pencil Case", "Pen", "Ruler", "Scissors", "Other"],
    "Book": ["Textbook", "Notebook", "Workbook", "Reading Book", "Folder", "Other"],
    "Lunch Box": ["Lunch Box", "Food Container", "Snack Box", "Other"],
    "Eyewear": ["Glasses", "Sunglasses", "Safety Glasses", "Other"],
    "Locker Keys": ["Locker Key", "Other"],
    "Other": ["Other"],
}

COLORS = [
    "Black", "White", "Grey", "Silver", "Gold", "Red", "Orange", "Yellow",
    "Green", "Blue", "Navy", "Purple", "Pink", "Brown", "Beige",
    "Clear/Transparent", "Multicolor", "Other"
]

VERIFY = {
    "Electronics": {
        "Color": COLORS,
        "Brand": ["Apple", "Samsung", "Microsoft", "Lenovo", "HP", "Dell", "ASUS", "Acer", "Huawei", "Sony", "JBL", "Bose", "Logitech", "Casio", "Other", "No visible brand"],
        "Case / Cover": ["No case/cover", "Black", "White", "Grey", "Clear/Transparent", "Red", "Green", "Blue", "Navy", "Purple", "Pink", "Other"],
        "Sticker / Decoration": ["None", "One sticker", "Multiple stickers", "Name label", "School label", "Other"],
        "Damage / Mark": ["None", "Scratch", "Crack", "Dent", "Chip", "Scuff", "Missing part", "Other"],
    },
    "Water Bottle": {
        "Color": COLORS,
        "Brand": ["Stanley", "Hydro Flask", "YETI", "Contigo", "Nike", "Adidas", "Other", "No visible brand"],
        "Lid": ["Straw lid", "Flip lid", "Screw lid", "Spout lid", "Other"],
        "Handle": ["No", "Yes"],
        "Sticker / Decoration": ["None", "One sticker", "Multiple stickers", "Name label", "School label", "Other"],
    },
    "Clothing": {
        "Color": COLORS,
        "Brand": ["Nike", "Adidas", "Puma", "Under Armour", "New Balance", "H&M", "Zara", "Other", "No visible brand"],
        "Size": ["XS", "S", "M", "L", "XL", "XXL", "Kids size", "Other", "Unknown"],
        "Pattern / Design": ["Plain", "Striped", "Checkered", "Floral", "Character/cartoon", "Logo/graphic", "Text", "Other"],
        "Damage / Mark": ["None", "Stain", "Tear", "Missing button", "Ink mark", "Other"],
    },
    "Bag": {
        "Color": COLORS,
        "Brand": ["Nike", "Adidas", "Puma", "Under Armour", "Herschel", "JanSport", "Other", "No visible brand"],
        "Pattern / Design": ["Plain", "Striped", "Checkered", "Floral", "Character/cartoon", "Logo/graphic", "Text", "Other"],
        "Keychain / Charm": ["None", "One", "More than one", "Other"],
        "Damage / Mark": ["None", "Scratch", "Tear", "Stain", "Broken zip", "Other"],
        "Name / Initials": ["No", "Yes - printed", "Yes - handwritten", "Yes - label", "Yes - other"],
    },
    "School Supplies": {
        "Color": COLORS,
        "Brand": ["Faber-Castell", "Staedtler", "Pilot", "BIC", "Maped", "Other", "No visible brand"],
        "Pattern / Design": ["Plain", "Character/cartoon", "Logo/graphic", "Text", "Multicolor pattern", "Other"],
        "Name / Initials": ["No", "Yes - printed", "Yes - handwritten", "Yes - sticker", "Yes - other"],
        "Damage / Mark": ["None", "Scratch", "Crack", "Ink mark", "Missing part", "Other"],
        "Sticker / Decoration": ["None", "One sticker", "Multiple stickers", "Other"],
    },
    "Book": {
        "Color": COLORS,
        "Subject": ["Arabic", "English", "Math", "Science", "Islamic", "Social Studies", "Computer", "Other"],
        "Name / Initials": ["No", "Yes - front", "Yes - inside", "Yes - back", "Yes - sticker", "Yes - other"],
        "Cover": ["No extra cover", "Clear cover", "Colored cover", "Decorated cover", "Other"],
        "Damage / Mark": ["None", "Bent corner", "Torn page", "Writing/ink", "Stain", "Other"],
    },
    "Lunch Box": {
        "Color": COLORS,
        "Brand": ["Sistema", "Thermos", "Bentgo", "Tupperware", "Other", "No visible brand"],
        "Pattern / Design": ["Plain", "Character/cartoon", "Logo/graphic", "Text", "Multicolor pattern", "Other"],
        "Compartments": ["One", "Two", "Three", "Four or more", "Other"],
        "Name / Initials": ["No", "Yes - printed", "Yes - handwritten", "Yes - sticker", "Yes - other"],
        "Damage / Mark": ["None", "Scratch", "Crack", "Stain", "Missing part", "Other"],
    },
    "Eyewear": {
        "Frame Color": COLORS,
        "Brand": ["Ray-Ban", "Oakley", "Nike", "Adidas", "Other", "No visible brand"],
        "Frame Shape": ["Round", "Oval", "Square", "Rectangle", "Cat-eye", "Other"],
        "Case": ["No case", "Black", "Brown", "Blue", "Pink", "Clear/Transparent", "Other"],
        "Damage / Mark": ["None", "Scratch", "Crack", "Bent arm", "Missing part", "Other"],
    },
    "Locker Keys": {
        "Key Color": COLORS,
        "Keychain Color": COLORS,
        "Keychain / Charm": ["None", "Plain tag", "Character", "Letter/initial", "Logo", "Other"],
        "Label / Writing": ["None", "Name", "Number", "Word", "Other"],
        "Damage / Mark": ["None", "Scratch", "Bent", "Other"],
    },
    "Other": {
        "Color": COLORS,
        "Name / Initials": ["No", "Yes - printed", "Yes - handwritten", "Yes - engraved", "Yes - sticker", "Yes - other"],
        "Sticker / Decoration": ["None", "One sticker", "Multiple stickers", "Name label", "Other"],
        "Damage / Mark": ["None", "Scratch", "Crack", "Dent", "Stain", "Tear", "Scuff", "Other"],
        "Pattern / Design": ["Plain", "Striped", "Checkered", "Character/cartoon", "Logo/graphic", "Text", "Other"],
        "Brand": ["Other", "No visible brand"],
    },
}

BUILDINGS = ["Girls Building", "Boys Building", "Administration Building"]
GRADE_LEVELS = ["High School", "Middle School", "Elementary School"]

CLASSES = {
    "Girls Building": {
        "High School": ["9K", "9L", "10K", "10L", "11K", "11L", "12K", "12L"],
        "Middle School": ["5K", "5L", "6K", "6L", "7K", "7L", "8K", "8L"],
        "Elementary School": ["1K", "1L", "2K", "2L", "3K", "3L", "4K", "4L"],
    },
    "Boys Building": {
        "High School": ["9H", "9G", "10H", "10G", "11H", "11G", "12H", "12G"],
        "Middle School": ["5H", "5G", "6H", "6G", "7H", "7G", "8H", "8G"],
        "Elementary School": ["1H", "1G", "2H", "2G", "3H", "3G", "4H", "4G"],
    },
}

PLACES = {
    "Girls Building": ["Classroom", "Computer Lab", "Art Room", "Theatre Room", "Gym", "Cafeteria", "Break Area", "Other"],
    "Boys Building": ["Classroom", "Computer Lab", "Art Room", "Ghaneema's Auditorium", "Gym", "Cafeteria", "Break Area", "Other"],
    "Administration Building": ["Library", "Ms Razan Room", "Ms Heba Alodaid Room", "Lobby", "Other"],
}

COLUMNS = [
    "ID", "Type", "Building", "ItemCategory", "ItemType", "GradeLevel", "Class",
    "ItemName", "Description", "Location", "EventDate", "Email", "Photo",
    "VerificationData", "SubmittedAt"
]

def empty_reports():
    return pd.DataFrame(columns=COLUMNS)

@st.cache_data(show_spinner=False, ttl=30)
def load_reports():
    if not DATA_FILE.exists():
        return empty_reports()
    try:
        df = pd.read_csv(DATA_FILE, dtype=str).fillna("")
    except Exception:
        return empty_reports()
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[COLUMNS]

def write_reports(df):
    df[COLUMNS].to_csv(DATA_FILE, index=False)
    load_reports.clear()

def save_report(report, photo):
    if photo is not None:
        try:
            IMAGE_DIR.mkdir(exist_ok=True)
            suffix = Path(photo.name).suffix.lower()
            path = IMAGE_DIR / f"{uuid.uuid4().hex}{suffix}"
            path.write_bytes(photo.getbuffer())
            report["Photo"] = str(path)
        except OSError:
            report["Photo"] = ""
    current = load_reports()
    updated = pd.concat([current, pd.DataFrame([report], columns=COLUMNS)], ignore_index=True)
    write_reports(updated)

def delete_report(report_id):
    df = load_reports()
    if df.empty:
        return False
    mask = df["ID"].astype(str) == str(report_id)
    if not mask.any():
        return False
    for p in df.loc[mask, "Photo"].astype(str):
        if p:
            try:
                path = Path(p)
                if path.exists():
                    path.unlink()
            except OSError:
                pass
    write_reports(df.loc[~mask].copy())
    return True

def valid_email(value):
    value = value.strip().lower()
    return value.endswith("@rawdalsaleheen.edu.kw") and value.split("@", 1)[0] != ""

def parse_verification(value):
    try:
        data = json.loads(str(value))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def goto(page):
    st.session_state.page = page
    st.rerun()

if "page" not in st.session_state:
    st.session_state.page = "home"
if "report_type" not in st.session_state:
    st.session_state.report_type = ""
if "selected_id" not in st.session_state:
    st.session_state.selected_id = ""

st.title("Rawd Al Saleheen School Lost & Found")
st.caption("Done by Nour O. Al Sultan")

page = st.session_state.page

if page == "home":
    st.subheader("What would you like to do?")
    if st.button("I LOST AN ITEM", use_container_width=True):
        goto("found")
    if st.button("I FOUND AN ITEM", use_container_width=True):
        st.session_state.report_type = "Found"
        goto("missing")
    if st.button("BROWSE FOUND ITEMS", use_container_width=True):
        goto("found")
    if st.button("BROWSE MISSING ITEMS", use_container_width=True):
        goto("missing")

elif page in ("found", "missing"):
    want_type = "Found" if page == "found" else "Lost"
    st.subheader("Found Items" if page == "found" else "Missing Items")
    reports = load_reports()
    items = reports[reports["Type"].str.casefold() == want_type.casefold()].copy() if not reports.empty else reports

    with st.form(f"search_{page}"):
        search = st.text_input("Search")
        do_search = st.form_submit_button("SEARCH", use_container_width=True)
    if do_search and search.strip() and not items.empty:
        haystack = (
            items["ItemName"].astype(str) + " " +
            items["ItemType"].astype(str) + " " +
            items["Description"].astype(str) + " " +
            items["Location"].astype(str)
        )
        items = items[haystack.str.contains(search.strip(), case=False, na=False, regex=False)]

    if items.empty:
        st.info("No items match your search yet.")
    else:
        items = items.sort_values("SubmittedAt", ascending=False)
        for row in items.to_dict("records"):
            st.markdown(f"### {row['ItemName']}")
            meta = " | ".join(x for x in [row["ItemCategory"], row["ItemType"], row["Building"], row["Location"]] if x)
            st.caption(meta)
            st.write(row["Description"])
            if st.button("VIEW ITEM", key=f"view_{row['ID']}", use_container_width=True):
                st.session_state.selected_id = row["ID"]
                goto("detail")
            st.divider()

    if page == "found":
        if st.button("I DID NOT FIND MY ITEM - REPORT IT", use_container_width=True):
            st.session_state.report_type = "Lost"
            goto("report_step1")
    elif st.session_state.report_type == "Found":
        if st.button("I DID NOT FIND A MATCH - REPORT FOUND ITEM", use_container_width=True):
            goto("report_step1")

    if st.button("BACK TO HOME", use_container_width=True):
        st.session_state.report_type = ""
        goto("home")

elif page == "report_step1":
    report_type = st.session_state.report_type
    st.subheader(f"Report a {report_type} Item")
    st.write("Step 1 of 2 — choose the location and item type.")

    with st.form("report_step1_form"):
        building = st.selectbox("Building *", ["Select"] + BUILDINGS)
        category = st.selectbox("Item category *", ["Select"] + list(ITEM_TYPES))
        item_type = ""
        if category != "Select":
            item_type = st.selectbox("Item type *", ["Select"] + ITEM_TYPES[category])
        next_step = st.form_submit_button("CONTINUE", use_container_width=True)

    if next_step:
        if building == "Select" or category == "Select" or not item_type or item_type == "Select":
            st.error("Please choose the building, item category, and item type.")
        else:
            st.session_state.draft = {
                "Building": building,
                "ItemCategory": category,
                "ItemType": item_type,
            }
            goto("report_step2")

    if st.button("CANCEL", use_container_width=True):
        goto("home")

elif page == "report_step2":
    report_type = st.session_state.report_type
    draft = st.session_state.get("draft", {})
    if not draft:
        goto("report_step1")

    building = draft["Building"]
    category = draft["ItemCategory"]
    item_type = draft["ItemType"]

    st.subheader(f"Report a {report_type} Item")
    st.caption(f"{category} → {item_type} | {building}")
    st.write("Step 2 of 2 — complete the report.")

    with st.form("report_step2_form", clear_on_submit=False):
        place = st.selectbox("Place *", ["Select"] + PLACES[building])

        grade = ""
        class_name = ""
        if place == "Classroom" and building in CLASSES:
            grade = st.selectbox("Grade Level *", ["Select"] + GRADE_LEVELS)
            if grade != "Select":
                class_name = st.selectbox("Class *", ["Select"] + CLASSES[building][grade])

        other_place = ""
        if place == "Other":
            other_place = st.text_input("Other place *")

        item_name = st.text_input("Item name *", placeholder="Example: Blue water bottle")
        description = st.text_area(
            "Description *",
            placeholder="Describe the item generally. Do not reveal private verification details."
        )

        verification = {}
        if report_type == "Found":
            st.markdown("#### Ownership Verification")
            st.caption("Four private checks are selected automatically for this item category.")
            details = list(VERIFY[category].items())[:4]
            for label, options in details:
                verification[label] = st.selectbox(label + " *", ["Select"] + options, key=f"verify_{label}")

        event_date = st.date_input(
            "Date found *" if report_type == "Found" else "Date lost *",
            value=date.today(),
            max_value=date.today()
        )
        email = st.text_input("Your RSS email *", placeholder="1730@rawdalsaleheen.edu.kw")
        photo = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"])
        submit = st.form_submit_button("SUBMIT REPORT", use_container_width=True)

    if submit:
        location = other_place.strip() if place == "Other" else place
        classroom_missing = place == "Classroom" and building in CLASSES and (
            grade in ("", "Select") or class_name in ("", "Select")
        )
        verification_missing = report_type == "Found" and any(v == "Select" for v in verification.values())

        if place == "Select" or not location or not item_name.strip() or not description.strip() or classroom_missing:
            st.error("Please complete all required fields.")
        elif verification_missing:
            st.error("Please answer all four ownership-verification questions.")
        elif not valid_email(email):
            st.error("Please enter a valid RSS email ending with @rawdalsaleheen.edu.kw.")
        else:
            report = {
                "ID": uuid.uuid4().hex,
                "Type": report_type,
                "Building": building,
                "ItemCategory": category,
                "ItemType": item_type,
                "GradeLevel": "" if grade in ("", "Select") else grade,
                "Class": "" if class_name in ("", "Select") else class_name,
                "ItemName": item_name.strip(),
                "Description": description.strip(),
                "Location": location,
                "EventDate": event_date.isoformat(),
                "Email": email.strip().lower(),
                "Photo": "",
                "VerificationData": json.dumps(verification, ensure_ascii=False),
                "SubmittedAt": datetime.now().isoformat(timespec="seconds"),
            }
            save_report(report, photo)
            st.session_state.pop("draft", None)
            goto("success")

    if st.button("BACK", use_container_width=True):
        goto("report_step1")

elif page == "detail":
    reports = load_reports()
    match = reports[reports["ID"].astype(str) == str(st.session_state.selected_id)] if not reports.empty else reports
    if match.empty:
        st.warning("This report is no longer available.")
        if st.button("BACK TO HOME", use_container_width=True):
            goto("home")
    else:
        item = match.iloc[0].to_dict()
        is_lost = item["Type"].casefold() == "lost"

        st.subheader(item["ItemName"])
        if item["Photo"]:
            try:
                path = Path(item["Photo"])
                if path.exists():
                    st.image(str(path), use_container_width=True)
            except OSError:
                pass

        st.write(f"**Category:** {item['ItemCategory']}")
        if item["ItemType"]:
            st.write(f"**Type:** {item['ItemType']}")
        st.write(f"**Building:** {item['Building']}")
        if item["GradeLevel"]:
            st.write(f"**Grade Level:** {item['GradeLevel']}")
        if item["Class"]:
            st.write(f"**Class:** {item['Class']}")
        st.write(f"**{'Last seen at' if is_lost else 'Found at'}:** {item['Location']}")
        st.write(f"**Date:** {item['EventDate']}")
        st.write(f"**Description:** {item['Description']}")

        if is_lost:
            st.subheader("I Found This Item")
            st.write(f"Contact the student: **{item['Email']}**")
        else:
            verification = parse_verification(item["VerificationData"])
            verified_key = f"verified_{item['ID']}"
            attempts_key = f"attempts_{item['ID']}"
            attempts = int(st.session_state.get(attempts_key, 0))

            if verification and not st.session_state.get(verified_key, False):
                st.subheader("This Is My Item")
                if attempts >= 3:
                    st.error("You have used 3 attempts. Please ask a teacher or staff member for help.")
                else:
                    answers = {}
                    with st.form(f"claim_{item['ID']}"):
                        for label, correct in verification.items():
                            options = VERIFY.get(item["ItemCategory"], {}).get(label, [])
                            if correct not in options:
                                options = options + [correct]
                            answers[label] = st.selectbox(label, ["Select"] + options, key=f"claim_{item['ID']}_{label}")
                        check = st.form_submit_button("CHECK MY ANSWERS", use_container_width=True)

                    if check:
                        if any(v == "Select" for v in answers.values()):
                            st.error("Please answer every question.")
                        elif all(answers.get(k) == v for k, v in verification.items()):
                            st.session_state[verified_key] = True
                            st.rerun()
                        else:
                            st.session_state[attempts_key] = attempts + 1
                            st.error("We couldn't verify this item. Please check your answers or ask a teacher for help.")
            else:
                if verification:
                    st.success("Ownership verification passed.")
                st.subheader("Contact the finder")
                st.write(f"Finder email: **{item['Email']}**")
                st.caption("For valuable electronics, school staff should also ask the claimant to unlock the device or provide another proof of ownership.")

        st.divider()
        st.subheader("Item returned?")
        if st.button("MARK AS RESOLVED", use_container_width=True):
            st.session_state.confirm_resolve = True
        if st.session_state.get("confirm_resolve", False):
            st.warning("Are you sure this item has been returned to its owner?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("YES", use_container_width=True):
                    if delete_report(item["ID"]):
                        st.session_state.confirm_resolve = False
                        goto("resolved")
            with c2:
                if st.button("CANCEL", use_container_width=True):
                    st.session_state.confirm_resolve = False
                    st.rerun()

        if st.button("BACK", use_container_width=True):
            goto("missing" if is_lost else "found")

elif page == "success":
    st.success("Report submitted successfully.")
    if st.button("BACK TO HOME", use_container_width=True):
        st.session_state.report_type = ""
        goto("home")

elif page == "resolved":
    st.success("The report has been removed from the active Lost & Found listings.")
    if st.button("BACK TO HOME", use_container_width=True):
        goto("home")
