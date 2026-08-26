# G Project — Simple Secure File Web App

Graduation project: a **simple local web application** for file upload, malware scan report, and download.

## Features

- Sign up and log in with **Firebase Authentication**
- Upload files (drag-and-drop)
- Automatic malware scan (shows a report)
- Download your own files
- Runs locally on your machine

**Removed for simplicity:** admin panel, quarantine blocking, audit log, file sharing.

## Firebase Auth setup

1. Open [Firebase Console](https://console.firebase.google.com/) and create a project.
2. Enable **Authentication → Sign-in method → Email/Password**.
3. Add a **Web app** (Project settings → Your apps → `</>`).
4. Copy the config values into `.env`:

```
FIREBASE_API_KEY=your-api-key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_APP_ID=your-app-id
```

5. Restart the Django server.

Sign up creates the user in Firebase, then the app stores the same email in Django so file upload/download still work.

## Run locally

```powershell
cd "C:\Users\youss\OneDrive\Desktop\G project"
.\.venv\Scripts\Activate.ps1
cd backend
python manage.py runserver
```

Open **http://127.0.0.1:8000/**

## First time setup

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

## How it works

1. **Sign up** with Firebase (email + password)
2. **Log in** with the same Firebase account
3. **Upload** a file on the dashboard
4. System **scans** the file and saves a report
5. **Download** the file anytime (scan report is informational only)

## Where files are saved

```
G project/storage/{your-user-id}/{file-id}.enc
```

Metadata is in `backend/db.sqlite3`.

## API

| Endpoint | Description |
|----------|-------------|
| `POST /api/auth/register/` | Register (local fallback) |
| `POST /api/auth/login/` | Login (local fallback) |
| `GET /api/auth/firebase-config/` | Firebase web config |
| `POST /api/auth/firebase/` | Firebase sign-up / login |
| `GET /api/files/` | List your files |
| `POST /api/files/upload/` | Upload |
| `GET /api/files/{id}/download/` | Download |
| `GET /api/scanning/report/{id}/` | Scan report |

## Tests

```powershell
pytest
```

## Deploy to Vercel (public website)

See **[VERCEL.md](VERCEL.md)** for full steps.

Quick deploy:

```powershell
npm install
npx vercel login
npx vercel --prod
```

Your app will be live at a `*.vercel.app` URL (not localhost).
