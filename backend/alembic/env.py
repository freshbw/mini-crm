from logging.config import fileConfig

from alembic import context
from sqlalchemy import URL, engine_from_config, pool

from app.config.settings import get_settings
from app.db.models.base import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

settings = get_settings()
pg = settings.postgres

sync_url = URL.create(
    drivername="postgresql+psycopg",  # sync; app использует asyncpg
    username=pg.user,
    password=pg.password.get_secret_value(),
    host=pg.host,
    port=pg.port,
    database=pg.db,
)

config.set_main_option(
    "sqlalchemy.url",
    sync_url.render_as_string(hide_password=False).replace("%", "%%"),
)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
