# 安全開發指南 (Security Development Guide)
## 實驗室專案進度管制系統

---

## 目錄
1. [安全概述](#安全概述)
2. [XSS 防護](#xss-防護)
3. [SQL 注入防護](#sql-注入防護)
4. [CSRF 防護](#csrf-防護)
5. [身份驗證安全](#身份驗證安全)
6. [授權與訪問控制](#授權與訪問控制)
7. [文件上傳安全](#文件上傳安全)
8. [API 安全](#api-安全)
9. [日誌與監控](#日誌與監控)
10. [安全檢查清單](#安全檢查清單)

---

## 安全概述

### OWASP Top 10 防護策略

本系統實現以下 OWASP Top 10 安全措施：

1. **注入攻擊防護** - SQL 注入、命令注入
2. **失效的身份驗證** - 強密碼策略、會話管理
3. **敏感資料外洩** - 加密、安全傳輸
4. **XML 外部處理器 (XXE)** - 禁用外部實體
5. **失效的訪問控制** - RBAC 實現
6. **安全配置錯誤** - 安全預設值
7. **跨站腳本 (XSS)** - 輸入驗證、輸出編碼
8. **不安全的反序列化** - 安全序列化
9. **使用已知漏洞的組件** - 依賴掃描
10. **日誌與監控不足** - 完整審計日誌

---

## XSS 防護

### 1. 輸出編碼 (Output Encoding)

#### Flask 模板自動轉義
```python
# app/__init__.py
from flask import Flask
from markupsafe import escape

def create_app():
    app = Flask(__name__)

    # Jinja2 預設啟用自動轉義
    app.jinja_env.autoescape = True

    return app
```

#### HTML 模板中的安全輸出
```html
<!-- app/templates/projects/list.html -->
<!-- 安全：Jinja2 自動轉義 -->
<td>{{ project.personnel }}</td>
<td>{{ project.case_number }}</td>
<td>{{ project.customer }}</td>

<!-- 如需原始 HTML（謹慎使用） -->
{% autoescape false %}
    {{ trusted_html_content }}
{% endautoescape %}

<!-- 或使用 safe 過濾器（僅用於可信內容） -->
{{ trusted_content|safe }}
```

#### JavaScript 中的 XSS 防護
```javascript
// app/static/js/security.js
class SecurityHelper {
    /**
     * HTML 編碼函數
     */
    static escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    /**
     * 安全地插入文本內容
     */
    static setTextContent(element, text) {
        element.textContent = text; // 使用 textContent 而非 innerHTML
    }

    /**
     * 安全地創建 DOM 元素
     */
    static createSafeElement(tagName, attributes, textContent) {
        const element = document.createElement(tagName);

        // 設置屬性
        for (const [key, value] of Object.entries(attributes || {})) {
            element.setAttribute(key, this.escapeHtml(value));
        }

        // 設置文本內容
        if (textContent) {
            element.textContent = textContent;
        }

        return element;
    }

    /**
     * 清理 URL 以防止 javascript: 協議
     */
    static sanitizeUrl(url) {
        const sanitized = url.trim().toLowerCase();
        if (sanitized.startsWith('javascript:') ||
            sanitized.startsWith('data:') ||
            sanitized.startsWith('vbscript:')) {
            return 'about:blank';
        }
        return url;
    }
}

// 使用示例
const userInput = '<script>alert("XSS")</script>';
const safeHtml = SecurityHelper.escapeHtml(userInput);
document.getElementById('output').textContent = safeHtml;
```

### 2. Content Security Policy (CSP)

```python
# app/utils/security.py
from flask import Response

def add_security_headers(response):
    """添加安全標頭到響應"""

    # Content Security Policy
    csp = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net; "
        "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://cdn.jsdelivr.net; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self';"
    )
    response.headers['Content-Security-Policy'] = csp

    # X-Content-Type-Options
    response.headers['X-Content-Type-Options'] = 'nosniff'

    # X-Frame-Options
    response.headers['X-Frame-Options'] = 'DENY'

    # X-XSS-Protection
    response.headers['X-XSS-Protection'] = '1; mode=block'

    # Referrer-Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

    # Permissions-Policy
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

    return response

# 在 Flask app 中註冊
def create_app():
    app = Flask(__name__)

    @app.after_request
    def apply_security_headers(response):
        return add_security_headers(response)

    return app
```

### 3. 輸入驗證與淨化

```python
# app/utils/validators.py
import re
from wtforms.validators import ValidationError
import bleach

class SecureValidator:
    """安全驗證器類"""

    # 允許的 HTML 標籤（用於富文本編輯器，如果需要）
    ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u']
    ALLOWED_ATTRIBUTES = {}

    @staticmethod
    def sanitize_html(html_content):
        """淨化 HTML 內容"""
        return bleach.clean(
            html_content,
            tags=SecureValidator.ALLOWED_TAGS,
            attributes=SecureValidator.ALLOWED_ATTRIBUTES,
            strip=True
        )

    @staticmethod
    def validate_alphanumeric(form, field):
        """驗證只包含字母數字和允許的字符"""
        if not re.match(r'^[a-zA-Z0-9\u4e00-\u9fff_\-\s]+$', field.data):
            raise ValidationError('只允許字母、數字、中文、底線、連字符和空格')

    @staticmethod
    def validate_no_script_tags(form, field):
        """驗證不包含腳本標籤"""
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'onerror\s*=',
            r'onclick\s*=',
            r'onload\s*='
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, field.data, re.IGNORECASE):
                raise ValidationError('檢測到不安全的內容')

    @staticmethod
    def validate_case_number(form, field):
        """驗證案號格式"""
        # 案號格式：字母數字和連字符，長度 3-50
        if not re.match(r'^[A-Z0-9\-]{3,50}$', field.data):
            raise ValidationError('案號格式不正確（只允許大寫字母、數字和連字符，長度 3-50）')

# 表單中使用
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class ProjectForm(FlaskForm):
    case_number = StringField('案號', validators=[
        DataRequired(message='案號為必填'),
        Length(min=3, max=50, message='案號長度必須在 3-50 之間'),
        SecureValidator.validate_case_number
    ])

    personnel = StringField('業務人員', validators=[
        DataRequired(message='業務人員為必填'),
        SecureValidator.validate_alphanumeric,
        SecureValidator.validate_no_script_tags
    ])

    customer = StringField('客戶', validators=[
        DataRequired(message='客戶為必填'),
        SecureValidator.validate_alphanumeric,
        SecureValidator.validate_no_script_tags
    ])
```

---

## SQL 注入防護

### 1. 使用 ORM (SQLAlchemy)

```python
# app/models/project.py
from app import db
from sqlalchemy import text

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(50), nullable=False)
    # ... 其他欄位

    @staticmethod
    def safe_search(search_term):
        """安全的搜尋方法 - 使用參數化查詢"""
        # 正確：使用參數綁定
        return Project.query.filter(
            Project.case_number.like(f'%{search_term}%')
        ).all()

        # 錯誤：字串拼接（易受 SQL 注入攻擊）
        # query = f"SELECT * FROM projects WHERE case_number LIKE '%{search_term}%'"
        # return db.session.execute(query).fetchall()

    @staticmethod
    def safe_raw_query(case_number):
        """如果必須使用原始 SQL，使用參數綁定"""
        # 正確：使用參數綁定
        sql = text("SELECT * FROM projects WHERE case_number = :case_num")
        result = db.session.execute(sql, {'case_num': case_number})
        return result.fetchall()
```

### 2. 輸入驗證與過濾

```python
# app/services/project_service.py
from sqlalchemy import and_, or_
import re

class ProjectService:

    @staticmethod
    def search_projects(filters):
        """安全的搜尋方法"""
        query = Project.query.filter_by(status='active')

        # 驗證和淨化輸入
        if 'case_number' in filters:
            case_number = filters['case_number'].strip()
            # 驗證格式
            if re.match(r'^[A-Z0-9\-]{1,50}$', case_number):
                query = query.filter(Project.case_number.like(f'%{case_number}%'))

        if 'personnel' in filters:
            personnel = filters['personnel'].strip()
            # 限制長度和字符
            if len(personnel) <= 100 and re.match(r'^[\w\u4e00-\u9fff\s\-]+$', personnel):
                query = query.filter(Project.personnel.like(f'%{personnel}%'))

        return query.all()

    @staticmethod
    def get_by_id(project_id):
        """安全地通過 ID 獲取專案"""
        # 確保 ID 是整數
        try:
            project_id = int(project_id)
        except (ValueError, TypeError):
            return None

        return Project.query.get(project_id)
```

---

## CSRF 防護

### 1. Flask-WTF CSRF 保護

```python
# app/__init__.py
from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'

    # 啟用 CSRF 保護
    csrf.init_app(app)

    # CSRF 配置
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = None  # 或設置為秒數
    app.config['WTF_CSRF_SSL_STRICT'] = True  # HTTPS 環境中強制執行

    return app
```

### 2. 表單中的 CSRF Token

```html
<!-- app/templates/projects/create.html -->
<form method="POST" action="/projects/create">
    <!-- CSRF Token -->
    {{ form.hidden_tag() }}

    <div class="mb-3">
        <label for="case_number" class="form-label">案號</label>
        {{ form.case_number(class="form-control") }}
    </div>

    <button type="submit" class="btn btn-primary">提交</button>
</form>
```

### 3. AJAX 請求中的 CSRF Token

```html
<!-- app/templates/base.html -->
<head>
    <meta name="csrf-token" content="{{ csrf_token() }}">
</head>
```

```javascript
// app/static/js/csrf.js
class CSRFHandler {
    static getToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    static setupAjax() {
        // 為所有 AJAX 請求添加 CSRF token
        const token = this.getToken();

        // Fetch API
        const originalFetch = window.fetch;
        window.fetch = function(url, options = {}) {
            if (!options.headers) {
                options.headers = {};
            }
            options.headers['X-CSRFToken'] = token;
            return originalFetch(url, options);
        };
    }

    static async secureFetch(url, options = {}) {
        const token = this.getToken();

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            credentials: 'same-origin'
        };

        const mergedOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };

        return fetch(url, mergedOptions);
    }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    CSRFHandler.setupAjax();
});

// 使用示例
async function createProject(projectData) {
    try {
        const response = await CSRFHandler.secureFetch('/api/projects', {
            method: 'POST',
            body: JSON.stringify(projectData)
        });

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}
```

### 4. API 端點 CSRF 豁免（謹慎使用）

```python
# app/routes/api.py
from flask import Blueprint, jsonify, request
from flask_wtf.csrf import csrf_exempt
from app.utils.decorators import token_required

api_bp = Blueprint('api', __name__)

# 對於使用 Token 認證的 API，可以豁免 CSRF
@api_bp.route('/api/external', methods=['POST'])
@csrf_exempt
@token_required  # 使用其他認證機制
def external_api():
    """外部 API 端點（使用 Token 認證）"""
    data = request.get_json()
    # 處理邏輯
    return jsonify({'status': 'success'})

# 內部 API 仍然需要 CSRF 保護
@api_bp.route('/api/projects', methods=['POST'])
def create_project():
    """內部 API（需要 CSRF token）"""
    data = request.get_json()
    # 處理邏輯
    return jsonify({'status': 'success'})
```

---

## 身份驗證安全

### 1. 密碼安全

```python
# app/models/user.py
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)

    # 密碼強度要求
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_DIGIT = True
    PASSWORD_REQUIRE_SPECIAL = True

    def set_password(self, password):
        """設置密碼（使用 bcrypt 雜湊）"""
        if not self.validate_password_strength(password):
            raise ValueError('密碼強度不足')

        # 使用 pbkdf2:sha256 和高迭代次數
        self.password_hash = generate_password_hash(
            password,
            method='pbkdf2:sha256:260000'
        )

    def check_password(self, password):
        """驗證密碼"""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_password_strength(password):
        """驗證密碼強度"""
        if len(password) < User.PASSWORD_MIN_LENGTH:
            return False, f'密碼長度必須至少 {User.PASSWORD_MIN_LENGTH} 個字符'

        if User.PASSWORD_REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
            return False, '密碼必須包含至少一個大寫字母'

        if User.PASSWORD_REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
            return False, '密碼必須包含至少一個小寫字母'

        if User.PASSWORD_REQUIRE_DIGIT and not re.search(r'\d', password):
            return False, '密碼必須包含至少一個數字'

        if User.PASSWORD_REQUIRE_SPECIAL and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, '密碼必須包含至少一個特殊字符'

        # 檢查常見弱密碼
        common_passwords = ['password', '12345678', 'qwerty', 'admin123']
        if password.lower() in common_passwords:
            return False, '密碼過於常見，請選擇更強的密碼'

        return True, '密碼強度合格'

    def is_account_locked(self):
        """檢查帳戶是否被鎖定"""
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        return False

    def increment_failed_login(self):
        """增加失敗登入次數"""
        self.failed_login_attempts += 1

        # 5 次失敗後鎖定帳戶 30 分鐘
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=30)

        db.session.commit()

    def reset_failed_login(self):
        """重置失敗登入次數"""
        self.failed_login_attempts = 0
        self.locked_until = None
        db.session.commit()
```

### 2. 會話管理

```python
# app/__init__.py
from flask import Flask, session
from flask_login import LoginManager
from datetime import timedelta

def create_app():
    app = Flask(__name__)

    # 會話配置
    app.config['SESSION_COOKIE_SECURE'] = True  # 僅 HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # 防止 JavaScript 訪問
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF 保護
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True

    # Flask-Login 配置
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = 'strong'  # 強會話保護

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
```

### 3. 登入端點安全實現

```python
# app/routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user
from app.models.user import User
from app.forms.auth_forms import LoginForm
import logging

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('projects.list'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        # 查找用戶
        user = User.query.filter_by(username=username).first()

        if user is None:
            # 不透露用戶是否存在
            logger.warning(f'登入失敗：用戶名不存在 - {username} (IP: {request.remote_addr})')
            flash('用戶名或密碼錯誤', 'danger')
            return render_template('auth/login.html', form=form)

        # 檢查帳戶是否被鎖定
        if user.is_account_locked():
            logger.warning(f'登入失敗：帳戶被鎖定 - {username}')
            flash('帳戶已被鎖定，請稍後再試', 'danger')
            return render_template('auth/login.html', form=form)

        # 驗證密碼
        if not user.check_password(password):
            user.increment_failed_login()
            logger.warning(f'登入失敗：密碼錯誤 - {username} (IP: {request.remote_addr})')
            flash('用戶名或密碼錯誤', 'danger')
            return render_template('auth/login.html', form=form)

        # 登入成功
        user.reset_failed_login()
        user.last_login = datetime.utcnow()
        db.session.commit()

        # 設置會話
        login_user(user, remember=form.remember_me.data)
        session.permanent = True

        # 記錄成功登入
        logger.info(f'登入成功 - {username} (IP: {request.remote_addr})')

        # 重定向到之前的頁面或首頁
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('dashboard.index')

        return redirect(next_page)

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logger.info(f'登出 - {current_user.username}')
    logout_user()
    session.clear()
    flash('您已成功登出', 'success')
    return redirect(url_for('auth.login'))
```

---

## 授權與訪問控制

### 1. 角色基礎訪問控制 (RBAC)

```python
# app/utils/decorators.py
from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def role_required(*roles):
    """要求特定角色的裝飾器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('請先登入', 'warning')
                return redirect(url_for('auth.login'))

            if current_user.role not in roles:
                logger.warning(f'訪問被拒絕 - 用戶 {current_user.username} 嘗試訪問需要角色 {roles} 的資源')
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """要求管理員角色的裝飾器"""
    return role_required('admin')(f)

def owner_or_admin_required(get_resource_owner):
    """要求資源擁有者或管理員的裝飾器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)

            # 獲取資源擁有者
            owner_id = get_resource_owner(*args, **kwargs)

            # 檢查是否為擁有者或管理員
            if current_user.id != owner_id and current_user.role != 'admin':
                logger.warning(f'訪問被拒絕 - 用戶 {current_user.username} 嘗試訪問非自己的資源')
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 使用示例
@app.route('/admin/users')
@admin_required
def manage_users():
    """僅管理員可訪問"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/projects/<int:project_id>/edit')
@login_required
def edit_project(project_id):
    """僅專案創建者或管理員可編輯"""
    project = Project.query.get_or_404(project_id)

    # 檢查權限
    if current_user.id != project.created_by and current_user.role != 'admin':
        abort(403)

    return render_template('projects/edit.html', project=project)
```

---

## 文件上傳安全

```python
# app/utils/file_upload.py
import os
from werkzeug.utils import secure_filename
from flask import current_app
import magic
import hashlib

class SecureFileUpload:
    # 允許的文件類型
    ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv', 'pdf', 'png', 'jpg', 'jpeg'}
    ALLOWED_MIME_TYPES = {
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
        'text/csv',
        'application/pdf',
        'image/png',
        'image/jpeg'
    }
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    @staticmethod
    def allowed_file(filename):
        """檢查文件擴展名"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in SecureFileUpload.ALLOWED_EXTENSIONS

    @staticmethod
    def validate_file(file):
        """驗證上傳的文件"""
        # 檢查文件是否存在
        if not file or file.filename == '':
            return False, '沒有選擇文件'

        # 檢查文件擴展名
        if not SecureFileUpload.allowed_file(file.filename):
            return False, '不允許的文件類型'

        # 讀取文件內容
        file_content = file.read()
        file.seek(0)  # 重置文件指針

        # 檢查文件大小
        if len(file_content) > SecureFileUpload.MAX_FILE_SIZE:
            return False, f'文件大小超過限制 ({SecureFileUpload.MAX_FILE_SIZE / 1024 / 1024}MB)'

        # 檢查 MIME 類型
        mime = magic.from_buffer(file_content, mime=True)
        if mime not in SecureFileUpload.ALLOWED_MIME_TYPES:
            return False, f'不允許的文件類型：{mime}'

        return True, '文件驗證通過'

    @staticmethod
    def save_file(file, upload_folder):
        """安全地保存文件"""
        # 驗證文件
        is_valid, message = SecureFileUpload.validate_file(file)
        if not is_valid:
            raise ValueError(message)

        # 使用安全的文件名
        original_filename = secure_filename(file.filename)

        # 生成唯一文件名
        file_hash = hashlib.md5(file.read()).hexdigest()
        file.seek(0)

        file_ext = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{file_hash}.{file_ext}"

        # 確保上傳目錄存在
        os.makedirs(upload_folder, exist_ok=True)

        # 保存文件
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)

        return unique_filename, file_path
```

---

## API 安全

### 1. 速率限制

```python
# app/utils/rate_limit.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask

def create_app():
    app = Flask(__name__)

    # 配置速率限制
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="redis://localhost:6379"
    )

    # 應用到特定路由
    @app.route('/api/projects', methods=['POST'])
    @limiter.limit("10 per minute")
    def create_project():
        # 創建專案邏輯
        pass

    @app.route('/auth/login', methods=['POST'])
    @limiter.limit("5 per minute")
    def login():
        # 登入邏輯
        pass

    return app
```

### 2. API Token 認證

```python
# app/utils/api_auth.py
import secrets
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

class APIToken(db.Model):
    __tablename__ = 'api_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token_hash = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100))
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime)

    @staticmethod
    def generate_token():
        """生成安全的 API token"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_token(token):
        """雜湊 token"""
        return hashlib.sha256(token.encode()).hexdigest()

    def is_valid(self):
        """檢查 token 是否有效"""
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True

def token_required(f):
    """API token 認證裝飾器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': '缺少認證 token'}), 401

        # 移除 "Bearer " 前綴
        if token.startswith('Bearer '):
            token = token[7:]

        # 驗證 token
        token_hash = APIToken.hash_token(token)
        api_token = APIToken.query.filter_by(token_hash=token_hash).first()

        if not api_token or not api_token.is_valid():
            return jsonify({'error': '無效的認證 token'}), 401

        # 更新最後使用時間
        api_token.last_used_at = datetime.utcnow()
        db.session.commit()

        # 將用戶信息添加到請求上下文
        request.current_user = User.query.get(api_token.user_id)

        return f(*args, **kwargs)
    return decorated_function
```

---

## 日誌與監控

```python
# app/utils/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    """配置應用日誌"""

    # 創建日誌目錄
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # 應用日誌
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # 安全日誌
    security_handler = RotatingFileHandler(
        'logs/security.log',
        maxBytes=10240000,
        backupCount=10
    )
    security_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    security_handler.setLevel(logging.WARNING)

    security_logger = logging.getLogger('security')
    security_logger.addHandler(security_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('應用啟動')

# 安全事件記錄
def log_security_event(event_type, user, details, ip_address):
    """記錄安全事件"""
    security_logger = logging.getLogger('security')
    security_logger.warning(
        f'安全事件 - 類型: {event_type}, 用戶: {user}, '
        f'詳情: {details}, IP: {ip_address}'
    )
```

---

## 安全檢查清單

### 開發階段
- [ ] 所有用戶輸入都經過驗證和淨化
- [ ] 使用參數化查詢防止 SQL 注入
- [ ] 實現 CSRF 保護
- [ ] 實現 XSS 防護（輸出編碼）
- [ ] 密碼使用強雜湊算法（bcrypt/pbkdf2）
- [ ] 實現速率限制
- [ ] 敏感操作需要重新認證
- [ ] 實現適當的訪問控制
- [ ] 文件上傳驗證（類型、大小、內容）
- [ ] 實現安全標頭（CSP, X-Frame-Options 等）

### 部署前
- [ ] 更改所有預設密碼
- [ ] 禁用調試模式
- [ ] 配置 HTTPS/SSL
- [ ] 設置安全的會話配置
- [ ] 配置防火牆規則
- [ ] 限制資料庫訪問
- [ ] 設置日誌記錄和監控
- [ ] 進行安全掃描（OWASP ZAP, Burp Suite）
- [ ] 進行依賴漏洞掃描（pip-audit, safety）
- [ ] 備份和災難恢復計劃

### 運行時
- [ ] 定期更新依賴
- [ ] 監控異常活動
- [ ] 定期審查日誌
- [ ] 定期安全審計
- [ ] 定期備份
- [ ] 保持系統和軟件更新
- [ ] 定期檢查訪問控制
- [ ] 定期測試災難恢復

---

**文檔版本**: 1.0
**最後更新**: 2025-12-30
**狀態**: 完成
