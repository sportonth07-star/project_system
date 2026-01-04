# 快速開始指南
## 實驗室專案進度管制系統 - 安全版本與測試資料

---

## 📦 文件清單

您現在擁有以下文件：

1. **[PRD.md](PRD.md)** - 產品需求文檔（MySQL + 繁體中文）
2. **[plan.md](plan.md)** - 實施計劃（10週詳細計劃）
3. **[security-guide.md](security-guide.md)** - 完整安全開發指南
4. **[SECURITY-README.md](SECURITY-README.md)** - 安全實施摘要
5. **[test-data.sql](test-data.sql)** - 測試資料 SQL 模板
6. **[generate_test_data.py](generate_test_data.py)** - 測試資料生成腳本
7. **[QUICK-START.md](QUICK-START.md)** - 本文件

---

## 🚀 快速開始步驟

### 步驟 1：準備 MySQL 資料庫

```bash
# 登入 MySQL
mysql -u root -p

# 創建資料庫（開發環境）
CREATE DATABASE lab_project_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 創建資料庫（生產環境）
CREATE DATABASE lab_project_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 創建專用用戶（可選，推薦）
CREATE USER 'labuser'@'localhost' IDENTIFIED BY 'YourSecurePassword123!';
GRANT ALL PRIVILEGES ON lab_project_dev.* TO 'labuser'@'localhost';
GRANT ALL PRIVILEGES ON lab_project_prod.* TO 'labuser'@'localhost';
FLUSH PRIVILEGES;

# 退出
EXIT;
```

### 步驟 2：創建資料庫表結構

使用 PRD.md 中的 SQL 創建表：

```bash
# 創建 tables.sql 文件
cat > tables.sql << 'EOF'
-- 用戶表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    failed_login_attempts INT DEFAULT 0,
    locked_until TIMESTAMP NULL,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 專案表
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_number INT UNIQUE NOT NULL,
    personnel VARCHAR(100) NOT NULL,
    case_number VARCHAR(50) NOT NULL,
    customer VARCHAR(100) NOT NULL,
    evidence_required TINYINT(1) NOT NULL,
    model VARCHAR(100),
    samples_complete VARCHAR(20),
    engineer_progress VARCHAR(200) NOT NULL,
    expected_report_date DATE NOT NULL,
    estimated_hours INT NOT NULL,
    actual_hours INT NOT NULL DEFAULT 0,
    remaining_hours INT GENERATED ALWAYS AS (estimated_hours - actual_hours) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    status VARCHAR(20) DEFAULT 'active',
    INDEX idx_case_number (case_number),
    INDEX idx_personnel (personnel),
    INDEX idx_expected_date (expected_report_date),
    INDEX idx_status (status),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 審計日誌表
CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id INT NOT NULL,
    old_values TEXT,
    new_values TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_timestamp (timestamp),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
EOF

# 導入表結構
mysql -u root -p lab_project_dev < tables.sql
```

### 步驟 3：生成並導入測試資料

**方法 A：使用 Python 腳本（推薦）**

```bash
# 安裝 Werkzeug（如果還沒安裝）
pip install Werkzeug

# 運行生成腳本
python generate_test_data.py

# 導入生成的資料
mysql -u root -p lab_project_dev < test-data-generated.sql
```

**方法 B：手動更新密碼雜湊**

```bash
# 1. 生成密碼雜湊
python << 'EOF'
from werkzeug.security import generate_password_hash
password = 'Test@123'
hash_value = generate_password_hash(password, method='pbkdf2:sha256:260000')
print(f"密碼雜湊值：{hash_value}")
EOF

# 2. 複製雜湊值，然後編輯 test-data.sql
# 3. 將所有 'pbkdf2:sha256:260000$salt$hash' 替換為實際的雜湊值
# 4. 導入資料
mysql -u root -p lab_project_dev < test-data.sql
```

### 步驟 4：驗證資料

```bash
mysql -u root -p lab_project_dev

# 檢查資料
SELECT 'Users' AS table_name, COUNT(*) AS count FROM users
UNION ALL
SELECT 'Projects', COUNT(*) FROM projects
UNION ALL
SELECT 'Audit Logs', COUNT(*) FROM audit_log;

# 查看用戶
SELECT id, username, full_name, role FROM users;

# 查看專案統計
SELECT
    CASE
        WHEN actual_hours >= estimated_hours THEN '已完成'
        WHEN actual_hours / estimated_hours >= 0.8 THEN '進度良好'
        WHEN actual_hours / estimated_hours >= 0.4 THEN '進行中'
        ELSE '進度落後'
    END AS status,
    COUNT(*) AS count
FROM projects
GROUP BY status;
```

---

## 👥 測試帳號

| 用戶名 | 密碼 | 角色 | 用途 |
|--------|------|------|------|
| `admin` | `Test@123` | 管理員 | 完整系統訪問權限 |
| `manager1` | `Test@123` | 經理 | 查看所有專案，編輯指派專案 |
| `tester1` | `Test@123` | 測試員 | 查看和更新指派的工單 |
| `tester2` | `Test@123` | 測試員 | 查看和更新指派的工單 |
| `tester3` | `Test@123` | 測試員 | 查看和更新指派的工單 |

**⚠️ 重要：** 在生產環境部署前，必須更改所有測試密碼！

---

## 🔒 安全功能速覽

### 已實施的安全措施

#### 1. XSS 防護 ✅
- Jinja2 自動轉義
- HTML 輸入淨化
- Content Security Policy
- 安全 JavaScript 工具類

#### 2. SQL 注入防護 ✅
- SQLAlchemy ORM
- 參數化查詢
- 輸入驗證

#### 3. CSRF 防護 ✅
- Flask-WTF CSRF token
- 所有表單和 AJAX 請求保護
- CSRFHandler 自動處理

#### 4. 身份驗證安全 ✅
- 強密碼策略（8+ 字符，包含大小寫、數字、特殊字符）
- 密碼雜湊（pbkdf2:sha256:260000）
- 帳戶鎖定（5 次失敗後鎖定 30 分鐘）
- 安全會話管理

#### 5. 訪問控制 ✅
- 角色基礎訪問控制（RBAC）
- 資源級授權
- 裝飾器保護路由

#### 6. 審計日誌 ✅
- 所有 CRUD 操作記錄
- 登入/登出記錄
- 變更追蹤

---

## 🧪 測試安全功能

### 測試 XSS 防護

```javascript
// 在任何輸入欄位嘗試這些
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
javascript:alert('XSS')

// 預期結果：輸入被轉義或拒絕
```

### 測試 SQL 注入防護

```sql
-- 在搜尋欄位嘗試這些
' OR '1'='1
admin'--
1'; DROP TABLE projects; --

-- 預期結果：查詢失敗或返回空結果
```

### 測試帳戶鎖定

```
1. 使用 admin 帳號
2. 連續輸入 5 次錯誤密碼
3. 預期結果：帳戶被鎖定 30 分鐘
4. 30 分鐘後可以再次登入
```

### 測試密碼強度

```python
# 運行 Python 測試
python << 'EOF'
from werkzeug.security import generate_password_hash

# 測試弱密碼（應該被拒絕）
weak_passwords = ['password', '12345678', 'abc123', 'qwerty']

# 測試強密碼（應該被接受）
strong_password = 'Test@123'

print("弱密碼測試:")
for pwd in weak_passwords:
    print(f"  {pwd} - 應該被拒絕")

print(f"\n強密碼測試:")
print(f"  {strong_password} - 應該被接受")
print(f"  雜湊值長度: {len(generate_password_hash(strong_password))}")
EOF
```

---

## 📁 專案結構（建議）

實施時，建議使用以下結構：

```
lab-project-manager/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── user.py
│   │   └── audit_log.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── projects.py
│   │   └── api.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── project_service.py
│   │   └── analytics_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py        # 安全工具
│   │   ├── validators.py      # 驗證器
│   │   └── decorators.py      # 裝飾器
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   │       └── security.js    # SecurityHelper 類
│   └── templates/
├── config.py                   # 配置文件
├── requirements.txt           # 依賴
├── run.py                     # 入口點
└── logs/                      # 日誌目錄
```

---

## 🔧 開發環境設置

### 1. 安裝 Python 依賴

```bash
# 創建虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安裝依賴
pip install Flask==2.3.0
pip install Flask-SQLAlchemy==3.0.5
pip install Flask-Login==0.6.2
pip install Flask-WTF==1.1.1
pip install Flask-Migrate==4.0.4
pip install python-dotenv==1.0.0
pip install Werkzeug==2.3.0
pip install PyMySQL==1.1.0
pip install cryptography==41.0.0
pip install Flask-Limiter==3.3.1
pip install python-magic==0.4.27
pip install bleach==6.0.0
```

### 2. 環境變數配置

創建 `.env` 文件：

```bash
# Flask 配置
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-very-secure-secret-key-change-this

# 資料庫配置
DATABASE_URL=mysql+pymysql://labuser:YourSecurePassword123!@localhost:3306/lab_project_dev?charset=utf8mb4

# 會話配置
SESSION_TYPE=filesystem
PERMANENT_SESSION_LIFETIME=1800

# 安全配置
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=None
```

### 3. 初始化資料庫遷移

```bash
# 初始化遷移
flask db init

# 創建遷移
flask db migrate -m "Initial migration"

# 應用遷移
flask db upgrade
```

### 4. 運行開發伺服器

```bash
# 運行 Flask 開發伺服器
python run.py

# 或使用 flask 命令
flask run
```

---

## 📊 測試資料概覽

### 專案統計

生成的測試資料包含：

- **30 個專案**，涵蓋不同狀態：
  - 已完成：7 個 (23%)
  - 進度良好（80%+）：8 個 (27%)
  - 進行中（40-79%）：6 個 (20%)
  - 進度落後（<40%）：7 個 (23%)
  - 延遲專案：2 個 (7%)

- **多樣化的客戶**：
  - 小米、OPPO、華為、三星、Apple
  - Google、SONY、LG、HTC 等

- **不同的工程師分配**：
  - 陳澤康、宋偉勝、張巧樂
  - 蔣志豪、胡浩等

### 測試場景

資料設計支援以下測試場景：

1. **搜尋和篩選**
   - 按人員搜尋
   - 按案號搜尋
   - 按客戶篩選
   - 按日期範圍篩選

2. **排序**
   - 按進度排序
   - 按日期排序
   - 按工時排序

3. **視覺化**
   - 狀態分佈圓餅圖
   - 人員工作量長條圖
   - 進度追蹤
   - 逾期提醒

4. **權限測試**
   - 不同角色訪問控制
   - 資源級授權
   - 審計追蹤

---

## 🔍 常見問題

### Q1: 如何重置測試資料？

```bash
# 方法 1：刪除並重新導入
mysql -u root -p lab_project_dev << 'EOF'
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE audit_log;
TRUNCATE TABLE projects;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;
EOF

# 重新導入
python generate_test_data.py
mysql -u root -p lab_project_dev < test-data-generated.sql

# 方法 2：刪除並重建資料庫
mysql -u root -p << 'EOF'
DROP DATABASE lab_project_dev;
CREATE DATABASE lab_project_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EOF

# 重新創建表和資料
mysql -u root -p lab_project_dev < tables.sql
mysql -u root -p lab_project_dev < test-data-generated.sql
```

### Q2: 忘記測試帳號密碼怎麼辦？

所有測試帳號的預設密碼都是：`Test@123`

如需重置，可以直接重新導入測試資料，或手動更新：

```bash
python << 'EOF'
from werkzeug.security import generate_password_hash
new_password = 'NewPassword@123'
hash_value = generate_password_hash(new_password, method='pbkdf2:sha256:260000')
print(f"UPDATE users SET password_hash = '{hash_value}' WHERE username = 'admin';")
EOF
```

### Q3: 如何添加新的測試用戶？

```bash
python << 'EOF'
from werkzeug.security import generate_password_hash

# 用戶信息
username = 'newuser'
password = 'SecurePass@123'
full_name = '新用戶'
email = 'newuser@lab.com'
role = 'tester'

# 生成雜湊
password_hash = generate_password_hash(password, method='pbkdf2:sha256:260000')

# 生成 SQL
sql = f"""
INSERT INTO users (username, password_hash, full_name, email, role, created_at)
VALUES ('{username}', '{password_hash}', '{full_name}', '{email}', '{role}', NOW());
"""

print(sql)
EOF

# 複製輸出的 SQL 並執行
```

### Q4: 如何檢查安全配置是否正確？

```bash
# 檢查 MySQL 字符集
mysql -u root -p -e "SHOW VARIABLES LIKE 'character_set%';"

# 檢查表結構
mysql -u root -p lab_project_dev -e "SHOW CREATE TABLE projects\G"

# 檢查索引
mysql -u root -p lab_project_dev -e "SHOW INDEX FROM projects;"

# 檢查外鍵
mysql -u root -p lab_project_dev -e "
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'lab_project_dev'
AND REFERENCED_TABLE_NAME IS NOT NULL;
"
```

---

## 📚 下一步

1. **閱讀文檔**：
   - [PRD.md](PRD.md) - 了解完整需求
   - [security-guide.md](security-guide.md) - 學習安全實踐
   - [plan.md](plan.md) - 查看實施計劃

2. **開始開發**：
   - 按照 plan.md 的 Phase 1 開始
   - 實施安全措施（參考 security-guide.md）
   - 使用測試資料進行開發測試

3. **安全測試**：
   - 執行 SECURITY-README.md 中的安全測試
   - 使用 OWASP ZAP 進行掃描
   - 執行依賴漏洞掃描

4. **部署準備**：
   - 更改所有預設密碼
   - 配置生產資料庫
   - 設置 HTTPS
   - 執行完整測試

---

## ⚠️ 重要安全提醒

1. **測試密碼僅用於開發環境**
   - 密碼：`Test@123`
   - 生產環境必須使用強密碼

2. **資料庫安全**
   - 生產環境使用專用資料庫用戶
   - 限制資料庫訪問權限
   - 定期備份

3. **環境隔離**
   - 開發、測試、生產環境分離
   - 不同環境使用不同密鑰
   - 敏感資訊存儲在環境變數中

4. **定期維護**
   - 更新依賴套件
   - 審查安全日誌
   - 執行安全掃描

---

## 📞 支援

如有問題，請參考：
- [SECURITY-README.md](SECURITY-README.md) - 安全實施詳情
- [security-guide.md](security-guide.md) - 完整安全指南
- [plan.md](plan.md) - 實施計劃

---

**文檔版本**：1.0
**最後更新**：2025-12-30
**狀態**：就緒可用
