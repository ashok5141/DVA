CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    profile_image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS blogs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT IGNORE INTO users (username, password) VALUES ('admin', 'admin123');
INSERT INTO blogs (user_id, title, content)  
VALUES ((SELECT id FROM users WHERE username = 'admin'), 'Security Best Practices', 'Enable MFA, Use IAM Roles, Encrypt Data');
INSERT INTO blogs (user_id, title, content)  
VALUES ((SELECT id FROM users WHERE username = 'Ashok'), 'To Do List', 'Build a GraphQL, JWT Tokens');