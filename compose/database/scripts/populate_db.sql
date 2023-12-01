INSERT INTO Doctor(last_name, first_name, specialization) VALUES
    ('Shepherd', 'Derek', 'Neurosurgery'),
    ('Robbins', 'Arizona', 'Pediatry'),
    ('Montgomery', 'Addison', 'Gynecology'),
    ('Torres', 'Callie', 'Orthopedy');

INSERT INTO Patient(code, first_name, last_name, birthdate) VALUES
    ('AT001', 'John', 'Doe', '1990-05-15'),
    ('CD456', 'Emily', 'Johnson', '1985-08-22'),
    ('AB123', 'Michael', 'Smith', '1995-03-10'),
    ('KD884', 'Sarah', 'Davis', '1982-11-28');

INSERT INTO Visit(reservation_date, diagnosis, price, paid, patient, doctor) VALUES
    ('2023-11-15 09:00:00', 'Upper respiratory infection', 50.00, 1, 'AT001', 4),
    ('2023-11-30 11:00:00', 'Urinary tract infection', 60.00, 0, 'CD456', 3),
    ('2023-12-07 12:00:00', NULL, NULL, 0, 'AB123', NULL),
    ('2023-12-07 13:00:00', NULL, NULL, 0, 'KD884', 1),
    ('2023-12-14 09:00:00', NULL, NULL, 0, 'AB123', 1),
    ('2023-12-08 09:00:00', NULL, NULL, 0, 'AT001', 1);