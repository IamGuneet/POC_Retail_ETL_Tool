from pathlib import Path
import pandas as pd
# Custom error
class MappingError(Exception):
    pass

def load_mappings(file_path: str)-> dict:

    mapping_path = Path(file_path)

    if not mapping_path.exists():
        raise FileNotFoundError(f"Mapping File not Found: {file_path}")
    
    df = pd.read_excel(mapping_path)
    # Cleaning Column Headers for extra spaces and capitalizing them
    df.columns = df.columns.str.strip().str.upper()
    
    
    required_columns =[
        "FILE PATTERN",
        "STANDARD COLUMN",
        "SOURCE COLUMN",
        "REQUIRED",
        "CONSTANT COLUMN"
    ]

    # checking for missing columns
    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]
    

    if missing_columns:
        raise MappingError(
            f"Missing Columns in mapping file: {missing_columns}"
        )

    df = df.map(
        lambda x: x.strip() if isinstance(x,str) else x
    )
    df["SOURCE COLUMN"] = (
        df["SOURCE COLUMN"].replace("",pd.NA)
    )

    df["CONSTANT COLUMN"] = (
        df["CONSTANT COLUMN"].replace("",pd.NA)
    )

    invalid_patterns = df["FILE PATTERN"].isna()

    if invalid_patterns.any():
        raise MappingError(
            f"Missing Patterns in mapping file: {invalid_patterns}"
        )
    

    mappings = {}

    for _,row in df.iterrows():

        pattern = row["FILE PATTERN"].upper()
        standard_col = row["STANDARD COLUMN"]
        source_col = row["SOURCE COLUMN"]
        constant_col = row["CONSTANT COLUMN"]
        required = str(row["REQUIRED"]).strip().upper() in ["Y","YES","TRUE"]

        # 
        if pd.isna(source_col):
            source_col = None
        if pd.isna(constant_col):
            constant_col = None

        if pattern not in mappings:
            mappings[pattern]={}

        mappings[pattern][standard_col] ={
            "source":source_col,
            "required":required,
            "constant":constant_col
        }
        if source_col and constant_col:
            raise MappingError(
            f"{standard_col} cannot have both Source Column and Constant Value"
        )

    return mappings