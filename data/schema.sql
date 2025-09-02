-- Main activity table
CREATE TABLE IF NOT EXISTS activity (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    course_id VARCHAR(50) NOT NULL,
    lesson_completed BOOLEAN NOT NULL DEFAULT FALSE,
    time_spent INTEGER NOT NULL DEFAULT 0,
    device_type VARCHAR(20) NOT NULL DEFAULT 'unknown',
    subscription_type VARCHAR(20) NOT NULL DEFAULT 'free',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    signup_date DATE NOT NULL,
    first_device_type VARCHAR(20),
    initial_course_id VARCHAR(50),
    acquisition_channel VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courses table
CREATE TABLE IF NOT EXISTS courses (
    course_id VARCHAR(50) PRIMARY KEY,
    course_name VARCHAR(200) NOT NULL,
    total_lessons INTEGER NOT NULL DEFAULT 0,
    difficulty_level VARCHAR(20) DEFAULT 'beginner',
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- A/B tests table
CREATE TABLE IF NOT EXISTS ab_tests (
    test_id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    test_name VARCHAR(100) NOT NULL,
    variant VARCHAR(50) NOT NULL,
    assignment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    payment_id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    amount_usd DECIMAL(10,2) NOT NULL,
    payment_date TIMESTAMP NOT NULL,
    subscription_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_activity_date_user ON activity(date, user_id);
CREATE INDEX IF NOT EXISTS idx_activity_user_date ON activity(user_id, date);
CREATE INDEX IF NOT EXISTS idx_activity_course ON activity(course_id);
CREATE INDEX IF NOT EXISTS idx_users_signup_date ON users(signup_date);
CREATE INDEX IF NOT EXISTS idx_ab_tests_user_test ON ab_tests(user_id, test_name);

-- Sample courses data
INSERT INTO courses (course_id, course_name, total_lessons, difficulty_level, category) VALUES
('C101', 'Introduction to Python', 15, 'beginner', 'Programming'),
('C102', 'Data Science Basics', 20, 'intermediate', 'Data Science'),
('C103', 'Advanced Machine Learning', 25, 'advanced', 'Machine Learning'),
('C104', 'Web Development Fundamentals', 18, 'beginner', 'Web Development'),
('C105', 'SQL for Analytics', 12, 'intermediate', 'Data Analytics')
ON CONFLICT (course_id) DO NOTHING;