"""
Seed or reset CRM admin users and default tenants.
Compatible with PostgreSQL and SQLite.
"""
import hashlib
from datetime import datetime, timezone
import bcrypt
from sqlalchemy import text
from sqlmodel import Session, select

from database import User, Tenant, engine, create_db_and_tables


def _hash_password_sha256(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def _hash_password_bcrypt(pw: str) -> str:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


USERS_TO_SEED = [
    {
        "name": "System Admin",
        "email": "admin@example.com",
        "password": "Admin@123",
        "role": "Admin",
        "tenant_id": 1,
    },
    {
        "name": "Serphawk Admin",
        "email": "admin@serphawk.com",
        "password": "Admin123!",
        "role": "Admin",
        "tenant_id": 1,
    },
    {
        "name": "Super Admin",
        "email": "superadmin@serphawk.in",
        "password": "password123",
        "role": "SuperAdmin",
        "tenant_id": None,
    },
    {
        "name": "Demo User",
        "email": "demo@serphawk.com",
        "password": "DemoPass123!",
        "role": "Demo",
        "tenant_id": 1,
    },
]


def seed_admin():
    create_db_and_tables()
    now = datetime.now(timezone.utc)

    with Session(engine) as session:
        # Ensure Default Tenant exists
        tenant = session.get(Tenant, 1)
        if not tenant:
            tenant = Tenant(id=1, name="Default Tenant", created_at=now, is_active=True)
            session.add(tenant)
            session.commit()
            print("[Seed] Default Tenant (id=1) created.")
        else:
            print("[Seed] Default Tenant (id=1) already exists.")

        for user_data in USERS_TO_SEED:
            email = user_data["email"]
            pw = user_data["password"]
            role = user_data["role"]
            name = user_data["name"]
            tenant_id = user_data["tenant_id"]

            sha = _hash_password_sha256(pw)
            bcrypt_hash = _hash_password_bcrypt(pw)

            existing = session.exec(select(User).where(User.email == email)).first()
            if existing:
                existing.password = sha
                existing.hashed_password = bcrypt_hash
                existing.name = name
                existing.role = role
                existing.tenant_id = tenant_id
                existing.is_active = True
                existing.status = "APPROVED"
                session.add(existing)
                session.commit()
                print(f"[Seed] Updated user {email} (role: {role}).")
            else:
                user = User(
                    name=name,
                    email=email,
                    role=role,
                    is_active=True,
                    hashed_password=bcrypt_hash,
                    password=sha,
                    status="APPROVED",
                    tenant_id=tenant_id,
                    createdAt=now,
                    updatedAt=now,
                )
                session.add(user)
                session.commit()
                print(f"[Seed] Created user {email} (role: {role}).")

    print("\n--- Seeded Accounts ---")
    for u in USERS_TO_SEED:
        print(f"Role: {u['role']:<12} | Email: {u['email']:<25} | Password: {u['password']}")


if __name__ == "__main__":
    seed_admin()
