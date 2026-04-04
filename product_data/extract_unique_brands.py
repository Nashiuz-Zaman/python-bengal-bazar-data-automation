import csv
from utils import resolve_csv_paths


def extract_unique_brands(csv_filenames):
    seen_brands = set()
    brand_data = []

    # Use the first file just to resolve the correct output path (brands.csv)
    _, output_path = resolve_csv_paths(
        input_csv_name="brands.csv", replace_from=None, replace_to=None
    )

    for filename in csv_filenames:
        # Resolve path for each input file
        input_path, _ = resolve_csv_paths(input_csv_name=filename)

        if not input_path.exists():
            print(f"⚠️ Skipping {filename}: File not found.")
            continue

        with open(input_path, mode="r", encoding="utf-8") as read_file:
            reader = csv.DictReader(read_file)
            for row in reader:
                # Map your CSV headers to your Prisma fields
                b_name = row.get("itemBrandName", "").strip()
                b_display = row.get("brandDisplayName", "").strip()

                if b_name and b_name not in seen_brands:
                    seen_brands.add(b_name)
                    brand_data.append(
                        {"brandName": b_name, "brandDisplayName": b_display}
                    )

    # Write the master list to brands.csv
    with open(output_path, mode="w", encoding="utf-8", newline="") as write_file:
        writer = csv.DictWriter(
            write_file, fieldnames=["brandName", "brandDisplayName"]
        )
        writer.writeheader()
        writer.writerows(brand_data)
