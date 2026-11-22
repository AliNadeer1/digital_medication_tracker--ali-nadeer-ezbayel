import streamlit as st
import myutils

st.set_page_config(page_title="Digital Medication Tracker", page_icon="🧪") #sets the browser tab's title and icon.

COLS = ["Name", "Ingredients", "Frequency", "Time", "Instructions", "Urgency", "Category", "Stock"]
CATEGORIES = ["Prescription", "OTC", "Supplement"]
LOW = 5  # this many pills or less needs a refill
URG = {"Low": "green", "Medium": "orange", "High": "red"}  # urgency badge colors
DOSES = {"Once a day": 1, "Twice a day": 2, "Three times a day": 3, "As needed": 1}  # how many time boxes each frequency needs
ICONS = {"Home Page": "🏠 Home Page", "Add Medication": "➕ Add Medication",
         "Interaction Check": "🧪 Interaction Check", "Daily Schedule": "🗓️ Daily Schedule",
         "Inventory": "📦 Inventory"}

if "meds" not in st.session_state: 
    st.session_state.meds = myutils.create_empty_table(COLS)

with st.sidebar:#the side panel
    st.title("💊 MedTracker")
    page_chosen = st.radio("MENU", list(ICONS), format_func=ICONS.get, label_visibility="collapsed") #The menu , you pick one option and it returns your choice.
    st.divider()

    uploaded_file = st.file_uploader("📂 Upload your starting meds CSV", type="csv") #the upload box for the CSV
    if uploaded_file is None:
        st.session_state.loaded = None  # file removed, so it can be loaded again
    elif st.session_state.get("loaded") != uploaded_file.name:  # load once, so edits are not erased
        try:
            st.session_state.meds = myutils.read_meds_csv(uploaded_file, COLS)
            st.session_state.loaded = uploaded_file.name
            st.toast("CSV loaded ✅") #a small pop-up that disappears by itself
        except ValueError as error:
            st.error(str(error))  # says which column is missing (Ai helped with this)

meds = st.session_state.meds

if page_chosen == "Home Page":
    st.title("💉💊( ・_・)ノ💊 :red[Digital Medication Tracker #1]🩻🧪")
    st.subheader(":red[Ready to stay on track?]")
    if st.button("❄️ Feeling sick !??"):
        st.snow() #snow animation (why not)

    st.divider()
    if len(meds) == 0:
        st.info("Add or upload medications on the left side bar to see your summary here!!!  💊⚕️")
    else:
        low_names = meds[meds["Stock"] <= LOW]["Name"].tolist()  # meds that need a refill

        # row 1: three number cards
        col_total, col_low, col_high = st.columns(3)
        with col_total.container(border=True):
            st.metric("💊 Total meds", len(meds)) #the fuinction metric; a big number card with a label
        with col_low.container(border=True):
            st.metric("⚠️ Running low", len(low_names))
        with col_high.container(border=True):
            st.metric("🔴 High urgency", myutils.count_high_urgency(meds))


if page_chosen == "Add Medication": 
    st.title("⚕️Add Your Meds Here 💉")

    # frequency is outside the form, so the right number of time boxes shows up as soon as it changes
    frequency = st.selectbox("Dosage frequency (°ロ°) !💉", list(DOSES))

    with st.form("add_form", clear_on_submit=True, border=True):  # sends everything at once, then clears, itroups fields so nothing is sent until submiting
        med = st.text_input("Kindly input The Name Of The Medication ")
        active_ing = st.text_input("Add active ingredient(s), separate with commas") 

        time_columns = st.columns(DOSES[frequency])  # one time box per dose
        dose_times = []
        for number, time_column in enumerate(time_columns):
            label = "Time to take it" if DOSES[frequency] == 1 else f"Dose {number + 1} time"
            dose_times.append(time_column.time_input(label, key=f"dose_time_{number}"))

        instructions = st.text_area("Instructions")

        col_urgency, col_category, col_stock = st.columns(3)
        urgency = col_urgency.selectbox("Urgency level", list(URG))
        category = col_category.selectbox("Category", CATEGORIES)
        stock = col_stock.number_input("Pills left", min_value=0, step=1)

        submitted = st.form_submit_button("Add medication", type="primary") #the button that submit the form and ti confirms adding the new data to the data frame

    if submitted:
        if med == "":
            st.error("Please enter a medication name.")
        else:
            new_row = myutils.make_new_row(med, active_ing, frequency, dose_times,
                                           instructions, urgency, category, stock)
            st.session_state.meds = myutils.add_medication(meds, new_row)
            st.success(f"Medication added: {med} 🎉")
            st.badge(f"{urgency} urgency", color=URG[urgency]) #a small coloured tag, like high urgency
            st.toast("Saved!!!!!!!!!!!!! 💊")

if page_chosen == "Interaction Check":
    st.title("🧪 Interaction Check")

    ingredient = st.text_input("Type an active ingredient").strip().lower()  # so "P"aracetamol or if its all CAps still matches

    if ingredient:
        shared_meds = myutils.find_shared_ingredient(meds, ingredient)
        if len(shared_meds) > 1:
            st.warning("⚠️ These medications share it: " + ", ".join(shared_meds))
        else:
            st.success("✅ No interaction found.")
            
if page_chosen == "Daily Schedule":
    st.title("🗓️ Daily Schedule")

    if len(meds) == 0:
        st.info("No medications yet. Add one first! 💊")
    else:
        schedule = myutils.build_schedule(meds)
        edited_schedule = st.data_editor(schedule, disabled=["Time", "Name", "Instructions"], hide_index=True)
        progress = myutils.calculate_progress(edited_schedule)  # 0 to 1
        st.progress(progress, text=f"{int(progress * 100)}% taken today")
        if progress == 1:
            st.balloons()
            st.success("All done for today! 🏆")

if page_chosen == "Inventory":
    st.title("📦 Inventory")

    if len(meds) == 0:
        st.info("No medications yet. Add one first! 💊") 
    else:
        picked_categories = st.multiselect("Filter by category", CATEGORIES, default=CATEGORIES) #multi is a dropdown where you can pick several options
        search_text = st.text_input("🔍 Search by name or ingredient") #search bar 
        filtered_meds = myutils.search_meds(myutils.filter_by_category(meds, picked_categories), search_text)

        found = len(filtered_meds)  # how many rows match the search and filter
        st.markdown(f"`{found}` {'med' if found == 1 else 'meds'} found")

        if found == 0:
            st.info("No medication matches your search.")

        low_count = int((filtered_meds["Stock"] <= LOW).sum())  # how many shown meds need a refill
        if low_count > 0:
            st.warning(f"⚠️ {low_count} of these need a refill. See Refill Request below.")

        edited_meds = st.data_editor( #data editor allows  ediitng the data directly on the app
            filtered_meds,
            hide_index=True,
            column_config={
                "Urgency": st.column_config.SelectboxColumn("Urgency", options=list(URG)),
                "Category": st.column_config.SelectboxColumn("Category", options=CATEGORIES),
                "Stock": st.column_config.NumberColumn("Pills left", min_value=0, step=1),
            }, 
        )
        st.session_state.meds = myutils.save_edits(meds, edited_meds)

        # Refill Request, on the same page, built from the latest edited table (AI Helped me with it)
        st.divider()
        st.subheader("🔔 Refill Request")

        refill_table = myutils.build_refill_table(st.session_state.meds, LOW)

        if len(refill_table) == 0:
            st.success("All medications are well stocked ✅")
        else:
            st.warning(f"⚠️ {len(refill_table)} medication(s) are running low ({LOW} pill(s) or less)")
            edited_refill = st.data_editor(
                refill_table,
                disabled=["Name", "Category", "Stock"],
                hide_index=True,
                column_config={"Stock": st.column_config.NumberColumn("Pills left")},
            ) #(AI Helped me with it)

            if st.button("📨 Send refill request", type="primary"):
                requested = edited_refill[edited_refill["Request refill"]]["Name"].tolist()
                if len(requested) == 0:
                    st.error("Tick at least one medication to request a refill.")
                else:
                    st.success("Refill requested for: " + ", ".join(requested))
                    st.toast("Refill request sent 📨") 

with st.sidebar:  # at the end, so the file has the latest table
    st.download_button("⬇️ Download CSV", st.session_state.meds.to_csv(index=False), "meds.csv", mime="text/csv") #saves the table as a CSV file
