CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        username TEXT
    )
"""

CREATE_TASKS_TABLE = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT,
        is_done INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
"""

# --- USERS ---

CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        username TEXT
    )
"""

GET_USER_BY_TG_ID = """
    SELECT * FROM users
    WHERE telegram_id = ?
"""

INSERT_USER = """
    INSERT OR IGNORE INTO users (telegram_id, username)
    VALUES (?, ?)
"""

UPDATE_USER_USERNAME = """
    UPDATE users
    SET username = ?
    WHERE telegram_id = ?
"""


# --- TASKS ---

CREATE_TASKS_TABLE = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT,
        is_done INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE
    )
"""

INSERT_TASK = """
    INSERT INTO tasks (user_id, title)
    VALUES (?, ?)
"""

GET_ALL_TASKS = """
    SELECT
        tasks.id AS task_id,
        tasks.title,
        tasks.is_done,
        users.username
    FROM tasks
    INNER JOIN users ON tasks.user_id = users.id
    WHERE tasks.user_id = ?
    ORDER BY tasks.id
"""

GET_TASK_BY_ID = """
    SELECT *
    FROM tasks
    WHERE id = ? AND user_id = ?
"""

MARK_TASK_DONE = """
    UPDATE tasks
    SET is_done = 1
    WHERE id = ? AND user_id = ?
"""

DELETE_TASK = """
    DELETE FROM tasks
    WHERE id = ? AND user_id = ?
"""

GET_TASK_STATS = """
    SELECT is_done, COUNT(*) AS total
    FROM tasks
    WHERE user_id = ?
    GROUP BY is_done
"""

#---TASKS---
GET_TASK_BY_ID = 'SELECT * FROM tasks WHERE id = ? AND user_id = ?'
INSERT_TASK = 'INSERT INTO tasks (user_id, title) VALUES (?, ?)'


GET_ALL_TASKS = """
    SELECT *
    FROM tasks
    INNER JOIN users ON tasks.user_id = users.id
    WHERE tasks.user_id = ?
"""

MARK_TASK_DONE = 'UPDATE tasks SET is_done = 1 WHERE id = ? AND user_id = ?' 
DELETE_TASK = 'DELETE FROM tasks WHERE id = ? AND user_id = ?'