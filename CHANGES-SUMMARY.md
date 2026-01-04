# 系統更新摘要 (2026年1月4日)

## 概述
完成了資安專案進度管制系統的重大功能更新，主要涉及角色權限調整、工程師多選功能、以及相關UI/UX改進。

---

## 1. 角色權限修改

### 移除「經理」(Manager) 角色
- 刪除了所有系統中對「manager」角色的引用
- 將經理的權限合併到測試員(Tester)角色中

### 新的角色定義
| 角色 | 訪問權限 | 功能 |
|------|--------|------|
| **Admin** | 完全訪問 | 管理用戶、查看所有專案、訪問儀表板、建立刪除專案 |
| **Tester** | 受限訪問 | 只能看/修改自己創建或被指派的專案；可刪除專案；無法訪問用戶管理和儀表板 |

---

## 2. 工程師/測試人員多選功能

### 新增多對多關係
**檔案**: `app/models/project.py`

```python
# 關聯表：專案 <-> 工程師（多對多）
project_engineers = db.Table(
    'project_engineers',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

# 為 Project 模型添加多對多關係
Project.engineers = db.relationship(...)
```

**特性**：
- 一個專案可以指派給多個工程師/測試人員
- 在「創建」和「編輯」專案頁面中，可以使用多選框選擇指派的工程師
- 選項包含所有非Admin用戶（格式：姓名 (用戶名)）

### 表單更新
**檔案**: `app/forms/project_forms.py`

新增欄位：
```python
assigned_engineers = SelectMultipleField('指派工程師', coerce=int)
```

---

## 3. 專案可見性規則

### Tester 用戶
- ✅ 可以看到自己**創建**或**被指派**的專案
- ✅ 可以編輯自己創建或被指派的專案
- ✅ 可以刪除專案
- ❌ 無法訪問 `/dashboard/`
- ❌ 無法訪問 `/users/`
- ✅ 只能訪問 `/projects/`

### Admin 用戶
- ✅ 可以看到所有專案
- ✅ 可以編輯所有專案
- ✅ 可以刪除專案
- ✅ 可以訪問所有功能（儀表板、用戶管理）

---

## 4. 儀表板工作量計算優化

**檔案**: `app/routes/dashboard.py` - `api_personnel_workload()` 函數

### 新邏輯
專案工時根據指派的工程師數量**均勻分配**：

```
若專案有 N 個指派工程師：
- 每個工程師分配的預計工時 = 項目預計工時 / N
- 每個工程師分配的已完工時 = 項目已完工時 / N
- 完成百分比 = (分配已完工時 / 分配預計工時) × 100%
```

**示例**：
- 項目A：預計100小時，指派給 工程師1 和 工程師2
  - 工程師1: 50小時
  - 工程師2: 50小時

---

## 5. UI/UX 更新

### 導航欄
**檔案**: `app/templates/base.html`

- Tester 用戶：隱藏「儀表板」和「用戶管理」菜單項
- Admin 用戶：顯示所有菜單項

### 專案列表頁面
**檔案**: `app/templates/projects/list.html`

新增列：「指派工程師」
- 顯示該專案的所有指派工程師名稱
- 未指派則顯示「未指派」

刪除權限調整：
- 只有 Admin 和 Tester 可以刪除專案

### 專案詳情頁面
**檔案**: `app/templates/projects/detail.html`

新增區塊：「指派工程師」
- 以徽章(Badge)形式顯示 "姓名 (用戶名)"
- 未指派則顯示「未指派」

### 創建/編輯專案頁面
**檔案**: `app/templates/projects/create.html` 和 `edit.html`

新增欄位：「指派工程師」
- 多選框(Checkbox)
- 選項列表：所有非Admin用戶
- 説明文本：「從現有用戶中選擇（可多選，不包含管理員）」

### 版權年份更新
**檔案**: `app/templates/base.html`

```html
<!-- 舊 -->
<span class="text-muted">資安專案進度管制系統 © 2024</span>

<!-- 新 -->
<span class="text-muted">資安專案進度管制系統 © 2026</span>
```

---

## 6. 數據庫架構

### 新增表格
**project_engineers** (關聯表)
| 欄位 | 類型 | 說明 |
|------|------|------|
| project_id | Integer | 專案ID（外鍵） |
| user_id | Integer | 用戶ID（外鍵） |

### 修改表格
**projects**
- 無結構更改（關係通過關聯表管理）

**users**
- `role` 欄位：刪除「manager」選項，保留 "admin" 和 "tester"

---

## 7. API 路由權限變更

| 路由 | 舊權限 | 新權限 | 說明 |
|------|-------|-------|------|
| `DELETE /projects/<id>/delete` | admin, manager | admin, tester | Tester可刪除 |
| `POST /users/<id>/unlock` | admin, manager | admin, tester | Tester可解鎖用戶 |
| 角色驗證 | admin, manager, tester | admin, tester | 移除manager |

---

## 8. 影響範圍

### 受影響的文件
```
app/models/project.py          ✓ 修改
app/forms/project_forms.py     ✓ 修改
app/routes/projects.py         ✓ 修改
app/routes/users.py            ✓ 修改
app/routes/dashboard.py        ✓ 修改
app/templates/base.html        ✓ 修改
app/templates/projects/create.html  ✓ 修改
app/templates/projects/edit.html    ✓ 修改
app/templates/projects/list.html    ✓ 修改
app/templates/projects/detail.html  ✓ 修改
```

---

## 9. 測試建議

### 功能測試清單

#### ✅ 工程師多選功能
- [ ] 創建專案時選擇多個工程師
- [ ] 編輯專案修改指派的工程師
- [ ] 驗證未指派情況下顯示「未指派」
- [ ] 在專案列表、詳情中查看指派工程師

#### ✅ Tester 權限
- [ ] Tester 用戶只能看到自己創建的專案
- [ ] Tester 用戶能看到被指派的專案
- [ ] Tester 用戶可以編輯被指派的專案
- [ ] Tester 用戶可以刪除專案
- [ ] Tester 用戶無法訪問 `/dashboard/`
- [ ] Tester 用戶無法訪問 `/users/`

#### ✅ 儀表板工作量計算
- [ ] 多工程師項目的工時正確平均分配
- [ ] 完成百分比計算正確
- [ ] 排序按工時降序

#### ✅ UI/UX
- [ ] Tester 導航欄隱藏儀表板和用戶管理
- [ ] Admin 導航欄顯示所有選項
- [ ] 版權年份顯示為 2026

---

## 10. 向後相容性

### 破壞性變更
- **角色字段**: "manager" 角色被完全移除，原有manager用戶需要手動升級為admin或降級為tester
- **刪除權限**: 原有manager用戶的刪除權限現在由tester承擔

### 無風險變更
- 新增指派工程師欄位（可選）
- 新增多對多關係（不影響現有數據）

---

## 11. 部署步驟

```bash
# 1. 備份資料庫
# (備份您的MySQL資料庫)

# 2. 更新代碼
git pull  # 或手動更新文件

# 3. 初始化數據庫（如果使用新數據庫）
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# 4. 啟動應用
python run.py

# 5. 用戶角色遷移（如適用）
# 在 /users/ 管理頁面中，將原有 manager 用戶更改為 tester 或 admin
```

---

## 12. 已知問題

無。

---

## 聯絡方式

有任何問題或建議，請聯繫系統管理員。
