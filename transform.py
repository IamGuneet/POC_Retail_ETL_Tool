import pandas as pd
import numpy as np

STANDARD_SCHEMA = [
    "RETAILER",
    "STORE NAME",
    "MONTH",
    "DATE",
    "FY",
    "BILL NO",
    "BARCODE",
    "STYLECODE",
    "COLOR",
    "SIZE",
    "CATEGORY",
    "SEASON",
    "QTY",
    "PROMO DETAILS",
    "DISCOUNT",
    "MRP",
    "TOTAL MRP",
    "NET VALUE"
]

def transform_data(df):
    df['MRP'] = df["MRP"].abs()
    df['Date'] = pd.to_datetime(df['Date'],format = "%d-%m-%Y",errors="coerce")
    df = add_month(df)
    df = calculate_season(df)
    df = add_financial_year(df)
    df = calculate_total_mrp(df)
    df = calculate_discount(df)
    df = standardize_store_names(df)
    df = fill_product_attributes(df)
    df = derive_category(df)
    df['DATE'] = df['DATE'].dt.strftime('%Y-%m-%d')
    df = df[STANDARD_SCHEMA]
    return df



def calculate_season(df):
    df ['Season'] = np.where(
                    df["Date"].dt.month >6,
                    "AW",
                    "SS"
                    )

    return df


def add_month(df):
    df["Month"] = df["Date"].dt.month
    return df

def add_financial_year(df):
    year = np.where(
            df["Date"].dt.month >= 4,
            df["Date"].dt.year,
            df["Date"].dt.year-1 
    )
    df["FY"] = [f"FY-{str(y)[2:]}"for y in year]
    return df

def calculate_total_mrp(df):
    df["Total MRP"] = df['Qty']*df['MRP']
    return df

def calculate_discount(df):
    df["Discount"] = df["Total MRP"] - df["Net Value"]
    return df

def standardize_store_names(df):

    master_df = pd.read_excel(r"C:\Users\HI\Documents\scripts\Consolidating Script\config\StoreName_Mapping.xlsx")
    
    # duplicates = master_df[
        # master_df.duplicated(
            # subset=["Retailer","Store Name"],
            # keep=False
        # )
    # ]
    # print(duplicates)
    # print(f"Duplicate mappings : {len(duplicates)}")
    
    # dropping duplicates
    master_df = master_df.drop_duplicates(
    subset=["Retailer", "Store Name"],
    keep="first"
    )

    for col in ["Retailer","Store Name"]:
        master_df[col] = master_df[col].astype(str).str.strip().str.upper()
        df[col] = df[col].astype(str).str.strip().str.upper()
    
    df = df.merge(
        master_df,
        on=["Retailer", "Store Name"],
        how="left"
    )

    df["Store Name"] = (
        df["Master Name"]
        .fillna(df["Store Name"])
    )

    df.drop(columns=["Master Name"], inplace=True)
    print("After Store Standrdization: ",len(df))


    return df

def fill_product_attributes(df):
    df.columns = df.columns.str.upper()
    master_df = pd.read_excel(r"C:\Users\HI\Documents\scripts\Consolidating Script\config\Master-Bar_Code.xlsx")
    print(f"Master Table Lenght:{len(master_df)}")
    print(f"df length:{len(df)}")
    
    master_df = master_df.drop_duplicates(subset="BARCODE", keep="first")
    
    print(f"Master Table Lenght After Cleaning:{len(master_df)}")
    lookup_cols = [
        'STYLECODE',
        'COLOR',
        'SIZE'
    ]
    # standardize data type of bar code
    df["BARCODE"] = df["BARCODE"].astype(int) 
    master_df["BARCODE"] = master_df["BARCODE"].astype(int)


    df = df.merge(
        master_df,
        on="BARCODE",
        how = "left",
        suffixes= ("","_master")
    )

    # print(df.columns.tolist())

    for col in lookup_cols:
        df[col] = df[col].fillna(df[f"{col}_master"])

    drop_col = [
        'STYLECODE',
        'COLOR',
        'SIZE'
    ]
    df.drop(
        columns=[f"{col}_master" for col in drop_col],
        inplace=True
    )

    print(f"df length after transforming:{len(df)}")
    print(df.columns.tolist())
    return df

def clean_data(df):

    return df

def derive_category(df):

    def get_category(stylecode):

        if pd.isna(stylecode):
            return "PROMO BAG"

        stylecode = str(stylecode).upper()

        if "46X25X26" in stylecode:
            return "TRAVEL BAG"
        elif "PTB" in stylecode:
            return "DUFFLE"
        elif "SH" in stylecode:
            return "SHIRT"
        elif "TS" in stylecode:
            return "T-SHIRT"
        elif "SS" in stylecode:
            return "SWEAT SHIRT"
        elif "TR" in stylecode:
            return "TROUSER"
        elif "DN" in stylecode:
            return "JEANS"
        elif "SO" in stylecode:
            return "SHORTS"
        else:
            return "PROMO BAG"
        
    df['CATEGORY'] = df['STYLECODE'].apply(get_category)
    return df