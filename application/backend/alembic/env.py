from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.core.config import settings
from app.core.database import Base
from app.models import Monitor


# Alembic Config object.
# This provides access to values inside alembic.ini.
config = context.config


# Use the DATABASE_URL from our UptimeHub application settings
# instead of hardcoding the database connection in alembic.ini.
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url.replace("%", "%%"),
)


# Configure Python logging using alembic.ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Tell Alembic which SQLAlchemy metadata contains our tables.
# This allows:
#
# alembic revision --autogenerate
#
# to detect our SQLAlchemy models.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.

    Alembic generates SQL without creating a live
    database connection.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in online mode.

    Alembic connects directly to PostgreSQL and
    applies the migrations to the database.
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
