import streamlit as st

st.set_page_config(page_title="RSS Lost & Found", layout="centered")

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

if "reports" not in st.session_state:
    st.session_state.reports = []

st.title("Rawd Al Saleheen School")
st.subheader("Lost & Found")
st.caption("Done by Nour O. Al Sultan")

tab1, tab2 = st.tabs(["Browse Items", "Report Item"])

with tab1:
    if not st.session_state.reports:
        st.info("No items have been reported in this session yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.reports)):
            st.markdown(f"### {item['name']}")
            st.write(f"**Status:** {item['status']}")
            st.write(f"**Category:** {item['category']} — {item['item_type']}")
            st.write(f"**Building:** {item['building']}")
            st.write(f"**Location:** {item['location']}")
            st.write(item["description"])
            st.divider()

with tab2:
    with st.form("report_form", clear_on_submit=True):
        status = st.selectbox("Report type", ["Lost", "Found"])
        building = st.selectbox(
            "Building",
            ["Girls Building", "Boys Building", "Administration Building"]
        )
        category = st.selectbox("Category", list(ITEM_TYPES))
        item_type = st.selectbox("Item type", ITEM_TYPES[category])
        name = st.text_input("Item name")
        location = st.text_input("Location")
        description = st.text_area("Description")
        email = st.text_input("RSS email")
        submitted = st.form_submit_button("Submit Report", use_container_width=True)

    if submitted:
        if not name.strip() or not location.strip() or not description.strip():
            st.error("Please complete the item name, location, and description.")
        elif not email.strip().lower().endswith("@rawdalsaleheen.edu.kw"):
            st.error("Please enter a valid RSS email.")
        else:
            st.session_state.reports.append({
                "status": status,
                "building": building,
                "category": category,
                "item_type": item_type,
                "name": name.strip(),
                "location": location.strip(),
                "description": description.strip(),
                "email": email.strip().lower(),
            })
            st.success("Report submitted.")
