def get_valid_csv_name(prompt: str) -> str | None:
    csv_name = input(prompt).strip()

    if not csv_name:
        print("❌ CSV filename cannot be empty. Returning to menu.")
        return None

    if not csv_name.endswith(".csv"):
        csv_name += ".csv"

    return csv_name
