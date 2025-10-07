import numpy as np
import pandas as pd


def clean_nan_values(df):
    """
    Cleans NaN values from a DataFrame by identifying columns with missing values 
    and either dropping or flagging them for imputation.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame to clean.

    Returns
    -------
    df: pandas.DataFrame
        The cleaned DataFrame with selected NaN rows removed.
    replacing_nans: list of str
        Columns with a high proportion of NaNs (to be imputed or replaced)
    """
    colummns_wnan = df.columns[df.isna().any()].tolist()
    len_df = len(df)
    replacing_nans, drop_nans = id_nan_columns(df, colummns_wnan, len_df)
    df = drop_cols(df, drop_nans, len_df)
    return df, replacing_nans

def id_nan_columns(df, columns, len_df, max_nans=0.05):
    """
    Classifies columns with NaN values into two groups based on the proportion of missing data.

    Columns with a NaN proportion greater than `max_nans` are flagged for replacement,
    while those below the threshold are flagged for row removal.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    columns : list of str
        List of column names to inspect.
    len_df : int
        The total number of rows in the DataFrame.
    max_nans : float, optional (default=0.05)
        The threshold proportion of NaN values (e.g., 0.05 = 5%).

    Returns
    -------
    replacing_nans : list of str
        Columns with a high proportion of NaNs (to be imputed or replaced).
    drop_nans : list of str
        Columns with a low proportion of NaNs (rows will be dropped).
    """
    # Dropping the rows of those columns that have <5% of nans
    drop_nans = []
    # Replacing those nan values where its columns have >5% of nans
    replacing_nans =[]
    for column in colummns_wnan:
        if df[column].isna().sum() > len_df*max_nans:
            replacing_nans.append(column)
        else:
            drop_nans.append(column)
    return replacing_nans, drop_nans

def drop_cols(df, cols, len_df):
    """
    Drops rows containing NaN values in specified columns and logs the action.

    For each column provided, rows with NaN values are removed, and a message is printed
    showing how many rows were dropped and what percentage of the dataset they represent.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : list of str
        List of column names from which to drop NaN rows.
    len_df : int
        Total number of rows in the original DataFrame (for percentage calculation).

    Returns
    -------
    pandas.DataFrame
        DataFrame with NaN rows removed from specified columns.
    """
    for drop_col in cols:
        num_nan = df[drop_col].isna().sum()
        print(f'Dropped {num_nan} rows due to nan values in {drop_col} column, corresponding to a {round((num_nan/len_df)*100,3)}% of the dataset length')
        df.dropna(subset=drop_col, inplace=True)
    return df