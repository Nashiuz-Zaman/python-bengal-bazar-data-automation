# Bengal Bazar: Data Automation Engine ⚡

A specialized Python-based ETL (Extract, Transform, Load) pipeline designed to bridge the gap between raw, messy e-commerce data and the **Bengal Bazar (PERN)** production database.

This project automates the cleaning, SKU generation, and relational formatting of thousands of product entries, ensuring strict data integrity before they are processed by the Prisma ORM in the Node.js backend.

---

## 🚀 The Problem
E-commerce data sourced from various suppliers or scrapers often arrives in inconsistent formats:
* **Inconsistent SKUs:** Missing unique identifiers or irregular naming conventions.
* **Flat Structure:** Flat CSV data that does not match the nested relational structure of a Product-Variant database.
* **UI Incompatibility:** Category names that don't easily map to frontend Icon components.
* **Scalability:** Manual data entry for thousands of items is prone to human error and creates massive bottlenecks.

## 🛠️ The Solution
This automation engine performs four critical roles:

1.  **Normalization:** Standardizes technical names, display names, and pricing logic.
2.  **SKU Orchestration:** Generates unique, human-readable SKUs using a combination of Brand, Category, and Slug logic.
3.  **Frontend Sync:** Automatically generates **PascalCase** icon keys (e.g., `FrozenFoods`) to allow the React frontend to dynamically render the correct UI icons (e.g., `FaFrozenFoods`).
4.  **Relational Preparation:** Transforms flat CSV rows into structured JSON-compatible entries, ready for the TypeScript bulk-uploader and Prisma nested creates.

---

## 🏗️ Architecture

The system follows a classic ETL pipeline architecture:

1.  **Extract:** Reads raw CSV files from local directories using `pathlib`.
2.  **Transform:** * Parses pricing to ensure valid numeric/decimal formats.
    * Generates SEO metadata (titles, descriptions, canonical URLs).
    * Wraps variant-specific data into JSON structures.
3.  **Load:** Exports a "Gold Standard" CSV ready for database ingestion.

### Key Logic Modules:
* **Transform Engine:** Processes raw CSVs and applies business rules (e.g., defaulting stock, formatting currency, slicing SEO descriptions).
* **Utility Toolkit:** * `generate_sku`: Creates unique identifiers for product tracking.
    * `to_pascal_case`: Maps category strings to frontend icon components.
    * `resolve_csv_paths`: Handles OS-independent path management for input/output files.

---

## 📊 Data Transformation Mapping

| Raw Source Header | Bengal Bazar Format (Automated) | Purpose |
| :--- | :--- | :--- |
| `itemDisplayName` | `productDisplayName` | User-facing title |
| `itemCategoryName` | `category_icon` (PascalCase) | Dynamic React Icon mapping |
| `unit` | `attributes` (JSON String) | Variant selector dropdown logic |
| `N/A` | `sku` (Generated) | Unique inventory management |
| `fullImageUrl` | `globalImages` (JSON Array) | Image gallery synchronization |

---

## 💻 Technical Stack
* **Language:** Python 3.10+
* **Core Libraries:** `csv`, `json`, `pathlib`
* **Dev Context:** This is part of the **Bengal Bazar Ecosystem**, acting as the specialized data-feeder for the PERN (PostgreSQL, Express, React, Node.js) production app.

---

## ⚙️ Setup & Usage

1.  **Prepare Data:** Place your raw supplier CSV in the `/data/raw/` directory.
2.  **Run Pipeline:**
    ```bash
    python main.py
    ```
3.  **Review Output:** The cleaned, formatted CSV will appear in `/data/transformed/`, ready for the TypeScript/Node.js bulk-uploader.

---

## 🌟 Why this matters
This project demonstrates **Backend Engineering** and **Data Architect** competencies:
* **Scalability:** Capable of processing 10,000+ items in seconds, a task that would take days manually.
* **Maintainability:** Decoupled logic using utility functions makes the pipeline easy to update as data sources change.
* **Systems Thinking:** Shows an understanding of the full lifecycle of data—from a raw scraper state to a rendered UI component in a web application.