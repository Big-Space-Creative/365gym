import os
import subprocess
import sys
import tempfile
from pathlib import Path

import environ
from django.db.utils import load_backend

BASE_DIR = Path(__file__).resolve().parent.parent


def test_missing_secret_key_raises_error():
    """Comprova que sem SECRET_KEY a aplicação falha de forma explícita (ImproperlyConfigured)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_gym = Path(tmpdir) / "gym365"
        tmp_gym.mkdir()
        for py_file in (BASE_DIR / "gym365").glob("*.py"):
            (tmp_gym / py_file.name).write_bytes(py_file.read_bytes())

        # Executa import do settings sem nenhum .env e sem SECRET_KEY no os.environ
        clean_env = {
            "PATH": os.environ.get("PATH", ""),
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
        }
        proc = subprocess.run(
            [sys.executable, "-c", "import gym365.settings"],
            capture_output=True,
            text=True,
            cwd=tmpdir,
            env=clean_env,
        )
        assert proc.returncode != 0
        assert "ImproperlyConfigured" in proc.stderr
        assert "SECRET_KEY" in proc.stderr


def test_debug_is_false_by_default():
    """Comprova que DEBUG é falso por padrão quando não especificado."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_gym = Path(tmpdir) / "gym365"
        tmp_gym.mkdir()
        for py_file in (BASE_DIR / "gym365").glob("*.py"):
            (tmp_gym / py_file.name).write_bytes(py_file.read_bytes())

        env_file = Path(tmpdir) / ".env"
        env_file.write_text("SECRET_KEY=dummy-secret-key-for-test\n", encoding="utf-8")

        clean_env = {
            "PATH": os.environ.get("PATH", ""),
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
        }
        proc = subprocess.run(
            [
                sys.executable,
                "-c",
                "import gym365.settings as s; print(f'DEBUG={s.DEBUG}')",
            ],
            capture_output=True,
            text=True,
            cwd=tmpdir,
            env=clean_env,
            check=True,
        )
        assert "DEBUG=False" in proc.stdout


def test_debug_can_be_set_to_true_via_env():
    """Comprova que DEBUG pode ser ativado via .env ou ambiente."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_gym = Path(tmpdir) / "gym365"
        tmp_gym.mkdir()
        for py_file in (BASE_DIR / "gym365").glob("*.py"):
            (tmp_gym / py_file.name).write_bytes(py_file.read_bytes())

        env_file = Path(tmpdir) / ".env"
        env_file.write_text("SECRET_KEY=dummy-key\nDEBUG=True\n", encoding="utf-8")

        clean_env = {
            "PATH": os.environ.get("PATH", ""),
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
        }
        proc = subprocess.run(
            [
                sys.executable,
                "-c",
                "import gym365.settings as s; print(f'DEBUG={s.DEBUG}')",
            ],
            capture_output=True,
            text=True,
            cwd=tmpdir,
            env=clean_env,
            check=True,
        )
        assert "DEBUG=True" in proc.stdout


def test_database_url_sqlite_and_postgres():
    """Comprova que DATABASE_URL configura SQLite por padrão e PostgreSQL quando informado."""
    env = environ.Env()

    # SQLite padrão
    sqlite_conf = env.db_url_config("sqlite:///db.sqlite3")
    assert sqlite_conf["ENGINE"] == "django.db.backends.sqlite3"
    assert sqlite_conf["NAME"] == "db.sqlite3"

    # PostgreSQL via DATABASE_URL
    pg_url = "postgres://postgres_user:secret_pass@localhost:5432/gym365_db"
    pg_conf = env.db_url_config(pg_url)
    assert pg_conf["ENGINE"] == "django.db.backends.postgresql"
    assert pg_conf["NAME"] == "gym365_db"
    assert pg_conf["USER"] == "postgres_user"
    assert pg_conf["PASSWORD"] == "secret_pass"
    assert pg_conf["HOST"] == "localhost"
    assert pg_conf["PORT"] == 5432

    # Verifica se o backend PostgreSQL do Django carrega com sucesso
    backend = load_backend(pg_conf["ENGINE"])
    assert backend.__name__ == "django.db.backends.postgresql.base"


def test_environment_variables_configured_via_env():
    """Comprova que TIME_ZONE, LANGUAGE_CODE e ALLOWED_HOSTS vêm do ambiente."""
    env = environ.Env(
        ALLOWED_HOSTS=(list, ["127.0.0.1", "localhost"]),
    )
    # ALLOWED_HOSTS
    parsed_hosts = env("ALLOWED_HOSTS")
    assert "127.0.0.1" in parsed_hosts

    # TIME_ZONE e LANGUAGE_CODE
    assert env("TIME_ZONE", default="America/Fortaleza") == "America/Fortaleza"
    assert env("LANGUAGE_CODE", default="pt-br") == "pt-br"
