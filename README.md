# Bizprospex-Search-Portal - Public Google Sheets Filter UI (Streamlit)

## 🔒 Security-First Design
This app is designed for **public use** - no secrets or API keys required!

### How Users Use Your App:
1. Users open their Google Sheet
2. They publish it to web as CSV (File → Share → Publish to web → CSV)
3. They paste the CSV URL into your app
4. They filter and download the data

**No server-side secrets needed** - completely secure for public deployment!

## 🚀 Quick Deploy (No Secrets Required!)

### 1. Deploy to Streamlit Community Cloud:
```bash
# Push to GitHub (already done!)
git push origin main

# Connect to Streamlit Cloud - no secrets needed!
```

### 2. Your app will be live at:
`https://your-app-name.streamlit.app`

## 📋 For Your Users:

### Quick Start
1. **Open your Google Sheet**
2. **File → Share → Publish to web**
3. **Select "CSV" format**
4. **Copy the generated URL**
5. **Paste into the app's sidebar**

### Example CSV URL:
```
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv
```

## ✨ Features
- **🔍 Advanced Filtering**: Text search, numeric ranges, multi-select
- **📥 CSV Download**: Export filtered results
- **🎨 Clean UI**: Responsive sidebar with filter controls
- **⚡ Fast Loading**: Cached data loading
- **🔒 Secure**: No API keys or secrets required

## 🛠️ For Users With Private Sheets

If users have private sheets, they should:
1. Set sharing to "Anyone with link can view"
2. Then publish to web as CSV
3. Use that public CSV URL in your app

## 📁 Project Structure
```
your-repo/
├── streamlit_app.py    # Main app (no secrets!)
├── requirements.txt    # Minimal dependencies
├── README.md          # This file
└── .gitignore         # Excludes secrets (even though none needed)
