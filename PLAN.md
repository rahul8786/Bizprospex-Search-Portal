# Vibe Coding Plan: Filterable Google Sheets UI with Download (Streamlit)

## Objective
Build a lightweight web UI that loads records from a Google Sheet, lets users filter by the specified fields, and download the filtered results as CSV. Target platform: Streamlit (local or Streamlit Community Cloud). Alternative: deploy on any Python host.

## Data Source
- Primary: Google Sheets provided by the user.
- Supported access methods:
  1. Published CSV URL (`GOOGLE_SHEET_CSV_URL`). Fastest to set up; requires the sheet/tab to be published to the web.
  2. Service Account via Google API (`GOOGLE_SERVICE_ACCOUNT_JSON` + `GOOGLE_SHEET_ID` + optional `GOOGLE_SHEET_GID`). Private access.

## Columns (filters)
- Keyword
- Industry
- Headcount (numeric or numeric-like)
- Employee Size (numeric or numeric-like)
- Company Location
- Title
- Person Location

We will preserve all other columns and allow them to appear in the results table and CSV download.

## UI/UX (Streamlit)
- Left sidebar: filter controls
  - Text/multi-select for categorical columns: Keyword, Industry, Company Location, Title, Person Location
  - Numeric range sliders for Headcount and Employee Size (auto-infer min/max from data; graceful fallback if non-numeric)
  - Reset/Clear filters button
- Main area:
  - Data preview of filtered results (paginated via Streamlit’s native table virtualization)
  - Download button for filtered CSV
  - Record count summary

## Data Handling
- Load sheet into a pandas DataFrame
- Normalize header names; trim whitespace in string columns
- Coerce `Headcount` and `Employee Size` to numeric if possible (errors coerced to NaN); when non-numeric, fall back to string filter (multi-select)
- Apply filters incrementally and efficiently
- Cache the raw DataFrame for performance (cache invalidates when source URL/credentials change)

## Security & Privacy
- If using Service Account:
  - Store credentials in Streamlit secrets or environment variables
  - Do not log sensitive data
- If using published CSV URL:
  - Data becomes publicly readable at the URL; confirm acceptability

## Files to Create
- `streamlit_app.py`: Main app
- `requirements.txt`: Dependencies (streamlit, pandas, gspread, google-auth, python-dotenv optional)
- `README.md`: Setup, run, and deploy instructions

## Deploy Targets
1. Streamlit Community Cloud
   - Push repo to GitHub
   - Configure secrets (if using Service Account)
   - Select `streamlit_app.py` as entrypoint
2. Any Python host (Docker/Heroku/Render): run `streamlit run streamlit_app.py`

## Stretch Enhancements (post-MVP)
- Column visibility toggles
- Save/load filter presets
- Multi-tab support for multiple sheets
- Simple role-based access via password/secret

## Acceptance Criteria
- User can load data from Google Sheets via either method
- User can filter by all listed fields
- Numeric filters work for `Headcount` and `Employee Size` when numeric data present
- User can download filtered results as CSV
- App deploys on Streamlit and runs locally


