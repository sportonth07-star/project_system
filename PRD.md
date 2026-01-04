# Product Requirements Document (PRD)
## Laboratory Project Progress Management System

---

## 1. Project Overview

### 1.1 Product Name
Laboratory Project Progress Management System (實驗室專案進度管制表)

### 1.2 Product Vision
A web-based management system designed to track and visualize laboratory project progress, enabling efficient monitoring of test cases, work orders, personnel assignments, and project timelines.

### 1.3 Technology Stack
- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: MySQL 8.0+
- **Visualization**: Chart.js or similar library

---

## 2. Target Users

### 2.1 Primary Users
- Laboratory managers
- Test engineers/personnel
- Project coordinators
- Quality assurance teams

### 2.2 User Roles
- **Admin**: Full CRUD permissions, system configuration
- **Manager**: View all projects, edit assigned projects
- **Tester**: View and update assigned work orders

---

## 3. Core Features

### 3.1 Data Management (CRUD Operations)

#### 3.1.1 Create
- Add new project entries with all required fields
- Bulk import from CSV/Excel (optional enhancement)
- Duplicate existing entries for similar projects

#### 3.1.2 Read/View
- Display project list in table format
- Search and filter capabilities
- Sort by any column (ascending/descending)
- Pagination for large datasets

#### 3.1.3 Update
- Edit individual project fields inline or via modal
- Update progress percentages
- Modify dates and personnel assignments
- Track modification history (audit log)

#### 3.1.4 Delete
- Soft delete with confirmation dialog
- Archive completed projects
- Permanent deletion (admin only)

### 3.2 Data Fields

Based on the reference image, the system must support the following columns:

| Field Name (CN) | Field Name (EN) | Data Type | Required | Description |
|----------------|-----------------|-----------|----------|-------------|
| item | Item Number | Integer | Yes | Sequential project ID |
| 业务 | Business/Personnel | String | Yes | Test personnel name |
| 案号 | Case Number | String | Yes | Work order/case ID |
| 客户 | Customer | String | Yes | Customer name |
| 取证否 | Evidence Required | Boolean | Yes | Yes/No (是/否) |
| 型号 | Model | String | No | Device/product model |
| 样机是否到齐 | Samples Complete | String | No | Sample status (是/是(10)/是(11)) |
| 工程师/测试进度 | Engineer/Test Progress | String | Yes | Engineer name and progress % |
| 预计初测报告日 | Expected Initial Report Date | Date | Yes | Target date for initial report |
| 预计工时 | Estimated Hours | Integer | Yes | Estimated work hours |
| 已填工时 | Actual Hours | Integer | Yes | Actual hours logged |
| 剩余工时 | Remaining Hours | Integer | Auto | Calculated: Estimated - Actual |

### 3.3 Visualization Features

#### 3.3.1 Dashboard
- **Project Status Overview**: Pie chart showing distribution of project statuses
- **Progress Summary**: Bar chart of overall completion rates
- **Personnel Workload**: Stacked bar chart showing work distribution by tester
- **Timeline View**: Gantt chart or timeline visualization
- **Deadline Alerts**: Highlight overdue or approaching deadlines

#### 3.3.2 Progress Indicators
- Visual progress bars for each project row
- Color-coded status indicators:
  - Green: On track (≥80% progress)
  - Yellow: At risk (40-79% progress)
  - Red: Delayed (<40% progress or overdue)
  - Grey: Completed (100%)

#### 3.3.3 Analytics
- Average completion time by project type
- Personnel efficiency metrics
- Workload distribution reports
- Export reports as PDF/Excel

---

## 4. Functional Requirements

### 4.1 Table Display
- **FR-001**: Display all projects in a responsive table layout matching the reference format
- **FR-002**: Support column resizing and reordering
- **FR-003**: Fixed header for scrollable content
- **FR-004**: Alternating row colors for readability
- **FR-005**: Highlight selected rows

### 4.2 Search & Filter
- **FR-006**: Global search across all fields
- **FR-007**: Advanced filter by:
  - Personnel name
  - Date range (start date, end date)
  - Case number
  - Customer
  - Progress status
  - Evidence requirement
- **FR-008**: Save filter presets

### 4.3 CRUD Operations
- **FR-009**: Add new project via form modal
- **FR-010**: Edit project inline or via modal
- **FR-011**: Delete project with confirmation
- **FR-012**: Batch operations (delete, update status)
- **FR-013**: Form validation for all required fields

### 4.4 Data Visualization
- **FR-014**: Dashboard with 4+ chart types
- **FR-015**: Interactive charts with drill-down capability
- **FR-016**: Real-time data updates
- **FR-017**: Export charts as images

### 4.5 User Management
- **FR-018**: User authentication (login/logout)
- **FR-019**: Role-based access control
- **FR-020**: User profile management

### 4.6 Data Export/Import
- **FR-021**: Export table data to Excel/CSV
- **FR-022**: Import data from Excel/CSV
- **FR-023**: Generate PDF reports

---

## 5. Non-Functional Requirements

### 5.1 Performance
- **NFR-001**: Page load time < 2 seconds
- **NFR-002**: Support 1000+ project records without performance degradation
- **NFR-003**: Search results returned in < 500ms

### 5.2 Usability
- **NFR-004**: Responsive design (desktop, tablet, mobile)
- **NFR-005**: Intuitive UI with minimal training required
- **NFR-006**: Support Traditional Chinese (繁體中文) language interface
- **NFR-007**: Keyboard shortcuts for common operations

### 5.3 Security
- **NFR-008**: Secure password storage (hashing)
- **NFR-009**: SQL injection prevention
- **NFR-010**: XSS protection
- **NFR-011**: CSRF token implementation
- **NFR-012**: Session timeout after 30 minutes of inactivity

### 5.4 Reliability
- **NFR-013**: 99% uptime
- **NFR-014**: Automatic database backup daily
- **NFR-015**: Error logging and monitoring

### 5.5 Maintainability
- **NFR-016**: Clean code architecture
- **NFR-017**: Comprehensive documentation
- **NFR-018**: Unit test coverage > 70%

---

## 6. User Interface Requirements

### 6.1 Layout
- **Top Navigation Bar**: Logo, search bar, user menu
- **Sidebar**: Dashboard, Projects, Reports, Settings
- **Main Content Area**: Data table or dashboard
- **Footer**: Copyright, version info

### 6.2 Color Scheme
- Primary: Professional blue (#2196F3)
- Secondary: Gray tones for backgrounds
- Success: Green (#4CAF50)
- Warning: Yellow/Orange (#FF9800)
- Danger: Red (#F44336)
- Neutral: White/Light gray backgrounds

### 6.3 Typography
- Headers: Sans-serif font (e.g., Arial, Roboto, Microsoft JhengHei)
- Body: Readable font size (14-16px)
- Support for Traditional Chinese characters (繁體中文)

### 6.4 Components
- Data table with sorting and filtering
- Modal dialogs for forms
- Toast notifications for user feedback
- Progress bars and status badges
- Date pickers for date fields
- Dropdown selectors for predefined values

---

## 7. Data Model

### 7.1 Database Schema

#### Projects Table
```sql
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
```

#### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### Audit Log Table
```sql
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
```

---

## 8. API Endpoints

### 8.1 Project Management
- `GET /api/projects` - Get all projects (with pagination, filtering)
- `GET /api/projects/<id>` - Get single project
- `POST /api/projects` - Create new project
- `PUT /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project
- `GET /api/projects/export` - Export projects to Excel/CSV

### 8.2 Dashboard & Analytics
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/charts` - Get chart data
- `GET /api/reports/personnel` - Personnel workload report
- `GET /api/reports/timeline` - Timeline data

### 8.3 User Management
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/users` - Get all users (admin)
- `POST /api/users` - Create user (admin)
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user (admin)

---

## 9. Implementation Phases

### Phase 1: Foundation (Week 1-2)
- Set up Flask project structure
- Design database schema
- Implement user authentication
- Create basic CRUD operations
- Design responsive table layout

### Phase 2: Core Features (Week 3-4)
- Implement full CRUD functionality
- Add search and filter capabilities
- Create form validation
- Implement pagination
- Add sorting functionality

### Phase 3: Visualization (Week 5-6)
- Build dashboard page
- Implement chart components
- Add progress indicators
- Create timeline view
- Implement real-time updates

### Phase 4: Enhancement (Week 7-8)
- Add export/import functionality
- Implement audit logging
- Create user management interface
- Add batch operations
- Performance optimization

### Phase 5: Testing & Deployment (Week 9-10)
- Unit testing
- Integration testing
- User acceptance testing
- Bug fixes
- Documentation
- Deployment to production

---

## 10. Success Metrics

### 10.1 Adoption Metrics
- Number of active users (weekly/monthly)
- Number of projects managed
- User login frequency

### 10.2 Engagement Metrics
- Average session duration
- Number of CRUD operations per user
- Dashboard view frequency

### 10.3 Performance Metrics
- Page load time
- API response time
- Error rate

### 10.4 Business Metrics
- Time saved in project tracking
- Reduction in missed deadlines
- Improved project completion rate

---

## 11. Risks & Mitigations

### 11.1 Technical Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Database performance degradation | High | Medium | Implement indexing, pagination, caching |
| Browser compatibility issues | Medium | Low | Test on major browsers, use polyfills |
| Data loss | High | Low | Regular backups, transaction management |

### 11.2 Project Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Scope creep | High | Medium | Clear requirements, change management |
| Delayed timeline | Medium | Medium | Phased delivery, MVP approach |
| User adoption resistance | Medium | Low | Training, intuitive UI design |

---

## 12. Dependencies

### 12.1 Technical Dependencies
- Python 3.8+
- Flask 2.x
- SQLAlchemy (ORM)
- PyMySQL or mysqlclient (MySQL driver)
- Flask-Login (authentication)
- Chart.js or Plotly (visualization)
- Bootstrap or Tailwind CSS (UI framework)

### 12.2 External Dependencies
- MySQL 8.0+ database server
- Web server (Gunicorn/uWSGI)
- Reverse proxy (Nginx)

---

## 13. Open Questions

1. Should the system support multiple languages or only Traditional Chinese?
2. What is the expected number of concurrent users?
3. Is there an existing system to migrate data from?
4. Are there specific compliance or audit requirements?
5. What authentication method is preferred (local, LDAP, OAuth)?
6. Should the system send email notifications for deadlines?
7. Is mobile app support required in the future?
8. What is the preferred MySQL hosting environment (on-premise, cloud)?

---

## 14. Appendix

### 14.1 Glossary
- **Work Order**: A tracked project or test case
- **Case Number**: Unique identifier for each work order
- **Evidence Required**: Flag indicating if documentation is needed
- **Initial Report**: First test report for a project

### 14.2 References
- Reference design: 1.png
- Requirements document: idea.md
- Flask documentation: https://flask.palletsprojects.com/
- Chart.js documentation: https://www.chartjs.org/

---

**Document Version**: 1.0
**Last Updated**: 2025-12-30
**Author**: Claude Code
**Status**: Draft - Awaiting Approval
