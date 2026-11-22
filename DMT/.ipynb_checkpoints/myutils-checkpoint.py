import pandas as pd

def clean_stock(meds):
    meds = meds.copy()
    meds["Stock"] = pd.to_numeric(meds["Stock"], errors="coerce").fillna(0).astype(int)
    return meds #make the stock column numbers, so counting and editing work.

def create_empty_table(columns):
    return pd.DataFrame(columns=columns) # return an empty medication table with the given columns.

def read_meds_csv(uploaded_file, columns):
    #Read an uploaded CSV. Raises ValueError if a required column is missing.
    table = pd.read_csv(uploaded_file).fillna("")
    missing = [column for column in columns if column not in table.columns]
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))
    return clean_stock(table[columns]) #AI Helped me with it

def count_high_urgency(meds):
    return int((meds["Urgency"] == "High").sum())
        #count how many meds have High urgency

def has_ingredient(ingredient_text, ingredient):
    names = [name.strip().lower() for name in str(ingredient_text).split(",")]
    return ingredient in names
        #return true if the comma separated text contains the exact ingredient 

def find_shared_ingredient(meds, ingredient):
    mask = meds["Ingredients"].map(lambda text: has_ingredient(text, ingredient)).astype(bool)
    return meds[mask]["Name"].tolist()
        #eturn the names of meds that contain the given ingredient


def filter_by_category(meds, categories):
    return meds[meds["Category"].isin(categories)]
        #return only the meds in the chosen categorie


def search_meds(meds, search_text):
    search_text = search_text.strip().lower()
    if search_text == "":
        return meds
        #return the meds whose name or ingredients contain the search text

    matching_rows = []
    for row_number, med_row in meds.iterrows():
        if search_text in str(med_row["Name"]).lower() or search_text in str(med_row["Ingredients"]).lower():
            matching_rows.append(row_number)
    return meds.loc[matching_rows]

def make_new_row(name, ingredients, frequency, dose_times, instructions, urgency, category, stock):
    times_text = ", ".join(t.strftime("%H:%M") for t in sorted(dose_times))  # text like "08:00, 20:00" so it can be sorted
    return pd.DataFrame([{
        "Name": name,
        "Ingredients": ingredients,
        "Frequency": frequency,
        "Time": times_text,
        "Instructions": instructions,
        "Urgency": urgency,
        "Category": category,
        "Stock": stock,
    }])     #turn the form answers into a one-row table


def add_medication(meds, new_row):
    return clean_stock(pd.concat([meds, new_row], ignore_index=True))
    #add the new row under the old rows and return the full table

def save_edits(meds, edited_rows):
    updated = meds.copy()
    updated.loc[edited_rows.index, edited_rows.columns] = edited_rows
    return updated
     #copy the user's edits from the shown table back into the full table

def build_schedule(meds):
    rows = []
    for _, med in meds.iterrows():
        for dose_time in str(med["Time"]).split(","):  # a med with 2 times gets 2 rows
            rows.append({"Time": dose_time.strip(), "Name": med["Name"],
                         "Instructions": med["Instructions"], "Taken": False})
    schedule = pd.DataFrame(rows, columns=["Time", "Name", "Instructions", "Taken"])
    return schedule.sort_values("Time").reset_index(drop=True)
    #return one row per dose, sorted by time, with an empty Taken tick box column

def calculate_progress(schedule):
    return schedule["Taken"].mean()
        #return the share of meds ticked as taken, from 0 to 1.

def count_by_column(meds, column, order=None):
    counts = meds[column].value_counts()
    if order is not None:
        counts = counts.reindex(order, fill_value=0)
    return counts
     #count how many meds are in each value of a column

def find_all_shared_ingredients(meds):
    ingredient_to_meds = {}
    for name, ingredients in zip(meds["Name"], meds["Ingredients"]):
        for ingredient in str(ingredients).split(","):
            ingredient = ingredient.strip().lower()
            if ingredient:
                ingredient_to_meds.setdefault(ingredient, []).append(name)
    return {ingredient: names for ingredient, names in ingredient_to_meds.items() if len(names) > 1}
        #Return ingredients that appear in more than one med , Example: {"paracetamol": ["Panadol", "Cold Relief"]} (AI Helped me with it)

def build_refill_table(meds, low_limit):
    refill = meds[meds["Stock"] <= low_limit][["Name", "Category", "Stock"]].copy()
    refill["Request refill"] = False
    return refill  #return meds with low stock, with an empty 'Request refill' tick box colum
