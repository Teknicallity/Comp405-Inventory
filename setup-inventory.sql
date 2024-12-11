
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
    url VARCHAR(200),
    description VARCHAR(50),
    item_id INT,
    FOREIGN KEY (item_id) REFERENCES items (item_id) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO statuses (name) VALUES ('Available'), ('Checked Out'), ('Missing'), ('Damaged');
INSERT INTO locations (name)
    VALUES ('Hand-tool Pegboard'), ('Drill Rack'), ('Charging Station'), ('Paint Station'), ('Electronics Bench'),
           ('Safety Cabinet');

INSERT INTO items (name, brand, model, serial, location_id) VALUES
    ('Hammer', 'Milwaukee', '17 oz. Smooth Face', 'HT001', 1),
    ('Screwdriver Set', 'DeWalt', 'DWHT65201', 'HT002', 1),
    ('Measuring Tape', 'Stanley', '25ft Powerlock', 'HT003', 1),

    ('Cordless Drill', 'Makita', 'LXT 18V', 'DRL003', 2),
    ('Skill Saw', 'Bosch', 'CS5 Professional', 'PT005', 2),
    ('Nail Gun', 'Ryobi', 'ONE+ 18V', 'DRL007', 2),

    ('Battery Pack', 'Ridgid', 'R87002', 'CHG001', 3),

    ('Sander', 'Black+Decker', 'BDEQS300', 'PT004', 4),
    ('Paint Brushes Set', 'Purdy', 'PRO-Extra Glide', 'PT006', 4),
    ('Paint Cans', 'Behr', 'Ultra Pure White', 'PT007', 4),

    ('Multimeter', 'Fluke', 'FLUKE-117', 'ELE005', 5),
    ('Wire Cutter', 'Klein Tools', '11055', 'ELE006', 5),
    ('Soldering Iron', 'Weller', 'WE1010NA', 'ELE007', 5),

    ('Safety Goggles', '3M', 'Virtua CCS', 'SFT001', 6),
    ('Respirator Mask', 'Honeywell', 'RU8500', 'SFT002', 6);

INSERT INTO documentation (url, description, item_id) VALUES
    ('https://www.homedepot.com/p/Milwaukee-17-oz-Smooth-Face-Framing-Hammer-48-22-9017/301688587', 'Home Depot Shop', 1),
    ('https://www.homedepot.com/p/DEWALT-Phillips-Screwdriver-Set-10-Piece-DWHT65201/317264613', 'Home Depot Shopping', 2),
    ('https://images.thdstatic.com/catalog/pdfImages/62/62d40ab8-7fbc-43b6-91d8-2171f5361483.pdf', 'Warranty', 3),

    ('https://images.thdstatic.com/catalog/pdfImages/5d/5d92752f-2ad8-464e-82c2-1d9490eacd4a.pdf', 'Drill Manual', 4),
    ('https://images.thdstatic.com/catalog/pdfImages/18/18cc4b70-f559-4da4-a5f6-b47281645125.pdf', 'Safety/Warranty', 4),

    ('https://www.manualslib.com/manual/537912/Bosch-Cs5.html?page=2#manual', 'Safety Guide', 5),
    ('https://www.manualslib.com/manual/537912/Bosch-Cs5.html?page=12#manual', 'Maintenance Manual', 5),

    ('https://images.thdstatic.com/catalog/pdfImages/3d/3d35f81c-42b0-4544-b07c-34207230191e.pdf', 'Operators Manual', 6),
    ('https://images.thdstatic.com/catalog/pdfImages/e3/e3e57198-567f-4e5f-8fd3-a55a115a938f.pdf', 'Warranty', 6),

    ('https://images.thdstatic.com/catalog/pdfImages/98/983bc60d-ec20-4efb-babc-2e5360981263.pdf', 'Warranty', 7),

    ('https://www.toolservicenet.com/i/BLACK_DECKER/GLOBALBOM/QU/BDEQS300/1/Instruction_Manual/EN/90611851_BDEQS300.pdf', 'Setup guide', 8),

    ('https://www.purdy.com/en/products/brushes/pro-extra-glide', 'Cleaning instructions', 9),

    ('https://www.behr.com/consumer/ColorDetailView/1850', 'Storage guidelines', 10),

    ('https://dam-assets.fluke.com/s3fs-public/110__117umeng0000_0.pdf?VersionId=kuO8Q80mS6nSqKkZOd2JFMEnAStiGspq', 'Multimeter usage', 11),
    ('https://dam-assets.fluke.com/s3fs-public/11x_____sseng0000.pdf?VersionId=h.Kf.gNRgkiaNYXWydWjMYEqh19.Gihk', 'Safety precautions', 11),

    ('https://www.kleintools.com/catalog/combination-cutting-tools/high-visibility-klein-kurve-wire-stripper-cutter', 'Compliance', 12),

    ('https://www.weller-tools.com/sites/default/files/products/documents/WEL_DSX80_120_DXV80_OI_T0055687210_web.pdf', 'Soldering guide', 13),

    ('https://multimedia.3m.com/mws/mediawebserver?mwsId=SSSSSu9n_zu8l00xNx_UoY_vnv70k17zHvu9lxtD7xt1evSSSSSS-', 'Regulatory Data Sheet', 14),

    ('https://www.honeywellstore.com/store/products/honeywell-mc-p100-multi-purpose-half-mask-respirator-rws-54032.htm', 'Respirator Shop page', 15);