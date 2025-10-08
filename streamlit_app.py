import os
import io
import json
import base64
from typing import Optional, Tuple, List

import numpy as np
import pandas as pd
import streamlit as st

# Removed Google service account imports - no longer needed!


# -----------------------------
# Configuration
# -----------------------------
APP_TITLE = "Bizprospex: Google Sheets Filter UI"
FILTER_COLUMNS = {
	"Keyword": "text",
	"Industry": "text",
	"Headcount": "numeric",
	"Employee Size": "numeric",
	"Company Location": "text_search",
	"Title": "text_search",
	"Person Location": "text_search",
}


@st.cache_data(show_spinner=False)
def load_csv_from_url(csv_url: str) -> pd.DataFrame:
	df = pd.read_csv(csv_url)
	return df


# Removed service account functions - no longer needed for public CSV URLs!


def coerce_numeric(series: pd.Series) -> Tuple[pd.Series, bool]:
	coerced = pd.to_numeric(series, errors="coerce")
	is_numeric = coerced.notna().sum() > 0
	return coerced, is_numeric


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
	"""Trim strings without turning NaN into the string 'nan'."""
	df = df.copy()
	df.columns = [str(c).strip() for c in df.columns]
	for col in df.columns:
		if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):
			df[col] = df[col].apply(lambda v: v.strip() if isinstance(v, str) else v)
	return df


def _tokenize(value: str) -> List[str]:
	return [t.strip() for t in value.split(",") if t.strip()]


def build_sidebar_filters(df: pd.DataFrame) -> dict:
	st.sidebar.header("Filters")
	applied = {}

	for col, kind in FILTER_COLUMNS.items():
		if col not in df.columns:
			continue

		if kind == "numeric":
			coerced, has_numeric = coerce_numeric(df[col])
			if has_numeric:
				finite_vals = coerced[np.isfinite(coerced)]
				if finite_vals.empty:
					options = sorted([v for v in df[col].dropna().unique().tolist() if v != ""])
					selected = st.sidebar.multiselect(f"{col}", options, key=f"ms_{col}")
					if selected:
						applied[col] = ("in", selected)
				else:
					min_val = int(finite_vals.min())
					max_val = int(finite_vals.max())
					start, end = st.sidebar.slider(
						f"{col} range",
						min_value=min_val,
						max_value=max_val,
						value=(min_val, max_val),
						key=f"rng_{col}"
					)
					applied[col] = ("range", (start, end))
			else:
				options = sorted([v for v in df[col].dropna().unique().tolist() if v != ""])
				selected = st.sidebar.multiselect(f"{col}", options, key=f"ms_{col}")
				if selected:
					applied[col] = ("in", selected)
		elif kind == "text_search":
			col_key = col.replace(" ", "_").lower()
			text_val = st.sidebar.text_input(f"{col} contains (comma-separated)", key=f"txt_{col_key}")
			op = st.sidebar.selectbox(
				f"{col} operator",
				["OR", "AND"],
				index=0,
				key=f"op_{col_key}"
			)
			if text_val.strip():
				tokens = _tokenize(text_val)
				applied[col] = ("contains_all" if op == "AND" else "contains_any", tokens)
		else:
			options = sorted([v for v in df[col].dropna().unique().tolist() if v != ""])
			selected = st.sidebar.multiselect(f"{col}", options, key=f"ms_{col}")
			if selected:
				applied[col] = ("in", selected)

	if st.sidebar.button("Clear filters"):
		# Clear known session_state keys for filters and rerun
		for col in FILTER_COLUMNS.keys():
			col_key = col.replace(" ", "_").lower()
			for key in (f"ms_{col}", f"rng_{col}", f"txt_{col_key}", f"op_{col_key}"):
				if key in st.session_state:
					del st.session_state[key]
		st.rerun()

	return applied


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
	result = df.copy()
	for col, (op, value) in filters.items():
		if col not in result.columns:
			continue
		if op == "range":
			start, end = value
			num_col, _ = coerce_numeric(result[col])
			result = result[(num_col >= start) & (num_col <= end)]
		elif op == "in":
			result = result[result[col].isin(value)]
		elif op in ("contains_any", "contains_all"):
			series = result[col].astype(str).str.lower()
			masks = [series.str.contains(tok.lower(), na=False) for tok in value]
			mask = masks[0]
			for m in masks[1:]:
				mask = mask | m if op == "contains_any" else mask & m
			result = result[mask]
	return result


def to_csv_bytes(df: pd.DataFrame) -> bytes:
	buf = io.StringIO()
	df.to_csv(buf, index=False)
	return buf.getvalue().encode("utf-8")


def load_data(csv_url: Optional[str] = None) -> pd.DataFrame:
	"""Load data from user-provided CSV URL only."""
	if not csv_url or not csv_url.strip():
		st.info("👆 Please enter a Google Sheets CSV URL in the sidebar to load data.")
		st.stop()

	try:
		df = load_csv_from_url(csv_url)
		return normalize_dataframe(df)
	except Exception as e:
		st.error(f"❌ Failed to load data from URL: {e}")
		st.info("💡 Make sure the Google Sheet is published to web as CSV (File → Share → Publish to web)")
		st.stop()


def main() -> None:
	st.set_page_config(page_title=APP_TITLE, layout="wide")
	st.title(APP_TITLE)

	with st.sidebar:
		st.subheader("🔗 Data Source")
		st.info("📋 To use this app: Open your Google Sheet → File → Share → Publish to web → CSV → Copy URL below")

		csv_input = st.text_input(
			"Google Sheets CSV URL *",
			placeholder="https://docs.google.com/spreadsheets/d/.../export?format=csv",
			help="Paste the published CSV URL from your Google Sheet"
		)

	df = load_data(csv_input.strip() or None)
	if df.empty:
		st.info("No data available.")
		return

	filters = build_sidebar_filters(df)
	filtered = apply_filters(df, filters)

	st.subheader("Results")
	st.write(f"Showing {len(filtered)} of {len(df)} rows")
	st.dataframe(filtered, use_container_width=True)

	csv_bytes = to_csv_bytes(filtered)
	st.download_button(
		label="Download filtered CSV",
		data=csv_bytes,
		file_name="filtered_results.csv",
		mime="text/csv",
	)


if __name__ == "__main__":
	main()


