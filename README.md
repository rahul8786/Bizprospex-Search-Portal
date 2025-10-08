## Filterable Google Sheets UI (Streamlit)

### Quick Start
1. Create and activate a Python 3.10+ environment.
2. Install deps:
```bash
pip install -r requirements.txt
```
3. Provide data source (choose one):
   - Published CSV: set env var `GOOGLE_SHEET_CSV_URL` to the published CSV URL of your sheet/tab.
   - Service Account: add `GOOGLE_SERVICE_ACCOUNT_JSON` (base64 or plain JSON path), and `GOOGLE_SHEET_ID` (and optional `GOOGLE_SHEET_GID`).
4. Run:
```bash
streamlit run streamlit_app.py
```

### Publish CSV URL (easiest)
- In Google Sheets: File → Share → Publish to web → Select the specific sheet (tab) → CSV.
- Copy the generated CSV URL and set it as `GOOGLE_SHEET_CSV_URL`.

### Service Account (private sheets)
- Create a Service Account with Google Sheets API access.
- Share the target Google Sheet with the service account email (Viewer or higher).
- Provide credentials:
  - Option A: Place the JSON at `service_account.json` and set env var `GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json`.
  - Option B: Store JSON content in an env/secret and set `GOOGLE_SERVICE_ACCOUNT_JSON` to that JSON string (or base64 and set `GOOGLE_SERVICE_ACCOUNT_JSON_BASE64`).
- Set `GOOGLE_SHEET_ID` to the sheet ID (from the URL). Optionally set `GOOGLE_SHEET_GID` to a specific tab gid.

### Deploy on Streamlit Community Cloud
- Push this repo to GitHub.
- In Streamlit Cloud, create a new app pointing to `streamlit_app.py`.
- Add secrets (if using Service Account) under App Settings → Secrets.
- Deploy.

### Filters Supported
- Keyword, Industry, Headcount, Employee Size, Company Location, Title, Person Location

### Notes
- Numeric coercion is attempted for Headcount and Employee Size. If data is non-numeric, the UI falls back to text filters.
- Download button exports the currently filtered rows as CSV.
