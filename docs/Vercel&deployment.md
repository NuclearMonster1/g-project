# Vercel & Deployment

How to deploy **G Project** (frontend + backend) to a public Vercel URL.

**Live production URL:** [https://g-project-ten.vercel.app](https://g-project-ten.vercel.app)

---

## Architecture on Vercel

One Vercel project serves everything on the same domain:

| Path | Handler |
|------|---------|
| `/static/*` | Vercel static CDN (`frontend/static/`) |
| `/`, `/signup/`, `/dashboard/` | Django WSGI (`api/index.py`) |
| `/api/*` | Django WSGI (`api/index.py`) |

```
Browser
  ├── /static/css/style.css  →  Vercel CDN
  ├── /                      →  Django (login page)
  └── /api/files/upload/     →  Django REST API
```

---

## Key deploy files

| File | Role |
|------|------|
| `vercel.json` | Build config, routes, Python runtime |
| `api/index.py` | Serverless WSGI entry point |
| `api/requirements.txt` | Python dependencies for the function |
| `build.sh` | Runs `collectstatic` + `migrate` on build |
| `requirements.txt` | Root install command for Vercel |
| `scripts/deploy.ps1` | Automated deploy script |
| `deploy-setup.bat` | First-time setup (login, link, env, deploy) |
| `deploy.bat` | Production deploy |

---

## First-time setup

### 1. Install Node.js

Download from [nodejs.org](https://nodejs.org/) or use:

```powershell
winget install OpenJS.NodeJS
```

### 2. Install project dependencies

```powershell
cd "C:\Users\youss\OneDrive\Desktop\G project"
npm install
```

### 3. Log in to Vercel (OAuth Device Flow)

Double-click **`vercel-login.bat`**, or run:

```powershell
$env:Path = "C:\Program Files\nodejs;" + $env:Path
& "C:\Program Files\nodejs\npx.cmd" vercel login
```

1. A code and URL appear in the terminal
2. Open the URL in any browser and enter the code
3. Verify location, IP, and time before approving

### 4. Deploy (first time)

Double-click **`deploy-setup.bat`**, or run:

```powershell
npm run deploy:setup
```

This will:
- Link project as `g-project` on Vercel
- Sync environment variables from `.env`
- Connect GitHub for auto-deploy on push to `master`
- Deploy to production

---

## Environment variables (Vercel Dashboard)

Set in [vercel.com/nuke10/g-project](https://vercel.com/nuke10/g-project) → **Settings → Environment Variables**:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | Random long secret string |
| `DEBUG` | `False` |
| `FILE_ENCRYPTION_KEY` | 32+ character encryption key |
| `FIREBASE_API_KEY` | From Firebase console |
| `FIREBASE_AUTH_DOMAIN` | e.g. `g-project-bc659.firebaseapp.com` |
| `FIREBASE_PROJECT_ID` | Your Firebase project ID |
| `FIREBASE_APP_ID` | Firebase web app ID |
| `FIREBASE_STORAGE_BUCKET` | Firebase storage bucket |
| `FIREBASE_MESSAGING_SENDER_ID` | Firebase sender ID |

Optional: `DATABASE_URL` for persistent PostgreSQL (Neon / Vercel Postgres).

Sync from local `.env`:

```powershell
npm run deploy:env
```

---

## Firebase (required for live login)

1. [Firebase Console](https://console.firebase.google.com/) → your project
2. **Authentication → Settings → Authorized domains**
3. Add: `g-project-ten.vercel.app`

---

## Auto-deploy on git push

GitHub repo `NuclearMonster1/g-project` is connected to Vercel.

Every push to **`master`** triggers a new production deployment automatically.

```powershell
git add .
git commit -m "Your changes"
git push
```

---

## Manual redeploy

```powershell
npm run deploy
# or
.\deploy.bat
```

---

## npm scripts

| Script | Command |
|--------|---------|
| `npm run deploy` | Production deploy |
| `npm run deploy:setup` | First-time setup + deploy |
| `npm run deploy:env` | Sync `.env` to Vercel + deploy |
| `npm run vercel:dev` | Local Vercel dev server |

---

## Windows troubleshooting

### `npm` or `npx` not found

Refresh PATH in your terminal:

```powershell
$env:Path = "C:\Program Files\nodejs;" + $env:Path
```

Or close and reopen Cursor completely.

### PowerShell blocks `npx`

Use the `.cmd` shim directly:

```powershell
& "C:\Program Files\nodejs\npx.cmd" vercel login
```

Or use the `.bat` files (`deploy-setup.bat`, `vercel-login.bat`).

---

## Vercel limitations (demo)

| Item | On Vercel |
|------|-----------|
| Database | `/tmp/db.sqlite3` — may reset on redeploy |
| Uploaded files | `/tmp/storage/` — ephemeral |
| Cold starts | First request may be slower |

For a graduation demo this is fine. For production, add `DATABASE_URL` (PostgreSQL) and external file storage.

---

## Vercel dashboard

- **Project:** [vercel.com/nuke10/g-project](https://vercel.com/nuke10/g-project)
- **Account:** nuke10
- **Production branch:** `master`
- **Production URL:** `https://g-project-ten.vercel.app`
