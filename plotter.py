import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from analysis import BusinessAnalysis


class Plotter:
    """Handles data visualization tasks for business analysis."""
    
    @staticmethod
    def plot_distributions(df: pd.DataFrame, columns: list = None):
        """Plot distributions of numerical columns"""
        numeric_cols = columns if columns else df.select_dtypes(include=['number']).columns
        plt.figure(figsize=(14, 10))
        
        for i, col in enumerate(numeric_cols, 1):
            plt.subplot(4, 4, i)
            sns.histplot(df[col], kde=True, bins=30)
            plt.title(f'Distribution of {col}')
        
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_device_breakdown(df: pd.DataFrame):
        """Visualize mobile vs desktop usage"""
        # Create device type classification
        df['device_type'] = df['operating_systems'].apply(
            lambda x: 'Mobile' if x in ['iOS', 'Android'] else 'Desktop'
        )
        
        plt.figure(figsize=(10, 6))
        sns.countplot(x='device_type', data=df)
        plt.title('Device Type Distribution')
        plt.xlabel('Device Category')
        plt.ylabel('User Count')
        plt.show()

    @staticmethod
    def plot_os_browser_combo(df: pd.DataFrame):
        """Show browser usage breakdown by OS"""
        plt.figure(figsize=(14, 8))
        cross_tab = pd.crosstab(df['operating_systems'], df['browser'])
        sns.heatmap(cross_tab, annot=True, fmt="d", cmap="YlGnBu")
        plt.title('Browser Usage by Operating System')
        plt.xlabel('Browser')
        plt.ylabel('Operating System')
        plt.show()
    @staticmethod
    def plot_null_distribution(df: pd.DataFrame):
        """Visualize null values distribution"""
        null_counts = df.isnull().sum()
        plt.figure(figsize=(10,6))
        sns.barplot(x=null_counts.index, y=null_counts.values)
        plt.xticks(rotation=45)
        plt.title('Null Values Distribution')
        plt.show()
    
    @staticmethod
    def plot_correlation_matrix(df: pd.DataFrame):
        """Plot correlation heatmap with proper categorical handling"""
        # Create a numeric-only dataframe
        numeric_df = df.copy()
        
        # Convert categorical columns to numeric codes
        for col in numeric_df.select_dtypes(include=['category']).columns:
            numeric_df[col] = numeric_df[col].cat.codes
            
        # Select only numeric columns
        numeric_df = numeric_df.select_dtypes(include=['number'])
        
        # Plot correlation matrix
        plt.figure(figsize=(16, 10))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix (Categorical Columns Encoded)')
        plt.show()

    @staticmethod
    def plot_regional_revenue(df: pd.DataFrame):
        """Visualize revenue by region"""
        regional_revenue = BusinessAnalysis.regional_revenue_analysis(df)
        plt.figure(figsize=(10, 6))
        sns.barplot(x=regional_revenue.index, y=regional_revenue.values)
        plt.title("Revenue by Region")
        plt.xlabel("Region")
        plt.ylabel("Total Revenue")
        plt.xticks(rotation=45)
        plt.show()

    @staticmethod
    def plot_traffic_analysis(df: pd.DataFrame):
        """Visualize traffic type performance"""
        traffic_stats = BusinessAnalysis.traffic_analysis(df)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=traffic_stats.index, y=traffic_stats['revenue'])
        plt.title("Revenue by Traffic Type")
        plt.xlabel("Traffic Type")
        plt.ylabel("Total Revenue")
        plt.xticks(rotation=45)
        plt.show()    

   

    @staticmethod
    def plot_traffic_types(df: pd.DataFrame):
        """Visualize traffic type distribution and conversion rates"""
        plt.figure(figsize=(14, 6))
        
        # Traffic type distribution
        plt.subplot(1, 2, 1)
        traffic_counts = df['traffic_type'].value_counts().sort_index()
        sns.barplot(x=traffic_counts.index, y=traffic_counts.values, palette="Blues_d")
        plt.title('Traffic Type Distribution')
        plt.xlabel('Traffic Type Code')
        plt.ylabel('Number of Visits')

        # Conversion rates by traffic type
        plt.subplot(1, 2, 2)
        conversion_rates = df.groupby('traffic_type')['revenue'].mean().sort_index()
        sns.barplot(x=conversion_rates.index, y=conversion_rates.values, palette="Reds_d")
        plt.title('Conversion Rates by Traffic Type')
        plt.xlabel('Traffic Type Code')
        plt.ylabel('Conversion Rate (%)')

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_visitor_conversion(conversion_rates: pd.Series):
        """Plot customer type conversion rates"""
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=conversion_rates.index, y=conversion_rates.values)
        plt.title('Conversion Rates by Visitor Type')
        plt.ylabel('Conversion Rate')
        plt.xlabel('Visitor Type')
        
        # Add percentage labels
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.1%}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', 
                        xytext=(0, 5), 
                        textcoords='offset points')
            
        plt.show()

    @staticmethod
    def plot_weekend_comparison(weekend_sales: pd.Series):
        """Plot weekend vs weekday comparison"""
        plt.figure(figsize=(8, 5))
        ax = sns.barplot(x=weekend_sales.index, y=weekend_sales.values)
        plt.title('Conversion Rates: Weekend vs Weekdays')
        plt.xlabel('Weekend')
        plt.ylabel('Conversion Rate')
        
        # Add value labels
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.2f}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', 
                        xytext=(0, 5), 
                        textcoords='offset points')
            
        plt.show()

   
    @staticmethod
    def plot_monthly_sales(df: pd.DataFrame):
        """Plot monthly sales trend from raw DataFrame"""
        monthly_sales = df.groupby('month')['revenue'].sum()
        ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        plt.figure(figsize=(12, 6))
        ax = sns.lineplot(
            x=pd.Categorical(monthly_sales.index, categories=ordered_months, ordered=True),
            y=monthly_sales.values,
            marker='o',
            linewidth=2.5
        )
        plt.title('Monthly Sales Performance')
        plt.xlabel('Month')
        plt.ylabel('Total Revenue')
        plt.grid(True)
        
        # Add data labels
        for x, y in zip(ax.get_xticks(), monthly_sales.reindex(ordered_months)):
            ax.text(x, y, f'${y/1000:.0f}K', 
                    ha='center', va='bottom')
            
        plt.show()

    
    @staticmethod
    def plot_traffic_contribution(df: pd.DataFrame, traffic_mapping: dict):
        """Plot traffic source contribution"""
        traffic_contribution = df.groupby('traffic_type')['revenue'].sum()
        labels = traffic_contribution.index.map(
            lambda x: f"{traffic_mapping.get(x, 'Other')} ({x})"
        )
        
        plt.figure(figsize=(10, 6))
        plt.pie(traffic_contribution, labels=labels,
                autopct='%1.1f%%', startangle=90,
                explode=[0.1 if i == traffic_contribution.idxmax() else 0 
                         for i in traffic_contribution.index])
        plt.title('Revenue Contribution by Traffic Source')
        plt.show()       

    @staticmethod
    def plot_traffic_roi(df: pd.DataFrame, traffic_mapping: dict):
        """Visualize traffic source effectiveness"""
        # Calculate metrics
        traffic_stats = df.groupby('traffic_type').agg(
            total_revenue=('revenue', 'sum'),
            conversions=('revenue', 'sum'),
            total_visits=('revenue', 'count')
        ).assign(
            conversion_rate=lambda x: x['conversions']/x['total_visits'],
            traffic_name=lambda x: x.index.map(traffic_mapping)
        ).reset_index()

        plt.figure(figsize=(14, 6))
        
        # Revenue comparison
        plt.subplot(1, 2, 1)
        sns.barplot(x='traffic_name', y='total_revenue', data=traffic_stats)
        plt.title('Total Revenue by Traffic Source')
        plt.xlabel('Traffic Source')
        plt.ylabel('Revenue')
        plt.xticks(rotation=45)

        # Conversion rates
        plt.subplot(1, 2, 2)
        sns.barplot(x='traffic_name', y='conversion_rate', data=traffic_stats)
        plt.title('Conversion Rates by Traffic Source')
        plt.xlabel('Traffic Source')
        plt.ylabel('Conversion Rate')
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_bounce_rates(df: pd.DataFrame):
        """Visualize bounce rates by region and traffic type"""
        plt.figure(figsize=(16, 8))
        
        # Bounce rates by region
        plt.subplot(1, 2, 1)
        regional_bounce = df.groupby('region')['bounce_rates'].mean().sort_values()
        sns.barplot(x=regional_bounce.index, y=regional_bounce.values)
        plt.title('Average Bounce Rate by Region')
        plt.xlabel('Region')
        plt.ylabel('Bounce Rate')
        plt.ylim(0, 1)
        
        # Bounce rates by traffic type
        plt.subplot(1, 2, 2)
        traffic_bounce = df.groupby('traffic_type')['bounce_rates'].mean().sort_values()
        sns.barplot(x=traffic_bounce.index, y=traffic_bounce.values)
        plt.title('Average Bounce Rate by Traffic Type')
        plt.xlabel('Traffic Type')
        plt.ylabel('')
        plt.ylim(0, 1)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_regional_anomalies(df: pd.DataFrame):
        """Identify regional performance anomalies using Z-scores"""
        # Calculate regional revenue statistics
        regional_stats = df.groupby('region').agg(
            total_revenue=('revenue', 'sum'),
            avg_bounce_rate=('bounce_rates', 'mean'),
            conversion_rate=('revenue', 'mean')
        )
        
        # Calculate Z-scores for total revenue
        regional_stats['revenue_zscore'] = (
            (regional_stats['total_revenue'] - regional_stats['total_revenue'].mean()) 
            / regional_stats['total_revenue'].std()
        )
        
        # Create visualization
        plt.figure(figsize=(14, 8))
        sns.heatmap(
            regional_stats[['revenue_zscore', 'avg_bounce_rate', 'conversion_rate']],
            annot=True, 
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            linewidths=.5
        )
        plt.title('Regional Performance Anomalies\n(Z-scores for Revenue)')
        plt.xlabel('Metrics')
        plt.ylabel('Region')
        plt.show()    