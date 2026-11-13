
import sqlite3
from datetime import date

from database import get_connection


# 1. ADD INCOME
def add_income(user_id):

    print("\n========== ADD INCOME ==========")

    try:

        amount = float(input("Enter income amount: "))

        if amount <= 0:
            print("Amount must be greater than zero!")
            return

        category = input("Enter income category: ").strip()

        if not category:
            print("Category cannot be empty!")
            return

        description = input("Enter description: ").strip()

        transaction_date = input(
            "Enter date (YYYY-MM-DD) or press Enter for today: "
        ).strip()

        if not transaction_date:
            transaction_date = date.today().isoformat()

        # Validate date
        date.fromisoformat(transaction_date)

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO transactions
            (user_id, transaction_type, amount, category,
             description, transaction_date)

            VALUES (?, 'Income', ?, ?, ?, ?)
        """, (
            user_id,
            amount,
            category,
            description,
            transaction_date
        ))

        connection.commit()
        connection.close()

        print("\nIncome added successfully!")

    except ValueError:
        print("Invalid amount or date format!")

    except sqlite3.Error as error:
        print("Database error:", error)


# 2. VIEW ALL INCOME
def view_income(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM transactions
        WHERE user_id = ? AND transaction_type = 'Income'
        ORDER BY transaction_date DESC
    """, (user_id,))

    records = cursor.fetchall()

    connection.close()

    print("\n========== INCOME RECORDS ==========")

    if not records:
        print("No income records found!")
        return

    print("-" * 75)

    print(
        f"{'ID':<8}{'Amount':<12}{'Category':<18}"
        f"{'Date':<15}{'Description':<20}"
    )

    print("-" * 75)

    for record in records:

        print(
            f"{record['transaction_id']:<8}"
            f"{record['amount']:<12.2f}"
            f"{record['category']:<18}"
            f"{record['transaction_date']:<15}"
            f"{record['description']:<20}"
        )

    print("-" * 75)


# 3. SEARCH INCOME
def search_income(user_id):

    print("\n========== SEARCH INCOME ==========")

    try:

        transaction_id = int(
            input("Enter Income Transaction ID: ")
        )

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM transactions
            WHERE transaction_id = ?
            AND user_id = ?
            AND transaction_type = 'Income'
        """, (transaction_id, user_id))

        record = cursor.fetchone()

        connection.close()

        if record:

            print("\nIncome Record Found!")

            print("Transaction ID:", record["transaction_id"])
            print("Amount:", record["amount"])
            print("Category:", record["category"])
            print("Description:", record["description"])
            print("Date:", record["transaction_date"])

        else:

            print("Income record not found!")

    except ValueError:
        print("Please enter a valid transaction ID!")


# 4. UPDATE INCOME
def update_income(user_id):

    print("\n========== UPDATE INCOME ==========")

    try:

        transaction_id = int(
            input("Enter Transaction ID: ")
        )

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM transactions
            WHERE transaction_id = ?
            AND user_id = ?
            AND transaction_type = 'Income'
        """, (transaction_id, user_id))

        record = cursor.fetchone()

        if not record:

            print("Income record not found!")
            connection.close()
            return

        print("Press Enter to keep the existing value.")

        new_amount = input(
            f"New amount [{record['amount']}]: "
        ).strip()

        new_category = input(
            f"New category [{record['category']}]: "
        ).strip()

        new_description = input(
            f"New description [{record['description']}]: "
        ).strip()

        new_date = input(
            f"New date [{record['transaction_date']}]: "
        ).strip()

        amount = (
            float(new_amount) if new_amount else record["amount"]
        )

        if amount <= 0:
            print("Amount must be greater than zero!")
            connection.close()
            return

        category = new_category or record["category"]

        description = (
            new_description or record["description"]
        )

        transaction_date = new_date or record["transaction_date"]

        date.fromisoformat(transaction_date)

        cursor.execute("""
            UPDATE transactions

            SET amount = ?,
                category = ?,
                description = ?,
                transaction_date = ?

            WHERE transaction_id = ?
            AND user_id = ?
            AND transaction_type = 'Income'
        """, (
            amount,
            category,
            description,
            transaction_date,
            transaction_id,
            user_id
        ))

        connection.commit()
        connection.close()

        print("\nIncome updated successfully!")

    except ValueError:
        print("Invalid amount or date format!")

    except sqlite3.Error as error:
        print("Database error:", error)


# 5. DELETE INCOME
def delete_income(user_id):

    print("\n========== DELETE INCOME ==========")

    try:

        transaction_id = int(
            input("Enter Transaction ID: ")
        )

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM transactions
            WHERE transaction_id = ?
            AND user_id = ?
            AND transaction_type = 'Income'
        """, (transaction_id, user_id))

        record = cursor.fetchone()

        if not record:

            print("Income record not found!")
            connection.close()
            return

        print("Amount:", record["amount"])
        print("Category:", record["category"])

        confirm = input(
            "Confirm deletion? (yes/no): "
        ).strip().lower()

        if confirm == "yes":

            cursor.execute("""
                DELETE FROM transactions
                WHERE transaction_id = ?
                AND user_id = ?
                AND transaction_type = 'Income'
            """, (transaction_id, user_id))

            connection.commit()

            print("Income deleted successfully!")

        else:

            print("Deletion cancelled!")

        connection.close()

    except ValueError:
        print("Please enter a valid transaction ID!")

    except sqlite3.Error as error:
        print("Database error:", error)


# 6. TOTAL INCOME
def total_income(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount) AS total
        FROM transactions
        WHERE user_id = ?
        AND transaction_type = 'Income'
    """, (user_id,))

    result = cursor.fetchone()

    connection.close()

    total = result["total"] or 0

    print("\nTotal Income: Rs.", round(total, 2))

    return total
