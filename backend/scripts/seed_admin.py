"""Standalone CLI script to initialize or create an administrator account.

Usage:
    python -m scripts.seed_admin
    python -m scripts.seed_admin --email custom_admin@example.com --password StrongPassword123! --name "Lead Admin"
"""
import argparse
import asyncio
import sys
from app.core.database import init_db
from app.services.admin_seed_service import admin_seed_service
from app.core.config import settings


async def main():
    parser = argparse.ArgumentParser(description="Seed or initialize administrator account.")
    parser.add_argument("--email", default=settings.DEFAULT_ADMIN_EMAIL, help="Admin email address")
    parser.add_argument("--password", default=settings.DEFAULT_ADMIN_PASSWORD, help="Admin password")
    parser.add_argument("--name", default=settings.DEFAULT_ADMIN_NAME, help="Admin full name")

    args = parser.parse_args()

    print("[AdminSeeder] Initializing database schema...")
    await init_db()

    print(f"[AdminSeeder] Ensuring administrator account exists for: {args.email}...")
    seeded = await admin_seed_service.seed_initial_admin_if_empty(
        email=args.email,
        password=args.password,
        full_name=args.name,
    )

    if seeded:
        print("[AdminSeeder] SUCCESS: Administrator account created successfully.")
    else:
        print("[AdminSeeder] INFO: Administrator account already exists. No modifications made.")


if __name__ == "__main__":
    asyncio.run(main())
