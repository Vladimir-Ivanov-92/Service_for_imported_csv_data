"""File with settings and configs for the project"""

from envparse import Env

env = Env()

# connect for the database
REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres_user:postgres_password@0.0.0:5433/postgres_db"
)

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://postgres_user_test:postgres_password_test@0.0.0:5434/postgres_db_test"
)
