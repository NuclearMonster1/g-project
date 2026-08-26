# Folder & File Structure

Complete map of the **G Project** repository.

---

## Root tree

```
G project/
│
├── api/                          # Vercel serverless entry point
│   ├── index.py                  # Bootstraps Django WSGI for Vercel
│   └── requirements.txt          # Python deps for the Vercel function
│
├── backend/                      # Django backend
│   ├── manage.py                 # Django CLI
│   ├── requirements.txt          # Local dev deps (includes pytest)
│   ├── db.sqlite3                # Local database (gitignored)
│   ├── config/                   # Project settings and routing
│   │   ├── settings.py           # Main configuration
│   │   ├── urls.py               # Root URL routes
│   │   ├── middleware.py         # Vercel startup (migrations)
│   │   ├── wsgi.py               # WSGI application
│   │   └── asgi.py               # ASGI application
│   └── apps/
│       ├── accounts/             # Users, Firebase auth, JWT
│       ├── files/                # Upload, encrypt, download, delete
│       └── scanning/             # Malware scan + security reports
│
├── frontend/                     # Web UI (served by Django + Vercel static)
│   ├── templates/
│   │   ├── index.html            # Login page (home)
│   │   ├── signup.html           # Sign up page
│   │   └── dashboard.html        # File upload & management
│   └── static/
│       ├── css/style.css         # App styling (dark theme)
│       └── js/
│           ├── auth.js           # Firebase login / sign-up
│           └── dashboard.js      # Upload, list, download, delete
│
├── ml/                           # Machine learning / malware detection
│   └── inference.py              # Heuristic scan engine (entropy, EICAR, extensions)
│
├── docker/                       # Optional local Docker setup
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── scripts/                      # Deployment scripts (Windows)
│   ├── deploy.ps1                # Main Vercel deploy script
│   └── refresh-path.ps1          # Fixes Node.js PATH on Windows
│
├── tests/                        # Automated tests
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_files.py
│   └── test_scanning.py
│
├── docs/                         # Project documentation
│   ├── Folder&fileStructure.md   # This file
│   ├── Backend.md
│   ├── Frontend.md
│   └── Vercel&deployment.md
│
├── media/                        # Django MEDIA_ROOT (runtime, mostly empty)
├── storage/                      # Encrypted uploaded files (gitignored)
│
├── .env.example                  # Environment variable template
├── .gitignore
├── .vercelignore                 # Files excluded from Vercel upload
├── build.sh                      # Vercel build (collectstatic + migrate)
├── deploy.bat                    # One-click production deploy
├── deploy-setup.bat              # First-time Vercel setup + deploy
├── vercel-login.bat              # Vercel OAuth login helper
├── package.json                  # Vercel CLI + npm scripts
├── pytest.ini                    # Test configuration
├── requirements.txt              # Root Python deps (used by Vercel install)
├── vercel.json                   # Vercel routing and build config
└── README.md                     # Project overview
```

---

## Folder purposes

| Folder | Purpose |
|--------|---------|
| `api/` | Vercel Python function — runs Django as a serverless app |
| `backend/` | All server-side logic: auth, files, scanning, database |
| `frontend/` | User-facing HTML, CSS, and JavaScript |
| `ml/` | Malware detection logic used by the scanning app |
| `docker/` | Optional containerized local development |
| `scripts/` | PowerShell helpers for Windows deploy workflow |
| `tests/` | API and integration tests |
| `docs/` | Detailed documentation |
| `storage/` | Encrypted files at rest: `storage/{user-id}/{file-id}.enc` |
| `media/` | Reserved for Django media uploads (not heavily used) |

---

## Key config files

| File | Role |
|------|------|
| `backend/config/settings.py` | Database, Firebase, JWT, encryption, Vercel detection |
| `backend/config/urls.py` | Maps URLs to pages and API endpoints |
| `vercel.json` | Routes `/static/*` to CDN and everything else to Django |
| `.env` | Secrets and config (never commit — copy from `.env.example`) |
| `build.sh` | Runs on Vercel build: install deps, collectstatic, migrate |

---

## Generated / ignored files

These exist locally but are **not** in git:

| Path | What it is |
|------|------------|
| `.venv/` | Python virtual environment |
| `node_modules/` | Vercel CLI (npm) |
| `.vercel/` | Local Vercel project link |
| `backend/db.sqlite3` | Local SQLite database |
| `storage/**/*.enc` | Encrypted uploaded files |
| `__pycache__/` | Python bytecode cache |
| `.env` | Your local secrets |

---

## Data flow (upload)

```
Browser (dashboard.js)
  → POST /api/files/upload/  (JWT in header)
  → files app encrypts file
  → saves to storage/{user-id}/{file-id}.enc
  → scanning app runs ml/inference.py
  → report saved to database
  → user can download via GET /api/files/{id}/download/
```
