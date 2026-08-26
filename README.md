# G Project

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.14-red)
![Firebase](https://img.shields.io/badge/Firebase-Auth-FFCA28?logo=firebase&logoColor=black)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-Local_DB-003B57?logo=sqlite&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?logo=vercel&logoColor=white)
![License](https://img.shields.io/badge/License-Graduation_Project-lightgrey)

**G Project** is a secure file web platform for a graduation project. Users sign up and log in with Firebase, upload files, receive an automatic malware scan report, and download their own encrypted files.

**Live site:** [https://g-project-ten.vercel.app](https://g-project-ten.vercel.app)

---

## Tools & stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, Django 4.2, Django REST Framework |
| Auth | Firebase Authentication + JWT (SimpleJWT) |
| Frontend | Django templates, HTML, CSS, vanilla JavaScript |
| Security | AES file encryption (`cryptography`), malware heuristics |
| Database | SQLite (local) / PostgreSQL optional (production) |
| Static files | WhiteNoise (local), Vercel static CDN (production) |
| Tests | pytest, pytest-django |
| Deploy | Vercel serverless (Python + static assets) |
| Optional | Docker Compose for local container runs |

---

## Features

- Firebase email/password sign up and login
- Drag-and-drop file upload
- Automatic malware scan with confidence score and report
- AES-256 encrypted storage on disk
- Download and delete your own files
- Single URL for frontend pages and REST API

---

## Quick start (local)

```powershell
cd "C:\Users\youss\OneDrive\Desktop\G project"
copy .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd backend
python manage.py migrate
python manage.py runserver
```

Open **http://127.0.0.1:8000/**

---

## Deploy to Vercel

```powershell
# First time
.\deploy-setup.bat

# Later deploys
.\deploy.bat
```

See [docs/Vercel&deployment.md](docs/Vercel&deployment.md) for full details.

---

## Documentation

| Document | Description |
|----------|-------------|
| [Folder & file structure](docs/Folder&fileStructure.md) | Project tree and what each folder does |
| [Backend](docs/Backend.md) | Django apps, API, auth, files, scanning |
| [Frontend](docs/Frontend.md) | Templates, CSS, JavaScript, pages |
| [Vercel & deployment](docs/Vercel&deployment.md) | Production hosting and auto-deploy |

---

## API overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/auth/firebase-config/` | Firebase web config |
| `POST` | `/api/auth/firebase/` | Firebase login / sign-up |
| `GET` | `/api/auth/me/` | Current user |
| `GET` | `/api/files/` | List your files |
| `POST` | `/api/files/upload/` | Upload a file |
| `GET` | `/api/files/{id}/download/` | Download a file |
| `DELETE` | `/api/files/{id}/delete/` | Delete a file |
| `GET` | `/api/scanning/report/{id}/` | Malware scan report |

---

## Tests

```powershell
cd backend
pytest
```

---

## Project structure (short)

```
G project/
├── api/           # Vercel serverless entry
├── backend/       # Django project + apps
├── frontend/      # HTML templates + static assets
├── ml/            # Malware inference engine
├── scripts/       # Deploy automation
├── tests/         # pytest suite
├── docs/          # Documentation
└── vercel.json    # Vercel config
```

---

## Author

Graduation project — **NuclearMonster1**
