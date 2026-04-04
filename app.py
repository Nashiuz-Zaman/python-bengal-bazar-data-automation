import sys
from product_data import (
    clean_data,
    extract_unique_brands,
) 
from utils import get_valid_csv_name


def show_menu():
    print("\n--- Bengal Bazar Data Tool ---")
    print("1. Clean Data")
    print("2. Extract Unique Brands (Merge from multiple CSVs)")
    print("3. Convert To Bengal Bazar Format")
    print("4. Upload To Bengal Bazar")
    print("5. Exit")


def handle_clean_data():
    csv_name = get_valid_csv_name(
        "Enter product data CSV filename (e.g., meat_product_data.csv): "
    )
    if not csv_name:
        return

    try:
        clean_data(csv_name)
        print("✅ Data cleaned successfully.")
    except Exception as e:
        print(f"❌ Failed to clean data: {e}")

    input("\nPress Enter to return to the menu...")


def handle_brand_extraction():
    print("\n--- Brand Extraction (Multi-file) ---")
    print("Enter up to 10 filenames. Type 'done' to finish early.")

    csv_list = []

    while len(csv_list) < 10:
        prompt = f"Enter CSV name {len(csv_list) + 1} (or 'done'): "
        valid_name = get_valid_csv_name(prompt)

        if not valid_name:
            break

        if valid_name.lower() == "done.csv":
            break

        csv_list.append(valid_name)
        print(f"Added: {valid_name}")

    if not csv_list:
        print("⚠️ No files provided.")
        return

    try:
        extract_unique_brands(csv_list)
        print(
            f"✅ successfully extracted unique brands from {len(csv_list)} files into brands.csv"
        )
    except Exception as e:
        print(f"❌ Failed to extract brands: {e}")

    input("\nPress Enter to return to the menu...")


def main():
    while True:
        show_menu()
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            handle_clean_data()
        elif choice == "2":
            handle_brand_extraction()
        elif choice == "5":
            print("👋 Bye!")
            sys.exit()
        else:
            print("Invalid selection, please try again.")


if __name__ == "__main__":
    main()
