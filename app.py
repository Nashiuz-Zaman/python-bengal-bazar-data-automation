import sys
from product_data import clean_data
from utils import get_valid_csv_name


def show_menu():
    print("\nWhat do you want to do?")
    print("1. Clean Data")
    print("2. Upload Data")
    print("3. Exit")


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


def main():
    while True:
        show_menu()
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            handle_clean_data()

        else:
            print("👋 Bye!")
            sys.exit()


if __name__ == "__main__":
    main()
