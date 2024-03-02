from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {"default": "postgres://postgres:123123@localhost:5432/monitoring"},
    "apps": {
        "models": {
            "models": ["models.app_models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db() -> None:
    await Tortoise.init(config=TORTOISE_ORM)

    await Tortoise.generate_schemas()
