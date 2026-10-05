import streamlit as st

from database import add_item, get_items
from utils import save_uploaded_image, validate_image
from matching import (
    calculate_similarity,
    calculate_text_similarity,
    calculate_location_similarity,
    calculate_overall_score
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Lost & Found",
    page_icon="🔎",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🔎 AI-Powered Lost & Found")

st.write(
    "Find lost items using AI-powered image, "
    "description and location matching."
)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

lost_count = len(get_items("lost"))
found_count = len(get_items("found"))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔴 Lost Items", lost_count)

with col2:
    st.metric("📦 Found Items", found_count)

with col3:
    st.metric("🤖 AI Matching", "Active")


st.markdown("---")


# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3 = st.tabs([
    "📢 Report Lost Item",
    "📦 Report Found Item",
    "🤖 Find Matches"
])


# --------------------------------------------------
# REPORT ITEM FUNCTION
# --------------------------------------------------

def report_item(item_type):

    name = st.text_input(
        "Item Name",
        key=f"{item_type}_name"
    )

    description = st.text_area(
        "Description",
        key=f"{item_type}_desc"
    )

    location = st.text_input(
        "Location",
        key=f"{item_type}_location"
    )

    contact = st.text_input(
        "📞 Contact Number / Email",
        key=f"{item_type}_contact"
    )

    image = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"],
        key=f"{item_type}_image"
    )

    if st.button(
        f"Submit {item_type.title()} Item",
        key=f"{item_type}_submit"
    ):

        if not name or not location or not contact or not image:

            st.error(
                "Please fill all required fields."
            )

            return

        if not validate_image(image):

            st.error(
                "Invalid image."
            )

            return

        folder = f"uploads/{item_type}"

        image_path = save_uploaded_image(
            image,
            folder
        )

        add_item(
            item_type,
            name,
            description,
            location,
            image_path,
            contact
        )

        st.success(
            f"{item_type.title()} item registered successfully! 🎉"
        )


# --------------------------------------------------
# LOST ITEM TAB
# --------------------------------------------------

with tab1:

    st.subheader("📢 Report Lost Item")

    report_item("lost")


# --------------------------------------------------
# FOUND ITEM TAB
# --------------------------------------------------

with tab2:

    st.subheader("📦 Report Found Item")

    report_item("found")


# --------------------------------------------------
# AI MATCHING TAB
# --------------------------------------------------

with tab3:

    st.subheader("🤖 AI Matching")

    lost_items = get_items("lost")
    found_items = get_items("found")

    if not lost_items:

        st.info(
            "No lost items registered yet."
        )

    elif not found_items:

        st.info(
            "No found items registered yet."
        )

    else:

        for lost in lost_items:

            st.markdown("---")

            st.markdown(
                f"## 🔴 Lost: {lost.name}"
            )

            st.write(
                f"📍 Lost Location: **{lost.location}**"
            )

            matches = []


            # ------------------------------------------
            # COMPARE ITEMS
            # ------------------------------------------

            for found in found_items:

                try:

                    image_score = calculate_similarity(
                        lost.image_path,
                        found.image_path
                    )

                    text_score = calculate_text_similarity(
                        lost.description or "",
                        found.description or ""
                    )

                    location_score = calculate_location_similarity(
                        lost.location or "",
                        found.location or ""
                    )

                    overall_score = calculate_overall_score(
                        image_score,
                        text_score,
                        location_score
                    )

                    matches.append({

                        "item": found,

                        "score":
                            overall_score * 100,

                        "image_score":
                            max(0, image_score) * 100,

                        "text_score":
                            max(0, text_score) * 100,

                        "location_score":
                            location_score * 100

                    })

                except Exception as e:

                    st.error(
                        f"Matching error: {e}"
                    )


            # ------------------------------------------
            # SORT MATCHES
            # ------------------------------------------

            matches.sort(
                key=lambda x: x["score"],
                reverse=True
            )


            # ------------------------------------------
            # DISPLAY MATCHES
            # ------------------------------------------

            for match in matches:

                found = match["item"]

                percentage = match["score"]


                # Match confidence
                if percentage >= 80:

                    match_status = "🟢 Strong Match"

                elif percentage >= 60:

                    match_status = "🟡 Possible Match"

                else:

                    match_status = "🔴 Low Match"


                # Show matches above 50%
                if percentage >= 50:

                    # ----------------------------------
                    # IMAGES
                    # ----------------------------------

                    col1, col2 = st.columns(2)

                    with col1:

                        st.image(
                            lost.image_path,
                            caption="Lost Item",
                            width=250
                        )

                    with col2:

                        st.image(
                            found.image_path,
                            caption="Found Item",
                            width=250
                        )


                    # ----------------------------------
                    # MATCH STATUS
                    # ----------------------------------

                    if percentage >= 80:

                        st.success(
                            f"{match_status}: **{found.name}**"
                        )

                    elif percentage >= 60:

                        st.warning(
                            f"{match_status}: **{found.name}**"
                        )

                    else:

                        st.error(
                            f"{match_status}: **{found.name}**"
                        )


                    # ----------------------------------
                    # SCORE
                    # ----------------------------------

                    st.progress(
                        min(int(percentage), 100)
                    )

                    st.write(
                        f"🏆 Overall Match Score: "
                        f"**{percentage:.2f}%**"
                    )

                    st.write(
                        f"🖼️ Image Similarity: "
                        f"**{match['image_score']:.2f}%**"
                    )

                    st.write(
                        f"📝 Description Similarity: "
                        f"**{match['text_score']:.2f}%**"
                    )

                    st.write(
                        f"📍 Location Similarity: "
                        f"**{match['location_score']:.2f}%**"
                    )

                    st.write(
                        f"📍 Found Location: "
                        f"**{found.location}**"
                    )


                    # ----------------------------------
                    # CLAIM / CONTACT
                    # ----------------------------------

                    st.markdown("### 🤝 Claim / Contact")

                    st.info(
                        "A possible match has been found. "
                        "Click the button below to view "
                        "the recovery details."
                    )


                    # Unique button for each match
                    claim_key = f"claim_{lost.id}_{found.id}"


                    if st.button(
                        "🤝 Claim This Item",
                        key=claim_key
                    ):

                        st.session_state[
                            f"claimed_{lost.id}_{found.id}"
                        ] = True


                    # ----------------------------------
                    # SHOW DETAILS AFTER CLAIM
                    # ----------------------------------

                    if st.session_state.get(
                        f"claimed_{lost.id}_{found.id}",
                        False
                    ):

                        st.success(
                            "✅ Claim request initiated!"
                        )

                        st.markdown(
                            "### 📋 Recovery Details"
                        )

                        detail_col1, detail_col2 = st.columns(2)

                        with detail_col1:

                            st.write(
                                f"📦 **Found Item:** "
                                f"{found.name}"
                            )

                            st.write(
                                f"🏆 **Match Score:** "
                                f"{percentage:.2f}%"
                            )

                            st.write(
                                f"📍 **Found Location:** "
                                f"{found.location}"
                            )

                        with detail_col2:

                            if found.contact:

                                st.write(
                                    f"📞 **Finder Contact:** "
                                    f"{found.contact}"
                                )

                            else:

                                st.warning(
                                    "⚠️ Finder contact details "
                                    "are not available."
                                )


                        st.info(
                            "Please contact the finder and "
                            "verify the item details before "
                            "recovering it."
                        )


                    st.markdown("---")