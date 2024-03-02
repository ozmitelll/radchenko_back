from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "orders" ALTER COLUMN "technics" DROP NOT NULL;
        ALTER TABLE "orders" ALTER COLUMN "number_order" DROP NOT NULL;
        ALTER TABLE "orders" ALTER COLUMN "total_cost" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "orders" ALTER COLUMN "technics" SET NOT NULL;
        ALTER TABLE "orders" ALTER COLUMN "number_order" SET NOT NULL;
        ALTER TABLE "orders" ALTER COLUMN "total_cost" SET NOT NULL;"""
