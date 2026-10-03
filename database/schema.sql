CREATE DATABASE IF NOT EXISTS phishing_awareness;
USE phishing_awareness;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(180) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin','trainer','user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS campaigns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(160) NOT NULL,
    scenario VARCHAR(255) NOT NULL,
    difficulty ENUM('Beginner','Intermediate','Advanced') DEFAULT 'Beginner',
    status ENUM('Draft','Active','Completed') DEFAULT 'Draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS simulation_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    campaign_id INT NOT NULL,
    event_type ENUM('opened','clicked','reported','training_viewed') NOT NULL,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS awareness_content (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(180) NOT NULL,
    category VARCHAR(100) NOT NULL,
    body TEXT NOT NULL
);

INSERT INTO awareness_content(title, category, body)
SELECT 'Spot the sender', 'Email Safety',
'Check the full sender address. Attackers often use look-alike domains, unexpected subdomains, or spelling changes.'
WHERE NOT EXISTS (SELECT 1 FROM awareness_content);

INSERT INTO awareness_content(title, category, body)
SELECT 'Inspect links before clicking', 'Link Safety',
'Hover over links and verify the destination. Treat unexpected login, payment, and document links with caution.'
WHERE NOT EXISTS (SELECT 1 FROM awareness_content WHERE title='Inspect links before clicking');

INSERT INTO awareness_content(title, category, body)
SELECT 'Use reporting channels', 'Incident Reporting',
'When something feels suspicious, report it through your organization''s security channel instead of interacting with it.'
WHERE NOT EXISTS (SELECT 1 FROM awareness_content WHERE title='Use reporting channels');

INSERT INTO campaigns(name, scenario, difficulty, status)
SELECT 'Invoice Verification Drill', 'Unexpected invoice email', 'Beginner', 'Active'
WHERE NOT EXISTS (SELECT 1 FROM campaigns);
