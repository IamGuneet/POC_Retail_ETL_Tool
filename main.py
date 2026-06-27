from pathlib import Path
import pandas as pd

from mapping_loader import load_mappings
from file_matcher import get_mapping_for_file
from source_validator import validate_source_file
from extraction_engine import extract_data
from transform import transform_data


# ==========================
# Configuration
# ==========================

INPUT_FOLDER = Path(
    r"G:\.shortcut-targets-by-id\1pLLJ2r3gkex791VCkEckPWLMYBMOaJUG\MIS\Guneet\June\June-25\Sales"
)

OUTPUT_FILE = INPUT_FOLDER / "Consolidated_Output.xlsx"

MAPPING_FILE = (
    r"C:\Users\HI\Documents\scripts\Consolidating Script\config\JUNE-2025-MAPPING.xlsx"
)


# ==========================
# Load configuration
# ==========================

print("=" * 60)
print("Loading Mapping File...")

mappings = load_mappings(MAPPING_FILE)

print("✓ Mapping Loaded")
print("=" * 60)


# ==========================
# Process Files
# ==========================

excel_files = list(INPUT_FOLDER.glob("*.xlsx"))

all_data = []

processed_files = []
failed_files = []

for file in excel_files:

    print(f"\nProcessing : {file.name}")

    try:

        # Read File
        df = pd.read_excel(file)
        print(f"Rows Read : {len(df)}")

        # Match Mapping
        matched_pattern, mapping = get_mapping_for_file(
            file.name,
            mappings
        )

        print(f"Matched Mapping : {matched_pattern}")

        # Validate
        validate_source_file(df, mapping)
        print("✓ Validation Passed")

        # Extract
        standardized_df = extract_data(
            df,
            mapping
        )

        print(f"Rows After Extraction : {len(standardized_df)}")

        # Transform
        transformed_df = transform_data(
            standardized_df
        )

        print(f"Rows After Transformation : {len(transformed_df)}")

        # Add to consolidated list
        all_data.append(transformed_df)

        processed_files.append(file.name)

        print("✓ Completed Successfully")

    except Exception as e:

        print(f"✗ Failed : {e}")

        failed_files.append({
            "File": file.name,
            "Error": str(e)
        })


# ==========================
# Consolidate
# ==========================

if all_data:

    final_df = pd.concat(
        all_data,
        ignore_index=True
    )

    final_df.to_excel(
        OUTPUT_FILE,
        index=False
    )

    print("\nConsolidated file saved successfully.")

else:

    print("\nNo files were processed successfully.")


# ==========================
# Summary
# ==========================

print("\n" + "=" * 60)

print("PROCESS SUMMARY")

print("=" * 60)

print(f"Total Files      : {len(excel_files)}")
print(f"Processed Files  : {len(processed_files)}")
print(f"Failed Files     : {len(failed_files)}")

if all_data:
    print(f"Total Rows       : {len(final_df)}")

print("=" * 60)

if failed_files:

    print("\nFailed Files:")

    for item in failed_files:

        print(f"- {item['File']}")
        print(f"  Reason : {item['Error']}")