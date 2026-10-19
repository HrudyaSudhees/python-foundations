
CREATE TABLE IF NOT EXISTS people (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    expense_name TEXT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    paid_by INTEGER NOT NULL REFERENCES people(id)
);

CREATE TABLE IF NOT EXISTS expense_participants (
    expense_id INTEGER NOT NULL
        REFERENCES expenses(id) ON DELETE CASCADE,
    person_id INTEGER NOT NULL
        REFERENCES people(id),
    share NUMERIC(12, 2) NOT NULL CHECK (share >= 0),
    PRIMARY KEY (expense_id, person_id)
);
