
from database import initialize_database

from authentication import register_user, login_user, logout_user

from income import (
    add_income,
    view_income,
    search_income,
    update_income,
    delete_income,
    total_income
)

from expenses import (
    add_expense,
    view_expenses,
    search_expense,
    update_expense,
    delete_expense,
    total_expenses,
    category_wise_expenses
)

from reports import (
    monthly_report,
    yearly_report,
    monthly_comparison,
    overall_summary
)

from analytics import analytics_menu


def income_menu(user_id):
    while True:
        print("\n========== INCOME MANAGEMENT ==========")
        print("1. Add Income")
        print("2. View Income")
        print("3. Search Income")
        print("4. Update Income")
        print("5. Delete Income")
        print("6. View Total Income")
        print("7. Back to Dashboard")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_income(user_id)
        elif choice == "2":
            view_income(user_id)
        elif choice == "3":
            search_income(user_id)
        elif choice == "4":
            update_income(user_id)
        elif choice == "5":
            delete_income(user_id)
        elif choice == "6":
            total_income(user_id)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")


def expense_menu(user_id):
    while True:
        print("\n========== EXPENSE MANAGEMENT ==========")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Search Expense")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. View Total Expenses")
        print("7. Category-wise Expense Summary")
        print("8. Back to Dashboard")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense(user_id)
        elif choice == "2":
            view_expenses(user_id)
        elif choice == "3":
            search_expense(user_id)
        elif choice == "4":
            update_expense(user_id)
        elif choice == "5":
            delete_expense(user_id)
        elif choice == "6":
            total_expenses(user_id)
        elif choice == "7":
            category_wise_expenses(user_id)
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")


def reports_menu(user_id):
    while True:
        print("\n========== FINANCIAL REPORTS ==========")
        print("1. Monthly Financial Report")
        print("2. Yearly Financial Report")
        print("3. Monthly Comparison")
        print("4. Overall Financial Summary")
        print("5. Back to Dashboard")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            monthly_report(user_id)
        elif choice == "2":
            yearly_report(user_id)
        elif choice == "3":
            monthly_comparison(user_id)
        elif choice == "4":
            overall_summary(user_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def user_dashboard(user):
    user_id = user["user_id"]
    username = user["username"]

    while True:
        print("\n========================================")
        print(f"       WELCOME, {username.upper()}!")
        print("       COGNEVANCE EXPENSE TRACKER")
        print("========================================")
        print("1. Income Management")
        print("2. Expense Management")
        print("3. Financial Reports")
        print("4. Financial Analytics & Charts")
        print("5. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            income_menu(user_id)
        elif choice == "2":
            expense_menu(user_id)
        elif choice == "3":
            reports_menu(user_id)
        elif choice == "4":
            analytics_menu(user_id)
        elif choice == "5":
            logout_user()
            print("You have been logged out.")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    # Create the database and required tables if they do not exist.
    initialize_database()

    while True:
        print("\n========================================")
        print("       COGNEVANCE EXPENSE TRACKER")
        print("========================================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()

        elif choice == "2":
            user = login_user()

            if user:
                print(f"\nLogin successful. Welcome, {user['username']}!")
                user_dashboard(user)
            else:
                print("\nLogin failed. Please check your credentials.")

        elif choice == "3":
            print("\nThank you for using Cognevance Expense Tracker!")
            print("Exiting application...")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
