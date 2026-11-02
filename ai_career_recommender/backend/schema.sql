-- Database Schema for AI-Based Skill & Career Recommendation System

CREATE DATABASE IF NOT EXISTS ai_career_recommender;
USE ai_career_recommender;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Student profiles table
CREATE TABLE IF NOT EXISTS student_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    full_name VARCHAR(150) DEFAULT '',
    phone VARCHAR(50) DEFAULT '',
    degree VARCHAR(100) DEFAULT '',
    branch VARCHAR(100) DEFAULT '',
    graduation_year INT DEFAULT 2026,
    experience_level VARCHAR(50) DEFAULT 'Beginner',
    target_career_id INT DEFAULT NULL,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Skills table
CREATE TABLE IF NOT EXISTS skills (
    id INT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(100) DEFAULT 'General',
    difficulty_level VARCHAR(50) DEFAULT 'Beginner'
);

-- Careers table
CREATE TABLE IF NOT EXISTS careers (
    id INT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(100) DEFAULT 'General',
    description TEXT,
    average_salary VARCHAR(50) DEFAULT '$85,000',
    job_outlook VARCHAR(100) DEFAULT 'High Demand (15% growth)'
);

-- Career Skills requirement join table
CREATE TABLE IF NOT EXISTS career_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    career_id INT NOT NULL,
    skill_id INT NOT NULL,
    importance FLOAT DEFAULT 0.8,
    skill_type VARCHAR(50) DEFAULT 'Required',
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

-- Domain interests table
CREATE TABLE IF NOT EXISTS interests (
    id INT PRIMARY KEY,
    name VARCHAR(150) NOT NULL
);

-- Education eligibility mapping
CREATE TABLE IF NOT EXISTS education (
    id INT AUTO_INCREMENT PRIMARY KEY,
    career_id INT NOT NULL,
    degree VARCHAR(100) NOT NULL,
    branch VARCHAR(100) NOT NULL,
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE
);

-- Student verified skills
CREATE TABLE IF NOT EXISTS student_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_id INT NOT NULL,
    proficiency_level VARCHAR(50) DEFAULT 'Intermediate',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

-- Student declared interests
CREATE TABLE IF NOT EXISTS student_interests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    interest_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (interest_id) REFERENCES interests(id) ON DELETE CASCADE
);

-- Recommendations audit log
CREATE TABLE IF NOT EXISTS recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    career_id INT NOT NULL,
    hybrid_score FLOAT DEFAULT 0.0,
    ml_score FLOAT DEFAULT 0.0,
    gnn_score FLOAT DEFAULT 0.0,
    rank_position INT DEFAULT 1,
    explanation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE
);

-- Skill gaps breakdown table
CREATE TABLE IF NOT EXISTS skill_gaps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    career_id INT NOT NULL,
    skill_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'missing',
    importance FLOAT DEFAULT 0.8,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);
