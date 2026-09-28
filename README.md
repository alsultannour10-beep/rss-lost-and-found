# RSS Lost & Found 🔎

A Streamlit website created for the RSS Tech Expo.

## Features

- Report lost items
- Report found items
- Search and filter reports
- Building, floor, location, grade, date and time
- Optional item photos
- Mark items as returned
- Smart Match between lost and found reports

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy with Streamlit Community Cloud

1. Upload `app.py` and `requirements.txt` to a GitHub repository.
2. Go to Streamlit Community Cloud.
3. Connect your GitHub account.
4. Select the repository.
5. Select `app.py` as the main file.
6. Deploy.

## Important

This version stores reports in Streamlit session memory, so it is designed as a Tech Expo demonstration.

For a real school-wide system, use a persistent database such as Google Sheets, Supabase, or another school-approved database, and add authentication/admin approval.
