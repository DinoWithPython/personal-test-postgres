# tests/__init__.py
import os
import sys
import psycopg2
import unittest
from contextlib import contextmanager
import logging
from datetime import datetime

class BaseIntegrationTest(unittest.TestCase):
    DB_NAME = os.getenv('POSTGRES_DB', 'test_db')
    DB_USER = os.getenv('POSTGRES_USER', 'test_user')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'test_password')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', '5432')
    
    # Настройка логирования
    LOG_FILE = f'test_logs_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log'
    
    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(__name__)
        cls.logger.info("Starting tests setup")
        
        cls.connection = cls.create_connection()
        cls.create_schema()
        
    @classmethod
    def tearDownClass(cls):
        cls.logger.info("Cleaning up after tests")
        cls.drop_schema()
        cls.connection.close()
        
    @classmethod
    def create_connection(cls):
        cls.logger.info("Creating database connection")
        return psycopg2.connect(
            dbname=cls.DB_NAME,
            user=cls.DB_USER,
            password=cls.DB_PASSWORD,
            host=cls.DB_HOST,
            port=cls.DB_PORT
        )
        
    @classmethod
    def create_schema(cls):
        cls.logger.info("Creating database schema")
        try:
            with open('tests/test_data/schema.sql', 'r') as f:
                schema_sql = f.read()
            with cls.connection.cursor() as cursor:
                cursor.execute(schema_sql)
            cls.connection.commit()
        except Exception as e:
            cls.logger.error(f"Failed to create schema: {str(e)}")
            raise
            
    @classmethod
    def drop_schema(cls):
        cls.logger.info("Dropping database schema")
        try:
            with cls.connection.cursor() as cursor:
                cursor.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
            cls.connection.commit()
        except Exception as e:
            cls.logger.error(f"Failed to drop schema: {str(e)}")
            raise
            
    @contextmanager
    def transaction(self):
        with self.connection.cursor() as cursor:
            try:
                yield cursor
                self.connection.commit()
            except Exception as e:
                self.connection.rollback()
                self.logger.error(f"Transaction failed: {str(e)}")
                raise

    def log_test_start(self):
        self.logger.info(f"Starting test: {self._testMethodName}")

    def log_test_end(self):
        self.logger.info(f"Finished test: {self._testMethodName}")
