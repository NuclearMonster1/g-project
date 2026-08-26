# Vercel Deployment Guide

Deploy the full app (frontend + backend) to a public Vercel URL.

## 1. Install tools (one time)

```powershell
cd "C:\Users\youss\OneDrive\Desktop\G project"
npm install
```

This installs the **Vercel CLI** locally.

## 2. Login to Vercel

```powershell
npx vercel login
```

Use the same account as https://vercel.com/nuke10

## 3. Set environment variables on Vercel

In [Vercel Dashboard](https://vercel.com/nuke10) → your project → **Settings → Environment Variables**, add:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | random long secret string |
| `DEBUG` | `False` |
| `FILE_ENCRYPTION_KEY` | your 32+ char key |
| `FIREBASE_API_KEY` | from Firebase |
| `FIREBASE_AUTH_DOMAIN` | g-project-bc659.firebaseapp.com |
| `FIREBASE_PROJECT_ID` | g-project-bc659 |
| `FIREBASE_APP_ID` | your app id |
| `FIREBASE_STORAGE_BUCKET` | g-project-bc659.firebasestorage.app |
| `FIREBASE_MESSAGING_SENDER_ID` | 187747563131 |

Optional (recommended for production data):
| `DATABASE_URL` | PostgreSQL URL from Neon or Vercel Postgres |

## 4. Firebase — add Vercel domain

1. Open [Firebase Console](https://console.firebase.google.com/) → your project
2. **Authentication → Settings → Authorized domains**
3. Add your Vercel URL, e.g. `g-project.vercel.app`

## 5. Deploy

```powershell
cd "C:\Users\youss\OneDrive\Desktop\G project"
npx vercel --prod
```

First time it will ask:
- Link to existing project? **No** (or Yes if you already created one)
- Project name: `g-project`
- Directory: `.` (current folder)

After deploy you get a link like:
**https://g-project-xxxx.vercel.app**

## 6. Open your website

Open the Vercel link in any browser — no localhost needed.

---

## Notes

- **Frontend + backend** are served from the same Vercel app.
- Without `DATABASE_URL`, Vercel uses temporary `/tmp` storage (data may reset on redeploy).
- For a graduation demo, `/tmp` is fine. For real use, add **Neon PostgreSQL** (free tier).
- Uploaded files on Vercel `/tmp` are also temporary.

## Redeploy after changes

```powershell
git add .
git commit -m "Update"
git push
npx vercel --prod
```

Or connect GitHub repo in Vercel dashboard for automatic deploys on push.
