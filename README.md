# Bengal Bazar: Data Automation Engine ⚡

A specialized Python-based interactive CLI ETL (Extract, Transform, Load) tool designed to bridge the gap between raw, messy e-commerce data and the **Bengal Bazar (PERN)** production database.

This project automates data cleaning, extraction, relational formatting, and uploading for thousands of product entries, ensuring strict data integrity before they reach the backend.

---

## 🚀 The Problem
E-commerce data sourced from various suppliers or scrapers often arrives in inconsistent formats:
* **Inconsistent SKUs:** Missing unique identifiers or irregular naming conventions.
* **Flat Structure:** Flat CSV data that does not match the nested relational structure of a PostgreSQL database.
* **UI Incompatibility:** Category names that don't easily map to frontend Icon components.
* **Scalability:** Manual data entry for thousands of items is prone to human error and creates massive bottlenecks.

## 🛠️ The Solution
This interactive automation engine provides five core capabilities:

1.  **Clean Data:** Normalizes text, sanitizes inputs, and preps raw CSVs.
2.  **Brand Extraction:** Parses and merges unique brand lists from up to 10 different supplier CSVs at once.
3.  **Taxonomy Extraction:** Automatically maps and extracts Categories and SubCategories across multiple files.
4.  **Format Conversion:** Transforms flat rows into Bengal Bazar's structured schema. Generates unique SKUs, formats JSON attributes, and maps category strings to **PascalCase** icon components (e.g., `FrozenFoods`) for the React frontend.
5.  **Direct Upload:** Pushes the finalized "Gold Standard" data directly to the Bengal Bazar system.

---

## 💻 Technical Stack
* **Language:** Python 3.14+
* **Interface:** Interactive Command-Line Interface (CLI)
* **Dev Context:** This acts as the specialized data-transformer for the **Bengal Bazar Ecosystem**, bridging raw web scraper outputs to the PERN with Next.js (PostgreSQL, Express, React, Node.js) production app.

---

## ⚙️ Setup & Usage

1.  **Run Pipeline:**
    ```bash
    python app.py
2. Use the Interactive Menu: The CLI will guide you through the ETL process step-by-step.    

    --- Bengal Bazar Data Tool ---
    1. Clean Data
    2. Extract Unique Brands (Merge from multiple CSVs)
    3. Extract Categories & SubCategories
    4. Convert To Bengal Bazar Format
    5. Upload To Bengal Bazar
    6. Exit


3.  **Provide Files:** Simply type the names of your CSV files (e.g., `meat_product_data.csv`) when prompted to execute the desired transformation or upload step.

---

## 🌟 Why this matters
* **Scalability:** Capable of processing huge csv data in seconds, a task that would take days manually.
* **Systems Thinking:** Handles the full lifecycle of data-conversion from a raw data scraper state to a tranformed UI component-ready state.