PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS statuses;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS checkouts;
DROP TABLE IF EXISTS documentation;


CREATE TABLE items
(
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT,
    model_number TEXT,
    serial_number TEXT,
    uuid TEXT,
    location_id INTEGER,
    FOREIGN KEY (location_id) REFERENCES locations (location_id) ON DELETE restrict
);

CREATE TABLE locations
(
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE statuses
(
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE employees
(
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    title TEXT,
    reports_to INTEGER,
    FOREIGN KEY (reports_to) REFERENCES employees (employee_id) ON DELETE restrict
);

CREATE TABLE checkouts
(
    checkout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    status_id INTEGER,
    employee_id INTEGER,
    checkout_date TIMESTAMP NOT NULL,
    returned_date TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items (item_id) ON DELETE cascade,
    FOREIGN KEY (status_id) REFERENCES statuses (status_id) ON DELETE set null,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id) ON DELETE set null
);

CREATE TABLE documentation
(
    documentation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    description TEXT,
    item_id INTEGER,
    FOREIGN KEY (item_id) REFERENCES items (item_id) ON DELETE CASCADE
);