
import sqlite3
import json

from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "test_cases.db"


def get_connection():

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def init_db():

    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS test_runs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                requirement TEXT NOT NULL,

                analysis_json TEXT NOT NULL,

                cases_json TEXT NOT NULL,

                case_count INTEGER NOT NULL,

                created_at TEXT NOT NULL
            )
        """)


def save_run(requirement, analysis, cases):

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO test_runs
            (
                requirement,
                analysis_json,
                cases_json,
                case_count,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                requirement,
                json.dumps(analysis, ensure_ascii=False),
                json.dumps(cases, ensure_ascii=False),
                len(cases),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        return cursor.lastrowid


def get_runs():

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT id, requirement, case_count, created_at
            FROM test_runs
            ORDER BY id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]


def get_run(run_id):

    with get_connection() as connection:

        row = connection.execute(
            "SELECT * FROM test_runs WHERE id = ?",
            (run_id,)
        ).fetchone()

        if row is None:
            return None

        result = dict(row)

        result["analysis"] = json.loads(
            result.pop("analysis_json")
        )

        result["cases"] = json.loads(
            result.pop("cases_json")
        )

        return result


def delete_run(run_id):

    with get_connection() as connection:

        connection.execute(
            "DELETE FROM test_runs WHERE id = ?",
            (run_id,)
        )
