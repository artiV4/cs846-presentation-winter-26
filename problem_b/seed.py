"""
Seed users for local development/testing.
"""

from argon2 import PasswordHasher

from database import get_db_connection, init_db

SEED_USERS = [
    {
        "email": "admin@example.com",
        "password": "admin-pass-123",
        "full_name": "Admin User",
        "role": "admin",
    },
    {
        "email": "support@example.com",
        "password": "support-pass-123",
        "full_name": "Support User",
        "role": "support",
    },
    {
        "email": "user@example.com",
        "password": "user-pass-123",
        "full_name": "Regular User",
        "role": "user",
    },
]


def seed_users() -> int:
    init_db()
    hasher = PasswordHasher()
    conn = get_db_connection()
    inserted = 0
    try:
        existing_emails = {
            row["email"] for row in conn.execute("SELECT email FROM users").fetchall()
        }

        for user in SEED_USERS:
            if user["email"] in existing_emails:
                continue

            conn.execute(
                """
                INSERT INTO users (email, password_hash, full_name, role)
                VALUES (?, ?, ?, ?)
                """,
                (
                    user["email"],
                    hasher.hash(user["password"]),
                    user["full_name"],
                    user["role"],
                ),
            )
            inserted += 1

        conn.commit()
        return inserted
    finally:
        conn.close()


if __name__ == "__main__":
    created = seed_users()
    print(f"Seed complete: {created} user(s) inserted.")
