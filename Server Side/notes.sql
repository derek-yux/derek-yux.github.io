CREATE DATABASE misc CHARACTER SET=utf8mb4;
CREATE USER 'root'@'localhost' IDENTIFIED BY '';
GRANT ALL ON misc.* TO 'root'@'localhost';
CREATE USER 'fred'@'127.0.0.1' IDENTIFIED BY 'zap';
GRANT ALL ON misc.* TO 'fred'@'127.0.0.1';

USE misc;

CREATE TABLE users (
   user_id INTEGER NOT NULL
     AUTO_INCREMENT,
   name VARCHAR(128),
   email VARCHAR(128),
   password VARCHAR(128),
   PRIMARY KEY(user_id),
   INDEX(email)
) ENGINE=InnoDB CHARSET=utf8mb4;
