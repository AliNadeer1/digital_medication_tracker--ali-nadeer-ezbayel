# Digital Medication Tracker

A small Streamlit app . You can add meds, see what to take today, check if two meds have the same ingredient, and see which ones are running out.

## What it does

- Home page with a quick summary (total meds, running low, high urgency)
- Add a medication (if you take it twice a day, you pick two times)
- Check if meds share an ingredient
- Daily schedule with a tick box for each dose
- Inventory where you can search, filter and edit the table, and request a refill when pills are low
- Upload a CSV to start, and download it when you're done

## How to run

Install what it needs:

```
pip install streamlit pandas streamlit-keyup
```

Then run it from the folder with the files:

```
streamlit run digital_app.py
```

`digital_app.py` and `myutils.py` need to be in the same folder.

## CSV file

If you upload a CSV it needs these columns: Name, Ingredients, Frequency, Time, Instructions, Urgency, Category, Stock.

- If a med has more than one time, put them in one cell with quotes, like "08:00, 20:00"
- Write times like 08:00, not 8:00, or the schedule won't sort right
- Stock is the number of pills left
- Don't open and save the CSV in Excel before uploading, it can add blank rows
  APP Link: https://digitalmedicationtracker--ali-nadeer-ezbayel.streamlit.app/
video link here : https://youtu.be/bX9QR7Qblu4
## Refill warning

In `digital_app.py` there is a line `LOW = 5`. Any med with 5 pills or less shows up as running low. Change the number if you want.
