import psycopg2
import os
import logging


logger = logging.getLogger(__name__)


class DatabaseConnection:
    @staticmethod
    def get_connection():
        config = {
            "host": os.environ.get("DB_HOST"),
            "database": os.environ.get("DB_NAME"),
            "user": os.environ.get("DB_USER"),
            "password": os.environ.get("DB_PASSWORD"),
            "port": os.environ.get("DB_PORT"),
        }
        try:
            conn = psycopg2.connect(**config)
            logger.info("Database connection established.")
            return conn
        except psycopg2.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
