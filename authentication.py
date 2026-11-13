
import sqlite3
import hashlib
import secrets
import hmac
import re

from database import get_connection



# PASSWORD SECURITY SETTINGS
HASH_ITERATIONS = 600_000


# 1. HASH PASSWORD
def hash_password(password):

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        HASH_ITERATIONS
    )

    # Store salt and hash together
    return salt.hex() + "$" + password_hash.hex()


# 2. VERIFY PASSWORD
def verify_password(password, stored_hash):

    try:
        salt_hex, original_hash = stored_hash.split("$")

        salt = bytes.fromhex(salt_hex)

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            HASH_ITERATIONS
        ).hex()

        return hmac.compare_digest(new_hash, original_hash)

    except (ValueError, TypeError):
        return False


# 3. REGISTER NEW USER
def register_user():

    print("\n========== USER REGISTRATION ==========")

    username = input("Enter Username: ").strip()
    email = input("Enter Email: ").strip().lower()
    password = input("Enter Password: ")

    # Validate username
    if len(username) < 3:
        print("Username must contain at least 3 characters!")
        return False

    # Validate email
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(email_pattern, email):
        print("Please enter a valid email address!")
        return False

    # Validate password
    if len(password) < 8:
        print("Password must contain at least 8 characters!")
        return False

    # Hash password
    secured_password = hash_password(password)

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        """, (username, email, secured_password))

        connection.commit()

        print("\nRegistration successful!")
        print("You can now log in.")

        return True

    except sqlite3.IntegrityError:

        print("Username or email already exists!")
        return False

    except sqlite3.Error as error:

        print("Registration error:", error)
        return False

    finally:

        connection.close()


# 4. USER LOGIN
def login_user():

    print("\n========== USER LOGIN ==========")

    username = input("Enter Username: ").strip()
    password = input("Enter Password: ")

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT user_id, username, email, password_hash
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        if user is None:
            print("\nInvalid username or password!")
            return None

        if verify_password(password, user["password_hash"]):

            print("\nLogin successful!")
            print("Welcome,", user["username"])

            # Do not return the password hash
            return {
                "user_id": user["user_id"],
                "username": user["username"],
                "email": user["email"]
            }

        print("\nInvalid username or password!")
        return None

    except sqlite3.Error as error:

        print("Login error:", error)
        return None

    finally:

        connection.close()


# 5. USER LOGOUT
def logout_user():

    print("\nYou have logged out successfully!")
