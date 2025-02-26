import pandas as pd
class BusinessAnalysis:
    @staticmethod
    def weekend_sales_analysis(df: pd.DataFrame):
        """Analyze sales distribution on weekends vs weekdays."""
        return df.groupby('weekend', observed=False)['revenue'].mean()  # Explicit observed=False
    @staticmethod
    def regional_revenue_analysis(df: pd.DataFrame):
        """Identify top revenue-generating regions."""
        return df.groupby('region')['revenue'].sum().sort_values(ascending=False)
    @staticmethod
    def traffic_analysis(df: pd.DataFrame):
        """Analyze traffic type performance"""
        return df.groupby('traffic_type').agg({
            'revenue': 'sum',
            'bounce_rates': 'mean'
        }).sort_values('revenue', ascending=False)