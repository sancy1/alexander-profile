# Alexander Cyril Profile Backend API

![Django](https://img.shields.io/badge/Django-5.x-green)
![DRF](https://img.shields.io/badge/Django_REST_Framework-API-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange)
![Render](https://img.shields.io/badge/Deploy-Render-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

An enterprise-grade Django REST Framework backend powering the **Alexander Cyril Portfolio Platform**.

This service provides:

- Identity & Access Management (IAM)
- JWT Authentication & Authorization
- Contact & Support Ticket Management
- Newsletter Subscription System
- CodeHub Developer Platform
- Email Verification & Password Recovery
- Administrative Analytics & Management Tools

Designed with scalability, maintainability, and security as first-class priorities.

---

# Table of Contents

- Overview
- Features
- Technology Stack
- Architecture
- Project Structure
- API Modules
- Installation
- Environment Variables
- Security
- Deployment
- Testing
- API Documentation
- Roadmap
- Author
- License

---

# Overview

The Profile Backend Service acts as the central API layer for the Alexander Cyril ecosystem.

It is responsible for:

- User authentication and profile management
- Email verification workflows
- Password reset processes
- Contact form processing
- Newsletter subscription lifecycle management
- CodeHub snippet management
- Administrative operations
- Telemetry and analytics support

The project follows a modular architecture using Django applications with clear separation of concerns through:

- Services
- Validators
- Middleware
- Permissions
- Serializers
- Business Logic Layers

---

# Features

## Authentication & Identity Management

- JWT Authentication
- Access & Refresh Tokens
- Email Verification
- Password Reset Workflow
- Secure Logout
- Change Password
- Custom User Model
- Profile Management
- Role-Based Access Control

---

## Contact Management

- Contact Form Submission
- Message Tracking
- Read/Unread Status
- Archiving System
- Search & Filtering
- Administrative Dashboard

---

## Newsletter Platform

- Subscribe
- Unsubscribe
- Welcome Email Templates
- Subscriber Reactivation
- Subscriber Analytics
- Deleted Subscriber Tracking

---

## CodeHub Platform

A developer-focused code sharing platform.

Features include:

- Code Snippet CRUD
- Categories
- Comments
- Reactions
- Sharing
- Search & Filtering
- User Activity Tracking
- Popularity Metrics
- Execution Tracking

---

## Operational Features

- PostgreSQL Support
- SQLite Development Support
- Render Deployment Optimization
- Automated Database Migrations
- Health Monitoring Middleware
- Logging System
- Environment-Based Configuration

---

# Technology Stack

## Backend

| Technology | Purpose |
|------------|----------|
| Python 3.11+ | Programming Language |
| Django 5.x | Web Framework |
| Django REST Framework | REST APIs |
| Simple JWT | Authentication |
| PostgreSQL | Production Database |
| SQLite | Development Database |
| Gunicorn | Production Server |
| Pillow | Image Processing |
| Django Filter | Filtering & Search |
| Django CORS Headers | CORS Management |

---

## Infrastructure

| Service | Purpose |
|----------|----------|
| Render | Application Hosting |
| Neon PostgreSQL | Cloud Database |
| GitHub | Source Control |

---

# Architecture

The project follows a modular service-oriented architecture.

```text
Client Applications
        │
        ▼
Django REST API Layer
        │
 ┌──────┼──────┐
 ▼      ▼      ▼

IAM   CodeHub Contact

 ▼      ▼      ▼

Services Layer
Validators Layer
Permissions Layer
Middleware Layer

        ▼

PostgreSQL Database
```

---

# Project Structure

```text
profile-backend/
│
├── src/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── user_account/
│   ├── services/
│   ├── validators/
│   ├── middleware/
│   ├── permissions.py
│   ├── serializers.py
│   ├── models.py
│   └── views.py
│
├── codehub/
│   ├── services/
│   ├── views/
│   ├── filters.py
│   ├── search_utils.py
│   ├── serializers.py
│   └── models.py
│
├── contact/
│   ├── templates/newsletter/
│   ├── services.py
│   ├── serializers.py
│   ├── models.py
│   └── views.py
│
├── scripts/
│   └── generate_secret_key.py
│
├── media/
├── logs/
│
├── build.sh
├── render.yaml
├── manage.py
└── requirements.txt
```

---

# API Modules

## User Account Module

Handles:

- Registration
- Login
- Logout
- Email Verification
- Password Reset
- Profile Updates
- Administrative User Management

### Key Endpoints

```http
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/verify-email/
POST /api/auth/request-password-reset/
POST /api/auth/reset-password/

GET  /api/auth/profile/
PUT  /api/auth/profile/update/
```

---

## Contact Module

Handles:

- Contact Form Submission
- Contact Administration
- Message Analytics

### Key Endpoints

```http
POST /api/contacts/create/
GET  /api/contacts/
GET  /api/contacts/stats/
```

---

## Newsletter Module

Handles:

- Subscription Management
- Unsubscription Workflows
- Subscriber Administration

### Key Endpoints

```http
POST /api/newsletter/subscribe/
POST /api/newsletter/unsubscribe/
GET  /api/newsletter/subscribers/
```

---

## CodeHub Module

Handles:

- Snippets
- Categories
- Comments
- Reactions
- Sharing

### Key Endpoints

```http
GET    /api/codehub/snippets/
POST   /api/codehub/snippets/create/

GET    /api/codehub/categories/
POST   /api/codehub/categories/create/
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/profile-backend.git

cd profile-backend
```

---

## Create Virtual Environment

### Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

### Windows

```powershell
python -m venv venv

venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create:

```bash
.env
```

Example:

```env
DEBUG=True

SECRET_KEY=your-secret-key

ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://user:password@localhost:5432/dbname

FRONTEND_URL=http://localhost:3000
```

Generate a secure secret key:

```bash
python scripts/generate_secret_key.py
```

---

## Run Migrations

```bash
python manage.py migrate
```

---

## Create Admin User

```bash
python manage.py createsuperuser
```

---

## Start Development Server

```bash
python manage.py runserver
```

API:

```text
http://localhost:8000/api/
```

---

# Security

The platform includes:

- JWT Authentication
- Refresh Token Rotation
- Password Hashing (PBKDF2)
- Email Verification
- Password Reset Tokens
- Role-Based Access Control
- Object-Level Permissions
- ORM-Based SQL Injection Protection
- CSRF Protection
- XSS Protection
- Environment Variable Isolation
- Secure File Upload Validation

---

# Deployment

## Render

The project includes:

### render.yaml

Infrastructure configuration.

### build.sh

```bash
pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate
```

### Start Command

```bash
gunicorn src.wsgi:application
```

---

# Testing

Run tests:

```bash
python manage.py test
```

Coverage:

```bash
coverage run manage.py test

coverage report

coverage html
```

---

# API Documentation

Interactive API documentation is available through DRF documentation tooling.

```text
/api/docs/

/api/schema/
```

---

# Roadmap

Future enhancements include:

- Redis Caching Layer
- API Versioning
- Analytics Dashboard
- Webhooks
- Multi-Language Support
- Newsletter Campaign Builder
- Export Features (CSV / Excel)
- Advanced Search
- Snippet Templates
- Code Execution Sandbox

---

# Author

## Alexander Cyril

Software Engineer specializing in:

- Full-Stack & Backend Engineering
- AI & Agentic Systems Development
- Distributed Systems & Event-Driven Architecture
- API Design & Platform Engineering
- Cloud Infrastructure, DevOps & Automation
- System Design & Scalable Architecture

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for full details.
