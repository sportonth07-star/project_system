# Implementation Plan
## Laboratory Project Progress Management System

---

## Document Information
- **Based on**: PRD.md v1.0
- **Created**: 2025-12-30
- **Project Duration**: 10 weeks (5 phases)
- **Technology Stack**: Python Flask, MySQL 8.0+, HTML/CSS/JavaScript, Chart.js
- **Language**: Traditional Chinese (繁體中文)

---

## Table of Contents
1. [Project Structure](#project-structure)
2. [Phase 1: Foundation](#phase-1-foundation)
3. [Phase 2: Core Features](#phase-2-core-features)
4. [Phase 3: Visualization](#phase-3-visualization)
5. [Phase 4: Enhancement](#phase-4-enhancement)
6. [Phase 5: Testing & Deployment](#phase-5-testing--deployment)
7. [Development Standards](#development-standards)
8. [Testing Strategy](#testing-strategy)
9. [Deployment Plan](#deployment-plan)
10. [Maintenance Plan](#maintenance-plan)

---

## Project Structure

### Directory Layout
```
lab-project-manager/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project.py              # Project model
│   │   ├── user.py                 # User model
│   │   └── audit_log.py            # Audit log model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                 # Authentication routes
│   │   ├── projects.py             # Project CRUD routes
│   │   ├── dashboard.py            # Dashboard routes
│   │   └── api.py                  # API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── project_service.py      # Business logic for projects
│   │   ├── user_service.py         # Business logic for users
│   │   ├── analytics_service.py    # Analytics calculations
│   │   └── export_service.py       # Export/import logic
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── auth_forms.py           # Login/register forms
│   │   └── project_forms.py        # Project forms
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css            # Main stylesheet
│   │   │   └── dashboard.css       # Dashboard styles
│   │   ├── js/
│   │   │   ├── main.js             # Main JavaScript
│   │   │   ├── projects.js         # Project table logic
│   │   │   ├── dashboard.js        # Dashboard charts
│   │   │   └── forms.js            # Form validation
│   │   └── images/
│   │       └── logo.png
│   ├── templates/
│   │   ├── base.html               # Base template
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── projects/
│   │   │   ├── list.html           # Project table view
│   │   │   ├── create.html         # Create project form
│   │   │   ├── edit.html           # Edit project form
│   │   │   └── detail.html         # Project details
│   │   ├── dashboard/
│   │   │   └── index.html          # Dashboard view
│   │   └── includes/
│   │       ├── navbar.html
│   │       ├── sidebar.html
│   │       └── footer.html
│   └── utils/
│       ├── __init__.py
│       ├── decorators.py           # Custom decorators
│       ├── validators.py           # Form validators
│       └── helpers.py              # Helper functions
├── migrations/                      # Database migrations
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_routes.py
│   ├── test_services.py
│   └── conftest.py                 # Pytest configuration
├── config.py                        # Configuration settings
├── requirements.txt                 # Python dependencies
├── run.py                          # Application entry point
├── .env.example                    # Environment variables template
├── .gitignore
└── README.md
```

---

## Phase 1: Foundation (Week 1-2)

### Week 1: Project Setup & Database Design

#### Day 1-2: Environment Setup
**Tasks:**
1. Initialize Git repository
2. Create virtual environment
3. Install base dependencies:
   ```bash
   pip install Flask==2.3.0
   pip install Flask-SQLAlchemy==3.0.5
   pip install Flask-Login==0.6.2
   pip install Flask-WTF==1.1.1
   pip install Flask-Migrate==4.0.4
   pip install python-dotenv==1.0.0
   pip install Werkzeug==2.3.0
   pip install PyMySQL==1.1.0
   pip install cryptography==41.0.0
   ```
4. Create project directory structure
5. Set up `.gitignore` and `.env` files
6. Initialize Flask app factory pattern

**Deliverables:**
- Working virtual environment
- Basic Flask app structure
- Configuration files (config.py, .env)

**Files to Create:**
- `config.py` - Environment configurations (Development, Testing, Production)
- `run.py` - Application entry point
- `app/__init__.py` - Flask app factory
- `requirements.txt` - Dependencies list
- `.env.example` - Environment variables template
- `README.md` - Project documentation

#### Day 3-4: Database Models
**Tasks:**
1. Design and implement Project model (app/models/project.py)
   - Define all fields from PRD section 3.2
   - Add relationships and constraints
   - Implement calculated fields (remaining_hours)
2. Design and implement User model (app/models/user.py)
   - Username, password_hash, email, role
   - Password hashing methods
   - Role validation
3. Design and implement AuditLog model (app/models/audit_log.py)
   - Track changes to projects
   - Store old and new values
4. Set up Flask-Migrate for database migrations
5. Create initial migration

**Deliverables:**
- Complete database models
- Initial database migration
- Database initialization script

**Code Snippets:**

**app/models/project.py:**
```python
from datetime import datetime
from app import db

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    item_number = db.Column(db.Integer, unique=True, nullable=False)
    personnel = db.Column(db.String(100), nullable=False)
    case_number = db.Column(db.String(50), nullable=False)
    customer = db.Column(db.String(100), nullable=False)
    evidence_required = db.Column(db.Boolean, nullable=False)
    model = db.Column(db.String(100))
    samples_complete = db.Column(db.String(20))
    engineer_progress = db.Column(db.String(200), nullable=False)
    expected_report_date = db.Column(db.Date, nullable=False)
    estimated_hours = db.Column(db.Integer, nullable=False)
    actual_hours = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='active')

    @property
    def remaining_hours(self):
        return self.estimated_hours - self.actual_hours

    def to_dict(self):
        return {
            'id': self.id,
            'item_number': self.item_number,
            'personnel': self.personnel,
            'case_number': self.case_number,
            'customer': self.customer,
            'evidence_required': self.evidence_required,
            'model': self.model,
            'samples_complete': self.samples_complete,
            'engineer_progress': self.engineer_progress,
            'expected_report_date': self.expected_report_date.isoformat(),
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours,
            'remaining_hours': self.remaining_hours,
            'status': self.status
        }
```

#### Day 5-7: Authentication System
**Tasks:**
1. Implement user registration functionality
2. Implement login/logout functionality
3. Set up Flask-Login for session management
4. Create password hashing utilities
5. Implement role-based access control decorators
6. Create login and registration forms
7. Design authentication templates

**Deliverables:**
- Working authentication system
- Login/logout pages
- Role-based access control
- Session management

**Files to Create:**
- `app/routes/auth.py` - Authentication routes
- `app/forms/auth_forms.py` - Login/register forms
- `app/templates/auth/login.html` - Login page
- `app/templates/auth/register.html` - Registration page
- `app/utils/decorators.py` - Role-based decorators

### Week 2: Basic CRUD & UI Foundation

#### Day 8-10: Project CRUD Operations
**Tasks:**
1. Create project service layer (app/services/project_service.py)
   - Create project
   - Read project (single & list)
   - Update project
   - Delete project (soft delete)
2. Implement project routes (app/routes/projects.py)
   - List all projects
   - Create project
   - Edit project
   - Delete project
3. Create project forms with validation
4. Implement pagination logic

**Deliverables:**
- Complete CRUD functionality
- Project service layer
- Form validation
- Basic project routes

**Code Snippets:**

**app/services/project_service.py:**
```python
from app.models.project import Project
from app.models.audit_log import AuditLog
from app import db
from datetime import datetime

class ProjectService:
    @staticmethod
    def create_project(data, user_id):
        project = Project(
            item_number=data['item_number'],
            personnel=data['personnel'],
            case_number=data['case_number'],
            customer=data['customer'],
            evidence_required=data['evidence_required'],
            model=data.get('model'),
            samples_complete=data.get('samples_complete'),
            engineer_progress=data['engineer_progress'],
            expected_report_date=data['expected_report_date'],
            estimated_hours=data['estimated_hours'],
            actual_hours=data.get('actual_hours', 0),
            created_by=user_id
        )
        db.session.add(project)
        db.session.commit()

        # Log creation
        AuditLog.log_action(user_id, 'CREATE', 'projects', project.id, None, project.to_dict())
        return project

    @staticmethod
    def get_projects(page=1, per_page=20, filters=None):
        query = Project.query.filter_by(status='active')

        if filters:
            if 'personnel' in filters:
                query = query.filter(Project.personnel.like(f"%{filters['personnel']}%"))
            if 'case_number' in filters:
                query = query.filter(Project.case_number.like(f"%{filters['case_number']}%"))
            # Add more filters as needed

        return query.order_by(Project.created_at.desc()).paginate(page=page, per_page=per_page)

    @staticmethod
    def update_project(project_id, data, user_id):
        project = Project.query.get_or_404(project_id)
        old_values = project.to_dict()

        for key, value in data.items():
            if hasattr(project, key):
                setattr(project, key, value)

        project.updated_by = user_id
        project.updated_at = datetime.utcnow()
        db.session.commit()

        # Log update
        AuditLog.log_action(user_id, 'UPDATE', 'projects', project.id, old_values, project.to_dict())
        return project

    @staticmethod
    def delete_project(project_id, user_id):
        project = Project.query.get_or_404(project_id)
        project.status = 'deleted'
        project.updated_by = user_id
        db.session.commit()

        # Log deletion
        AuditLog.log_action(user_id, 'DELETE', 'projects', project.id, project.to_dict(), None)
        return True
```

#### Day 11-14: Responsive UI Layout
**Tasks:**
1. Set up Bootstrap 5 or Tailwind CSS
2. Create base template with navbar, sidebar, footer
3. Design responsive project table layout
4. Implement table sorting functionality
5. Add pagination controls
6. Create modal for add/edit forms
7. Style forms and buttons
8. Add Traditional Chinese (繁體中文) language support

**Deliverables:**
- Responsive base template
- Project list page with table
- Add/edit modal forms
- Pagination UI
- Mobile-responsive design

**Files to Create:**
- `app/templates/base.html` - Base template
- `app/templates/includes/navbar.html` - Navigation bar
- `app/templates/includes/sidebar.html` - Sidebar menu
- `app/templates/includes/footer.html` - Footer
- `app/templates/projects/list.html` - Project table
- `app/static/css/main.css` - Main stylesheet
- `app/static/js/main.js` - Main JavaScript

**HTML Structure for Project Table:**
```html
<!-- app/templates/projects/list.html -->
{% extends "base.html" %}

{% block content %}
<div class="container-fluid">
    <div class="row mb-3">
        <div class="col">
            <h2>專案管理</h2>
        </div>
        <div class="col text-end">
            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addProjectModal">
                + 新增專案
            </button>
        </div>
    </div>

    <!-- Search and Filter -->
    <div class="row mb-3">
        <div class="col-md-4">
            <input type="text" class="form-control" id="searchInput" placeholder="搜尋...">
        </div>
        <div class="col-md-8 text-end">
            <button class="btn btn-outline-secondary" id="filterBtn">篩選</button>
            <button class="btn btn-outline-secondary" id="exportBtn">匯出</button>
        </div>
    </div>

    <!-- Project Table -->
    <div class="table-responsive">
        <table class="table table-striped table-hover" id="projectTable">
            <thead class="table-light sticky-top">
                <tr>
                    <th>Item</th>
                    <th>业务</th>
                    <th>案号</th>
                    <th>客户</th>
                    <th>取证否</th>
                    <th>型号</th>
                    <th>样机是否到齐</th>
                    <th>工程师/测试进度</th>
                    <th>预计初测报告日</th>
                    <th>预计工时</th>
                    <th>已填工时</th>
                    <th>剩余工时</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                {% for project in projects.items %}
                <tr data-id="{{ project.id }}">
                    <td>{{ project.item_number }}</td>
                    <td>{{ project.personnel }}</td>
                    <td>{{ project.case_number }}</td>
                    <td>{{ project.customer }}</td>
                    <td>{{ '是' if project.evidence_required else '否' }}</td>
                    <td>{{ project.model }}</td>
                    <td>{{ project.samples_complete }}</td>
                    <td>{{ project.engineer_progress }}</td>
                    <td>{{ project.expected_report_date }}</td>
                    <td>{{ project.estimated_hours }}</td>
                    <td>{{ project.actual_hours }}</td>
                    <td>{{ project.remaining_hours }}</td>
                    <td>
                        <button class="btn btn-sm btn-primary edit-btn" data-id="{{ project.id }}">編輯</button>
                        <button class="btn btn-sm btn-danger delete-btn" data-id="{{ project.id }}">刪除</button>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <!-- Pagination -->
    <nav>
        <ul class="pagination">
            {% if projects.has_prev %}
            <li class="page-item"><a class="page-link" href="?page={{ projects.prev_num }}">上一頁</a></li>
            {% endif %}
            {% for page_num in projects.iter_pages() %}
            <li class="page-item {{ 'active' if page_num == projects.page }}">
                <a class="page-link" href="?page={{ page_num }}">{{ page_num }}</a>
            </li>
            {% endfor %}
            {% if projects.has_next %}
            <li class="page-item"><a class="page-link" href="?page={{ projects.next_num }}">下一頁</a></li>
            {% endif %}
        </ul>
    </nav>
</div>

<!-- Add/Edit Modal -->
<div class="modal fade" id="addProjectModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
<h5 class="modal-title">新增專案</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <!-- Form content here -->
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Phase 2: Core Features (Week 3-4)

### Week 3: Advanced Table Features

#### Day 15-17: Search & Filter
**Tasks:**
1. Implement global search functionality
   - Search across all text fields
   - Highlight search results
2. Create advanced filter panel
   - Filter by personnel
   - Filter by date range
   - Filter by customer
   - Filter by evidence required
   - Filter by progress status
3. Add filter persistence (save to session)
4. Create filter presets functionality
5. Implement AJAX-based filtering

**Deliverables:**
- Global search bar
- Advanced filter panel
- Filter presets
- AJAX search/filter

**Files to Create:**
- `app/static/js/search-filter.js` - Search/filter logic
- `app/templates/projects/filter_panel.html` - Filter UI

**JavaScript for Search/Filter:**
```javascript
// app/static/js/search-filter.js
class ProjectFilter {
    constructor() {
        this.filters = {};
        this.init();
    }

    init() {
        this.setupSearchInput();
        this.setupFilterPanel();
        this.setupFilterPresets();
    }

    setupSearchInput() {
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', debounce((e) => {
            this.applyFilters({ search: e.target.value });
        }, 300));
    }

    applyFilters(newFilters) {
        this.filters = { ...this.filters, ...newFilters };
        this.fetchProjects();
    }

    fetchProjects() {
        const params = new URLSearchParams(this.filters);
        fetch(`/api/projects?${params}`)
            .then(response => response.json())
            .then(data => this.renderProjects(data))
            .catch(error => console.error('Error:', error));
    }

    renderProjects(data) {
        // Update table with filtered results
        const tbody = document.querySelector('#projectTable tbody');
        tbody.innerHTML = data.projects.map(project => this.renderRow(project)).join('');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    new ProjectFilter();
});
```

#### Day 18-21: Sorting & Advanced CRUD
**Tasks:**
1. Implement column sorting (ascending/descending)
2. Add sort indicators to table headers
3. Create inline editing capability
4. Implement batch operations:
   - Batch delete
   - Batch update status
   - Batch export
5. Add confirmation dialogs for destructive actions
6. Implement form validation with error messages
7. Add toast notifications for user feedback

**Deliverables:**
- Sortable table columns
- Inline editing
- Batch operations
- Toast notifications
- Enhanced form validation

**Files to Create:**
- `app/static/js/table-sort.js` - Sorting logic
- `app/static/js/notifications.js` - Toast notifications
- `app/utils/validators.py` - Custom validators

### Week 4: Data Management Enhancement

#### Day 22-24: Form Validation & Error Handling
**Tasks:**
1. Implement comprehensive form validation
   - Required fields validation
   - Date format validation
   - Numeric range validation
   - Unique case number validation
2. Create custom validators for business rules
3. Add client-side validation (JavaScript)
4. Add server-side validation (Flask-WTF)
5. Display validation errors clearly
6. Implement error logging system
7. Create error pages (404, 500, etc.)

**Deliverables:**
- Complete form validation
- Custom validators
- Error logging
- Error pages

**Validation Example:**
```python
# app/utils/validators.py
from wtforms.validators import ValidationError
from app.models.project import Project

def unique_case_number(form, field):
    if Project.query.filter_by(case_number=field.data, status='active').first():
        raise ValidationError('案號已存在，請使用其他案號。')

def valid_date_range(form, field):
    from datetime import datetime
    if field.data < datetime.now().date():
        raise ValidationError('預計報告日期不能早於今天。')
```

#### Day 25-28: Pagination & Performance
**Tasks:**
1. Optimize database queries
   - Add indexes to frequently queried columns
   - Implement query optimization
2. Enhance pagination
   - Add per-page selector (20, 50, 100)
   - Show total records count
   - Add "Go to page" functionality
3. Implement caching for frequently accessed data
4. Optimize JavaScript performance
5. Add loading indicators
6. Implement lazy loading for large datasets

**Deliverables:**
- Optimized database queries
- Enhanced pagination
- Caching layer
- Loading indicators

**Database Optimization:**
```python
# Add indexes to models
class Project(db.Model):
    __tablename__ = 'projects'
    __table_args__ = (
        db.Index('idx_case_number', 'case_number'),
        db.Index('idx_personnel', 'personnel'),
        db.Index('idx_expected_date', 'expected_report_date'),
        db.Index('idx_status', 'status'),
    )
```

---

## Phase 3: Visualization (Week 5-6)

### Week 5: Dashboard Foundation

#### Day 29-31: Dashboard Layout & Statistics
**Tasks:**
1. Design dashboard layout
2. Create statistics cards:
   - Total projects
   - Active projects
   - Completed projects
   - Overdue projects
   - Average completion time
   - Total work hours
3. Implement analytics service
4. Create API endpoints for dashboard data
5. Design responsive grid layout for charts

**Deliverables:**
- Dashboard page layout
- Statistics cards
- Analytics service
- Dashboard API endpoints

**Files to Create:**
- `app/routes/dashboard.py` - Dashboard routes
- `app/services/analytics_service.py` - Analytics calculations
- `app/templates/dashboard/index.html` - Dashboard page
- `app/static/js/dashboard.js` - Dashboard JavaScript
- `app/static/css/dashboard.css` - Dashboard styles

**Analytics Service:**
```python
# app/services/analytics_service.py
from app.models.project import Project
from sqlalchemy import func
from datetime import datetime, timedelta

class AnalyticsService:
    @staticmethod
    def get_project_statistics():
        total = Project.query.filter_by(status='active').count()

        # Calculate progress categories
        projects = Project.query.filter_by(status='active').all()
        in_progress = sum(1 for p in projects if 0 < p.actual_hours < p.estimated_hours)
        completed = sum(1 for p in projects if p.actual_hours >= p.estimated_hours)

        # Overdue projects
        today = datetime.now().date()
        overdue = Project.query.filter(
            Project.expected_report_date < today,
            Project.status == 'active',
            Project.actual_hours < Project.estimated_hours
        ).count()

        return {
            'total': total,
            'in_progress': in_progress,
            'completed': completed,
            'overdue': overdue
        }

    @staticmethod
    def get_personnel_workload():
        result = db.session.query(
            Project.personnel,
            func.sum(Project.estimated_hours).label('total_hours'),
            func.sum(Project.actual_hours).label('completed_hours'),
            func.count(Project.id).label('project_count')
        ).filter_by(status='active').group_by(Project.personnel).all()

        return [{
            'personnel': r.personnel,
            'total_hours': r.total_hours,
            'completed_hours': r.completed_hours,
            'project_count': r.project_count
        } for r in result]

    @staticmethod
    def get_progress_distribution():
        projects = Project.query.filter_by(status='active').all()

        distribution = {
            'not_started': 0,
            'low': 0,      # 0-40%
            'medium': 0,   # 40-80%
            'high': 0      # 80-100%
        }

        for project in projects:
            if project.actual_hours == 0:
                distribution['not_started'] += 1
            else:
                progress = (project.actual_hours / project.estimated_hours) * 100
                if progress < 40:
                    distribution['low'] += 1
                elif progress < 80:
                    distribution['medium'] += 1
                else:
                    distribution['high'] += 1

        return distribution
```

#### Day 32-35: Chart Implementation
**Tasks:**
1. Set up Chart.js library
2. Create project status pie chart
3. Create personnel workload bar chart
4. Create progress distribution chart
5. Create timeline/Gantt chart for upcoming deadlines
6. Implement chart interactivity (tooltips, click events)
7. Add chart export functionality (PNG/SVG)
8. Make charts responsive

**Deliverables:**
- 4+ interactive charts
- Chart export functionality
- Responsive chart design
- Real-time data updates

**Chart.js Implementation:**
```javascript
// app/static/js/dashboard.js
class DashboardCharts {
    constructor() {
        this.charts = {};
        this.init();
    }

    async init() {
        await this.loadData();
        this.createStatusChart();
        this.createWorkloadChart();
        this.createProgressChart();
        this.createTimelineChart();
    }

    async loadData() {
        const response = await fetch('/api/dashboard/charts');
        this.data = await response.json();
    }

    createStatusChart() {
        const ctx = document.getElementById('statusChart').getContext('2d');
        this.charts.status = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['進行中', '已完成', '逾期', '未開始'],
                datasets: [{
                    data: [
                        this.data.statistics.in_progress,
                        this.data.statistics.completed,
                        this.data.statistics.overdue,
                        this.data.statistics.not_started
                    ],
                    backgroundColor: ['#2196F3', '#4CAF50', '#F44336', '#9E9E9E']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' },
                    title: { display: true, text: '專案狀態分佈' }
                }
            }
        });
    }

    createWorkloadChart() {
        const ctx = document.getElementById('workloadChart').getContext('2d');
        const workloadData = this.data.workload;

        this.charts.workload = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: workloadData.map(d => d.personnel),
                datasets: [
                    {
                        label: '預計工時',
                        data: workloadData.map(d => d.total_hours),
                        backgroundColor: '#2196F3'
                    },
                    {
                        label: '已完成工時',
                        data: workloadData.map(d => d.completed_hours),
                        backgroundColor: '#4CAF50'
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    title: { display: true, text: '人員工作量分佈' }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    new DashboardCharts();
});
```

### Week 6: Progress Indicators & Real-time Updates

#### Day 36-38: Progress Visualization
**Tasks:**
1. Add progress bars to project table rows
2. Implement color-coded status indicators
3. Create progress percentage display
4. Add visual deadline alerts (red for overdue, yellow for approaching)
5. Create project detail page with enhanced visualizations
6. Add mini-charts to project cards
7. Implement progress history tracking

**Deliverables:**
- Progress bars in table
- Color-coded indicators
- Deadline alerts
- Project detail page with visualizations

**Progress Bar Component:**
```javascript
// app/static/js/progress-indicators.js
function renderProgressBar(project) {
    const progress = (project.actual_hours / project.estimated_hours) * 100;
    let colorClass = 'bg-danger';

    if (progress >= 80) colorClass = 'bg-success';
    else if (progress >= 40) colorClass = 'bg-warning';

    return `
        <div class="progress">
            <div class="progress-bar ${colorClass}"
                 role="progressbar"
                 style="width: ${progress}%"
                 aria-valuenow="${progress}"
                 aria-valuemin="0"
                 aria-valuemax="100">
                ${progress.toFixed(1)}%
            </div>
        </div>
    `;
}

function getDeadlineIndicator(expectedDate) {
    const today = new Date();
    const deadline = new Date(expectedDate);
    const daysUntil = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24));

    if (daysUntil < 0) {
        return '<span class="badge bg-danger">逾期</span>';
    } else if (daysUntil <= 7) {
        return `<span class="badge bg-warning">剩餘${daysUntil}天</span>`;
    } else {
        return `<span class="badge bg-success">剩餘${daysUntil}天</span>`;
    }
}
```

#### Day 39-42: Real-time Updates & Timeline
**Tasks:**
1. Implement WebSocket or Server-Sent Events for real-time updates
2. Add auto-refresh for dashboard data
3. Create notification system for project updates
4. Build timeline view for project schedules
5. Implement Gantt chart visualization
6. Add drag-and-drop for timeline adjustments
7. Create deadline reminder system

**Deliverables:**
- Real-time data updates
- Notification system
- Timeline/Gantt chart
- Deadline reminders

---

## Phase 4: Enhancement (Week 7-8)

### Week 7: Import/Export & Audit

#### Day 43-45: Export Functionality
**Tasks:**
1. Implement Excel export using openpyxl
2. Implement CSV export
3. Create PDF report generation using ReportLab
4. Add export options:
   - Export all records
   - Export filtered results
   - Export selected records
5. Include charts in PDF exports
6. Format exports to match original spreadsheet design
7. Add export progress indicator

**Deliverables:**
- Excel export
- CSV export
- PDF reports with charts
- Export UI controls

**Export Service:**
```python
# app/services/export_service.py
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
import csv
from io import BytesIO, StringIO

class ExportService:
    @staticmethod
    def export_to_excel(projects):
        wb = Workbook()
        ws = wb.active
        ws.title = "專案列表"

        # Headers
        headers = ['Item', '業務', '案號', '客戶', '取證否', '型號',
                   '樣機是否到齊', '工程師/測試進度', '預計初測報告日',
                   '預計工時', '已填工時', '剩餘工時']

        # Style headers
        header_fill = PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid")
        header_font = Font(bold=True)

        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center')

        # Data rows
        for row_num, project in enumerate(projects, 2):
            ws.cell(row=row_num, column=1, value=project.item_number)
            ws.cell(row=row_num, column=2, value=project.personnel)
            ws.cell(row=row_num, column=3, value=project.case_number)
            ws.cell(row=row_num, column=4, value=project.customer)
            ws.cell(row=row_num, column=5, value='是' if project.evidence_required else '否')
            ws.cell(row=row_num, column=6, value=project.model)
            ws.cell(row=row_num, column=7, value=project.samples_complete)
            ws.cell(row=row_num, column=8, value=project.engineer_progress)
            ws.cell(row=row_num, column=9, value=project.expected_report_date)
            ws.cell(row=row_num, column=10, value=project.estimated_hours)
            ws.cell(row=row_num, column=11, value=project.actual_hours)
            ws.cell(row=row_num, column=12, value=project.remaining_hours)

        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[column_letter].width = max_length + 2

        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output

    @staticmethod
    def export_to_csv(projects):
        output = StringIO()
        writer = csv.writer(output)

        # Headers
        writer.writerow(['Item', '業務', '案號', '客戶', '取證否', '型號',
                        '樣機是否到齊', '工程師/測試進度', '預計初測報告日',
                        '預計工時', '已填工時', '剩餘工時'])

        # Data
        for project in projects:
            writer.writerow([
                project.item_number,
                project.personnel,
                project.case_number,
                project.customer,
                '是' if project.evidence_required else '否',
                project.model,
                project.samples_complete,
                project.engineer_progress,
                project.expected_report_date,
                project.estimated_hours,
                project.actual_hours,
                project.remaining_hours
            ])

        output.seek(0)
        return output
```

#### Day 46-49: Import Functionality & Audit Logging
**Tasks:**
1. Implement Excel import with validation
2. Implement CSV import
3. Create import preview interface
4. Add data validation during import
5. Handle import errors gracefully
6. Complete audit logging system:
   - Log all CRUD operations
   - Store old and new values
   - Track user and timestamp
7. Create audit log viewer page
8. Add audit log export

**Deliverables:**
- Excel/CSV import
- Import preview and validation
- Complete audit logging
- Audit log viewer

### Week 8: User Management & Optimization

#### Day 50-52: User Management Interface
**Tasks:**
1. Create user list page (admin only)
2. Implement add/edit/delete user functionality
3. Create user profile page
4. Add password change functionality
5. Implement role management
6. Add user activity tracking
7. Create user permissions matrix

**Deliverables:**
- User management interface
- User profile page
- Role management
- Permissions system

**Files to Create:**
- `app/templates/users/list.html` - User list
- `app/templates/users/profile.html` - User profile
- `app/routes/users.py` - User management routes

#### Day 53-56: Performance Optimization & Caching
**Tasks:**
1. Implement Redis caching for:
   - Dashboard statistics
   - Frequently accessed queries
   - User sessions
2. Optimize SQL queries with eager loading
3. Add database connection pooling
4. Implement API rate limiting
5. Minify CSS and JavaScript
6. Optimize images
7. Add gzip compression
8. Implement lazy loading for images

**Deliverables:**
- Redis caching layer
- Optimized queries
- Minified assets
- Performance improvements

**Caching Implementation:**
```python
# app/utils/cache.py
from functools import wraps
from flask import current_app
import json

def cache_result(timeout=300):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"{f.__name__}:{str(args)}:{str(kwargs)}"

            # Try to get from cache
            cached = current_app.cache.get(cache_key)
            if cached:
                return json.loads(cached)

            # Execute function
            result = f(*args, **kwargs)

            # Store in cache
            current_app.cache.setex(cache_key, timeout, json.dumps(result))

            return result
        return decorated_function
    return decorator
```

---

## Phase 5: Testing & Deployment (Week 9-10)

### Week 9: Testing

#### Day 57-59: Unit Testing
**Tasks:**
1. Set up pytest environment
2. Write unit tests for models:
   - Test model creation
   - Test model relationships
   - Test calculated properties
3. Write unit tests for services:
   - Test CRUD operations
   - Test validation logic
   - Test business rules
4. Write unit tests for utilities
5. Achieve >70% code coverage
6. Set up continuous testing

**Deliverables:**
- Comprehensive unit tests
- >70% code coverage
- Test documentation

**Test Example:**
```python
# tests/test_models.py
import pytest
from app.models.project import Project
from datetime import date

def test_create_project(db_session):
    project = Project(
        item_number=1,
        personnel='Test User',
        case_number='TEST001',
        customer='Test Customer',
        evidence_required=True,
        model='Test Model',
        engineer_progress='Test Engineer/50%',
        expected_report_date=date(2025, 12, 31),
        estimated_hours=100,
        actual_hours=50
    )
    db_session.add(project)
    db_session.commit()

    assert project.id is not None
    assert project.remaining_hours == 50

def test_remaining_hours_calculation(db_session):
    project = Project(
        item_number=2,
        personnel='Test User',
        case_number='TEST002',
        customer='Test Customer',
        evidence_required=False,
        engineer_progress='Test Engineer/75%',
        expected_report_date=date(2025, 12, 31),
        estimated_hours=80,
        actual_hours=60
    )

    assert project.remaining_hours == 20
```

#### Day 60-63: Integration & End-to-End Testing
**Tasks:**
1. Write integration tests for API endpoints
2. Test authentication flows
3. Test CRUD operations through API
4. Test search and filter functionality
5. Test export/import functionality
6. Set up Selenium for E2E testing
7. Write E2E test scenarios:
   - User login
   - Create project
   - Edit project
   - Delete project
   - Dashboard interaction
8. Test browser compatibility

**Deliverables:**
- Integration tests
- E2E test scenarios
- Browser compatibility report

### Week 10: Deployment & Documentation

#### Day 64-66: Deployment Preparation
**Tasks:**
1. Set up production environment
2. Configure production database (MySQL 8.0+)
3. Set up Gunicorn/uWSGI
4. Configure Nginx reverse proxy
5. Set up SSL certificates (Let's Encrypt)
6. Configure environment variables
7. Set up logging and monitoring
8. Create backup scripts (mysqldump)
9. Set up automated MySQL database backups

**Deliverables:**
- Production environment
- Web server configuration
- SSL certificate
- Backup system

**Deployment Configuration:**
```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/lab_project_dev?charset=utf8mb4'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://user:password@localhost:3306/lab_project_prod?charset=utf8mb4'

    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/app/static;
        expires 30d;
    }
}
```

#### Day 67-70: Documentation & Final Testing
**Tasks:**
1. Write user documentation:
   - Getting started guide
   - User manual
   - Feature documentation
   - FAQ
2. Write technical documentation:
   - Architecture overview
   - API documentation
   - Database schema
   - Deployment guide
3. Create video tutorials (optional)
4. Conduct user acceptance testing (UAT)
5. Fix critical bugs found in UAT
6. Perform security audit
7. Load testing
8. Final deployment to production

**Deliverables:**
- Complete documentation
- User manual
- API documentation
- Production deployment
- Launch checklist

---

## Development Standards

### Code Style
- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Use Prettier for code formatting
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Git Workflow
- **Main branch**: Production-ready code
- **Develop branch**: Integration branch
- **Feature branches**: `feature/feature-name`
- **Bugfix branches**: `bugfix/bug-name`
- **Commit messages**: Use conventional commits format
  ```
  feat: Add user authentication
  fix: Fix pagination bug
  docs: Update API documentation
  style: Format code with prettier
  refactor: Refactor project service
  test: Add unit tests for models
  ```

### Code Review
- All code must be reviewed before merging
- Use pull request template
- Require at least one approval
- Run automated tests before merge
- Check code coverage

### Security Best Practices
- Never commit secrets to repository
- Use environment variables for sensitive data
- Implement CSRF protection
- Sanitize all user inputs
- Use parameterized queries
- Hash passwords with bcrypt
- Implement rate limiting
- Regular security audits

---

## Testing Strategy

### Test Coverage Requirements
- Unit tests: >70% coverage
- Integration tests: All API endpoints
- E2E tests: Critical user flows
- Performance tests: Load testing

### Testing Tools
- **Unit Testing**: pytest
- **Integration Testing**: pytest + Flask test client
- **E2E Testing**: Selenium
- **Load Testing**: Locust or Apache JMeter
- **Code Coverage**: pytest-cov

### Test Data
- Create fixtures for test data
- Use factory patterns for model creation
- Separate test database from development

---

## Deployment Plan

### Pre-Deployment Checklist
- [ ] All tests passing
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Backup system in place
- [ ] Monitoring configured
- [ ] SSL certificate installed
- [ ] Security audit completed

### Deployment Steps
1. Backup current production database
2. Pull latest code from repository
3. Install/update dependencies
4. Run database migrations
5. Collect static files
6. Restart application server
7. Verify deployment
8. Monitor for errors

### Rollback Plan
1. Restore database from backup
2. Revert to previous code version
3. Restart application server
4. Verify rollback successful
5. Investigate issue

---

## Maintenance Plan

### Regular Maintenance Tasks
- **Daily**: Monitor error logs, check system health
- **Weekly**: Review performance metrics, database backup verification
- **Monthly**: Security updates, dependency updates, database optimization
- **Quarterly**: Full security audit, performance review, user feedback review

### Monitoring
- Set up application monitoring (e.g., Sentry for error tracking)
- Monitor server resources (CPU, memory, disk)
- Track application performance metrics
- Set up alerts for critical issues

### Backup Strategy
- Automated daily database backups
- Retain backups for 30 days
- Weekly full system backups
- Store backups in separate location
- Regular backup restoration tests

---

## Risk Mitigation

### Technical Risks
1. **Database Performance**: Implement caching, optimize queries, add indexes
2. **Security Vulnerabilities**: Regular security audits, dependency updates
3. **Data Loss**: Automated backups, transaction management
4. **Server Downtime**: Load balancing, redundancy, monitoring

### Project Risks
1. **Scope Creep**: Strict change management, clear requirements
2. **Timeline Delays**: Buffer time in schedule, phased delivery
3. **Resource Constraints**: Prioritize features, MVP approach

---

## Success Metrics

### Technical Metrics
- Page load time < 2 seconds
- API response time < 500ms
- 99% uptime
- Error rate < 0.1%
- Test coverage > 70%

### User Metrics
- User satisfaction score > 4/5
- Active user count
- Feature adoption rate
- Support ticket reduction

---

## Appendix

### Useful Commands

**Development:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py

# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

**Database:**
```bash
# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

**Deployment:**
```bash
# Run with Gunicorn
gunicorn -w 4 -b 127.0.0.1:8000 run:app

# Collect static files
python manage.py collectstatic

# Create admin user
python manage.py create_admin
```

---

## Contact & Support

For questions or issues during implementation:
- Technical Lead: [Name]
- Project Manager: [Name]
- Repository: [URL]
- Documentation: [URL]

---

**Plan Version**: 1.0
**Last Updated**: 2025-12-30
**Status**: Ready for Implementation
