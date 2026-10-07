import pandas as pd


def inspect_dataset(file_path, id_column=None):

    df = pd.read_csv(file_path)

    report = {
        "file": file_path,
        "rows": len(df),
        "columns": list(df.columns),
        "missing_values": {},
        "duplicate_rows": 0,
        "duplicate_ids": 0,
        "date_columns": [],
        "numeric_columns": [],
        "unique_values": {}
    }

    # Check missing values
    missing = df.isnull().sum()

    for column, count in missing.items():
        if count > 0:
            report["missing_values"][column] = int(count)

    # Check duplicate rows
    report["duplicate_rows"] = int(df.duplicated().sum())

    # Check duplicate IDs
    if id_column and id_column in df.columns:
        report["duplicate_ids"] = int(
            df[id_column].duplicated().sum()
        )

    # Identify date columns
    for column in df.columns:
        if "date" in column.lower():
            report["date_columns"].append(column)

    # Identify numeric columns
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            report["numeric_columns"].append(column)

    # Get unique values for useful categorical columns
    for column in df.columns:
        if df[column].dtype == "object":
            values = df[column].dropna().unique()

            if len(values) <= 20:
                report["unique_values"][column] = values.tolist()

    return report


def inspect_all_datasets():

    customers_report = inspect_dataset(
        "data/customers.csv",
        "customer_id"
    )

    orders_report = inspect_dataset(
        "data/orders.csv",
        "order_id"
    )

    return {
        "customers": customers_report,
        "orders": orders_report
    }


if __name__ == "__main__":

    reports = inspect_all_datasets()

    print("===== CUSTOMERS DATASET =====")
    print(reports["customers"])

    print("\n===== ORDERS DATASET =====")
    print(reports["orders"])