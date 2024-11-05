
CREATE DATABASE IF NOT EXISTS inventory_system;

USE inventory_system;

DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS statuses;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS checkouts;
DROP TABLE IF EXISTS documentation;
DROP TABLE IF EXISTS qrcodes;

CREATE TABLE locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE statuses (
    status_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    title VARCHAR(20),
    reports_to INT,
    FOREIGN KEY (reports_to) REFERENCES employees (employee_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(50),
    model_number VARCHAR(50),
    serial_number VARCHAR(50),
    location_id INT,
    FOREIGN KEY (location_id) REFERENCES locations (location_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE checkouts (
    checkout_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT,
    status_id INT,
    employee_id INT,
    checkout_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    returned_date TIMESTAMP NULL,
    FOREIGN KEY (item_id) REFERENCES items (item_id) ON DELETE CASCADE,
    FOREIGN KEY (status_id) REFERENCES statuses (status_id) ON DELETE SET NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE documentation (
    documentation_id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(100),
    description VARCHAR(255),
    item_id INT,
    FOREIGN KEY (item_id) REFERENCES items (item_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE qrcodes (
    qrcode_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT,
    uuid CHAR(36),
    created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    last_used_date TIMESTAMP NULL,
    created_by INT,
    FOREIGN KEY (item_id) REFERENCES items (item_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES employees (employee_id) ON DELETE SET NULL
) ENGINE=InnoDB;
