from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "ranks" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "email" VARCHAR(100) NOT NULL UNIQUE DEFAULT 'default@example.com',
    "name" VARCHAR(50) NOT NULL,
    "surname" VARCHAR(50) NOT NULL,
    "thirdname" VARCHAR(50),
    "unit" VARCHAR(50) NOT NULL,
    "is_admin" BOOL NOT NULL  DEFAULT False,
    "rank_id" INT NOT NULL REFERENCES "ranks" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "orders" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "number_order" VARCHAR(10) NOT NULL UNIQUE,
    "technics" JSONB NOT NULL,
    "total_cost" DECIMAL(10,2) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT False,
    "time_of_execution" TIMESTAMPTZ NOT NULL,
    "customer_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
