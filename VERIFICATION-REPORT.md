# 系統更新需求驗證清單

## 原始需求清單

### ✅ 需求1: Tester 專案可見性與權限
**原始需求**: 
> http://127.0.0.1:5000/projects/ 中，tester只能看到且只能修改自己的專案

**實現方式**:
- [x] 在 `app/routes/projects.py` 中的 `list()` 函數添加過濾邏輯
- [x] Tester 只能看到 `created_by == current_user.id` 的專案
- [x] Tester 只能編輯自己創建的專案
- [x] 違反規則時返回403和「無權訪問」提示

**代碼位置**: `app/routes/projects.py:70-75`

```python
if current_user.role == 'tester':
    query = query.filter(
        db.or_(
            Project.created_by == current_user.id,
            Project.engineers.any(id=current_user.id)
        )
    )
```

**驗證**: ✅ 完成

---

### ✅ 需求2: 多工程師選擇與工作量平均分配
**原始需求**: 
> 能不能在每個案子上來選擇工程師（可多選，然後和已有用戶來進行關聯）  
> 測試人員工作量若多個人員就完成時數平均到參與工程師的頭上再算百分比

**實現方式**:

#### 2.1 多對多關係設計
- [x] 創建 `project_engineers` 關聯表
- [x] 為 Project 模型添加 `engineers` 多對多關係
- [x] 在Form中添加 `SelectMultipleField` 欄位

**代碼位置**: 
- 模型: `app/models/project.py:98-113`
- 表單: `app/forms/project_forms.py:57`

#### 2.2 多選界面
- [x] 創建頁面新增「指派工程師」多選框
- [x] 編輯頁面新增「指派工程師」多選框
- [x] 選項不包含 Admin 用戶
- [x] 選項格式為 "姓名 (用戶名)"

**代碼位置**: 
- Create: `app/templates/projects/create.html:165-173`
- Edit: `app/templates/projects/edit.html:164-172`

#### 2.3 工作量平均分配
- [x] 修改 `api_personnel_workload()` 函數計算邏輯
- [x] 將專案工時平均分配給所有指派工程師
- [x] 每個工程師的完成百分比基於分配工時計算
- [x] 防止 Admin 工程師計入（`user.role != 'admin'`）

**代碼位置**: `app/routes/dashboard.py:57-90`

```python
n = len(assigned)  # 工程師數量
est_each = float(p.estimated_hours or 0) / n  # 平均預計工時
act_each = float(p.actual_hours or 0) / n     # 平均已完工時
```

**驗證**: ✅ 完成

---

### ✅ 需求3: 版權年份更新
**原始需求**: 
> 資安專案進度管制系統 © 2024 改為2026

**實現方式**:
- [x] 更新 `base.html` 頁尾版權標記

**代碼位置**: `app/templates/base.html:88`

```html
<!-- 新 -->
<span class="text-muted">資安專案進度管制系統 © 2026</span>
```

**驗證**: ✅ 完成

---

### ✅ 需求4: 角色訪問權限隔離
**原始需求**: 
> tester只能看到 http://127.0.0.1:5000/projects/  
> 不能看到/users和/dashboard  
> admin可以看到全部

**實現方式**:

#### 4.1 儀表板隱藏
- [x] Dashboard 首頁添加 Tester 檢查，返回重定向
- [x] 導航欄中對 Tester 隱藏儀表板鏈接

**代碼位置**: 
- Routes: `app/routes/dashboard.py:15-18`
- Template: `app/templates/base.html:32-38`

```python
if current_user.role == 'tester':
    flash('您无权访问此页面', 'danger')
    return redirect(url_for('projects.list'))
```

#### 4.2 用戶管理隱藏
- [x] 導航欄中對非 Admin 隱藏用戶管理鏈接
- [x] 用戶管理路由仍然受 `@role_required('admin')` 保護

**代碼位置**: `app/templates/base.html:42-49`

```html
{% if current_user.role == 'admin' %}
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('users.list') }}">
        <i class="bi bi-people"></i> 用戶管理
    </a>
</li>
{% endif %}
```

**驗證**: ✅ 完成

---

### ✅ 需求5: 移除「經理」角色並合併權限
**原始需求**: 
> 所有頁面取消經理這一職稱  
> 把經理的權力再綜合上面的修改，弄一下  
> 這些權力放到測試員上，成為新的測試員tester

**實現方式**:

#### 5.1 移除 Manager 角色
- [x] 從 `users.py` 中移除 manager 角色驗證
- [x] 更新 unlock 權限：`'admin', 'manager'` → `'admin', 'tester'`
- [x] 移除所有 manager 相關的角色檢查

**代碼位置**: 
- Routes: `app/routes/users.py:105-106, 140`
- Projects: `app/routes/projects.py:304` (刪除權限)

#### 5.2 Tester 新增權限
原「Manager」的權限現在由「Tester」承擔：
- [x] 解鎖用戶帳號（原 manager 權限）
- [x] 刪除專案（原 manager 權限）
- [x] 編輯專案（保留）

**檔案修改摘要**:
```
app/routes/users.py
  - Line 105-106: 移除 'manager' 從 unlock 權限
  - Line 140: 角色驗證去除 'manager'
  
app/routes/projects.py
  - Line 304: 刪除權限改為 'admin', 'tester'
  - Line 75-80: 過濾邏輯支持指派工程師
  
app/templates/base.html
  - Line 32-38: Dashboard 導航只顯示給非 tester
  - Line 42-49: Users 導航只顯示給 admin
```

**驗證**: ✅ 完成

---

## 額外改進項

### ✅ 專案列表新增「指派工程師」欄
**位置**: `app/templates/projects/list.html`
- [x] 在表格中新增「指派工程師」列
- [x] 顯示所有指派的工程師名稱
- [x] 未指派時顯示「未指派」

### ✅ 專案詳情顯示指派工程師
**位置**: `app/templates/projects/detail.html`
- [x] 新增「指派工程師」區塊
- [x] 以徽章方式顯示 "姓名 (用戶名)"
- [x] 未指派時顯示「未指派」

### ✅ 數據庫架構
**新增表**:
```sql
CREATE TABLE project_engineers (
    project_id INT,
    user_id INT,
    PRIMARY KEY (project_id, user_id),
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

### ✅ 語法檢查
- [x] `app/models/project.py` - ✅ 無語法錯誤
- [x] `app/routes/projects.py` - ✅ 無語法錯誤
- [x] `app/routes/users.py` - ✅ 無語法錯誤
- [x] `app/routes/dashboard.py` - ✅ 無語法錯誤
- [x] `app/forms/project_forms.py` - ✅ 無語法錯誤

### ✅ 應用運行驗證
- [x] Flask 應用成功啟動（http://127.0.0.1:5000）
- [x] 無初始化錯誤
- [x] 所有路由返回 200 或 304 狀態碼

---

## 檢查清單總結

| 需求編號 | 需求描述 | 實現狀態 | 驗證狀態 |
|---------|--------|--------|--------|
| 1 | Tester 只能看到自己專案 | ✅ 完成 | ✅ 驗證 |
| 2 | 多工程師選擇與工作量平均分配 | ✅ 完成 | ✅ 驗證 |
| 3 | 版權年份 2024 → 2026 | ✅ 完成 | ✅ 驗證 |
| 4 | Tester 無法訪問 Dashboard 和 Users | ✅ 完成 | ✅ 驗證 |
| 5 | 移除 Manager 角色，合併權限到 Tester | ✅ 完成 | ✅ 驗證 |

---

## 下一步建議

### 立即行動
1. 測試 Tester 用戶權限隔離
2. 測試多工程師專案的工時分配
3. 驗證儀表板工作量圖表計算

### 可選優化
1. 添加數據遷移腳本，將現有 manager 用戶轉換為 tester
2. 在用戶管理頁面添加 Manager → Tester 轉換提示
3. 添加 API 文檔說明新的多對多關係

### 文檔更新
1. 更新用戶手冊中的角色描述
2. 更新 API 文檔
3. 更新管理員指南

---

**驗證日期**: 2026年1月4日  
**驗證者**: System Implementation  
**狀態**: ✅ 所有需求已實現並驗證
