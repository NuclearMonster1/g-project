# Backend

Django REST API that powers authentication, file storage, and malware scanning.

---

## Stack

- **Python 3.12**
- **Django 4.2** — web framework
- **Django REST Framework** — REST API
- **SimpleJWT** — JSON Web Tokens
- **Firebase** — email/password authentication (frontend → token → backend verify)
- **cryptography** — AES encryption for files at rest
- **WhiteNoise** — static file serving (local dev)
- **SQLite** — local database; PostgreSQL optional via `DATABASE_URL`

---

## Django apps

### `accounts` — Authentication

| File | Role |
|------|------|
| `models.py` | Custom `User` model with `email` and `firebase_uid` |
| `firebase.py` | Verify Firebase ID tokens via Identity Toolkit API |
| `views.py` | Register, login, Firebase auth, `/me` endpoint |
| `urls.py` | `/api/auth/*` routes |
| `serializers.py` | User registration and profile serializers |

**Auth flow:**
1. User signs in with Firebase on the frontend
2. Frontend sends Firebase ID token to `POST /api/auth/firebase/`
3. Backend verifies token, creates/updates Django user
4. Backend returns JWT access + refresh tokens
5. All file API calls use `Authorization: Bearer <token>`

### `files` — File management

| File | Role |
|------|------|
| `models.py` | `UploadedFile` model (metadata, status, encryption) |
| `services.py` | `delete_uploaded_file()` — cleans scan data + storage |
| `views.py` | Upload, list, download, delete endpoints |
| `urls.py` | `/api/files/*` routes |

**Storage:**
- Files encrypted with AES before saving
- Path: `storage/{user-id}/{file-id}.enc`
- On Vercel: `/tmp/storage/` (ephemeral)

**Statuses:** `uploading` → `scanning` → `clean`

### `scanning` — Malware detection

| File | Role |
|------|------|
| `models.py` | `ScanResult`, `SecurityReport` |
| `services.py` | Runs `ml.inference.scan_bytes()` after upload |
| `views.py` | `GET /api/scanning/report/{file_id}/` |
| `urls.py` | `/api/scanning/*` routes |

Scan is **informational only** — files remain downloadable even if flagged malicious.

---

## API endpoints

### Auth (`/api/auth/`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/register/` | No | Local registration (fallback) |
| `POST` | `/login/` | No | Local login (fallback) |
| `POST` | `/firebase/` | No | Firebase sign-up / login |
| `GET` | `/firebase-config/` | No | Firebase web SDK config |
| `GET` | `/me/` | Yes | Current user profile |
| `POST` | `/refresh/` | No | Refresh JWT token |

### Files (`/api/files/`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/` | Yes | List current user's files |
| `POST` | `/upload/` | Yes | Upload file (multipart) |
| `GET` | `/{id}/` | Yes | File metadata |
| `GET` | `/{id}/download/` | Yes | Download decrypted file |
| `DELETE` | `/{id}/delete/` | Yes | Delete file and scan data |

### Scanning (`/api/scanning/`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/report/{file_id}/` | Yes | Malware scan report |

---

## Page routes (HTML)

Served by Django `TemplateView` in `config/urls.py`:

| URL | Template | Page |
|-----|----------|------|
| `/` | `index.html` | Login |
| `/signup/` | `signup.html` | Sign up |
| `/dashboard/` | `dashboard.html` | File dashboard |

---

## Configuration (`config/settings.py`)

| Setting | Description |
|---------|-------------|
| `SECRET_KEY` | Django secret (required in production) |
| `DEBUG` | Auto-disabled on Vercel |
| `FILE_ENCRYPTION_KEY` | 32+ char key for AES file encryption |
| `FIREBASE_*` | Firebase web app credentials |
| `DATABASE_URL` | Optional PostgreSQL (ignored if SQLite on Vercel) |
| `MAX_UPLOAD_SIZE_MB` | Upload size limit (default: 25 MB) |
| `SCAN_CONFIDENCE_THRESHOLD` | Malware confidence cutoff (default: 0.7) |

---

## Database

**Local:** `backend/db.sqlite3`

**Vercel:** `/tmp/db.sqlite3` (resets on cold starts — fine for demo)

**Production (recommended):** Neon or Vercel Postgres via `DATABASE_URL`

---

## ML integration

`scanning/services.py` imports `ml.inference.scan_bytes()`:

- Checks file extension against suspicious list (`.exe`, `.dll`, `.bat`, etc.)
- Calculates byte entropy
- Detects EICAR test signature
- Returns `classification` (`clean` / `malicious`) and `confidence` score

---

## Running locally

```powershell
cd backend
python manage.py migrate
python manage.py runserver
```

## Running tests

```powershell
cd backend
pytest
```

Tests cover auth, file upload/download, and scanning.
