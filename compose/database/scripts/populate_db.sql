INSERT INTO Doctor(last_name, first_name, specialization) VALUES
    ('Shepherd', 'Derek', 'Neurosurgery'),
    ('Robbins', 'Arizona', 'Pediatry'),
    ('Montgomery', 'Addison', 'Gynecology'),
    ('Torres', 'Callie', 'Orthopedy');

INSERT INTO Patient(email, pwd, first_name, last_name, birthdate) VALUES
    ('j.doe@gmail.com', '57db1253b68b6802b59a969f750fa32b60cb5cc8a3cb19b87dac28f541dc4e2a', 'John', 'Doe', '1990-05-15'),
    ('emilyj85@gmail.com', '3e5082ed2d6cde7f56b57adaaee766f1b457540b08b5341f9dbf01eccbc86220', 'Emily', 'Johnson', '1985-08-22'),
    ('msmith1@gmail.com', 'ae155d46c805871a185ed71ee1f86baeb03cd2196af54c1bc787c580634dfd73', 'Michael', 'Smith', '1995-03-10'),
    ('davsar@gmail.com', 'fff8acd78f7528c143cb5a6971f911d3869368cbc177f3f4404d945c6accc08d', 'Sarah', 'Davis', '1982-11-28');

INSERT INTO Visit(reservation_date, diagnosis, price, paid, patient, doctor) VALUES
    ('2023-11-15 09:00:00', 'Upper respiratory infection', 50.00, 1, 'j.doe@gmail.com', 4),
    ('2023-11-30 11:00:00', 'Urinary tract infection', 60.00, 0, 'emilyj85@gmail.com', 3),
    ('2023-12-07 12:00:00', NULL, NULL, 0, 'j.doe@gmail.com', NULL),
    ('2023-12-07 13:00:00', NULL, NULL, 0, 'msmith1@gmail.com', 1),
    ('2023-12-14 09:00:00', NULL, NULL, 0, 'j.doe@gmail.com', 1),
    ('2023-12-08 09:00:00', NULL, NULL, 0, 'emilyj85@gmail.com', 1);