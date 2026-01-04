-- ==========================================
-- 数据库表结构创建脚本
-- 实验室专案进度管制系统
-- ==========================================

-- 使用数据库
USE lab_project_dev;

-- ==========================================
-- 1. 用户表 (users)
-- ==========================================

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) NOT NULL COMMENT 'admin, manager, tester',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    failed_login_attempts INT DEFAULT 0,
    locked_until DATETIME,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==========================================
-- 2. 专案表 (projects)
-- ==========================================

CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_number INT NOT NULL UNIQUE,
    personnel VARCHAR(100) NOT NULL,
    case_number VARCHAR(50) NOT NULL,
    customer VARCHAR(100) NOT NULL,
    evidence_required TINYINT(1) NOT NULL COMMENT '0=否, 1=是',
    model VARCHAR(100),
    samples_complete VARCHAR(20),
    engineer_progress VARCHAR(200) NOT NULL,
    expected_report_date DATE NOT NULL,
    estimated_hours INT NOT NULL,
    actual_hours INT NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    status VARCHAR(20) DEFAULT 'active',
    INDEX idx_personnel (personnel),
    INDEX idx_case_number (case_number),
    INDEX idx_expected_report_date (expected_report_date),
    INDEX idx_status (status),
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==========================================
-- 3. 审计日志表 (audit_log)
-- ==========================================

CREATE TABLE IF NOT EXISTS audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(50) NOT NULL COMMENT 'CREATE, UPDATE, DELETE',
    table_name VARCHAR(50) NOT NULL,
    record_id INT NOT NULL,
    old_values TEXT,
    new_values TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_timestamp (timestamp),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==========================================
-- 验证表创建
-- ==========================================

SHOW TABLES;

SELECT
    TABLE_NAME,
    TABLE_ROWS,
    CREATE_TIME
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'lab_project_dev'
ORDER BY TABLE_NAME;
