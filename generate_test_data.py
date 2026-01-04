#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
測試資料生成腳本
實驗室專案進度管制系統

此腳本生成包含正確密碼雜湊的測試資料
運行方式：python generate_test_data.py

所有測試用戶的預設密碼：Test@123
"""

from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import json
import random

# ==========================================
# 配置
# ==========================================

# 密碼設定
DEFAULT_PASSWORD = 'Test@123'
HASH_METHOD = 'pbkdf2:sha256:260000'

# ==========================================
# 生成密碼雜湊
# ==========================================

def generate_password_hashes():
    """生成所有用戶的密碼雜湊"""
    password_hash = generate_password_hash(DEFAULT_PASSWORD, method=HASH_METHOD)
    return password_hash

# ==========================================
# 用戶資料
# ==========================================

def generate_users_sql(password_hash):
    """生成用戶 SQL 插入語句"""

    users = [
        {
            'id': 1,
            'username': 'admin',
            'password_hash': password_hash,
            'full_name': '系統管理員',
            'email': 'admin@lab.com',
            'role': 'admin'
        },
        {
            'id': 2,
            'username': 'manager1',
            'password_hash': password_hash,
            'full_name': '陳澤康',
            'email': 'chen@lab.com',
            'role': 'manager'
        },
        {
            'id': 3,
            'username': 'tester1',
            'password_hash': password_hash,
            'full_name': '宋偉勝',
            'email': 'song@lab.com',
            'role': 'tester'
        },
        {
            'id': 4,
            'username': 'tester2',
            'password_hash': password_hash,
            'full_name': '朱偉勝',
            'email': 'zhu@lab.com',
            'role': 'tester'
        },
        {
            'id': 5,
            'username': 'tester3',
            'password_hash': password_hash,
            'full_name': '張巧樂',
            'email': 'zhang@lab.com',
            'role': 'tester'
        }
    ]

    sql_parts = []
    sql_parts.append("-- 插入用戶資料")
    sql_parts.append("INSERT INTO users (id, username, password_hash, full_name, email, role, created_at, last_login) VALUES")

    values = []
    for user in users:
        value = f"({user['id']}, '{user['username']}', '{user['password_hash']}', '{user['full_name']}', '{user['email']}', '{user['role']}', NOW(), NOW())"
        values.append(value)

    sql_parts.append(',\n'.join(values) + ';')
    sql_parts.append('')

    return '\n'.join(sql_parts)

# ==========================================
# 專案資料
# ==========================================

def generate_projects_sql():
    """生成專案 SQL 插入語句"""

    projects = [
        # 已完成的專案
        (1, '胡利紅', '592302', '小米（母）', 1, 'P1_CE/FCC/NCC', '是', '陳澤康/99%', '2025-10-15', 80, 80, 2, 2),
        (2, '陳穎', '570202-02', 'OPPO（子）', 1, 'CPH2795', '是（10）', '宋偉勝/99%', '2025-10-25', 40, 40, 3, 3),
        (3, '陳奕誠', 'R2S40073', '專音（母）', 1, '財務部未複核', '是（10）', '陳澤康/99%', '2025-10-22', 80, 0, 2, 2),
        (4, '賴心盈', '5o1316', '天瓏', 1, 'Nano25 DW010', '是（10）', '蔣志豪/99%', '2025-10-30', 100, 100, 3, 3),
        (5, '張玲', '591905', '摩托羅拉', 1, 'E5S5 手環', '是（10）', '胡浩/99%', '2025-10-30', 100, 100, 4, 4),

        # 進行中的專案
        (6, '李衛賢', 'S52224-01', '百富（子）是（43）', 0, 'A6630', '是（11）', '張巧樂/99%', '2025-11-07', 30, 30, 5, 5),
        (7, '張玲', '5o1033', '麥博韋爾', 1, 'MP5', '是（10）', '張巧樂/100%', '2025-10-30', 100, 100, 5, 5),
        (8, '錢秋蕾', '4D1312-06', '諾基亞', 1, 'GW4 voice', '是（10）', '宋偉勝/99%', '2025-10-30', 100, 100, 3, 3),
        (9, '錢秋蕾', '580713', '移遠', 1, '無', '是', '張巧樂/99%', '2025-09-31', 100, 100, 5, 5),
        (10, '陳穎', '5o2003', '一器是（44）', 0, 'W5110', '是（10）', '柏森，澤康/99%', '2025-11-10', 100, 100, 2, 2),

        # 延遲的專案
        (11, '陳穎', '592302-03', '小米（子）是（45）', 0, 'CE/FCC/NCC/India_IN', '是（11）', '澤康/99%', '2025-11-12', 40, 30, 2, 2),
        (12, '陳穎', '571801-02', 'vivo（子）是（45）', 0, 'PD2529（V2538）', '是（11）', '宋偉勝/99%', '2025-11-12', 40, 6, 3, 3),

        # 新專案（進度較低）
        (13, '王小明', 'TEST001', '華為技術', 1, 'Mate 60 Pro', '否', '陳澤康/20%', '2025-12-20', 120, 24, 2, 2),
        (14, '李美麗', 'TEST002', '三星電子', 1, 'Galaxy S24', '是（5）', '宋偉勝/35%', '2025-12-25', 100, 35, 3, 3),
        (15, '張偉強', 'TEST003', 'SONY', 0, 'Xperia 1 VI', '是（3）', '張巧樂/10%', '2026-01-15', 80, 8, 5, 5),

        # 高優先級專案
        (16, '劉佳慧', 'URGENT-001', 'Apple Inc.', 1, 'iPhone 16 Pro', '是（7）', '陳澤康/60%', '2025-12-10', 150, 90, 2, 2),
        (17, '陳建國', 'URGENT-002', 'Google', 1, 'Pixel 9 Pro', '是（8）', '宋偉勝/75%', '2025-12-15', 140, 105, 3, 3),

        # 長期專案
        (18, '楊淑芬', 'LONG-001', '聯發科技', 1, 'Dimensity 9400', '是（4）', '張巧樂/15%', '2026-02-28', 200, 30, 5, 5),
        (19, '林志明', 'LONG-002', '高通公司', 1, 'Snapdragon 8 Gen 4', '否', '陳澤康/5%', '2026-03-15', 250, 12, 2, 2),
        (20, '黃雅婷', 'LONG-003', '聯想集團', 1, 'ThinkPad X1 Carbon', '是（2）', '宋偉勝/8%', '2026-01-30', 180, 14, 3, 3),

        # 不同狀態的專案（用於測試篩選）
        (21, '周靜怡', 'FILTER-001', '戴爾科技', 1, 'XPS 15', '是（10）', '張巧樂/95%', '2025-11-25', 90, 85, 5, 5),
        (22, '吳文彬', 'FILTER-002', '惠普公司', 0, 'EliteBook 840', '是（6）', '陳澤康/50%', '2025-12-05', 110, 55, 2, 2),
        (23, '鄭美玲', 'FILTER-003', '華碩電腦', 1, 'ROG Zephyrus', '否', '宋偉勝/25%', '2025-12-30', 130, 32, 3, 3),

        # 多樣化客戶專案
        (24, '蔡依林', 'CUST-001', 'LG電子', 1, 'G Flex 4', '是（9）', '張巧樂/88%', '2025-11-20', 95, 83, 5, 5),
        (25, '孫翔宇', 'CUST-002', 'HTC', 1, 'U23 Pro', '是（5）', '陳澤康/42%', '2025-12-12', 105, 44, 2, 2),
        (26, '馬欣怡', 'CUST-003', '中興通訊', 0, 'Axon 60', '是（3）', '宋偉勝/18%', '2026-01-08', 88, 15, 3, 3),

        # 特殊情況專案
        (27, '趙麗穎', 'SPEC-001', '諾基亞（復興）', 1, 'Nokia 9.3', '是（10）', '張巧樂/100%', '2025-10-31', 75, 75, 5, 5),
        (28, '徐若瑄', 'SPEC-002', 'BlackBerry', 1, 'KeyOne 2', '是（7）', '陳澤康/70%', '2025-11-28', 120, 84, 2, 2),
        (29, '梁靜茹', 'SPEC-003', 'OnePlus', 1, '12 Pro', '是（4）', '宋偉勝/38%', '2025-12-18', 98, 37, 3, 3),
        (30, '蔡健雅', 'SPEC-004', 'Realme', 0, 'GT 6 Pro', '否', '張巧樂/12%', '2026-01-22', 85, 10, 5, 5),
    ]

    sql_parts = []
    sql_parts.append("-- 插入專案資料")
    sql_parts.append("""INSERT INTO projects (
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
) VALUES""")

    values = []
    for proj in projects:
        value = f"""({proj[0]}, '{proj[1]}', '{proj[2]}', '{proj[3]}', {proj[4]}, '{proj[5]}', '{proj[6]}', '{proj[7]}', '{proj[8]}', {proj[9]}, {proj[10]}, {proj[11]}, {proj[12]}, 'active', NOW(), NOW())"""
        values.append(value)

    sql_parts.append(',\n'.join(values) + ';')
    sql_parts.append('')

    return '\n'.join(sql_parts)

# ==========================================
# 主函數
# ==========================================

def main():
    """生成完整的測試資料 SQL 腳本"""

    print("正在生成測試資料...")
    print(f"預設密碼：{DEFAULT_PASSWORD}")
    print(f"密碼雜湊方法：{HASH_METHOD}")
    print("-" * 50)

    # 生成密碼雜湊
    password_hash = generate_password_hashes()
    print(f"生成的密碼雜湊：{password_hash[:50]}...")

    # 生成 SQL 文件
    sql_content = []

    # 文件頭
    sql_content.append("-- ==========================================")
    sql_content.append("-- 測試資料 SQL 腳本（自動生成）")
    sql_content.append("-- 實驗室專案進度管制系統")
    sql_content.append(f"-- 生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sql_content.append(f"-- 預設密碼：{DEFAULT_PASSWORD}")
    sql_content.append("-- ==========================================")
    sql_content.append("")

    # 清空現有資料
    sql_content.append("-- 清空現有資料（僅用於開發環境）")
    sql_content.append("SET FOREIGN_KEY_CHECKS = 0;")
    sql_content.append("TRUNCATE TABLE audit_log;")
    sql_content.append("TRUNCATE TABLE projects;")
    sql_content.append("TRUNCATE TABLE users;")
    sql_content.append("SET FOREIGN_KEY_CHECKS = 1;")
    sql_content.append("")

    # 用戶資料
    sql_content.append(generate_users_sql(password_hash))

    # 專案資料
    sql_content.append(generate_projects_sql())

    # 審計日誌
    sql_content.append("-- 插入審計日誌資料")
    sql_content.append("""INSERT INTO audit_log (user_id, action, table_name, record_id, old_values, new_values, timestamp) VALUES
(2, 'CREATE', 'projects', 1, NULL, '{"case_number":"592302","customer":"小米（母）"}', DATE_SUB(NOW(), INTERVAL 30 DAY)),
(2, 'UPDATE', 'projects', 1, '{"actual_hours":60}', '{"actual_hours":80}', DATE_SUB(NOW(), INTERVAL 15 DAY)),
(3, 'CREATE', 'projects', 2, NULL, '{"case_number":"570202-02","customer":"OPPO（子）"}', DATE_SUB(NOW(), INTERVAL 25 DAY)),
(3, 'UPDATE', 'projects', 2, '{"actual_hours":20}', '{"actual_hours":40}', DATE_SUB(NOW(), INTERVAL 10 DAY)),
(5, 'CREATE', 'projects', 5, NULL, '{"case_number":"591905","customer":"摩托羅拉"}', DATE_SUB(NOW(), INTERVAL 20 DAY)),
(2, 'UPDATE', 'projects', 13, '{"actual_hours":0}', '{"actual_hours":24}', DATE_SUB(NOW(), INTERVAL 5 DAY)),
(3, 'UPDATE', 'projects', 14, '{"actual_hours":10}', '{"actual_hours":35}', DATE_SUB(NOW(), INTERVAL 3 DAY)),
(5, 'UPDATE', 'projects', 15, '{"actual_hours":0}', '{"actual_hours":8}', DATE_SUB(NOW(), INTERVAL 2 DAY)),
(2, 'CREATE', 'projects', 16, NULL, '{"case_number":"URGENT-001","customer":"Apple Inc."}', DATE_SUB(NOW(), INTERVAL 7 DAY)),
(1, 'UPDATE', 'users', 2, '{"role":"tester"}', '{"role":"manager"}', DATE_SUB(NOW(), INTERVAL 60 DAY));
""")

    # 重置自動遞增
    sql_content.append("-- 重置自動遞增 ID")
    sql_content.append("ALTER TABLE users AUTO_INCREMENT = 6;")
    sql_content.append("ALTER TABLE projects AUTO_INCREMENT = 31;")
    sql_content.append("ALTER TABLE audit_log AUTO_INCREMENT = 11;")
    sql_content.append("")

    # 驗證查詢
    sql_content.append("""-- 驗證資料
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
""")

    # 寫入文件
    output_file = 'test-data-generated.sql'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_content))

    print("-" * 50)
    print(f"✓ 測試資料已生成到文件：{output_file}")
    print("\n測試帳號信息：")
    print("-" * 50)
    print(f"{'用戶名':<15} {'密碼':<15} {'角色':<10} {'姓名':<15}")
    print("-" * 50)
    print(f"{'admin':<15} {DEFAULT_PASSWORD:<15} {'管理員':<10} {'系統管理員':<15}")
    print(f"{'manager1':<15} {DEFAULT_PASSWORD:<15} {'經理':<10} {'陳澤康':<15}")
    print(f"{'tester1':<15} {DEFAULT_PASSWORD:<15} {'測試員':<10} {'宋偉勝':<15}")
    print(f"{'tester2':<15} {DEFAULT_PASSWORD:<15} {'測試員':<10} {'朱偉勝':<15}")
    print(f"{'tester3':<15} {DEFAULT_PASSWORD:<15} {'測試員':<10} {'張巧樂':<15}")
    print("-" * 50)
    print("\n使用方式：")
    print(f"mysql -u root -p lab_project_dev < {output_file}")
    print("\n" + "=" * 50)

if __name__ == '__main__':
    main()
