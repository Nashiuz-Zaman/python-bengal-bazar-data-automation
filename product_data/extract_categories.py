import csv
from utils import resolve_csv_paths, to_pascal_case


def extract_categories(csv_filenames):
    # Data structures to track uniqueness
    seen_categories = set()
    categories_list = []

    seen_subcategories = set()
    subcategories_list = []

    # Resolve output paths using the first filename as a base
    _, cat_output_path = resolve_csv_paths(
        input_csv_name=csv_filenames[0],
        replace_from=csv_filenames[0].split(".")[0],
        replace_to="categories",
    )
    _, sub_output_path = resolve_csv_paths(
        input_csv_name=csv_filenames[0],
        replace_from=csv_filenames[0].split(".")[0],
        replace_to="subcategories",
    )

    for filename in csv_filenames:
        if not filename.endswith(".csv"):
            filename += ".csv"

        input_path, _ = resolve_csv_paths(input_csv_name=filename)

        if not input_path.exists():
            print(f"⚠️ Warning: {filename} not found. Skipping...")
            continue

        with open(input_path, mode="r", encoding="utf-8") as read_file:
            reader = csv.DictReader(read_file)
            for row in reader:
                # --- 1. Process Category ---
                c_name = (row.get("itemCategoryName") or "").strip()
                c_display = (row.get("categoryDisplayName") or "").strip()

                if c_name and c_name not in seen_categories:
                    seen_categories.add(c_name)
                    categories_list.append(
                        {
                            "categoryName": c_name,
                            "categoryDisplayName": c_display,
                            "icon": to_pascal_case(c_display),
                        }
                    )

                # --- 2. Process SubCategory ---
                sc_name = row.get("itemSubCategoryName", "").strip()
                sc_display = row.get("subCategoryDisplayName", "").strip()

                if sc_name and sc_name not in seen_subcategories:
                    seen_subcategories.add(sc_name)

                    subcategories_list.append(
                        {
                            "subCategoryName": sc_name,
                            "subCategoryDisplayName": sc_display,
                            "parentCategoryName": c_name, 
                        }
                    )

    # Write categories.csv (No ID column)
    with open(cat_output_path, mode="w", encoding="utf-8", newline="") as write_file:
        writer = csv.DictWriter(
            write_file, fieldnames=["categoryName", "categoryDisplayName", "icon"]
        )
        writer.writeheader()
        writer.writerows(categories_list)

    # Write subcategories.csv (parentCategoryName instead of categoryId)
    with open(sub_output_path, mode="w", encoding="utf-8", newline="") as write_file:
        writer = csv.DictWriter(
            write_file, fieldnames=["subCategoryName", "subCategoryDisplayName", "parentCategoryName"]
        )
        writer.writeheader()
        writer.writerows(subcategories_list)

    return len(categories_list), len(subcategories_list)