import os
import requests
import csv
from utils import resolve_csv_paths, load_project_env

env_path = load_project_env()

if env_path:
    print(f"Loaded config from: {env_path}")
else:
    print("⚠️ No .env file found in path hierarchy.")

API_URL = os.getenv("API_URL")

if API_URL is None:
    raise EnvironmentError("❌ API_URL not found")


def upload_to_bengal_bazar(csv_file):
    input_path, _ = resolve_csv_paths(input_csv_name=csv_file)

    if not input_path.exists():
        print(f"❌ Source file not found at {input_path}")
        return

    # Read CSV and convert to a list of dictionaries
    payload_data = []
    try:
        with open(input_path, mode="r", encoding="utf-8") as read_file:
            reader = csv.DictReader(read_file)
            for row in reader:
                payload_data.append(row)
    except Exception as e:
        print(f"❌ Failed to read CSV: {e}")
        return

    # Construct the JSON Payload
    print(f"🚀 Sending {len(payload_data)} rows to {API_URL}...")

    # Execute the Request
    try:
        response = requests.post(API_URL, json=payload_data)

        # Check for HTTP errors (4xx, 5xx)
        response.raise_for_status()

        result = response.json()

        if result.get("success"):
            print("✅ Upload Complete!")
            summary = result.get("data", {})

            print("\n--- Import Summary ---")
            print(f"Total processed: {summary.get('total')}")
            print(f"Successfully saved: {summary.get('success')}")
            print(f"Failed: {summary.get('failed')}")

            if summary.get("errors"):
                print("\n❌ Detailed Errors:")
                for err in summary["errors"]:
                    print(f"  Row {err['row']} [{err['identifier']}]: {err['error']}")
        else:
            print(f"❌ Server logic error: {result.get('message')}")

    except requests.exceptions.HTTPError as e:
        # Handle cases where the server returns a 4xx or 5xx status
        try:
            error_data = e.response.json()
            print(
                f"❌ Server Error ({e.response.status_code}): {error_data.get('message', e)}"
            )
        except Exception:
            print(f"❌ HTTP Error ({e.response.status_code}): {e}")

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is your server running?")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    upload_to_bengal_bazar()
