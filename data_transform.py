import pandas as pd

class DataTransform:
    """Performs data type conversions for consistency and analysis readiness."""
    
    @staticmethod
    def convert_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts specific columns to appropriate data types:
        - 'month': Converts to an ordered categorical type, ensuring proper chronological sorting.
        - 'weekend': Converts to a boolean type, where True represents a weekend day.
        - 'revenue': Converts to a boolean type, indicating whether revenue was generated.
        
        Args:
            df (pd.DataFrame): The input DataFrame.
        
        Returns:
            pd.DataFrame: The transformed DataFrame with updated data types.
        """
        df['month'] = pd.Categorical(df['month'], categories=[
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ], ordered=True)
        df['weekend'] = df['weekend'].astype(bool)  # Changed from 'category' to bool
        df['revenue'] = df['revenue'].astype(bool)
        return df

class DataFrameInfo:
    """Provides descriptive information about the DataFrame."""
    
    @staticmethod
    def describe_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Returns the data types of each column in the DataFrame.
        
        Args:
            df (pd.DataFrame): The input DataFrame.
        
        Returns:
            pd.Series: A series where index represents column names and values represent data types.
        """
        return df.dtypes
    
    @staticmethod
    def get_statistics(df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates a statistical summary of numeric columns, including:
        - Count, mean, standard deviation, min, max, and quartiles.
        
        Args:
            df (pd.DataFrame): The input DataFrame.
        
        Returns:
            pd.DataFrame: A summary table with statistics for each numeric column.
        """
        return df.describe()
    
    @staticmethod
    def count_nulls(df: pd.DataFrame) -> pd.Series:
        """
        Counts the number of missing (NaN) values in each column.
        
        Args:
            df (pd.DataFrame): The input DataFrame.
        
        Returns:
            pd.Series: A series showing the number of missing values per column.
        """
        return df.isnull().sum()
    
    @staticmethod
    def get_shape(df: pd.DataFrame) -> tuple:
        """
        Returns the number of rows and columns in the DataFrame.
        
        Args:
            df (pd.DataFrame): The input DataFrame.
        
        Returns:
            tuple: A tuple in the form (number of rows, number of columns).
        """
        return df.shape

class DataFrameTransform:
    """"Handles data preprocessing by filling in missing values."""
    
    @staticmethod
    def impute_missing(df: pd.DataFrame, strategy: str = 'median') -> pd.DataFrame:
        """
        Fills missing values in numerical columns using the specified strategy:
        - 'median': Replaces missing values with the median of the respective column.
        - 'mean': Replaces missing values with the mean of the respective column.
        
        Args:
            df (pd.DataFrame): The input DataFrame.
            strategy (str, optional): The imputation method ('median' or 'mean'). Defaults to 'median'.
        
        Returns:
            pd.DataFrame: The DataFrame with missing values imputed.
        """
        for col in df.select_dtypes(include=['number']):
            if strategy == 'median':
                df[col].fillna(df[col].median(), inplace=True)
            elif strategy == 'mean':
                df[col].fillna(df[col].mean(), inplace=True)
        return df
    




