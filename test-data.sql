-- ==========================================
-- 測試資料 SQL 腳本
-- 實驗室專案進度管制系統
-- ==========================================

-- 清空現有資料（僅用於開發環境）
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE audit_log;
TRUNCATE TABLE projects;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;

-- ==========================================
-- 1. 用戶測試資料
-- ==========================================
-- 注意：密碼雜湊值對應的明文密碼都是 "Test@123"
-- 在實際應用中，密碼應該通過 Flask 的 generate_password_hash() 生成

INSERT INTO users (id, username, password_hash, full_name, email, role, created_at, last_login) VALUES
(1, 'admin', 'pbkdf2:sha256:260000$salt$hash', '系統管理員', 'admin@lab.com', 'admin', NOW(), NOW()),
(2, 'manager1', 'pbkdf2:sha256:260000$salt$hash', '陳澤康', 'chen@lab.com', 'manager', NOW(), NOW()),
(3, 'tester1', 'pbkdf2:sha256:260000$salt$hash', '宋伟胜', 'song@lab.com', 'tester', NOW(), NOW()),
(4, 'tester2', 'pbkdf2:sha256:260000$salt$hash', '朱伟胜', 'zhu@lab.com', 'tester', NOW(), NOW()),
(5, 'tester3', 'pbkdf2:sha256:260000$salt$hash', '張巧樂', 'zhang@lab.com', 'tester', NOW(), NOW());

-- ==========================================
-- 2. 專案測試資料
-- ==========================================

INSERT INTO projects (
    item_number,
    personnel,
    case_number,
    customer,
    evidence_required,
    model,
    samples_complete,
    engineer_progress,
    expected_report_date,
    estimated_hours,
    actual_hours,
    created_by,
    updated_by,
    status,
    created_at,
    updated_at
) VALUES
-- 已完成的專案
(1, '胡利红', '592302', '小米（母）', 1, 'P1_CE/FCC/NCC', '是', '陈泽康/99%', '2025-10-15', 80, 80, 2, 2, 'active', NOW(), NOW()),
(2, '陈颖', '570202-02', 'oppo（子）', 1, 'CPH2795', '是（10）', '宋伟胜/99%', '2025-10-25', 40, 40, 3, 3, 'active', NOW(), NOW()),
(3, '陈奕诚', 'R2S40073', '专音（母）', 1, '财务部未复核', '是（10）', '陈泽康/99%', '2025-10-22', 80, 0, 2, 2, 'active', NOW(), NOW()),
(4, '赖心盈', '5o1316', '天珑', 1, 'Nano25 DW010', '是（10）', '蒋志豪/99%', '2025-10-30', 100, 100, 3, 3, 'active', NOW(), NOW()),
(5, '张玲', '591905', '摩托罗拉', 1, 'E5S5 手环', '是（10）', '胡浩/99%', '2025-10-30', 100, 100, 4, 4, 'active', NOW(), NOW()),

-- 進行中的專案
(6, '李卫贤', 'S52224-01', '百富（子）是（43）', 0, 'A6630', '是（11）', '张巧乐/99%', '2025-11-07', 30, 30, 5, 5, 'active', NOW(), NOW()),
(7, '张玲', '5o1033', '麦博韦尔', 1, 'MP5', '是（10）', '张巧乐/100%', '2025-10-30', 100, 100, 5, 5, 'active', NOW(), NOW()),
(8, '钱秋蕾', '4D1312-06', '诺基亚', 1, 'GW4 voice', '是（10）', '宋伟胜/99%', '2025-10-30', 100, 100, 3, 3, 'active', NOW(), NOW()),
(9, '钱秋蕾', '580713', '移远', 1, '无', '是', '张巧乐/99%', '2025-09-31', 100, 100, 5, 5, 'active', NOW(), NOW()),
(10, '陈颖', '5o2003', '一器是（44）', 0, 'W5110', '是（10）', '柏森，泽康/99%', '2025-11-10', 100, 100, 2, 2, 'active', NOW(), NOW()),

-- 延遲的專案
(11, '陈颖', '592302-03', '小米（子）是（45）', 0, 'CE/FCC/NCC/India_IN', '是（11）', '泽康/99%', '2025-11-12', 40, 30, 2, 2, 'active', NOW(), NOW()),
(12, '陈颖', '571801-02', 'vivo（子）是（45）', 0, 'PD2529（V2538）', '是（11）', '宋伟胜/99%', '2025-11-12', 40, 6, 3, 3, 'active', NOW(), NOW()),

-- 新專案（進度較低）
(13, '王小明', 'TEST001', '華為技術', 1, 'Mate 60 Pro', '否', '陈泽康/20%', '2025-12-20', 120, 24, 2, 2, 'active', NOW(), NOW()),
(14, '李美麗', 'TEST002', '三星電子', 1, 'Galaxy S24', '是（5）', '宋伟胜/35%', '2025-12-25', 100, 35, 3, 3, 'active', NOW(), NOW()),
(15, '張偉強', 'TEST003', 'SONY', 0, 'Xperia 1 VI', '是（3）', '张巧乐/10%', '2026-01-15', 80, 8, 5, 5, 'active', NOW(), NOW()),

-- 高優先級專案
(16, '劉佳慧', 'URGENT-001', 'Apple Inc.', 1, 'iPhone 16 Pro', '是（7）', '陈泽康/60%', '2025-12-10', 150, 90, 2, 2, 'active', NOW(), NOW()),
(17, '陳建國', 'URGENT-002', 'Google', 1, 'Pixel 9 Pro', '是（8）', '宋伟胜/75%', '2025-12-15', 140, 105, 3, 3, 'active', NOW(), NOW()),

-- 長期專案
(18, '楊淑芬', 'LONG-001', '聯發科技', 1, 'Dimensity 9400', '是（4）', '张巧乐/15%', '2026-02-28', 200, 30, 5, 5, 'active', NOW(), NOW()),
(19, '林志明', 'LONG-002', '高通公司', 1, 'Snapdragon 8 Gen 4', '否', '陈泽康/5%', '2026-03-15', 250, 12, 2, 2, 'active', NOW(), NOW()),
(20, '黃雅婷', 'LONG-003', '聯想集團', 1, 'ThinkPad X1 Carbon', '是（2）', '宋伟胜/8%', '2026-01-30', 180, 14, 3, 3, 'active', NOW(), NOW()),

-- 不同狀態的專案（用於測試篩選）
(21, '周靜怡', 'FILTER-001', '戴爾科技', 1, 'XPS 15', '是（10）', '张巧乐/95%', '2025-11-25', 90, 85, 5, 5, 'active', NOW(), NOW()),
(22, '吳文彬', 'FILTER-002', '惠普公司', 0, 'EliteBook 840', '是（6）', '陈泽康/50%', '2025-12-05', 110, 55, 2, 2, 'active', NOW(), NOW()),
(23, '鄭美玲', 'FILTER-003', '華碩電腦', 1, 'ROG Zephyrus', '否', '宋伟胜/25%', '2025-12-30', 130, 32, 3, 3, 'active', NOW(), NOW()),

-- 多樣化客戶專案
(24, '蔡依林', 'CUST-001', 'LG電子', 1, 'G Flex 4', '是（9）', '张巧乐/88%', '2025-11-20', 95, 83, 5, 5, 'active', NOW(), NOW()),
(25, '孫翔宇', 'CUST-002', 'HTC', 1, 'U23 Pro', '是（5）', '陈泽康/42%', '2025-12-12', 105, 44, 2, 2, 'active', NOW(), NOW()),
(26, '馬欣怡', 'CUST-003', '中興通訊', 0, 'Axon 60', '是（3）', '宋伟胜/18%', '2026-01-08', 88, 15, 3, 3, 'active', NOW(), NOW()),

-- 特殊情況專案
(27, '趙麗穎', 'SPEC-001', '諾基亞（復興）', 1, 'Nokia 9.3', '是（10）', '张巧乐/100%', '2025-10-31', 75, 75, 5, 5, 'active', NOW(), NOW()),
(28, '徐若瑄', 'SPEC-002', 'BlackBerry', 1, 'KeyOne 2', '是（7）', '陈泽康/70%', '2025-11-28', 120, 84, 2, 2, 'active', NOW(), NOW()),
(29, '梁靜茹', 'SPEC-003', 'OnePlus', 1, '12 Pro', '是（4）', '宋伟胜/38%', '2025-12-18', 98, 37, 3, 3, 'active', NOW(), NOW()),
(30, '蔡健雅', 'SPEC-004', 'Realme', 0, 'GT 6 Pro', '否', '张巧乐/12%', '2026-01-22', 85, 10, 5, 5, 'active', NOW(), NOW());

-- ==========================================
-- 3. 審計日誌測試資料
-- ==========================================

INSERT INTO audit_log (user_id, action, table_name, record_id, old_values, new_values, timestamp) VALUES
(2, 'CREATE', 'projects', 1, NULL, '{"case_number":"592302","customer":"小米（母）"}', DATE_SUB(NOW(), INTERVAL 30 DAY)),
(2, 'UPDATE', 'projects', 1, '{"actual_hours":60}', '{"actual_hours":80}', DATE_SUB(NOW(), INTERVAL 15 DAY)),
(3, 'CREATE', 'projects', 2, NULL, '{"case_number":"570202-02","customer":"oppo（子）"}', DATE_SUB(NOW(), INTERVAL 25 DAY)),
(3, 'UPDATE', 'projects', 2, '{"actual_hours":20}', '{"actual_hours":40}', DATE_SUB(NOW(), INTERVAL 10 DAY)),
(5, 'CREATE', 'projects', 5, NULL, '{"case_number":"591905","customer":"摩托罗拉"}', DATE_SUB(NOW(), INTERVAL 20 DAY)),
(2, 'UPDATE', 'projects', 13, '{"actual_hours":0}', '{"actual_hours":24}', DATE_SUB(NOW(), INTERVAL 5 DAY)),
(3, 'UPDATE', 'projects', 14, '{"actual_hours":10}', '{"actual_hours":35}', DATE_SUB(NOW(), INTERVAL 3 DAY)),
(5, 'UPDATE', 'projects', 15, '{"actual_hours":0}', '{"actual_hours":8}', DATE_SUB(NOW(), INTERVAL 2 DAY)),
(2, 'CREATE', 'projects', 16, NULL, '{"case_number":"URGENT-001","customer":"Apple Inc."}', DATE_SUB(NOW(), INTERVAL 7 DAY)),
(1, 'UPDATE', 'users', 2, '{"role":"tester"}', '{"role":"manager"}', DATE_SUB(NOW(), INTERVAL 60 DAY));

-- ==========================================
-- 4. 重置自動遞增 ID
-- ==========================================

ALTER TABLE users AUTO_INCREMENT = 6;
ALTER TABLE projects AUTO_INCREMENT = 31;
ALTER TABLE audit_log AUTO_INCREMENT = 11;

-- ==========================================
-- 5. 驗證資料
-- ==========================================

-- 檢查插入的資料數量
SELECT 'Users' AS table_name, COUNT(*) AS record_count FROM users
UNION ALL
SELECT 'Projects', COUNT(*) FROM projects
UNION ALL
SELECT 'Audit Logs', COUNT(*) FROM audit_log;

-- 檢查專案狀態分佈
SELECT
    CASE
        WHEN actual_hours = 0 THEN '未開始'
        WHEN actual_hours >= estimated_hours THEN '已完成'
        WHEN actual_hours / estimated_hours >= 0.8 THEN '進度良好'
        WHEN actual_hours / estimated_hours >= 0.4 THEN '進行中'
        ELSE '進度落後'
    END AS status,
    COUNT(*) AS count
FROM projects
WHERE status = 'active'
GROUP BY
    CASE
        WHEN actual_hours = 0 THEN '未開始'
        WHEN actual_hours >= estimated_hours THEN '已完成'
        WHEN actual_hours / estimated_hours >= 0.8 THEN '進度良好'
        WHEN actual_hours / estimated_hours >= 0.4 THEN '進行中'
        ELSE '進度落後'
    END;

-- 檢查人員工作量分佈
SELECT
    personnel,
    COUNT(*) AS project_count,
    SUM(estimated_hours) AS total_estimated_hours,
    SUM(actual_hours) AS total_actual_hours,
    SUM(estimated_hours - actual_hours) AS remaining_hours
FROM projects
WHERE status = 'active'
GROUP BY personnel
ORDER BY project_count DESC;

-- ==========================================
-- 6. 創建用戶密碼生成腳本說明
-- ==========================================

-- 注意：以下 SQL 中的密碼雜湊值僅為示例
-- 實際應用中，請使用 Python 腳本生成正確的密碼雜湊：
--
-- Python 代碼示例：
-- from werkzeug.security import generate_password_hash
-- password_hash = generate_password_hash('Test@123', method='pbkdf2:sha256:260000')
-- print(password_hash)
--
-- 然後將生成的雜湊值更新到資料庫：
-- UPDATE users SET password_hash = '生成的雜湊值' WHERE username = 'admin';

-- ==========================================
-- 測試資料總結
-- ==========================================
-- 用戶數量：5 個（1 管理員，1 經理，3 測試員）
-- 專案數量：30 個
-- - 已完成：7 個
-- - 進行中（高進度）：8 個
-- - 進行中（中進度）：6 個
-- - 進行中（低進度）：7 個
-- - 延遲：2 個
-- 審計日誌：10 條記錄
-- ==========================================
