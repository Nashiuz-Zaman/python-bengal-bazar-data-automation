import csv
import json
from utils import resolve_csv_paths


def transform_to_bengal_bazar(input_csv_name: str):
    """
    Transforms a raw product CSV into the Bengal Bazar format
    using resolved paths from the utility function.
    """
    # 1. Resolve paths using the utility
    # We'll suffix the output with '_transformed' to distinguish it
    input_path, output_path = resolve_csv_paths(
        input_csv_name=input_csv_name,
        replace_from=".csv",
        replace_to="_transformed.csv",
    )

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 2. Define headers for the Bengal Bazar format
    headers = [
        "productSlug",
        "productDisplayName",
        "productBrandName",
        "categoryName",
        "subCategoryName",
        "warrantyAndSupport",
        "productDetails",
        "status",
        "specifications",
        "seoTitle",
        "seoDescription",
        "metaKeywords",
        "tags",
        "canonicalUrl",
        "globalVideos",
        "globalImages",
        "variantName",
        "sku",
        "stock",
        "unit",
        "unitSalesPrice",
        "unitDiscount",
        "discountSalesPrice",
        "variantVideos",
        "variantImages",
        "attributes",
    ]

    transformed_data = []

    # 3. Read and Process
    if not input_path.exists():
        print(f"❌ Error: Source file not found at {input_path}")
        return

    with open(input_path, mode="r", encoding="utf-8") as read_file:
        reader = csv.DictReader(read_file)

        for row in reader:

            full_img = row.get("fullImageUrl", "").strip()
            image_array_json = json.dumps([full_img]) if full_img else json.dumps([])
            display_name = row.get("itemDisplayName", "")
            details = row.get("itemDetails", "")

            entry = {
                # --- PRODUCT SECTION ---
                "productSlug": row.get("itemSlug", ""),
                "productDisplayName": display_name,
                "productBrandName": row.get("itemBrandName", ""),
                "categoryName": row.get("itemCategoryName", ""),
                "subCategoryName": row.get("itemSubCategoryName", ""),
                "warrantyAndSupport": "Standard Warranty",
                "productDetails": details,
                "status": "PUBLISHED",
                "specifications": json.dumps({}),
                "seoTitle": display_name,
                "seoDescription": details,
                "metaKeywords": "",
                "tags": "",
                "canonicalUrl": "",
                "globalVideos": json.dumps([]),
                "globalImages": image_array_json,
                # --- VARIANT SECTION ---
                "variantName": "",
                "sku": f"{row.get('itemSlug')}-{row.get('unit', 'default').lower()}",
                "stock": 100,
                "unit": row.get("unit", ""),
                "unitSalesPrice": row.get("unitSalesPrice", ""),
                "unitDiscount": row.get("unitDiscount", ""),
                "discountSalesPrice": row.get("discountSalesPrice", ""),
                "variantVideos": json.dumps([]),
                "variantImages": image_array_json,
                "attributes": json.dumps({}),
            }
            transformed_data.append(entry)

    # 4. Write the cleaned CSV
    with open(output_path, mode="w", encoding="utf-8", newline="") as read_file:
        writer = csv.DictWriter(read_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(transformed_data)

    print(f"✅ Success! Generated: {output_path.name}")
    print(f"📍 Location: {output_path}")
    print(f"🔗 Total Rows: {len(transformed_data)}")
