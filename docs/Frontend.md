# Frontend

Simple HTML/CSS/JavaScript UI served by Django and deployed on Vercel.

---

## Stack

- **HTML5** — page structure
- **CSS3** — dark theme styling (no framework)
- **Vanilla JavaScript** — no React, Vue, or build step
- **Firebase JS SDK** — client-side authentication

---

## Pages

| URL | Template | Purpose |
|-----|----------|---------|
| `/` | `frontend/templates/index.html` | Login page (home) |
| `/signup/` | `frontend/templates/signup.html` | Create account |
| `/dashboard/` | `frontend/templates/dashboard.html` | Upload & manage files |

All pages share the same stylesheet: `/static/css/style.css`

---

## File structure

```
frontend/
├── templates/
│   ├── index.html        # Login form + link to sign up
│   ├── signup.html       # Registration form
│   └── dashboard.html    # Upload zone + file list
└── static/
    ├── css/
    │   └── style.css     # Dark theme, cards, buttons, badges
    └── js/
        ├── auth.js       # Firebase auth (login + sign up)
        └── dashboard.js  # File upload, list, download, delete
```

---

## `auth.js` — Authentication

Used on **login** and **sign up** pages.

**Flow:**
1. Fetches Firebase config from `GET /api/auth/firebase-config/`
2. Initializes Firebase app
3. On login: `firebase.auth().signInWithEmailAndPassword()`
4. On sign up: `firebase.auth().createUserWithEmailAndPassword()`
5. Sends Firebase ID token to `POST /api/auth/firebase/`
6. Stores JWT tokens in `localStorage`
7. Redirects to `/dashboard/`

**API base:** `/api/auth` (relative — works on localhost and Vercel)

---

## `dashboard.js` — File management

Used on the **dashboard** page only.

**Features:**
- Checks JWT in `localStorage` — redirects to `/` if missing
- Shows current user email via `GET /api/auth/me/`
- Drag-and-drop upload zone
- `POST /api/files/upload/` with `FormData`
- Lists files via `GET /api/files/`
- Download via `GET /api/files/{id}/download/`
- View scan report via `GET /api/scanning/report/{id}/`
- Delete via `DELETE /api/files/{id}/delete/`
- Log out clears tokens and returns to login

---

## `style.css` — Design

Dark theme inspired by modern dashboards:

| Element | Style |
|---------|-------|
| Background | `#0f172a` (slate) |
| Cards | `#1e293b` with rounded borders |
| Primary button | `#2563eb` (blue) |
| Danger button | `#b91c1c` (red) |
| Status badges | Green (clean), blue (scanning), red (quarantined) |

Responsive layout with `max-width: 900px` container.

---

## How frontend connects to backend

All API calls use **relative URLs** (e.g. `/api/files/`), so the same code works on:

- `http://127.0.0.1:8000` (local)
- `https://g-project-ten.vercel.app` (production)

No CORS issues — frontend and API share the same origin.

---

## Static files on Vercel

| Route | Served by |
|-------|-----------|
| `/static/css/style.css` | Vercel static CDN |
| `/static/js/auth.js` | Vercel static CDN |
| `/static/js/dashboard.js` | Vercel static CDN |
| `/`, `/signup/`, `/dashboard/` | Django WSGI (HTML templates) |
| `/api/*` | Django WSGI (REST API) |

Configured in `vercel.json`:

```json
{ "src": "/static/(.*)", "dest": "/frontend/static/$1" }
```

---

## Firebase setup (required for login)

1. [Firebase Console](https://console.firebase.google.com/) → your project
2. Enable **Authentication → Email/Password**
3. Add your domain under **Authorized domains**:
   - `localhost` (local dev)
   - `g-project-ten.vercel.app` (production)
4. Copy web app config into `.env` (see `.env.example`)

---

## Local preview

```powershell
cd backend
python manage.py runserver
```

Open:
- http://127.0.0.1:8000/ — login
- http://127.0.0.1:8000/signup/ — sign up
- http://127.0.0.1:8000/dashboard/ — dashboard (requires login)
