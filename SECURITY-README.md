# 安全實施摘要
## 實驗室專案進度管制系統

---

## 📋 文檔概覽

本專案包含完整的安全措施和測試資料：

1. **[security-guide.md](security-guide.md)** - 完整的安全開發指南
2. **[test-data.sql](test-data.sql)** - 測試資料 SQL 腳本模板
3. **[generate_test_data.py](generate_test_data.py)** - 測試資料生成腳本（含正確密碼雜湊）

---

## 🔐 已實施的安全措施

### 1. XSS（跨站腳本）防護

#### ✅ 實施措施

**後端防護：**
- Flask Jinja2 自動轉義所有輸出
- 使用 `bleach` 庫淨化 HTML 輸入
- 自定義驗證器檢查危險模式
- 禁止 `<script>` 標籤和事件處理器

**前端防護：**
```javascript
// SecurityHelper 類提供
- escapeHtml() - HTML 編碼
- setTextContent() - 安全文本插入
- createSafeElement() - 安全 DOM 創建
- sanitizeUrl() - URL 清理
```

**HTTP 標頭：**
```python
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.jsdelivr.net
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
```

**測試方法：**
```html
<!-- 嘗試以下輸入測試 XSS 防護 -->
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
javascript:alert('XSS')
```

---

### 2. SQL 注入防護

#### ✅ 實施措施

**ORM 使用：**
- 所有資料庫操作使用 SQLAlchemy ORM
- 參數化查詢，避免字串拼接
- 輸入驗證和類型檢查

**示例（安全）：**
```python
# 正確：使用 ORM
Project.query.filter(Project.case_number.like(f'%{search_term}%')).all()

# 正確：使用參數綁定
sql = text("SELECT * FROM projects WHERE case_number = :case_num")
db.session.execute(sql, {'case_num': case_number})
```

**示例（不安全 - 禁止）：**
```python
# 錯誤：字串拼接
query = f"SELECT * FROM projects WHERE case_number LIKE '%{search_term}%'"
db.session.execute(query).fetchall()
```

**測試方法：**
```sql
-- 嘗試以下輸入測試 SQL 注入防護
' OR '1'='1
'; DROP TABLE projects; --
1' UNION SELECT * FROM users--
```

---

### 3. CSRF（跨站請求偽造）防護

#### ✅ 實施措施

**Flask-WTF CSRF：**
- 所有表單自動包含 CSRF token
- AJAX 請求攜帶 CSRF token
- CSRFHandler 類自動處理

**HTML 表單：**
```html
<form method="POST">
    {{ form.hidden_tag() }}  <!-- 自動插入 CSRF token -->
    <!-- 表單欄位 -->
</form>
```

**JavaScript AJAX：**
```javascript
// 自動為所有請求添加 CSRF token
CSRFHandler.setupAjax();

// 或使用安全 fetch
await CSRFHandler.secureFetch('/api/projects', {
    method: 'POST',
    body: JSON.stringify(data)
});
```

**測試方法：**
1. 嘗試不帶 CSRF token 提交表單
2. 使用過期的 CSRF token
3. 跨域請求測試

---

### 4. 身份驗證安全

#### ✅ 實施措施

**密碼強度要求：**
- 最小長度：8 個字符
- 必須包含：大寫字母、小寫字母、數字、特殊字符
- 禁止常見弱密碼

**密碼儲存：**
```python
# 使用 pbkdf2:sha256 with 260,000 iterations
password_hash = generate_password_hash(password, method='pbkdf2:sha256:260000')
```

**帳戶鎖定：**
- 5 次失敗登入後鎖定 30 分鐘
- 記錄所有登入嘗試
- 不洩露用戶是否存在

**會話安全：**
```python
SESSION_COOKIE_SECURE = True      # 僅 HTTPS
SESSION_COOKIE_HTTPONLY = True    # 防止 JavaScript 訪問
SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF 保護
PERMANENT_SESSION_LIFETIME = 30分鐘
```

---

### 5. 授權與訪問控制

#### ✅ 實施措施

**角色基礎訪問控制（RBAC）：**
- Admin：完全訪問
- Manager：查看所有專案，編輯指派的專案
- Tester：查看和更新指派的工單

**裝飾器：**
```python
@admin_required
def manage_users():
    # 僅管理員可訪問
    pass

@role_required('manager', 'admin')
def view_all_projects():
    # 經理和管理員可訪問
    pass
```

**資源級授權：**
```python
# 檢查用戶是否為專案創建者或管理員
if current_user.id != project.created_by and current_user.role != 'admin':
    abort(403)
```

---

### 6. 文件上傳安全

#### ✅ 實施措施

**文件驗證：**
- 檢查文件擴展名
- 驗證 MIME 類型（使用 python-magic）
- 限制文件大小（10MB）
- 使用 `secure_filename()`

**允許的文件類型：**
- 文檔：xlsx, xls, csv, pdf
- 圖片：png, jpg, jpeg

**安全保存：**
```python
# 生成唯一文件名（使用 MD5 雜湊）
file_hash = hashlib.md5(file.read()).hexdigest()
unique_filename = f"{file_hash}.{file_ext}"
```

---

### 7. API 安全

#### ✅ 實施措施

**速率限制：**
```python
# 使用 Flask-Limiter
@limiter.limit("10 per minute")
def create_project():
    pass

@limiter.limit("5 per minute")
def login():
    pass
```

**API Token 認證：**
- 安全的 token 生成（`secrets.token_urlsafe(32)`）
- Token 雜湊儲存
- Token 過期機制
- 最後使用時間追蹤

---

### 8. 日誌與監控

#### ✅ 實施措施

**日誌類型：**
- 應用日誌：`logs/app.log`
- 安全日誌：`logs/security.log`
- 審計日誌：資料庫 `audit_log` 表

**記錄事件：**
- 所有登入/登出
- 失敗的登入嘗試
- CRUD 操作（審計日誌）
- 訪問被拒絕
- 系統錯誤

**日誌輪轉：**
- 最大大小：10MB
- 保留備份：10 個文件

---

## 🧪 測試資料

### 生成測試資料

**方法 1：使用 Python 腳本（推薦）**
```bash
# 生成包含正確密碼雜湊的 SQL 文件
python generate_test_data.py

# 導入到資料庫
mysql -u root -p lab_project_dev < test-data-generated.sql
```

**方法 2：直接使用 SQL 模板**
```bash
# 注意：需要手動更新密碼雜湊值
mysql -u root -p lab_project_dev < test-data.sql
```

### 測試帳號

| 用戶名 | 密碼 | 角色 | 姓名 | 電子郵件 |
|--------|------|------|------|----------|
| admin | Test@123 | 管理員 | 系統管理員 | admin@lab.com |
| manager1 | Test@123 | 經理 | 陳澤康 | chen@lab.com |
| tester1 | Test@123 | 測試員 | 宋偉勝 | song@lab.com |
| tester2 | Test@123 | 測試員 | 朱偉勝 | zhu@lab.com |
| tester3 | Test@123 | 測試員 | 張巧樂 | zhang@lab.com |

### 測試資料統計

- **用戶數量**：5 個
- **專案數量**：30 個
  - 已完成：7 個
  - 進度良好：8 個
  - 進行中：6 個
  - 進度落後：7 個
  - 延遲：2 個
- **審計日誌**：10 條記錄

---

## 🔍 安全測試指南

### 1. XSS 測試

**測試用例：**
```javascript
// 在任何輸入欄位嘗試
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<iframe src="javascript:alert('XSS')">
<svg onload=alert('XSS')>
```

**預期結果：**
- 輸入被轉義或拒絕
- 不執行腳本
- 在頁面源碼中看到 `&lt;script&gt;` 而非 `<script>`

### 2. SQL 注入測試

**測試用例：**
```sql
-- 在搜尋欄位嘗試
' OR '1'='1
admin'--
' UNION SELECT * FROM users--
1'; DROP TABLE projects; --
```

**預期結果：**
- 查詢失敗或返回空結果
- 不執行注入的 SQL
- 資料庫表未被修改

### 3. CSRF 測試

**測試步驟：**
1. 開啟瀏覽器開發者工具
2. 找到 CSRF token（在 meta 標籤或隱藏欄位中）
3. 刪除或修改 token
4. 提交表單

**預期結果：**
- 請求被拒絕
- 返回 400 或 403 錯誤
- 顯示 CSRF token 錯誤訊息

### 4. 身份驗證測試

**測試用例：**
```
1. 使用錯誤密碼登入 5 次
   預期：帳戶被鎖定 30 分鐘

2. 使用弱密碼註冊
   預期：拒絕並顯示密碼要求

3. 嘗試訪問未授權資源
   預期：重定向到登入頁或 403 錯誤

4. 會話過期測試
   預期：30 分鐘後自動登出
```

### 5. 授權測試

**測試用例：**
```
1. 以 tester 角色訪問管理員頁面
   預期：403 Forbidden

2. 嘗試編輯其他用戶的專案
   預期：403 Forbidden（除非是管理員）

3. 使用 API token 訪問資源
   預期：僅能訪問授權的資源
```

### 6. 文件上傳測試

**測試用例：**
```
1. 上傳 .exe 文件
   預期：拒絕（不允許的文件類型）

2. 上傳超過 10MB 的文件
   預期：拒絕（文件過大）

3. 上傳偽裝的文件（.txt 重命名為 .xlsx）
   預期：拒絕（MIME 類型不匹配）

4. 上傳包含腳本的 SVG
   預期：拒絕或淨化
```

---

## 🛡️ 安全檢查清單

### 開發環境

- [x] 所有密碼使用強雜湊算法
- [x] 啟用 CSRF 保護
- [x] 實施 XSS 防護
- [x] 使用參數化查詢
- [x] 實施輸入驗證
- [x] 實施輸出編碼
- [x] 配置安全標頭
- [x] 實施速率限制
- [x] 實施訪問控制
- [x] 實施審計日誌

### 部署前檢查

- [ ] 更改所有預設密碼
- [ ] 禁用 Flask 調試模式（`DEBUG = False`）
- [ ] 配置 HTTPS/SSL 證書
- [ ] 設置強 `SECRET_KEY`
- [ ] 配置生產資料庫
- [ ] 設置防火牆規則
- [ ] 配置日誌輪轉
- [ ] 執行安全掃描
- [ ] 執行依賴漏洞掃描
- [ ] 配置備份策略

### 生產環境

- [ ] 監控系統日誌
- [ ] 設置入侵檢測
- [ ] 定期安全審計
- [ ] 定期更新依賴
- [ ] 定期備份資料庫
- [ ] 定期審查訪問日誌
- [ ] 定期測試災難恢復
- [ ] 保持系統更新

---

## 🔧 安全工具

### 推薦使用的工具

**1. 靜態代碼分析：**
```bash
# Bandit - Python 安全檢查
pip install bandit
bandit -r app/

# Safety - 依賴漏洞掃描
pip install safety
safety check

# pip-audit - 官方依賴審計
pip install pip-audit
pip-audit
```

**2. 動態應用掃描：**
- OWASP ZAP - Web 應用安全掃描
- Burp Suite - 滲透測試
- SQLMap - SQL 注入測試

**3. 依賴管理：**
```bash
# 檢查過時的依賴
pip list --outdated

# 更新依賴
pip install --upgrade <package>
```

**4. 密碼測試：**
```bash
# 測試密碼強度
python -c "from app.models.user import User; print(User.validate_password_strength('your_password'))"
```

---

## 📚 參考資源

### OWASP 資源
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

### Flask 安全
- [Flask Security](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Flask-WTF CSRF Protection](https://flask-wtf.readthedocs.io/en/stable/csrf.html)
- [Flask-Login](https://flask-login.readthedocs.io/)

### Python 安全
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [PEP 543 - A Unified TLS API](https://www.python.org/dev/peps/pep-0543/)

---

## 📝 安全更新日誌

### v1.0 (2025-12-30)
- ✅ 實施 XSS 防護
- ✅ 實施 SQL 注入防護
- ✅ 實施 CSRF 防護
- ✅ 實施強密碼策略
- ✅ 實施 RBAC 訪問控制
- ✅ 實施文件上傳驗證
- ✅ 實施 API 速率限制
- ✅ 實施安全標頭
- ✅ 實施審計日誌
- ✅ 創建安全開發指南
- ✅ 創建測試資料生成器

---

## ⚠️ 重要提醒

1. **生產環境部署前**：
   - 必須更改所有預設密碼
   - 必須配置 HTTPS
   - 必須禁用調試模式
   - 必須執行完整的安全測試

2. **定期維護**：
   - 每週檢查安全日誌
   - 每月更新依賴
   - 每季度進行安全審計
   - 定期備份資料庫

3. **事件響應**：
   - 建立安全事件響應計劃
   - 保持聯繫方式更新
   - 定期進行災難恢復演練

---

**文檔版本**：1.0
**最後更新**：2025-12-30
**維護者**：開發團隊
**狀態**：已完成
