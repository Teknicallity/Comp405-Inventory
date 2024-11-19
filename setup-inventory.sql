
USE inventory_system;

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

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(250),
    is_admin BOOL DEFAULT 0,
    employee_id INT,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(50),
    model VARCHAR(50),
    serial VARCHAR(50),
    location_id INT,
    status_id INT DEFAULT 1,
    FOREIGN KEY (location_id) REFERENCES locations (location_id) ON DELETE RESTRICT,
    FOREIGN KEY (status_id) REFERENCES statuses (status_id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE checkouts (
    checkout_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    employee_id INT,
    checkout_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    returned_date TIMESTAMP NULL,
    FOREIGN KEY (item_id) REFERENCES items (item_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE documentation (
    documentation_id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(100),
    description VARCHAR(255),
    item_id INT,
    FOREIGN KEY (item_id) REFERENCES items (item_id) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO statuses (name) VALUES ('Available'), ('Checked Out'), ('Missing'), ('Damaged');
INSERT INTO locations (name)
    VALUES ('Hand-tool Pegboard'), ('Drill Rack'), ('Charging Station'), ('Paint Station'), ('Electronics Bench'),
           ('Safety Cabinet');

INSERT INTO items (name, serial, location_id) VALUES
    ('Hammer', 'HT001', 1),
    ('Screwdriver Set', 'HT002', 1),
    ('Measuring Tape', 'HT003', 1),

    ('Cordless Drill', 'DRL003', 2),
    ('Skill Saw', 'PT005', 2),
    ('Nail Gun', 'DRL007', 2),

    ('Battery Pack', 'CHG001', 3),

    ('Sander', 'PT004', 4),
    ('Paint Brushes Set', 'PT006', 4),
    ('Paint Cans', 'PT007', 4),

    ('Multimeter', 'ELE005', 5),
    ('Wire Cutter', 'ELE006', 5),
    ('Soldering Iron', 'ELE007', 5),

    ('Safety Goggles', 'SFT001', 6),
    ('Respirator Mask', 'SFT002', 6),
    ('First Aid Kit', 'SFT003', 6);

INSERT INTO documentation (url, description, item_id) VALUES
    ('https://example.com/hammer-guide', 'Hammer user guide', 1),
    ('https://example.com/hammer-tips', 'Hammer usage tips', 1),

    ('https://example.com/screwdriver-guide', 'Screwdriver instructions', 2),
    ('https://example.com/screwdriver-set-maintenance', 'Maintenance tips', 2),

    ('https://example.com/measuring-tape', 'Measurement guide', 3),

    ('https://example.com/drill-setup', 'Setup instructions', 4),
    ('https://example.com/drill-safety', 'Drill safety tips', 4),

    ('https://example.com/saw-guide', 'Saw instructions', 5),

    ('https://example.com/nail-gun', 'Nail gun guide', 6),
    ('https://example.com/nail-gun-safety', 'Safety instructions', 6),

    ('https://example.com/battery-pack', 'Charging instructions', 7),

    ('https://example.com/sander-setup', 'Setup guide', 8),
    ('https://example.com/sander-maintenance', 'Maintenance tips', 8),

    ('https://example.com/paint-brushes', 'Cleaning instructions', 9),

    ('https://example.com/paint-cans', 'Storage guidelines', 10),

    ('https://example.com/multimeter-guide', 'Multimeter usage', 11),
    ('https://example.com/multimeter-safety', 'Safety precautions', 11),

    ('https://example.com/wire-cutter', 'Wire cutter tips', 12),

    ('https://example.com/soldering-iron', 'Soldering guide', 13),

    ('https://example.com/safety-goggles', 'Safety instructions', 14),
    ('https://example.com/safety-tips', 'General safety tips', 14),

    ('https://example.com/respirator-mask', 'Respirator usage', 15),

    ('https://example.com/first-aid', 'First aid instructions', 16),
    ('https://example.com/emergency-tips', 'Emergency usage tips', 16);
