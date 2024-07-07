import os
import sys
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

# Ensure the my_authentication_app directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from my_authentication_app.database import Base
from my_authentication_app.model.user import User
from my_authentication_app.model.organization import Organization
from my_authentication_app.model.organization_member import OrganizationMember

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata

# Get the database URL from the environment variable
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("No DATABASE_URL set for SQLAlchemy engine")

# Ensure the URL uses the correct dialect
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

config.set_main_option('sqlalchemy.url', database_url)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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
