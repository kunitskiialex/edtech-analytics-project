import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    """Create the main database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD'),
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        db_name = os.getenv('DB_NAME', 'edtech_analytics')
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if not cursor.fetchone():
            cursor.execute(f'CREATE DATABASE {db_name}')
            logger.info(f"Database '{db_name}' created successfully")
        else:
            logger.info(f"Database '{db_name}' already exists")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        raise

def setup_tables():
    """Create all necessary tables and indexes"""
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'schema.sql')
    with open(schema_path, 'r') as file:
        schema_sql = file.read()
    
    try:
        conn = psycopg2.connect(os.getenv('DB_URL'))
        cursor = conn.cursor()
        cursor.execute(schema_sql)
        conn.commit()
        logger.info("Tables and indexes created successfully")
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error setting up tables: {str(e)}")
        raise

def main():
    """Main setup function"""
    logger.info("Starting database setup...")
    create_database()
    setup_tables()
    logger.info("Database setup completed successfully!")

if __name__ == "__main__":
    main()