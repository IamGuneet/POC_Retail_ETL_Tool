import pandas as pd

class SourceColumnMissingError(Exception):
    pass


def validate_source_file(df, mapping):

    df.columns = df.columns.str.strip()
    missing_columns = []

    # print(df.columns.tolist())
    # print(mapping)
    
    for standard_col,config in mapping.items():

        source_col = config["source"]
        constant_value = config.get("constant")
        required = config["required"]
        # 
        # Derived Column
        if source_col is None and constant_value is None:
            continue

        # Constant column 
        if constant_value is not None:
            continue

        # Mapped Column
        if required and source_col not in df.columns:
            missing_columns.append(source_col)

    if missing_columns:
        raise SourceColumnMissingError(
            f"Missing source columns: {missing_columns}"
        )
    
    return True    