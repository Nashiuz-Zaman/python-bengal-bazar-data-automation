import csv
import json
from utils import generate_sku, resolve_csv_paths, to_pascal_case


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
        "brandName",
        "brandDisplayName",
        "categoryName",
        "categoryDisplayName",
        "categoryIcon",
        "subCategoryName",
        "subCategoryDisplayName",
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
            details = row.get("itemDetails") or "No details provided."
            slug = row.get("itemSlug", "")
            brand_name = row.get("itemBrandName", "Bengal Bazar")
            category_name = row.get("itemCategoryName", "")
            sub_category_name = row.get("itemSubCategoryName", "")
            unit = row.get("unit", "pcs")

            # Generate the unique short SKU
            sku = generate_sku(brand_name, category_name, slug, unit)

            entry = {
                # --- PRODUCT SECTION ---
                "productSlug": slug,
                "productDisplayName": display_name,
                "brandName": brand_name,
                "brandDisplayName": row.get("brandDisplayName", brand_name),
                "categoryName": category_name,
                "categoryDisplayName": row.get("categoryDisplayName", category_name),
                "categoryIcon": to_pascal_case(category_name),
                "subCategoryName": sub_category_name,
                "subCategoryDisplayName": row.get(
                    "subCategoryDisplayName", sub_category_name
                ),
                "warrantyAndSupport": "Standard Warranty",
                "productDetails": details,
                "status": "PUBLISHED",
                "specifications": json.dumps([]),
                "seoTitle": display_name,
                "seoDescription": details[:160],
                "metaKeywords": f"{category_name}, {sub_category_name}",
                "tags": f"{category_name}, {sub_category_name}",
                "canonicalUrl": f"https://bengalbazar.vercel.app/product/{slug}",
                "globalVideos": json.dumps([]),
                "globalImages": image_array_json,
                # --- VARIANT SECTION ---
                "variantName": unit if unit else "Default",
                "sku": sku,
                "stock": 100,
                "unit": unit,
                "unitSalesPrice": row.get("unitSalesPrice") or "0",
                "unitDiscount": row.get("unitDiscount") or "0",
                "discountSalesPrice": row.get("discountSalesPrice") or "0",
                "variantVideos": json.dumps([]),
                "variantImages": image_array_json,
                "attributes": json.dumps({"unit": unit}),
            }
            transformed_data.append(entry)

    # 4. Write the cleaned CSV
    with open(output_path, mode="w", encoding="utf-8", newline="") as write_file:
        writer = csv.DictWriter(write_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(transformed_data)

    print(f"✅ Success! Generated: {output_path.name}")
    print(f"Location: {output_path}")
    print(f"Total Rows: {len(transformed_data)}")
