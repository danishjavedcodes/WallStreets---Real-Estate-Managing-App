# WallStreets — Real Estate Management System (Flask + PostgreSQL)

**WallStreets** is an open-source **real estate property management platform** for agencies that operate across multiple branches. Built with **Python Flask**, **SQLAlchemy**, and **PostgreSQL**, it delivers role-based dashboards for **customers**, **CEOs**, and **Heads of Department (HOD)** — with secure auth, modern UI, and tools for listings, invoices, payroll, and branch operations.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-Open%20Source-green)]()

**Live demo (local):** run the app and open `http://127.0.0.1:5001`

---

## Table of Contents

- [Features](#features)
- [Screenshots & UI](#screenshots--ui)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [User Roles & Demo Accounts](#user-roles--demo-accounts)
- [Routes](#routes)
- [CLI Commands](#cli-commands)
- [Security](#security)
- [Contributing](#contributing)
- [Authors](#authors)
- [Keywords](#keywords)

---

## Features

### Customer portal
- Account **registration** and **sign-in**
- Browse and **search** property listings (category, type, city)
- Responsive property cards with rent/sale badges

### CEO dashboard
- Organization-wide **analytics** (properties, branches, revenue)
- **Open branches** and assign cities
- **Register / remove HOD** accounts
- Publish **property listings** (plot, house, shop, mall, apartment, commercial)
- Manage **employees** and run **salary payroll**
- Record branch **invoices** (income & expenses)

### HOD dashboard
- Branch-scoped **property** management
- **Employee** roster for assigned branch
- **Invoice** ledger and **payroll** processing

### Platform highlights
- Application **factory** pattern with Flask **blueprints**
- **SQLAlchemy ORM** (parameterized queries, no SQL injection)
- **Flask-Login** sessions + **Werkzeug** password hashing
- **Flask-WTF** forms with **CSRF** protection
- Professional **Bootstrap 5** UI with custom real-estate design system
- Scroll animations, flash alerts, mobile-friendly admin sidebar

---

## Screenshots & UI

The rebuilt interface includes:

- **Landing page** — hero section, live stats, featured listings
- **Auth pages** — polished sign-in / registration flows
- **Customer portal** — filterable property grid
- **Admin console** — sidebar navigation, stat cards, data tables

---

## Tech Stack

| Layer | Technology |
|--------|------------|
| Backend | [Flask](https://flask.palletsprojects.com/) 3.x |
| ORM | [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) / SQLAlchemy |
| Auth | [Flask-Login](https://flask-login.readthedocs.io/) |
| Forms | [Flask-WTF](https://flask-wtf.readthedocs.io/) |
| Database | [PostgreSQL](https://www.postgresql.org/) |
| Frontend | Bootstrap 5, Bootstrap Icons, custom CSS/JS |
| Config | python-dotenv |

---

## Architecture

```mermaid
flowchart TB
    subgraph users [Users]
        C[Customer]
        CEO[CEO]
        HOD[HOD]
    end

    subgraph flask [Flask App - run.py]
        BP[Blueprints]
        SVC[Services Layer]
        ORM[SQLAlchemy Models]
    end

    subgraph db [PostgreSQL]
        T[(Tables)]
    end

    C --> BP
    CEO --> BP
    HOD --> BP
    BP --> SVC
    SVC --> ORM
    ORM --> T
```

---

## Project Structure

```
WallStreets---Real-Estate-Managing-App/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Environment settings
│   ├── extensions.py        # db, login_manager, csrf
│   ├── models.py            # Branch, AdminUser, Customer, Product, ...
│   ├── forms.py             # WTForms
│   ├── services.py          # Business logic
│   ├── decorators.py        # Role-based access
│   ├── seed.py              # Seed & password migration
│   ├── blueprints/
│   │   ├── main/            # Home, about
│   │   ├── auth/            # Login, register, logout
│   │   ├── customer/        # Listings portal
│   │   └── admin/           # CEO & HOD console
│   ├── templates/           # Jinja2 HTML
│   └── static/              # CSS, JavaScript
├── run.py                   # Recommended entry point
├── main.py                  # Legacy wrapper → run.py
├── requirements.txt
├── .env.example
├── scripts/init_db.sql      # Legacy SQL bootstrap reference
├── adminusrquries.sql       # Original schema (historical)
└── README.md
```

---

## Prerequisites

- **Python 3.10+**
- **PostgreSQL 12+** (16 recommended)
- `pip` and `venv`
- **Git**

---

## Installation

```bash
git clone https://github.com/danishjavedcodes/WallStreets---Real-Estate-Managing-App.git
cd WallStreets---Real-Estate-Managing-App

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## Configuration

Copy the example environment file and edit values:

```bash
cp .env.example .env
```

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask session secret | Random string |
| `DATABASE_URL` | PostgreSQL connection URI | `postgresql://postgres:pass@localhost:5432/Wall-Street-Admin` |
| `PORT` | Server port (5001 avoids macOS AirPlay on 5000) | `5001` |

---

## Database Setup

### 1. Start PostgreSQL

```bash
# macOS (Homebrew)
brew services start postgresql@16
```

### 2. Create database

```bash
createdb "Wall-Street-Admin"
```

### 3. Initialize tables & seed data

```bash
export FLASK_APP=run:app
flask init-db
flask hash-passwords    # Hash any legacy plain-text passwords
```

---

## Running the Application

```bash
source venv/bin/activate
python run.py
```

Open in your browser:

**http://127.0.0.1:5001**

> **Note:** On macOS, port **5000** is often used by **AirPlay Receiver**. This project defaults to **5001** via the `PORT` environment variable.

---

## User Roles & Demo Accounts

| Role | User ID | Password | Access |
|------|---------|----------|--------|
| **CEO** | `1` | `ceo123` | Full admin console |
| **HOD** | `2` | `hod123` | Branch-scoped admin |
| **Customer** | `1` | `12347` | Property search & browse |

Sign in at **/auth/login** — admins and customers use the same page; the app routes you by role.

---

## Routes

| Route | Description |
|-------|-------------|
| `/` | Landing page with featured listings |
| `/about` | About the platform |
| `/auth/login` | Sign in (customer or admin) |
| `/auth/register` | Customer registration |
| `/auth/logout` | Sign out |
| `/customer/dashboard` | Customer home |
| `/customer/properties` | Searchable property listings |
| `/admin/dashboard` | CEO / HOD analytics |
| `/admin/properties` | Manage listings |
| `/admin/branches` | Open branches (CEO only) |
| `/admin/hods` | HOD management (CEO only) |
| `/admin/employees` | Employee roster |
| `/admin/invoices` | Invoices & payroll |

---

## CLI Commands

```bash
export FLASK_APP=run:app

flask init-db           # Create tables + seed demo data
flask hash-passwords    # Migrate plain-text passwords to hashes
```

---

## Security

- Passwords stored with **Werkzeug** hashing (`pbkdf2` / `scrypt`)
- **CSRF** tokens on all POST forms
- **Role decorators** restrict CEO-only routes
- Database access via **SQLAlchemy** (no string-built SQL)
- Never commit `.env` — use `.env.example` as a template

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit with a clear message
4. Push and open a Pull Request

---

## Authors

Originally developed as a collaborative university / team project. Rebuilt with a professional Flask architecture including:

- **Danish Javed** — schema, auth, products, invoices
- **Ali** — products table design
- **Shurahbeel** — backup triggers, payroll procedures

**Repository:** [danishjavedcodes/WallStreets---Real-Estate-Managing-App](https://github.com/danishjavedcodes/WallStreets---Real-Estate-Managing-App)

---

## Keywords

`real estate management system` · `property management software` · `Flask real estate app` · `PostgreSQL property database` · `real estate admin panel` · `multi-branch property management` · `CEO HOD dashboard` · `property listing CRUD` · `invoice management` · `employee payroll` · `Python web application` · `WallStreets` · `open source real estate`

---

## Star this repo

If this project helped you learn **Flask**, **PostgreSQL**, or **real estate web development**, consider giving it a star on GitHub.
