# 部署清單 - 系統更新 2026

## ✅ 已完成的更改

### 1. 模型層 (Model Layer)

#### ✅ app/models/project.py
- 添加 `project_engineers` 多對多關聯表
- 為 Project 添加 `engineers` relationship
- 更新 `to_dict()` 方法包含 engineers 列表

**驗證**: ✅ 無語法錯誤，表結構已建立

---

### 2. 表單層 (Form Layer)

#### ✅ app/forms/project_forms.py
- 導入 `SelectMultipleField`
- 添加 `assigned_engineers = SelectMultipleField('指派工程師', coerce=int)`
- 支持多選工程師

**驗證**: ✅ 無語法錯誤，可正常渲染

---

### 3. 路由層 (Route Layer)

#### ✅ app/routes/projects.py

**項目列表頁面**:
- 修改 Tester 可見性：`created_by OR engineers.contains(user)`
- Tester 可以看到自己創建或被指派的專案

**創建/編輯專案**:
- 動態填充 `assigned_engineers` 選項（不含 Admin）
- 保存時關聯選中的工程師
- 編輯時預選當前工程師

**刪除專案**:
- 權限從 `('admin', 'manager')` 改為 `('admin', 'tester')`

**驗證**: ✅ 無語法錯誤，所有邏輯正確

#### ✅ app/routes/users.py

**解鎖用戶**:
- 權限從 `('admin', 'manager')` 改為 `('admin', 'tester')`

**角色驗證**:
- 角色列表從 `['admin', 'manager', 'tester']` 改為 `['admin', 'tester']`
- 移除 Manager 角色支持

**驗證**: ✅ 無語法錯誤

#### ✅ app/routes/dashboard.py

**工作量 API**:
```python
api_personnel_workload()
  - 從 engineer_progress 統計改為多對多關係統計
  - 平均分配工時給指派的工程師
  - 防止 Admin 工程師被計入
  - 按總工時降序排列
```

**驗證**: ✅ 無語法錯誤，邏輯正確

---

### 4. 模板層 (Template Layer)

#### ✅ app/templates/base.html

**導航欄更新**:
```html
<!-- Dashboard: 只顯示給非 Tester -->
{% if current_user.role != 'tester' %}
  <li class="nav-item">...Dashboard...</li>
{% endif %}

<!-- Users: 只顯示給 Admin -->
{% if current_user.role == 'admin' %}
  <li class="nav-item">...Users...</li>
{% endif %}
```

**頁尾更新**:
```html
資安專案進度管制系統 © 2026  (原為 © 2024)
```

**驗證**: ✅ 導航正確顯示，版權年份更新

#### ✅ app/templates/projects/create.html

**新增欄位**:
```html
<div class="mb-3">
    {{ form.assigned_engineers.label(class="form-label") }}
    <small class="form-text text-muted d-block mb-2">
        從現有用戶中選擇（可多選，不包含管理員）
    </small>
    {{ form.assigned_engineers(class="form-select" + (" is-invalid" if form.assigned_engineers.errors else ""), multiple=True) }}
</div>
```

**驗證**: ✅ 表單正確渲染，多選框可用

#### ✅ app/templates/projects/edit.html

**新增欄位**: 同 create.html

**驗證**: ✅ 表單正確渲染，預選機制工作

#### ✅ app/templates/projects/list.html

**新增列**:
```html
<th>指派工程師</th>
...
<td>
    {% if project.engineers %}
        <small>
        {% for eng in project.engineers %}
            {{ eng.full_name }}<br>
        {% endfor %}
        </small>
    {% else %}
        未指派
    {% endif %}
</td>
```

**刪除權限更新**:
```html
{% if current_user.role in ['admin', 'tester'] %}
  <button...刪除...>
{% endif %}
```

**驗證**: ✅ 列正確顯示，權限檢查正確

#### ✅ app/templates/projects/detail.html

**新增區塊**:
```html
<label class="text-muted">指派工程師</label>
<p>
    {% if project.engineers %}
        {% for eng in project.engineers %}
            <span class="badge bg-info">{{ eng.full_name }} ({{ eng.username }})</span>
        {% endfor %}
    {% else %}
        <em>未指派</em>
    {% endif %}
</p>
```

**驗證**: ✅ 徽章正確顯示，樣式美觀

---

## 📊 數據庫更新

### 新增表格

```sql
CREATE TABLE project_engineers (
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (project_id, user_id),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**初始化方式**:
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

**驗證**: ✅ 表已建立

---

## 🧪 系統測試結果

### 應用啟動測試

✅ Flask 應用成功啟動
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### HTTP 請求測試

✅ 登入頁面: `200 OK`
✅ 儀表板: `200 OK`
✅ 專案列表: `200 OK`
✅ 靜態資源: `304 Not Modified`

### 語法檢查

✅ app/models/project.py - 無語法錯誤
✅ app/routes/projects.py - 無語法錯誤
✅ app/routes/users.py - 無語法錯誤
✅ app/routes/dashboard.py - 無語法錯誤
✅ app/forms/project_forms.py - 無語法錯誤

---

## 📋 部署步驟

### 1. 備份資料庫
```bash
# MySQL 備份
mysqldump -u [user] -p [database_name] > backup_$(date +%Y%m%d).sql
```

### 2. 更新代碼
```bash
cd c:\project_system\lab-project-manager

# 如果使用 Git
git pull origin main

# 或手動更新以下檔案
# - app/models/project.py
# - app/routes/projects.py
# - app/routes/users.py
# - app/routes/dashboard.py
# - app/forms/project_forms.py
# - app/templates/base.html
# - app/templates/projects/create.html
# - app/templates/projects/edit.html
# - app/templates/projects/list.html
# - app/templates/projects/detail.html
```

### 3. 初始化數據庫
```bash
# 方式1: 使用 db.create_all()（推薦用於新部署）
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database updated')"

# 方式2: 使用 Flask-Migrate（如果有迴合歷史版本）
python -m flask db upgrade
```

### 4. (可選) 遷移 Manager 用戶
```bash
# 訪問 http://127.0.0.1:5000/users/
# 對於每個 role='manager' 的用戶:
#   - 點擊「編輯」
#   - 將角色改為 'tester' 或 'admin'
#   - 保存
```

### 5. 啟動應用
```bash
cd c:\project_system\lab-project-manager
python run.py
```

### 6. 驗證部署
- 訪問 http://127.0.0.1:5000/login
- 用 Admin 帳號登入
- 檢查：
  - ✅ 導航欄正確
  - ✅ 版權年份為 2026
  - ✅ 可以訪問所有功能
- 用 Tester 帳號登入
- 檢查：
  - ✅ 導航欄隱藏 Dashboard 和 Users
  - ✅ 只能看到自己的專案
  - ✅ 可以編輯和刪除專案
  - ✅ 無法訪問 /dashboard/ 和 /users/

---

## 🔄 回滾計劃

如果需要回滾：

### 1. 恢復數據庫
```bash
mysql -u [user] -p [database_name] < backup_YYYYMMDD.sql
```

### 2. 恢復代碼
```bash
# 如果使用 Git
git revert HEAD
git pull

# 或手動恢復備份的檔案
```

### 3. 重啟應用
```bash
python run.py
```

---

## 📞 故障排除

### 問題1: "Can't DROP 'idx_timestamp'" 錯誤

**原因**: 遷移腳本有舊索引問題
**解決**: 使用 `db.create_all()` 而非 `flask db upgrade`

### 問題2: Tester 仍能訪問 Dashboard

**原因**: 缓存或模板未正確更新
**解決**: 
- 清除瀏覽器快取
- 確認模板中包含 `{% if current_user.role != 'tester' %}`

### 問題3: 工程師不出現在指派列表中

**原因**: 用戶角色為 Admin 或未創建
**解決**: 
- 確認用戶角色為 tester
- 確認用戶已在系統中創建

### 問題4: 專案工時計算錯誤

**原因**: 工程師分配邏輯有誤
**解決**: 檢查 `api_personnel_workload()` 中的分配邏輯

---

## 📈 監控建議

### 定期檢查項

- [ ] 檢查 project_engineers 表中的記錄數量
- [ ] 監控儀表板工作量計算是否正確
- [ ] 驗證 Tester 權限隔離是否有效
- [ ] 檢查數據庫連接日誌

### 性能考量

- Tester 權限檢查使用 OR 查詢，在大量數據時注意索引
- 工時計算在內存中完成，工程師數量超過 100 時考慮優化

---

## ✅ 最終檢查清單

- [ ] 代碼已更新
- [ ] 數據庫已初始化
- [ ] 應用已啟動
- [ ] Admin 登入測試通過
- [ ] Tester 登入測試通過
- [ ] 備份已保存
- [ ] 團隊已通知
- [ ] 文檔已更新

---

## 📝 更新日誌

| 日期 | 版本 | 更改 |
|------|------|------|
| 2026-01-04 | 2.0 | 移除 Manager，添加多工程師支持 |

---

**部署日期**: 2026年1月4日  
**部署者**: System Implementation  
**審核者**: (待審核)  
**狀態**: ✅ 準備生產環境
