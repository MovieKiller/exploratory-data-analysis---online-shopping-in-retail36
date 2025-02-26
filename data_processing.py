import pandas as pd
import numpy as np

class DataSkewTransformer:
    """Handles data skew transformations."""
    
    @staticmethod
    def fix_skew(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
        """
        Identifies and applies log transformation to skewed numerical columns.

        - Uses `np.log1p()` (log(1 + x)) to handle zero and positive values.
        - Only applies transformation if the absolute skewness exceeds the given threshold.

        Args:
            df (pd.DataFrame): The input DataFrame.
            threshold (float, optional): The skewness threshold above which transformation is applied. Defaults to 0.5.

        Returns:
            pd.DataFrame: The transformed DataFrame with reduced skewness.
        """
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            skewness = df[col].skew()
            if abs(skewness) > threshold:
                df[col] = np.log1p(df[col])
        return df

class OutlierHandler:
    """Detects and removes outliers from numerical columns using the Interquartile Range (IQR) method."""
    
    @staticmethod
    def remove_outliers(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Removes outliers from the specified numerical columns using the IQR method.

        - Outliers are defined as values below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR.
        - The method filters out rows containing outliers in the selected columns.

        Args:
            df (pd.DataFrame): The input DataFrame.
            columns (list): A list of numerical column names to check for outliers.

        Returns:
            pd.DataFrame: A DataFrame with outliers removed.
        """
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]
        return df