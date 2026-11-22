import importlib
import streamlit as st
import myutils

st.set_page_config(page_title="Digital Medication Tracker", page_icon="🧪") #sets the browser tab's title and icon.

COLS = ["Name", "Ingredients", "Frequency", "Time", "Instructions", "Urgency", "Category", "Stock"]
CATEGORIES = ["Prescription", "OTC", "Supplement"]
LOW = 5  # this many pills or less needs a refill
CARD_HEIGHT = 340  # same height for every chart card
URG = {"Low": "green", "Medium": "orange", "High": "red"}  # urgency badge colors
DOSES = {"Once a day": 1, "Twice a day": 2, "Three times a day": 3, "As needed": 1}  # how many time boxes each frequency needs
ICONS = {"Home Page": "🏠 Home Page", "Add Medication": "➕ Add Medication",
         "Interaction Check": "🧪 Interaction Check", "Daily Schedule": "🗓️ Daily Schedule",
         "Inventory": "📦 Inventory"}

if "meds" not in st.session_state:
    st.session_state.meds = myutils.create_empty_table(COLS)

with st.sidebar:  # the side panel
    st.title("💊 MedTracker")
    page_chosen = st.radio("MENU", list(ICONS), format_func=ICONS.get, label_visibility="collapsed")  # the menu, you pick one option and it returns your choice.
    st.divider()

    uploaded_file = st.file_uploader("📂 Upload your starting meds CSV", type="csv")  # the upload box for the CSV
    if uploaded_file is None:
        st.session_state.loaded = None  # file removed, so it can be loaded again
    elif st.session_state.get("loaded") != uploaded_file.name:  # load once, so edits are not erased
        try:
            st.session_state.meds = myutils.read_meds_csv(uploaded_file, COLS)
            st.session_state.loaded = uploaded_file.name
            st.toast("CSV loaded ✅")  # a small pop-up that disappears by itself
        except ValueError as error:
            st.error(str(error))  # says which column is missing (Ai helped with this)

meds = st.session_state.meds

if page_chosen == "Home Page":
    st.title("💉💊( ・_・)ノ💊 :red[Digital Medication Tracker #1]🩻🧪")
    st.subheader(":red[Ready to stay on track?]")
    if st.button("❄️ Feeling sick !??"):
        st.snow()  # snow animation (why not)

    st.divider()
    if len(meds) == 0:
        st.info("Add or upload medications on the left side bar to see your summary here!!!  💊⚕️")
    else:
        low_names = meds[meds["Stock"] <= LOW]["Name"].tolist()  # meds that need a refill

        # row 1: three number cards
        col_total, col_low, col_high = st.columns(3)
        with col_total.container(border=True):
            st.metric("💊 Total meds", len(meds))  # the function metric; a big number card with a label
        with col_low.container(border=True):
            st.metric("⚠️ Running low", len(low_names))
        with col_high.container(border=True):
            st.metric("🔴 High
