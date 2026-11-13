
import sqlite3
import os

# Database file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

DB_PATH = os.path.join(DATA_DIR, "expense_tracker.db")


# 1. CREATE DATABASE CONNECTION
def get_connection():

    os.makedirs(DATA_DIR, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    # Return rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    # Enable foreign key support
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# 2. CREATE DATABASE TABLES
def initialize_database():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # USERS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (

                user_id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT NOT NULL UNIQUE,

                email TEXT NOT NULL UNIQUE,

                password_hash TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        # TRANSACTIONS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (

                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                transaction_type TEXT NOT NULL
                    CHECK(transaction_type IN ('Income', 'Expense')),

                amount REAL NOT NULL
                    CHECK(amount > 0),

                category TEXT NOT NULL,

                description TEXT DEFAULT '',

                transaction_date TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE

            )
        """)

        # INDEX FOR FASTER TRANSACTION SEARCH
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_user_date
            ON transactions(user_id, transaction_date)
        """)

        connection.commit()

        print("Database initialized successfully!")
        print("Users and Transactions tables are ready.")

    except sqlite3.Error as error:

        connection.rollback()

        print("Database initialization error:", error)

    finally:

        connection.close()


# 3. TEST DATABASE CONNECTION
if __name__ == "__main__":

    initialize_database()

    print("\nDatabase location:")
    print(DB_PATH)
