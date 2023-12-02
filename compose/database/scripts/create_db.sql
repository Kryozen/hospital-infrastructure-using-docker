-- CREATE SCHEMA hospital_db;

-- USE hospital_db;

CREATE TABLE Doctor(
    id CHAR(4) PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(20) NOT NULL
);

CREATE TABLE Patient(
    email VARCHAR(50) PRIMARY KEY,
    pwd VARCHAR(64) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birthdate DATE NOT NULL
);

CREATE TABLE Visit(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    reservation_date DATETIME NOT NULL,
    diagnosis VARCHAR(200) DEFAULT '',
    price DECIMAL(7,2) DEFAULT NULL,
    paid TINYINT(1) DEFAULT 0,
    patient VARCHAR(50) NOT NULL,
    doctor CHAR(4) NULL,
    FOREIGN KEY (doctor) REFERENCES Doctor(id),
    FOREIGN KEY (patient) REFERENCES Patient(email)
);