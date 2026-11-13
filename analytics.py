
import sqlite3
import os
import calendar

import matplotlib.pyplot as plt

from database import get_connection


# CHART STORAGE DIRECTORY
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHART_DIR = os.path.join(BASE_DIR, "charts")

os.makedirs(CHART_DIR, exist_ok=True)


# HELPER FUNCTION: FETCH MONTHLY FINANCIAL DATA
def get_monthly_data(user_id, year):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                CAST(strftime('%m', transaction_date) AS INTEGER)
                    AS month,
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

        monthly_data = {
            month: {"Income": 0, "Expense": 0}
            for month in range(1, 13)
        }

        for record in records:

            month = record["month"]

            if month is not None and 1 <= month <= 12:

                monthly_data[month][
                    record["transaction_type"]
                ] = record["total"] or 0

        return monthly_data

    finally:
        connection.close()


# 1. MONTHLY INCOME VS EXPENSE CHART
def income_expense_chart(user_id):

    print("\n========== INCOME VS EXPENSE CHART ==========")

    try:

        year = int(input("Enter year (YYYY): "))

        if year < 1 or year > 9999:
            print("Invalid year!")
            return

        data = get_monthly_data(user_id, year)

        months = [
            calendar.month_abbr[month]
            for month in range(1, 13)
        ]

        income = [
            data[month]["Income"]
            for month in range(1, 13)
        ]

        expenses = [
            data[month]["Expense"]
            for month in range(1, 13)
        ]

        positions = list(range(12))
        width = 0.35

        plt.figure(figsize=(12, 6))

        plt.bar(
            [x - width / 2 for x in positions],
            income,
            width,
            label="Income"
        )

        plt.bar(
            [x + width / 2 for x in positions],
            expenses,
            width,
            label="Expenses"
        )

        plt.title(f"Monthly Income vs Expenses - {year}")
        plt.xlabel("Months")
        plt.ylabel("Amount (Rs.)")

        plt.xticks(positions, months)

        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.4)

        plt.tight_layout()

        file_path = os.path.join(
            CHART_DIR,
            f"income_expense_{year}.png"
        )

        plt.savefig(file_path, dpi=150)

        plt.show()
        plt.close()

        print("Chart saved:", file_path)

    except ValueError:
        print("Please enter a valid year!")

    except (sqlite3.Error, OSError) as error:
        print("Chart generation error:", error)


# 2. EXPENSE CATEGORY PIE CHART
def expense_category_chart(user_id):

    print("\n========== EXPENSE CATEGORY CHART ==========")

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

        if not records:

            print("No expense records available!")
            return

        categories = [
            record["category"]
            for record in records
        ]

        amounts = [
            record["total"]
            for record in records
        ]

        plt.figure(figsize=(9, 7))

        plt.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Expense Distribution by Category")
        plt.axis("equal")

        plt.tight_layout()

        file_path = os.path.join(
            CHART_DIR,
            "expense_category.png"
        )

        plt.savefig(file_path, dpi=150)

        plt.show()
        plt.close()

        print("Chart saved:", file_path)

    except (sqlite3.Error, OSError) as error:
        print("Chart generation error:", error)

    finally:
        connection.close()


# 3. MONTHLY SAVINGS TREND
def savings_trend_chart(user_id):

    print("\n========== SAVINGS TREND CHART ==========")

    try:

        year = int(input("Enter year (YYYY): "))

        if year < 1 or year > 9999:
            print("Invalid year!")
            return

        data = get_monthly_data(user_id, year)

        months = [
            calendar.month_abbr[month]
            for month in range(1, 13)
        ]

        savings = [
            data[month]["Income"] - data[month]["Expense"]
            for month in range(1, 13)
        ]

        plt.figure(figsize=(12, 6))

        plt.plot(
            months,
            savings,
            marker="o",
            linewidth=2,
            label="Monthly Savings"
        )

        plt.axhline(y=0, linestyle="--", alpha=0.6)

        plt.title(f"Monthly Savings Trend - {year}")
        plt.xlabel("Months")
        plt.ylabel("Savings (Rs.)")

        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.4)

        plt.tight_layout()

        file_path = os.path.join(
            CHART_DIR,
            f"savings_trend_{year}.png"
        )

        plt.savefig(file_path, dpi=150)

        plt.show()
        plt.close()

        print("Chart saved:", file_path)

    except ValueError:
        print("Please enter a valid year!")

    except (sqlite3.Error, OSError) as error:
        print("Chart generation error:", error)


# 4. YEARLY FINANCIAL COMPARISON
def yearly_comparison_chart(user_id):

    print("\n========== YEARLY COMPARISON CHART ==========")

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                CAST(strftime('%Y', transaction_date) AS INTEGER)
                    AS year,

                transaction_type,

                SUM(amount) AS total

            FROM transactions

            WHERE user_id = ?

            GROUP BY year, transaction_type

            ORDER BY year

        """, (user_id,))

        records = cursor.fetchall()

        if not records:

            print("No financial records available!")
            return

        yearly_data = {}

        for record in records:

            year = record["year"]

            if year is None:
                continue

            if year not in yearly_data:

                yearly_data[year] = {
                    "Income": 0,
                    "Expense": 0
                }

            yearly_data[year][
                record["transaction_type"]
            ] = record["total"] or 0

        if not yearly_data:

            print("No valid yearly data available!")
            return

        years = sorted(yearly_data.keys())

        income = [
            yearly_data[year]["Income"]
            for year in years
        ]

        expenses = [
            yearly_data[year]["Expense"]
            for year in years
        ]

        savings = [
            income[i] - expenses[i]
            for i in range(len(years))
        ]

        positions = list(range(len(years)))
        width = 0.25

        plt.figure(figsize=(11, 6))

        plt.bar(
            [x - width for x in positions],
            income,
            width,
            label="Income"
        )

        plt.bar(
            positions,
            expenses,
            width,
            label="Expenses"
        )

        plt.bar(
            [x + width for x in positions],
            savings,
            width,
            label="Savings"
        )

        plt.title("Yearly Financial Comparison")
        plt.xlabel("Year")
        plt.ylabel("Amount (Rs.)")

        plt.xticks(positions, years)

        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.4)

        plt.tight_layout()

        file_path = os.path.join(
            CHART_DIR,
            "yearly_comparison.png"
        )

        plt.savefig(file_path, dpi=150)

        plt.show()
        plt.close()

        print("Chart saved:", file_path)

    except (sqlite3.Error, OSError) as error:
        print("Chart generation error:", error)

    finally:
        connection.close()


# 5. MAIN ANALYTICS MENU
def analytics_menu(user_id):

    while True:

        print("\n========== FINANCIAL ANALYTICS ==========")

        print("1. Monthly Income vs Expenses Chart")
        print("2. Expense Category Pie Chart")
        print("3. Monthly Savings Trend")
        print("4. Yearly Financial Comparison")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            income_expense_chart(user_id)

        elif choice == "2":
            expense_category_chart(user_id)

        elif choice == "3":
            savings_trend_chart(user_id)

        elif choice == "4":
            yearly_comparison_chart(user_id)

        elif choice == "5":
            print("Exiting Financial Analytics...")
            break

        else:
            print("Invalid choice!")
