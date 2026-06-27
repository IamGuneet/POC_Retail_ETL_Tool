import pandas as pd

def extract_data(source_df,mapping):

    output_df = pd.DataFrame()

    for standard_col, config in mapping.items():

        source_col = config["source"]
        constant_value = config["constant"]

        #mapped column handling 
        # print(
        # f"{standard_col} | "
        # f"source={repr(source_col)} | "
        # f"constant={repr(constant_value)}"
        # )

        if source_col:
            output_df[standard_col] = source_df[source_col]
        # constant column handling
        elif constant_value is not None and constant_value!="":
            output_df[standard_col] = [constant_value] * len(source_df)
        else:
            output_df[standard_col] = None

    return output_df
