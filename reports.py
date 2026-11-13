
import sqlite3
from datetime import datetime

from database import get_connection


# HELPER FUNCTION: GET FINANCIAL TOTALS
def get_financial_totals(user_id, start_date, end_date):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                transaction_type,
                SUM(amount) AS total

            FROM transactions

            WHERE user_id = ?
            AND transaction_date >= ?
            AND transaction_date < ?

            GROUP BY transaction_type

        """, (user_id, start_date, end_date))

        records = cursor.fetchall()

        totals = {
            "Income": 0.0,
            "Expense": 0.0
        }

        for record in records:

            totals[record["transaction_type"]] = (
                record["total"] or 0.0
            )

        return totals

    except sqlite3.Error as error:

        print("Database error:", error)

        return None

    finally:

        connection.close()


# 1. MONTHLY FINANCIAL REPORT
def monthly_report(user_id):

    print("\n========== MONTHLY FINANCIAL REPORT ==========")

    try:

        year = int(input("Enter year (YYYY): "))
        month = int(input("Enter month (1-12): "))

        if year < 1 or year > 9999:
            print("Invalid year!")
            return

        if month < 1 or month > 12:
            print("Invalid month!")
            return

        # Create date boundaries
        start_date = f"{year:04d}-{month:02d}-01"

        if month == 12:
            end_date = f"{year + 1:04d}-01-01"
        else:
            end_date = f"{year:04d}-{month + 1:02d}-01"

        totals = get_financial_totals(
            user_id,
            start_date,
            end_date
        )

        if totals is None:
            return

        income = totals["Income"]
        expenses = totals["Expense"]

        savings = income - expenses

        print("\n===================================")
        print(f"MONTHLY REPORT: {month:02d}/{year}")
        print("===================================")

        print(f"Total Income   : Rs. {income:.2f}")
        print(f"Total Expenses : Rs. {expenses:.2f}")
        print("-----------------------------------")
        print(f"Net Savings    : Rs. {savings:.2f}")

        if savings > 0:
            print("Financial Status: Positive Savings")

        elif savings < 0:
            print("Financial Status: Expenses Exceed Income")

        else:
            print("Financial Status: Break Even")

        print("===================================")

    except ValueError:
        print("Please enter valid numeric year and month!")


# 2. YEARLY FINANCIAL REPORT
def yearly_report(user_id):

    print("\n========== YEARLY FINANCIAL REPORT ==========")

    try:

        year = int(input("Enter year (YYYY): "))

        if year < 1 or year > 9999:
            print("Invalid year!")
            return

        start_date = f"{year:04d}-01-01"
        end_date = f"{year + 1:04d}-01-01"

        totals = get_financial_totals(
            user_id,
            start_date,
            end_date
        )

        if totals is None:
            return

        income = totals["Income"]
        expenses = totals["Expense"]

        savings = income - expenses

        print("\n===================================")
        print(f"YEARLY FINANCIAL REPORT: {year}")
        print("===================================")

        print(f"Total Income   : Rs. {income:.2f}")
        print(f"Total Expenses : Rs. {expenses:.2f}")
        print("-----------------------------------")
        print(f"Net Savings    : Rs. {savings:.2f}")

        if savings > 0:
            print("Financial Status: Positive Savings")

        elif savings < 0:
            print("Financial Status: Expenses Exceed Income")

        else:
            print("Financial Status: Break Even")

        print("===================================")

    except ValueError:
        print("Please enter a valid year!")


# 3. MONTHLY INCOME AND EXPENSE COMPARISON
def monthly_comparison(user_id):

    print("\n========== MONTHLY COMPARISON ==========")

    try:

        year = int(input("Enter year (YYYY): "))

        if year < 1 or year > 9999:
            print("Invalid year!")
            return

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    CAST(
                        strftime('%m', transaction_date)
                        AS INTEGER
                    ) AS month,

                    transaction_type,

                    SUM(amount) AS total

                FROM transactions

                WHERE user_id = ?
                AND transaction_date >= ?
                AND transaction_date < ?

                GROUP BY month, transaction_type

                ORDER BY month

            """, (
                user_id,
                f"{year:04d}-01-01",
                f"{year + 1:04d}-01-01"
            ))

            records = cursor.fetchall()

        finally:
            connection.close()

        # Prepare all 12 months
        monthly_data = {}

        for month in range(1, 13):

            monthly_data[month] = {
                "Income": 0.0,
                "Expense": 0.0
            }

        # Fill actual database values
        for record in records:

            month = record["month"]

            if month is not None and 1 <= month <= 12:

                monthly_data[month][
                    record["transaction_type"]
                ] = record["total"] or 0.0

        print("\nMONTHLY FINANCIAL COMPARISON")
        print("=" * 65)

        print(
            f"{'Month':<15}"
            f"{'Income':<16}"
            f"{'Expenses':<16}"
            f"{'Savings':<16}"
        )

        print("=" * 65)

        total_income = 0.0
        total_expenses = 0.0

        for month in range(1, 13):

            income = monthly_data[month]["Income"]
            expenses = monthly_data[month]["Expense"]

            savings = income - expenses

            total_income += income
            total_expenses += expenses

            month_name = datetime(
                year, month, 1
            ).strftime("%B")

            print(
                f"{month_name:<15}"
                f"{income:<16.2f}"
                f"{expenses:<16.2f}"
                f"{savings:<16.2f}"
            )

        print("=" * 65)

        print(
            f"{'TOTAL':<15}"
            f"{total_income:<16.2f}"
            f"{total_expenses:<16.2f}"
            f"{total_income - total_expenses:<16.2f}"
        )

        print("=" * 65)

    except ValueError:
        print("Please enter a valid year!")

    except sqlite3.Error as error:
        print("Database error:", error)


# 4. OVERALL FINANCIAL SUMMARY
def overall_summary(user_id):

    print("\n========== OVERALL FINANCIAL SUMMARY ==========")

    totals = get_financial_totals(
        user_id,
        "0001-01-01",
        "10000-01-01"
    )

    if totals is None:
        return

    income = totals["Income"]
    expenses = totals["Expense"]

    savings = income - expenses

    print("\nTotal Income   : Rs.", round(income, 2))
    print("Total Expenses : Rs.", round(expenses, 2))
    print("Net Savings    : Rs.", round(savings, 2))

    if savings > 0:
        print("Status: Positive Savings")

    elif savings < 0:
        print("Status: Expenses Exceed Income")

    else:
        print("Status: Break Even")
