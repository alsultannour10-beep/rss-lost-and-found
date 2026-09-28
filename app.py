
import streamlit as st
from datetime import datetime
from difflib import SequenceMatcher

st.set_page_config(
    page_title="RSS Lost & Found",
    page_icon="🔎",
    layout="wide",
)

# -----------------------------
# Demo data storage
# -----------------------------
if "items" not in st.session_state:
    st.session_state.items = [
        {
            "id": 1,
            "type": "Found",
            "name": "Black Water Bottle",
            "description": "Black reusable water bottle with a silver cap.",
            "building": "Girls Building",
            "floor": "2nd Floor",
            "location": "Classroom 10K",
            "grade": "Grade 10",
            "date": "September 28, 2026",
            "time": "10:30 AM",
            "status": "Found",
            "reporter": "RSS Lost & Found",
            "photo": None,
        },
        {
            "id": 2,
            "type": "Lost",
            "name": "Blue Pencil Case",
            "description": "Small blue pencil case with school supplies inside.",
            "building": "Girls Building",
            "floor": "1st Floor",
            "location": "Library",
            "grade": "Grade 9",
            "date": "September 28, 2026",
            "time": "9:15 AM",
            "status": "Lost",
            "reporter": "Student",
            "photo": None,
        },
    ]

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 18px;
        color: #666;
        margin-top: 0;
        margin-bottom: 25px;
    }
    .item-card {
        padding: 18px;
        border: 1px solid #ddd;
        border-radius: 14px;
        margin-bottom: 14px;
        background-color: #ffffff;
    }
    .status {
        font-weight: 700;
        padding: 5px 10px;
        border-radius: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Header
# -----------------------------
st.markdown('<p class="main-title">🔎 RSS Lost & Found</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">A school-wide system for finding lost belongings across RSS.</p>',
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("🏫 RSS Lost & Found")
    st.write("Help students and staff reconnect with their belongings.")

    page = st.radio(
        "Go to",
        [
            "🏠 Home",
            "➕ Report an Item",
            "🔍 Search Items",
            "🤖 Smart Match",
        ],
    )

    st.divider()
    st.caption("Tech Expo Project")
    st.caption("Rawd Al Saleheen Bilingual School")

# -----------------------------
# Helper functions
# -----------------------------
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_matches(item):
    matches = []

    if item["type"] == "Lost":
        opposite = "Found"
    else:
        opposite = "Lost"

    for other in st.session_state.items:
        if other["id"] == item["id"]:
            continue
        if other["type"] != opposite:
            continue
        if other["status"] == "Returned":
            continue

        name_score = similarity(item["name"], other["name"])
        desc_score = similarity(item["description"], other["description"])

        location_score = 0
        if item["building"] == other["building"]:
            location_score += 0.25
        if item["floor"] == other["floor"]:
            location_score += 0.15
        if item["location"] == other["location"]:
            location_score += 0.20

        total = (name_score * 0.45) + (desc_score * 0.15) + location_score

        if total >= 0.45:
            matches.append((total, other))

    matches.sort(key=lambda x: x[0], reverse=True)
    return matches


# -----------------------------
# HOME
# -----------------------------
if page == "🏠 Home":
    total = len(st.session_state.items)
    lost = sum(1 for x in st.session_state.items if x["status"] == "Lost")
    found = sum(1 for x in st.session_state.items if x["status"] == "Found")
    returned = sum(1 for x in st.session_state.items if x["status"] == "Returned")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📦 Total Reports", total)
    c2.metric("🔴 Lost", lost)
    c3.metric("🔵 Found", found)
    c4.metric("🟢 Returned", returned)

    st.divider()

    st.subheader("How it works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 1️⃣ Report")
        st.write("Report something you lost or found and add its location.")

    with col2:
        st.markdown("### 2️⃣ Search")
        st.write("Search by item, building, floor, class, or date.")

    with col3:
        st.markdown("### 3️⃣ Match")
        st.write("Smart Match looks for similar lost and found reports.")

    st.divider()

    st.subheader("📌 Recent Reports")

    for item in reversed(st.session_state.items[-5:]):
        with st.container(border=True):
            left, right = st.columns([4, 1])

            with left:
                st.markdown(f"### {item['name']}")
                st.write(item["description"])
                st.caption(
                    f"📍 {item['building']} • {item['floor']} • {item['location']}"
                )
                st.caption(
                    f"🏫 {item['grade']} • 📅 {item['date']} • 🕐 {item['time']}"
                )

            with right:
                st.write(f"**{item['status']}**")

# -----------------------------
# REPORT
# -----------------------------
elif page == "➕ Report an Item":
    st.header("➕ Report an Item")
    st.write("Add the details so the owner can find their item.")

    with st.form("report_form", clear_on_submit=True):
        item_type = st.radio(
            "What are you reporting?",
            ["Lost", "Found"],
            horizontal=True,
        )

        name = st.text_input(
            "Item name *",
            placeholder="Example: Black AirPods case",
        )

        description = st.text_area(
            "Description *",
            placeholder="Describe the item, color, brand, stickers, etc.",
        )

        col1, col2 = st.columns(2)

        with col1:
            building = st.selectbox(
                "Building *",
                [
                    "Girls Building",
                    "Boys Building",
                    "KG / Elementary Building",
                ],
            )

            floor = st.selectbox(
                "Floor",
                [
                    "Ground Floor",
                    "1st Floor",
                    "2nd Floor",
                    "3rd Floor",
                    "Other",
                ],
            )

            grade = st.selectbox(
                "Grade",
                [
                    "KG",
                    "Grade 1",
                    "Grade 2",
                    "Grade 3",
                    "Grade 4",
                    "Grade 5",
                    "Grade 6",
                    "Grade 7",
                    "Grade 8",
                    "Grade 9",
                    "Grade 10",
                    "Grade 11",
                    "Grade 12",
                    "Staff",
                    "Unknown",
                ],
            )

        with col2:
            location = st.text_input(
                "Specific location *",
                placeholder="Example: Classroom 10K / cafeteria / hallway",
            )

            date = st.date_input("Date")

            time = st.time_input("Approximate time")

            reporter = st.text_input(
                "Your name",
                placeholder="Optional",
            )

        photo = st.file_uploader(
            "Add a photo (optional)",
            type=["png", "jpg", "jpeg"],
        )

        submitted = st.form_submit_button(
            "🚀 Submit Report",
            use_container_width=True,
        )

        if submitted:
            if not name.strip() or not description.strip() or not location.strip():
                st.error("Please complete all required fields marked with *.")
            else:
                new_id = max([x["id"] for x in st.session_state.items], default=0) + 1

                new_item = {
                    "id": new_id,
                    "type": item_type,
                    "name": name.strip(),
                    "description": description.strip(),
                    "building": building,
                    "floor": floor,
                    "location": location.strip(),
                    "grade": grade,
                    "date": date.strftime("%B %d, %Y"),
                    "time": time.strftime("%I:%M %p"),
                    "status": item_type,
                    "reporter": reporter.strip() if reporter.strip() else "Anonymous",
                    "photo": photo.getvalue() if photo else None,
                }

                st.session_state.items.append(new_item)

                st.success("✅ Your report has been added!")

                matches = find_matches(new_item)

                if matches:
                    st.info(
                        f"🤖 Smart Match found {len(matches)} possible matching report(s). "
                        "Check the Smart Match page."
                    )

# -----------------------------
# SEARCH
# -----------------------------
elif page == "🔍 Search Items":
    st.header("🔍 Search Lost & Found")

    col1, col2, col3 = st.columns(3)

    with col1:
        search = st.text_input(
            "Search",
            placeholder="water bottle, calculator, AirPods...",
        )

    with col2:
        status_filter = st.selectbox(
            "Status",
            ["All", "Lost", "Found", "Returned"],
        )

    with col3:
        building_filter = st.selectbox(
            "Building",
            [
                "All",
                "Girls Building",
                "Boys Building",
                "KG / Elementary Building",
            ],
        )

    col4, col5 = st.columns(2)

    with col4:
        floor_filter = st.selectbox(
            "Floor",
            [
                "All",
                "Ground Floor",
                "1st Floor",
                "2nd Floor",
                "3rd Floor",
                "Other",
            ],
        )

    with col5:
        grade_filter = st.selectbox(
            "Grade",
            [
                "All",
                "KG",
                "Grade 1",
                "Grade 2",
                "Grade 3",
                "Grade 4",
                "Grade 5",
                "Grade 6",
                "Grade 7",
                "Grade 8",
                "Grade 9",
                "Grade 10",
                "Grade 11",
                "Grade 12",
                "Staff",
                "Unknown",
            ],
        )

    results = []

    for item in st.session_state.items:
        if search:
            combined = (
                item["name"]
                + " "
                + item["description"]
                + " "
                + item["location"]
            ).lower()

            if search.lower() not in combined:
                continue

        if status_filter != "All" and item["status"] != status_filter:
            continue

        if building_filter != "All" and item["building"] != building_filter:
            continue

        if floor_filter != "All" and item["floor"] != floor_filter:
            continue

        if grade_filter != "All" and item["grade"] != grade_filter:
            continue

        results.append(item)

    st.write(f"**{len(results)} report(s) found**")

    if not results:
        st.info("No items matched your search.")
    else:
        for item in reversed(results):
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.subheader(item["name"])
                    st.write(item["description"])

                    st.write(
                        f"📍 **{item['building']}** → {item['floor']} → {item['location']}"
                    )

                    st.write(
                        f"🏫 {item['grade']}  |  📅 {item['date']}  |  🕐 {item['time']}"
                    )

                    st.caption(f"Reported by: {item['reporter']}")

                with col2:
                    st.markdown(f"**{item['status']}**")

                    if item["photo"]:
                        st.image(item["photo"], width=150)

                if item["status"] != "Returned":
                    if st.button(
                        "✅ Mark as Returned",
                        key=f"returned_{item['id']}",
                    ):
                        item["status"] = "Returned"
                        st.success("Item marked as returned!")
                        st.rerun()

# -----------------------------
# SMART MATCH
# -----------------------------
elif page == "🤖 Smart Match":
    st.header("🤖 Smart Match")
    st.write(
        "This feature compares lost and found reports and looks for similarities "
        "in the item name, description, and location."
    )

    lost_items = [
        x for x in st.session_state.items
        if x["type"] == "Lost" and x["status"] == "Lost"
    ]

    if not lost_items:
        st.info("There are currently no active lost-item reports.")
    else:
        for lost in lost_items:
            matches = find_matches(lost)

            with st.container(border=True):
                st.subheader(f"🔴 Lost: {lost['name']}")
                st.write(
                    f"{lost['building']} • {lost['floor']} • {lost['location']}"
                )

                if not matches:
                    st.caption("No possible matches found yet.")
                else:
                    st.write("### Possible matches")

                    for score, found in matches[:3]:
                        percentage = min(round(score * 100), 99)

                        st.markdown(
                            f"**🔵 {found['name']}** — Match: **{percentage}%**"
                        )
                        st.write(
                            f"📍 {found['building']} • {found['floor']} • "
                            f"{found['location']}"
                        )
                        st.caption(found["description"])

                        if found["photo"]:
                            st.image(found["photo"], width=120)

                        st.divider()

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption(
    "RSS Lost & Found • Tech Expo Project • Demo version"
)
