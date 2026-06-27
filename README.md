# Retail Sales ETL Tool

A configurable Python ETL pipeline for consolidating retailer sales data from multiple Excel formats into a standardized dataset using mapping-driven extraction, validation, and transformation.

---

## Overview

Retail sales data is often received from multiple retailers in Excel format, but each retailer follows a different reporting template. Column names, file structures, naming conventions, and available fields vary significantly, making monthly consolidation a repetitive and error-prone manual process.

This project automates that workflow by providing a configuration-driven ETL pipeline that reads sales files from different retailers, validates their structure, maps them to a common schema, applies business transformations, and produces a single consolidated dataset.

The objective was to build a solution that could easily accommodate new retailer formats without modifying the core processing logic.

<p align="center">
  <img src="/architecture.png" alt="Retail Sales ETL Architecture" width="900">
</p>

---

## The Problem

Every month, sales data arrived from multiple retailers in different Excel formats.

Some of the common challenges included:

* Different column names for the same information
* Different file naming conventions
* Missing fields in certain retailer reports
* Inconsistent store naming
* Missing product attributes
* Manual copy-paste consolidation
* Repetitive Excel transformations

As the number of retailers increased, maintaining separate scripts or Excel workflows became difficult and time-consuming.

---

## The Solution

Instead of creating separate logic for every retailer, this project uses a **configuration-driven approach**.

Each retailer format is defined in a mapping workbook containing:

* File matching pattern (Regex)
* Source column mappings
* Required fields
* Constant values

During execution, the pipeline:

1. Identifies the retailer using the filename.
2. Loads the appropriate mapping.
3. Validates the incoming file structure.
4. Extracts only the required columns.
5. Standardizes the data into a common schema.
6. Applies business transformations.
7. Consolidates all processed files into a single output workbook.

Adding support for a new retailer usually requires updating the mapping workbook rather than changing the application code.

---

## Features

* Configuration-driven column mapping
* Regex-based file identification
* Source file validation
* Support for multiple Excel formats
* Constant value injection
* Store name standardization
* Barcode-based product attribute enrichment
* Derived business fields
* Batch processing of multiple files
* Consolidated output generation
* Per-file error handling
* Processing summary after execution

---

## Business Transformations

The transformation layer currently supports:

* Store name standardization using a master mapping
* Product attribute enrichment using barcode lookup
* Category derivation from Style Code
* Month derivation from transaction date
* Financial Year calculation
* Standardized output schema
* Output column reordering

The transformation module is intentionally modular, allowing new business rules to be added without affecting extraction or validation.

---

## Project Structure

```text
Retail-Sales-ETL/
│
├── config/
│   ├── Mapping_Notebook.xlsx
│   ├── Product_Master.xlsx
│   └── StoreName_Mapping.xlsx
│
├── docs/
│   └── images/
│       └── architecture.png
│
├── src/
│   ├── main.py
│   ├── mapping_loader.py
│   ├── file_matcher.py
│   ├── source_validator.py
│   ├── extraction_engine.py
│   └── transform.py
│
├── sample_data/
│
├── output/
│
├── requirements.txt
│
└── README.md
```

---

## Architecture

```text
                 Input Folder
                      │
                      ▼
            File Pattern Matching
                      │
                      ▼
              Mapping Selection
                      │
                      ▼
             Source Validation
                      │
                      ▼
          Standardized Data Extraction
                      │
                      ▼
          Business Transformations
                      │
                      ▼
          Consolidate All Outputs
                      │
                      ▼
          Final Standardized Dataset
```

---

## Processing Flow

```text
Input Folder
      │
      ▼
Read Excel File
      │
      ▼
Match Filename Pattern
      │
      ▼
Load Configuration Mapping
      │
      ▼
Validate Source Columns
      │
      ▼
Extract Standard Schema
      │
      ▼
Apply Business Transformations
      │
      ▼
Append to Consolidated Dataset
      │
      ▼
Export Final Excel Output
```

---

## Why a Mapping-Based Design?

The project separates **configuration** from **processing logic**.

Rather than hardcoding retailer-specific rules into the application, mappings define how each retailer's data should be interpreted.

This approach offers several advantages:

* Easily supports new retailer formats
* Minimal code changes when report structures change
* Consistent validation across all inputs
* Reusable extraction engine
* Lower long-term maintenance effort

---

## Technologies Used

* Python
* Pandas
* OpenPyXL
* Pathlib
* Regular Expressions

---

## Future Improvements

Planned enhancements include:

* Logging using Python's `logging` module
* External configuration using JSON or YAML
* Command-line interface
* Simple desktop GUI
* Unit testing
* Parallel processing
* CSV support
* Automated data quality reports

---

## Impact

This tool replaces a repetitive manual consolidation process with a reusable and configurable ETL workflow.

Instead of manually cleaning and combining retailer reports every month, users only need to:

1. Place all source files into the input folder.
2. Update the mapping workbook if a new retailer format is introduced.
3. Run the application.

The output is a standardized, analysis-ready dataset that can be directly consumed by reporting tools such as Power BI or Excel, significantly reducing manual effort and improving consistency.
