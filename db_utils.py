import yaml
import pandas as pd
from sqlalchemy import create_engine

class RDSDatabaseConnector:
    """Connects to AWS RDS database and handles data extraction."""
    
    def __init__(self, credentials: dict):
        self.credentials = credentials
        self.engine = self._init_db_engine()
    
    def _init_db_engine(self):
        """Initialize SQLAlchemy engine using credentials."""
        conn_str = f"postgresql://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}"
        return create_engine(conn_str)
    
    def extract_data(self, table_name: str) -> pd.DataFrame:
        """Extract data from specified table into DataFrame."""
        with self.engine.connect() as conn:
            return pd.read_sql_table(table_name, conn)
    
    @staticmethod
    def save_data_to_csv(df: pd.DataFrame, filename: str):
        """Save DataFrame to CSV."""
        df.to_csv(filename, index=False)
    
    @staticmethod
    def load_data_from_csv(filename: str) -> pd.DataFrame:
        """Load DataFrame from CSV."""
        return pd.read_csv(filename)

def load_credentials(filename: str = 'credentials.yaml') -> dict:
    """Load database credentials from YAML file."""
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    credentials = load_credentials()
    connector = RDSDatabaseConnector(credentials)
    df = connector.extract_data('customer_activity')
    connector.save_data_to_csv(df, 'customer_activity.csv')
    loaded_df = connector.load_data_from_csv('customer_activity.csv')
    print(f"Data loaded with shape: {loaded_df.shape}")