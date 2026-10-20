from db.database import get_db
from db.queries import (
    GET_USER_BY_TG_ID,
    INSERT_USER,
    UPDATE_USER_USERNAME
)


def get_user(telegram_id: int):
    conn = get_db()
    try:
        user = conn.execute(
            GET_USER_BY_TG_ID, (telegram_id,)
        ).fetchone()

        return dict(user) if user else None
    finally:
        conn.close()


def create_user(telegram_id: int, username: str):
    conn = get_db()
    try:
        conn.execute(
            INSERT_USER, (telegram_id, username)
        )
        conn.commit()
    finally:
        conn.close()

    return get_user(telegram_id)


def update_user_username(
    telegram_id: int,
    new_username: str
):
    conn = get_db()
    try:
        conn.execute(
            UPDATE_USER_USERNAME,
            (new_username, telegram_id)
        )
        conn.commit()
    finally:
        conn.close()

    return get_user(telegram_id)