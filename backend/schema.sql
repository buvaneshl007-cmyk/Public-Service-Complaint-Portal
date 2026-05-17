-- Complaint Priority Management System Database Schema

-- Create database
CREATE DATABASE IF NOT EXISTS complaint_system;
USE complaint_system;

-- Create complaints table
CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_email VARCHAR(255) NOT NULL,
    subject VARCHAR(500) NOT NULL,
    body TEXT NOT NULL,
    priority ENUM('High', 'Medium', 'Low') NOT NULL DEFAULT 'Low',
    category VARCHAR(100) DEFAULT 'General',
    status ENUM('Pending', 'In Progress', 'Resolved', 'Closed', 'Rejected') NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_priority (priority),
    INDEX idx_status (status),
    INDEX idx_sender_email (sender_email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create admin_actions table (for tracking status changes)
CREATE TABLE IF NOT EXISTS admin_actions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id INT NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    old_value VARCHAR(100),
    new_value VARCHAR(100),
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE,
    INDEX idx_complaint_id (complaint_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create sample data (optional - for testing)
-- INSERT INTO complaints (sender_email, subject, body, priority, category, status) VALUES
-- ('user1@example.com', 'No power in Block B', 'There is no electricity in our hostel block. This is urgent!', 'High', 'Electrical', 'Pending'),
-- ('user2@example.com', 'Slow internet connection', 'The wifi speed is very slow in my room. Please fix it.', 'Medium', 'Network/IT', 'In Progress'),
-- ('user3@example.com', 'Room cleaning request', 'Need cleaning service for my room tomorrow.', 'Low', 'Cleaning', 'Pending');
