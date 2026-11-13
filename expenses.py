
import sqlite3
from datetime import date

from database import get_connection


# AVAILABLE EXPENSE CATEGORIES
EXPENSE_CATEGORIES = [
    "Food",
    "Travel",
    "Education",
    "Shopping",
    "Entertainment",
    "Bills",
    "Health",
    "Other"
]


# HELPER FUNCTION: DISPLAY CATEGORIES
def display_categories():

    print("\nAvailable Expense Categories:")

    for index, category in enumerate(EXPENSE_CATEGORIES, start=1):
        print(f"{index}. {category}")


# HELPER FUNCTION: GET VALID CATEGORY
def get_category():

    display_categories()

    try:
        choice = int(input("Select category number: "))

        if 1 <= choice <= len(EXPENSE_CATEGORIES):
            return EXPENSE_CATEGORIES[choice - 1]

        print("Invalid category selection!")
        return None

    except ValueError:
        print("Please enter a valid category number!")
        return None


# HELPER FUNCTION: VALIDATE DATE
def get_valid_date():

    transaction_date = input(
        "Enter date (YYYY-MM-DD) or press Enter for today: "
    ).strip()

    if not transaction_date:
        return date.today().isoformat()

    try:
        return date.fromisoformat(transaction_date).isoformat()

    except ValueError:
        print("Invalid date! Use YYYY-MM-DD format.")
        return None


# 1. ADD EXPENSE
def add_expense(user_id):

    print("\n========== ADD EXPENSE ==========")

    try:

        amount = float(input("Enter expense amount: "))

        if amount <= 0:
            print("Expense amount must be greater than zero!")
            return

        category = get_category()

        if category is None:
            return

        description = input("Enter description: ").strip()

        transaction_date = get_valid_date()

        if transaction_date is None:
            return

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO transactions
                (
                    user_id,
                    transaction_type,
                    amount,
                    category,
                    description,
                    transaction_date
                )

                VALUES (?, 'Expense', ?, ?, ?, ?)

            """, (
                user_id,
                amount,
                category,
                description,
                transaction_date
            ))

            connection.commit()

            print("\nExpense added successfully!")

        finally:
            connection.close()

    except ValueError:
        print("Invalid amount! Please enter a numeric value.")

    except sqlite3.Error as error:
        print("Database error:", error)


# 2. VIEW ALL EXPENSES
def view_expenses(user_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM transactions
            WHERE user_id = ?
            AND transaction_type = 'Expense'
            ORDER BY transaction_date DESC
        """, (user_id,))

        records = cursor.fetchall()

        print("\n========== EXPENSE RECORDS ==========")

        if not records:
            print("No expense records found!")
            return

        print("-" * 85)

        print(
            f"{'ID':<8}"
            f"{'Amount':<12}"
            f"{'Category':<18}"
            f"{'Date':<15}"
            f"{'Description':<25}"
        )

        print("-" * 85)

        for record in records:

            print(
                f"{record['transaction_id']:<8}"
                f"{record['amount']:<12.2f}"
                f"{record['category']:<18}"
                f"{record['transaction_date']:<15}"
                f"{record['description']:<25}"
            )

        print("-" * 85)

    except sqlite3.Error as error:
        print("Database error:", error)

    finally:
        connection.close()


# 3. SEARCH EXPENSE
def search_expense(user_id):

    print("\n========== SEARCH EXPENSE ==========")

    try:

        transaction_id = int(
            input("Enter Expense Transaction ID: ")
        )

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM transactions
                WHERE transaction_id = ?
                AND user_id = ?
                AND transaction_type = 'Expense'
            """, (transaction_id, user_id))

            record = cursor.fetchone()

            if record:

                print("\nExpense Record Found!")
                print("-" * 35)

                print("Transaction ID:", record["transaction_id"])
                print("Amount:", record["amount"])
                print("Category:", record["category"])
                print("Description:", record["description"])
                print("Date:", record["transaction_date"])

                print("-" * 35)

            else:
                print("Expense record not found!")

        finally:
            connection.close()

    except ValueError:
        print("Please enter a valid transaction ID!")

    except sqlite3.Error as error:
        print("Database error:", error)


# 4. UPDATE EXPENSE
def update_expense(user_id):

    print("\n========== UPDATE EXPENSE ==========")

    try:

        transaction_id = int(
            input("Enter Expense Transaction ID: ")
        )

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM transactions
                WHERE transaction_id = ?
                AND user_id = ?
                AND transaction_type = 'Expense'
            """, (transaction_id, user_id))

            record = cursor.fetchone()

            if not record:
                print("Expense record not found!")
                return

            print("\nExpense Record Found!")
            print("Press Enter to keep the existing value.")

            new_amount = input(
                f"New amount [{record['amount']}]: "
            ).strip()

            new_category_choice = input(
                "Change category? (yes/no): "
            ).strip().lower()

            new_description = input(
                f"New description [{record['description']}]: "
            ).strip()

            new_date = input(
                f"New date [{record['transaction_date']}]: "
            ).strip()

            # Validate amount
            amount = (
                float(new_amount)
                if new_amount
                else record["amount"]
            )

            if amount <= 0:
                print("Amount must be greater than zero!")
                return

            # Validate category
            category = record["category"]

            if new_category_choice == "yes":

                selected_category = get_category()

                if selected_category is None:
                    return

                category = selected_category

            elif new_category_choice not in ("yes", "no", ""):

                print("Please enter yes or no!")
                return

            description = (
                new_description
                if new_description
                else record["description"]
            )

            # Validate date
            transaction_date = (
                date.fromisoformat(new_date).isoformat()
                if new_date
                else record["transaction_date"]
            )

            cursor.execute("""
                UPDATE transactions

                SET amount = ?,
                    category = ?,
                    description = ?,
                    transaction_date = ?

                WHERE transaction_id = ?
                AND user_id = ?
                AND transaction_type = 'Expense'

            """, (
                amount,
                category,
                description,
                transaction_date,
                transaction_id,
                user_id
            ))

            connection.commit()

            print("\nExpense updated successfully!")

        finally:
            connection.close()

    except ValueError:
        print("Invalid amount, transaction ID or date!")

    except sqlite3.Error as error:
        print("Database error:", error)


# 5. DELETE EXPENSE
def delete_expense(user_id):

    print("\n========== DELETE EXPENSE ==========")

    try:

        transaction_id = int(
            input("Enter Expense Transaction ID: ")
        )

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM transactions
                WHERE transaction_id = ?
                AND user_id = ?
                AND transaction_type = 'Expense'
            """, (transaction_id, user_id))

            record = cursor.fetchone()

            if not record:
                print("Expense record not found!")
                return

            print("\nExpense Record Found!")

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
                    AND transaction_type = 'Expense'
                """, (transaction_id, user_id))

                connection.commit()

                print("\nExpense deleted successfully!")

            else:
                print("Deletion cancelled!")

        finally:
            connection.close()

    except ValueError:
        print("Please enter a valid transaction ID!")

    except sqlite3.Error as error:
        print("Database error:", error)


# 6. CALCULATE TOTAL EXPENSES
def total_expenses(user_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT SUM(amount) AS total
            FROM transactions
            WHERE user_id = ?
            AND transaction_type = 'Expense'
        """, (user_id,))

        result = cursor.fetchone()

        total = result["total"] or 0

        print("\n========== TOTAL EXPENSES ==========")
        print("Total Expenses: Rs.", round(total, 2))

        return total

    except sqlite3.Error as error:
        print("Database error:", error)
        return 0

    finally:
        connection.close()


# 7. CATEGORY-WISE EXPENSE SUMMARY
def category_wise_expenses(user_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT category, SUM(amount) AS total
            FROM transactions
            WHERE user_id = ?
            AND transaction_type = 'Expense'
            GROUP BY category
            ORDER BY total DESC
        """, (user_id,))

        records = cursor.fetchall()

        print("\n========== CATEGORY-WISE EXPENSES ==========")

        if not records:
            print("No expense records found!")
            return

        print("-" * 45)

        for record in records:

            print(
                f"{record['category']:<20}"
                f"Rs. {record['total']:.2f}"
            )

        print("-" * 45)

    except sqlite3.Error as error:
        print("Database error:", error)

    finally:
        connection.close()
