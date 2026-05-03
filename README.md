
# 🚀 SchedulAI – AI Timetable Generator

# 📅 SchedulAI — AI-Powered School Timetable Generator

> *From chaos to schedule in seconds. Built for schools, powered by intelligence.*

---

## 🌟 What is SchedulAI?

SchedulAI is a full-stack Django web application that automates the creation of school timetables using constraint-based scheduling logic. What used to take a vice-principal days of manual work — juggling teachers, classrooms, subjects, periods, and breaks — SchedulAI does in under 30 seconds.

It is built for **school administrators** who manage multiple grades, divisions, faculty members, and bell schedules simultaneously, and need a reliable, conflict-free timetable every single term.

---

## 🎯 The Problem It Solves

Manual timetable creation in schools is:
- **Time-consuming** — takes 2–5 days per term for a medium-sized school
- **Error-prone** — teachers double-booked, rooms clashing, periods miscounted
- **Inflexible** — one change cascades into dozens of manual corrections
- **Opaque** — no visibility into workload distribution or scheduling gaps

SchedulAI eliminates all of this.

---

## 🚀 Core Features

### 🗓 Timetable Generation
- AI-powered constraint-based scheduling engine
- Generates conflict-free timetables across all divisions and days
- Supports multiple working days (Mon–Sat configurable)
- Real-time generation status with live polling
- Handles failed generation gracefully with error logs

### 🔔 Bell Schedule Management
- Create and manage multiple bell schedules
- Define class periods, break periods, and their timings
- Assign bell schedules to specific timetables
- Add/remove periods dynamically

### 👨‍🏫 Faculty Management
- Full CRUD for faculty profiles
- Track active/inactive status
- Store email addresses for direct communication
- Faculty leave history tracking
- Workload analytics per teacher

### 🏫 Resources Management
- Manage grades, divisions, subjects, and rooms
- Room type classification (lab, classroom, hall, etc.)
- Capacity and building tracking
- Subject-to-division assignment

### 📊 Reports & Analytics
- Faculty workload distribution with visual bar charts
- Subject slot distribution analysis
- Day-wise scheduling density charts
- Leave history overview
- Per-timetable deep analytics

### 📧 Email Distribution
- Send personalized timetables to each faculty member
- Attaches an Excel file with their individual schedule
- Sends in background thread — no UI blocking
- Bulk select all or specific faculty members

### 📤 Export Options
- **Excel export** — full timetable as `.xlsx` with auto-sized columns
- **PDF export** — print-ready timetable layout (via WeasyPrint)

### 🔴 Live View Mode
- Real-time view of what's happening right now
- Shows current period, current classes, next period
- Auto-refreshes every 2 minutes
- Dark-themed dashboard display for notice boards

### 🤖 AI Chatbot
- Integrated chatbot for scheduling queries
- Natural language interface for timetable insights

---

## 🎨 Design Philosophy

SchedulAI was designed with a **dark sidebar + clean white content** aesthetic — a deliberate choice to create visual hierarchy and reduce cognitive load for administrators who spend hours inside the app.

### Design Decisions

| Decision | Reason |
|---|---|
| Dark sidebar (`#0f0e1a`) | Grounds the UI, reduces eye strain on long sessions |
| Syne font for headings | Geometric, authoritative — feels like a scheduling tool |
| DM Sans for body | Highly readable at small sizes in dense data tables |
| Indigo primary (`#5b4ff5`) | Professional yet distinctive, avoids corporate blue clichés |
| Card-based layout | Isolates data contexts, prevents information overload |
| Color-coded timetable cells | Instant subject recognition without reading text |
| Hover scale on timetable cells | Subtle interactivity cue in dense grid layouts |
| Division tab switching | Avoids overwhelming the user with all data at once |
| Live pulse animation | Real-time status communicated without text |

### Component Highlights
- **Timetable grid** — responsive, scrollable, color-coded per subject with hover states
- **Email modal** — avatar initials, checkbox selection, live count, animated send state
- **Generation spinner** — live log output during AI generation with polling
- **Bell schedule builder** — period-by-period construction with type classification
- **Analytics charts** — pure CSS bar/progress charts, no external chart library needed

---

## 🏗 Technical Architecture

```
schedulai/
├── config/                  # Django project settings & root URLs
├── timetables/              # Core app — timetables, slots, generation
│   ├── models.py            # Timetable, Lesson, TimetableSlot, BellSchedule, Period
│   ├── views.py             # 15+ class-based views
│   ├── urls.py              # Named URL patterns with namespace
│   ├── forms.py             # TimetableForm, LessonForm, BellScheduleForm
│   └── templatetags/        # Custom template filters (get_div, get_day, get_period)
├── faculty/                 # Faculty profiles, leave management
├── resources/               # Grades, divisions, subjects, rooms
├── reports/                 # Analytics and workload reports
├── chatbot/                 # AI assistant interface
├── scheduling/              # Constraint-based generation engine
│   └── engine.py            # TimetableGenerator core algorithm
└── templates/               # All HTML templates
```

### Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2 (Python 3.12) |
| Database | SQLite (dev) / PostgreSQL (prod-ready) |
| Auth | Django built-in + LoginRequiredMixin |
| Email | Django SMTP + Gmail App Password |
| Excel | openpyxl |
| PDF | WeasyPrint |
| Frontend | Vanilla HTML/CSS/JS (no frontend framework) |
| Fonts | Google Fonts — Syne + DM Sans |
| Task Queue | Threading (dev) / Celery-ready (prod) |

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repo
git clone https://github.com/yourname/schedulai.git
cd schedulai

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

### Environment / Settings

```python
# config/settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'   # Gmail App Password
DEFAULT_FROM_EMAIL = 'your@gmail.com'
```

---

## 📌 Key URLs

| URL | View | Purpose |
|---|---|---|
| `/timetables/` | TimetableListView | All timetables |
| `/timetables/create/` | TimetableCreateView | New timetable |
| `/timetables/<pk>/setup/` | TimetableSetupView | Add lessons, configure |
| `/timetables/<pk>/generate/` | GenerateTimetableView | Trigger AI generation |
| `/timetables/<pk>/view/` | TimetableGridView | Visual grid + export |
| `/timetables/<pk>/live/` | TimetableLiveView | Live period view |
| `/timetables/<pk>/export/excel/` | ExportExcelView | Download Excel |
| `/timetables/<pk>/export/pdf/` | ExportPdfView | Download PDF |
| `/timetables/<pk>/send-email/` | SendEmailView | Email faculty |
| `/timetables/bells/` | BellScheduleListView | Bell schedules |
| `/faculty/` | Faculty CRUD | Manage teachers |
| `/resources/` | Resources CRUD | Grades, rooms, subjects |
| `/reports/` | reports_home | Analytics dashboard |
| `/chatbot/` | AI chatbot | Natural language queries |

---

## 💡 Impact

### For Schools
- **Saves 2–5 days** of manual scheduling work per academic term
- **Zero conflicts** — no teacher double-booked, no room clash
- **Instant changes** — regenerate in 30 seconds after any curriculum change
- **Direct delivery** — faculty receive their personal schedules via email with Excel attachment

### For Administrators
- Full visibility into faculty workload and subject distribution
- Analytics to identify scheduling imbalances before they become problems
- One-click export for printing and sharing

### For Faculty
- Personal timetable delivered to inbox
- Excel format they can open anywhere
- Live view available on any screen for real-time period tracking

---

## 🛣 Roadmap

- [ ] Celery + Redis for true async email delivery
- [ ] Constraint customization UI (teacher preferences, room preferences)
- [ ] Multi-school / SaaS mode with organization isolation
- [ ] Mobile app (PWA)
- [ ] Google Calendar sync
- [ ] Substitution management when faculty are on leave
- [ ] iCal export

---

## 👨‍💻 Built By

Built as a full-stack Django project with a focus on real-world school administration problems. Every feature — from the scheduling engine to the email system to the live view — was designed around actual pain points in school management.

---

*SchedulAI — Because your time is better spent teaching than scheduling.*

## ⚙️ Setup

```bash
git clone https://github.com/your-username/schedulai.git
cd schedulai
pip install -r requirements.txt
```

Create `.env` file:

```
SECRET_KEY=your-key
GROQ_API_KEY=your-key
```

Run:

```bash
python manage.py migrate
python manage.py runserver
```

## 🌐 Deployment
https://schedulai-1-1zfs.onrender.com/
Render / Railway recommended


