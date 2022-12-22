create database vkeducation;
use vkeducation;
CREATE TABLE `test_users` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `surname` varchar(255) NOT NULL,
    `middle_name` varchar(255) DEFAULT NULL,
    `username` varchar(16) DEFAULT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(64) NOT NULL,
    `access` smallint DEFAULT NULL,
    `active` smallint DEFAULT NULL,
    `start_active_time` datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`),
    UNIQUE KEY `ix_test_users_username` (`username`)
);
CREATE USER 'test_qa' IDENTIFIED BY 'qa_test';
FLUSH PRIVILEGES;
GRANT ALL PRIVILEGES ON vkeducation.test_users TO 'test_qa';
FLUSH PRIVILEGES;
INSERT INTO test_users(name, surname, middle_name, username, password, email, access, active)
VALUES ('test_name', 'test_surname', 'test_middle_name', 'test_username', 'test_password', 'test@test.com', 1, 0);
