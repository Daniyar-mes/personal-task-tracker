from db.database import get_db
from db.queries import (
    INSERT_TASK,
    GET_ALL_TASKS,
    MARK_TASK_DONE,
    DELETE_TASK,
    GET_TASK_STATS
)


def add_task(user_id: int, title: str):
    conn = get_db()
    try:
        conn.execute(INSERT_TASK, (user_id, title))
        conn.commit()
    finally:
        conn.close()


def get_tasks(user_id: int):
    conn = get_db()
    try:
        tasks = conn.execute(
            GET_ALL_TASKS, (user_id,)
        ).fetchall()

        return [dict(task) for task in tasks]
    finally:
        conn.close()


def mark_task_done(task_id: int, user_id: int):
    conn = get_db()
    try:
        cursor = conn.execute(
            MARK_TASK_DONE, (task_id, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_task(task_id: int, user_id: int):
    conn = get_db()
    try:
        cursor = conn.execute(
            DELETE_TASK, (task_id, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def get_task_stats(user_id: int):
    conn = get_db()
    try:
        rows = conn.execute(
            GET_TASK_STATS, (user_id,)
        ).fetchall()

        stats = {
            "total": 0,
            "done": 0,
            "not_done": 0
        }

        for row in rows:
            count = row["total"]
            stats["total"] += count

            if row["is_done"] == 1:
                stats["done"] = count
            else:
                stats["not_done"] = count

        return stats
    finally:
        conn.close()