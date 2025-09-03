import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Advanced data processing for dashboard analytics"""
    
    @staticmethod
    def calculate_retention_rates(df, cohort_col='signup_date', return_col='date', user_col='user_id'):
        """Calculate cohort retention rates"""
        try:
            # Create cohort table
            cohort_data = df.groupby([cohort_col, return_col])[user_col].nunique().reset_index()
            cohort_sizes = df.groupby(cohort_col)[user_col].nunique().reset_index()
            cohort_sizes.columns = [cohort_col, 'cohort_size']
            
            # Merge and calculate retention rates
            cohort_data = cohort_data.merge(cohort_sizes, on=cohort_col)
            cohort_data['retention_rate'] = (cohort_data[user_col] / cohort_data['cohort_size']) * 100
            
            return cohort_data
        except Exception as e:
            logger.error(f"Error calculating retention rates: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def detect_anomalies(df, metric_col, threshold=2):
        """Detect anomalies in time series data using z-score"""
        try:
            df = df.copy()
            df['z_score'] = np.abs((df[metric_col] - df[metric_col].mean()) / df[metric_col].std())
            df['is_anomaly'] = df['z_score'] > threshold
            
            return df
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return df
    
    @staticmethod
    def calculate_growth_rates(df, metric_col, date_col='date', periods=7):
        """Calculate growth rates over specified periods"""
        try:
            df = df.sort_values(date_col)
            df[f'{metric_col}_growth'] = df[metric_col].pct_change(periods=periods) * 100
            
            return df
        except Exception as e:
            logger.error(f"Error calculating growth rates: {e}")
            return df
    
    @staticmethod
    def segment_users(df, engagement_col='total_sessions', subscription_col='subscription_type'):
        """Segment users based on engagement and subscription"""
        try:
            df = df.copy()
            
            # Define engagement segments
            df['engagement_segment'] = pd.cut(
                df[engagement_col], 
                bins=[0, 1, 5, 20, np.inf], 
                labels=['Inactive', 'Low', 'Medium', 'High']
            )
            
            # Create combined segments
            df['user_segment'] = df['engagement_segment'].astype(str) + '_' + df[subscription_col]
            
            return df
        except Exception as e:
            logger.error(f"Error segmenting users: {e}")
            return df