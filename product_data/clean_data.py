import csv
import re
from utils import resolve_csv_paths

#  Basic building blocks
num = r"\d+(?:\.\d+)?"
units = r"(?:gm|g|ml|kg|l(?:tr)?|mg|pkt|pcs?|pieces?|slices?)"
units_compiled = re.compile(units, flags=re.IGNORECASE)

# total_product_unit_pattern = (
#     rf"(\(?\s*{num}.*\)?.*?{units}\s*?(?:\/?\s*?{units})?\)?.*?)"
# )
total_product_unit_pattern = rf"( \(? \s* {num} \s* {units}? \)? (?:\s|-|up)* (?:{num} \s* {units}? (?:\s|up)* \)? (?:\s|up)* {units}? \/? {units}? \)? )? )"
total_product_unit_pattern_compiled = re.compile(
    total_product_unit_pattern, re.IGNORECASE | re.VERBOSE
)
unwanted_chars_regex_compiled = re.compile(r"[^a-zA-Z0-9./()+-]+")
USD_RATE = 110


def strip_unwanted_chars(text: str) -> str:
    new_text = unwanted_chars_regex_compiled.sub(" ", text)
    new_text = re.sub(r"\(\s*?([a-zA-Z]+)\s*?\)", r"(\1)", new_text)
    return new_text


def normalize_text(text: str) -> str:
    units_regex = r"(?:kg|gm|mg|pieces?)"

    text = re.sub(r"\+", r" Up", text)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

    text = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", text)
    text = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", text)
    text = re.sub(r"\)([a-zA-Z])", r") \1", text)
    text = re.sub(r"([a-zA-Z])\(", r"\1 (", text)
    text = re.sub(r"(\w)\s*-", r"\1 -", text)
    text = re.sub(r"-\s*(\w)", r"- \1", text)
    text = re.sub(
        rf"({units_regex})\s*({units_regex})", r"\1/\2", text, flags=re.IGNORECASE
    )

    return text


def format_unit_callback(match):
    # Extract the actual text found (e.g., "Gm" or "pieces")
    unit = match.group(0).lower()

    # 1. Normalization Logic
    if unit in ["pcs", "pieces", "slices"]:
        unit = "pieces"
    elif unit in ["pc", "piece", "slice"]:
        unit = "piece"
    elif unit == "g":
        unit = "gm"
    elif unit == "l":
        unit = "ltr"

    # 2. Casing Logic
    # If it's a "piece" variation, use Title Case. Otherwise, ALL CAPS.
    if "piece" in unit or "pcs" in unit:
        return unit.title()
    else:
        return unit.upper()


def replace_contn(text: str) -> str:
    return re.sub(r"contn", "container", text, flags=re.IGNORECASE)


def clean_unit(matched: re.Match, isDisplay: bool) -> str:
    matched_text = matched.group(1).strip()

    if isDisplay:

        matched_text = re.sub(r"[\(\)]", "", matched_text)
        matched_text = re.sub(
            rf"(?<=[\/\)\d\s])\b{units}\b",
            format_unit_callback,
            matched_text,
            flags=re.IGNORECASE,
        )
        return f" ({matched_text})"

    else:
        matched_text = re.sub(r"[\(\)]", "", matched_text)
        matched_text = re.sub(
            rf"(?<=[\/\)\d\s])\b{units}\b",
            format_unit_callback,
            matched_text,
            flags=re.IGNORECASE,
        )
        return " " + matched_text


def normalize_units(text: str, isDisplay: bool) -> str:
    return total_product_unit_pattern_compiled.sub(
        lambda m: clean_unit(m, isDisplay), text
    )


def replace_multiple_hyphens_with_single_hyphen(text: str) -> str:
    return re.sub(r"-{2,}", "-", text)


def format_display_name(text):
    if not text:
        return text

    text = strip_unwanted_chars(text)
    text = normalize_text(text)
    text = replace_contn(text)
    text = text.title()
    text = normalize_units(text, isDisplay=True)
    text = re.sub(rf"({num})\s*-\s*({num})", r"\1-\2", text, flags=re.IGNORECASE)
    text = re.sub(r"(\s{2,}|((?<=[a-zA-Z]) - (?=[a-zA-Z])))", " ", text)
    text = re.sub(r"(?<=[a-zA-Z])\s?-\s?(?=\()", r" ", text, flags=re.IGNORECASE)

    return text


def format_slug(text: str) -> str:
    if not text:
        return text

    text = strip_unwanted_chars(text)
    text = normalize_text(text)
    text = replace_contn(text)
    text = normalize_units(text, isDisplay=False)
    text = re.sub(r"[\/\s]+", r"-", text)
    text = replace_multiple_hyphens_with_single_hyphen(text)

    text = text.lower()

    return text


def format_unit_cell(text: str) -> str:
    if not text:
        return text

    text = strip_unwanted_chars(text)
    text = normalize_text(text)
    text = normalize_units(text, isDisplay=False).title().strip()

    return text


def convert_tk_to_usd(value: str) -> str:
    if not value:
        return value

    try:
        # Remove commas, spaces, currency symbols if any
        clean = re.sub(r"[^\d.]", "", value)

        if not clean:
            return value

        tk = float(clean)
        usd = tk / USD_RATE

        # format to 2 decimal places
        return f"{usd:.2f}"
    except Exception:
        return value


def normalize_brand(value: str) -> str:
    if not value:
        return "Bengal Bazar"

    val = value.strip()

    if not val or val.lower() == "no brand":
        return "Bengal Bazar"

    return val


def clean_data(csv_name: str):
    input_csv_path, output_csv_path = resolve_csv_paths(
        input_csv_name=csv_name,
        replace_from="_product_data.csv",
        replace_to="_product_data_cleaned.csv",
    )

    with open(input_csv_path, mode="r", newline="", encoding="utf-8") as infile, open(
        output_csv_path, mode="w", newline="", encoding="utf-8"
    ) as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            cleaned_row = {}

            for key, value in row.items():
                if not isinstance(value, str) or not value:
                    cleaned_row[key] = value
                    continue

                if key == "itemSlug":
                    new_value = value.strip()
                    cleaned_row[key] = format_slug(new_value)

                elif key == "itemDisplayName":
                    new_value = value.strip()
                    cleaned_row[key] = format_display_name(new_value)

                elif key == "unit":
                    new_value = value.strip()
                    cleaned_row[key] = format_unit_cell(new_value)

                elif key in ["unitSalesPrice", "unitDiscount", "discountSalesPrice"]:
                    cleaned_row[key] = convert_tk_to_usd(value.strip())

                elif key in ["itemBrandName", "brandDisplayName"]:
                    cleaned_row[key] = normalize_brand(value)

                else:
                    cleaned_row[key] = value.strip()

            writer.writerow(cleaned_row)

    print(f"Cleaned CSV written to: {output_csv_path}")
