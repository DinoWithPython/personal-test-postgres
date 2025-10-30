-- Создаем таблицу users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создаем индекс для быстрого поиска по email
CREATE INDEX idx_email ON users(email);

-- Создаем таблицу для хранения данных о действиях пользователей
CREATE TABLE IF NOT EXISTS user_actions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details JSONB
);

-- Создаем последовательность для автоинкремента
CREATE SEQUENCE IF NOT EXISTS global_seq START 1 INCREMENT 1;

-- Пример создания типа данных
CREATE TYPE action_status AS ENUM ('pending', 'completed', 'failed');

-- Пример создания функции
CREATE OR REPLACE FUNCTION get_user_count()
RETURNS INTEGER AS $$
BEGIN
    RETURN (SELECT COUNT(*) FROM users);
END;
$$ LANGUAGE plpgsql;

-- Вставляем тестовые данные
INSERT INTO users (name, email) VALUES
('Test User 1', 'test1@example.com'),
('Test User 2', 'test2@example.com');