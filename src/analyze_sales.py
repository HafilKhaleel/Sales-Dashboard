"""Clean the fictional starter CSV and calculate basic sales metrics.

This is a teaching example. Confirm column definitions and business rules against
real source data before using the calculations in a portfolio or business report.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "raw" / "sales_sample.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "sales_clean.csv"
REQUIRED_COLUMNS = {
    "order_id", "order_date", "customer_id", "customer_name", "region",
    "product_id", "product_name", "category", "quantity", "unit_price", "unit_cost",
}


def main() -> None:
    # Read the CSV into a pandas DataFrame (a table of rows and columns).
    df = pd.read_csv(INPUT_FILE)

    # Fail with a useful message if a replacement dataset has a different shape.
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")

    # Convert columns to useful types. Invalid dates/numbers become missing values.
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for column in ["quantity", "unit_price", "unit_cost"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Drop rows that cannot support the core calculations; report how many.
    before = len(df)
    df = df.dropna(subset=["order_id", "order_date", "quantity", "unit_price", "unit_cost"])
    df = df[df["quantity"] >= 0].copy()
    removed = before - len(df)

    # These starter definitions exclude discounts, tax, shipping, and returns.
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["cost"] = df["quantity"] * df["unit_cost"]
    df["profit"] = df["revenue"] - df["cost"]
    df["profit_margin"] = df["profit"].div(df["revenue"].where(df["revenue"] != 0))

    # Save a CSV that Excel, SQLite tools, and Power BI can all open.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, date_format="%Y-%m-%d")

    # These figures describe whichever input file was used; the bundled one is fictional.
    print(f"Input rows: {before}")
    print(f"Rows excluded for missing/invalid core fields or negative quantity: {removed}")
    print(f"Rows written: {len(df)}")
    print(f"Revenue total: {df['revenue'].sum():.2f}")
    print(f"Profit total: {df['profit'].sum():.2f}")
    print(f"Processed file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
