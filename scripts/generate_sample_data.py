import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_sample_data():
    """Generate simple sample data"""
    # Sample data like from your original example
    data = [
        ('2024-01-01', 'U001', 'C101', True, 45, 'mobile', 'free'),
        ('2024-01-01', 'U002', 'C102', False, 15, 'desktop', 'premium'),
        ('2024-01-01', 'U003', 'C101', True, 60, 'tablet', 'premium'),
        ('2024-01-02', 'U001', 'C101', True, 40, 'mobile', 'free'),
        ('2024-01-02', 'U002', 'C102', True, 55, 'desktop', 'premium'),
        # Add more sample data...
    ]
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=[
        'date', 'user_id', 'course_id', 'lesson_completed', 
        'time_spent', 'device_type', 'subscription_type'
    ])
    
    return df

def save_to_database(df):
    """Save data to database"""
    try:
        conn = psycopg2.connect(os.getenv('DB_URL'))
        cursor = conn.cursor()
        
        # Insert data
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO activity (date, user_id, course_id, lesson_completed, 
                                    time_spent, device_type, subscription_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, tuple(row))
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Inserted {len(df)} records")
        
    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")
        raise

def main():
    logger.info("Generating sample data...")
    df = generate_sample_data()
    save_to_database(df)
    logger.info("Sample data generated successfully!")

if __name__ == "__main__":
    main()