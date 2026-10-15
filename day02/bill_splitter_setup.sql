-- Bill Splitter SQLite database setup
-- Run this script against your bill_splitter.db database.
-- Safe to run more than once: existing tables will not be recreated.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS people (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE
);

CREATE TABLE IF NOT EXISTS expenses (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_name TEXT NOT NULL,
    amount       REAL NOT NULL CHECK (amount > 0),
    paid_by      INTEGER NOT NULL,
    FOREIGN KEY (paid_by) REFERENCES people(id)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS expense_participants (
    expense_id INTEGER NOT NULL,
    person_id  INTEGER NOT NULL,
    share      REAL NOT NULL CHECK (share >= 0),
    PRIMARY KEY (expense_id, person_id),
    FOREIGN KEY (expense_id) REFERENCES expenses(id)
        ON DELETE CASCADE,
    FOREIGN KEY (person_id) REFERENCES people(id)
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_expenses_paid_by
    ON expenses(paid_by);

CREATE INDEX IF NOT EXISTS idx_participants_person_id
    ON expense_participants(person_id);
