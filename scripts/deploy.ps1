# Deploy frontend + backend to Vercel (single app, same URL).
# Usage:
#   npm run deploy          # production deploy
#   npm run deploy:setup    # first-time: login, link, env, GitHub auto-deploy
#   npm run deploy:env      # sync .env vars to Vercel then deploy

param(
    [switch]$SyncEnv,
    [switch]$Setup,
    [switch]$Preview,
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "refresh-path.ps1")
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

$ProjectName = "g-project"
$ProductionBranch = "master"
$envKeys = @(
    "SECRET_KEY",
    "DEBUG",
    "FILE_ENCRYPTION_KEY",
    "FIREBASE_API_KEY",
    "FIREBASE_AUTH_DOMAIN",
    "FIREBASE_PROJECT_ID",
    "FIREBASE_APP_ID",
    "FIREBASE_STORAGE_BUCKET",
    "FIREBASE_MESSAGING_SENDER_ID",
    "DATABASE_URL"
)

function Write-Step($Message) {
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Ensure-Npm {
    if ($SkipInstall) { return }
    if (-not (Test-Path "node_modules")) {
        Write-Step "Installing npm dependencies..."
        npm install
    }
}

function Ensure-VercelLogin {
    Write-Step "Checking Vercel login..."
    $null = npx vercel whoami 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Not logged in. Vercel uses OAuth Device Flow:" -ForegroundColor Yellow
        Write-Host "  1. A code and URL will appear in this terminal" -ForegroundColor Yellow
        Write-Host "  2. Open the URL in any browser and enter the code" -ForegroundColor Yellow
        Write-Host "  3. Verify location, IP, and time before approving" -ForegroundColor Yellow
        npx vercel login
        $null = npx vercel whoami 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Vercel login failed. Run: npx vercel login"
        }
    }
    $user = (npx vercel whoami 2>$null | Select-Object -Last 1)
    Write-Host "Logged in as: $user" -ForegroundColor Green
}

function Ensure-VercelLink {
    if (Test-Path ".vercel/project.json") { return }
    Write-Step "Linking Vercel project '$ProjectName' (first time)..."
    npx vercel link --yes --project $ProjectName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Creating new Vercel project '$ProjectName'..." -ForegroundColor Yellow
        npx vercel link --yes
    }
    if (-not (Test-Path ".vercel/project.json")) {
        throw "Could not link Vercel project. Run: npx vercel link"
    }
}

function Ensure-GitHubAutoDeploy {
    $remote = git remote get-url origin 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "No git remote 'origin' found. Skipping GitHub auto-deploy hook." -ForegroundColor Yellow
        return
    }

    Write-Step "Enabling auto-deploy from GitHub ($ProductionBranch branch)..."
    Write-Host "If prompted, connect repo: NuclearMonster1/g-project" -ForegroundColor Yellow
    npx vercel git connect 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "GitHub connected. Pushes to $ProductionBranch will auto-deploy." -ForegroundColor Green
    } else {
        Write-Host "Connect GitHub manually: Vercel Dashboard -> Project -> Settings -> Git" -ForegroundColor Yellow
    }
}

function Read-DotEnv {
    $result = @{}
    if (-not (Test-Path ".env")) { return $result }
    Get-Content ".env" | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#")) { return }
        $idx = $line.IndexOf("=")
        if ($idx -lt 1) { return }
        $key = $line.Substring(0, $idx).Trim()
        $value = $line.Substring($idx + 1).Trim().Trim('"').Trim("'")
        $result[$key] = $value
    }
    return $result
}

function Sync-EnvToVercel {
    $dotenv = Read-DotEnv
    if ($dotenv.Count -eq 0) {
        Write-Host "No .env file found. Add env vars in Vercel Dashboard." -ForegroundColor Yellow
        return
    }

    if (-not $dotenv.ContainsKey("DEBUG")) {
        $dotenv["DEBUG"] = "False"
    } else {
        $dotenv["DEBUG"] = "False"
    }

    Write-Step "Syncing environment variables from .env to Vercel..."
    foreach ($key in $envKeys) {
        if (-not $dotenv.ContainsKey($key)) { continue }
        $value = $dotenv[$key]
        if (-not $value) { continue }
        Write-Host "  $key"
        $value | npx vercel env add $key production --force 2>$null | Out-Null
        $value | npx vercel env add $key preview --force 2>$null | Out-Null
    }
    Write-Host "Environment variables synced." -ForegroundColor Green
}

function Test-DeployConfig {
    Write-Step "Validating deploy files..."
    $required = @("vercel.json", "api/index.py", "build.sh", "requirements.txt")
    foreach ($file in $required) {
        if (-not (Test-Path $file)) {
            throw "Missing required file: $file"
        }
    }
    Write-Host "Deploy config looks good." -ForegroundColor Green
}

Ensure-Npm
Test-DeployConfig
Ensure-VercelLogin
Ensure-VercelLink

if ($Setup -or $SyncEnv) {
    Sync-EnvToVercel
}

if ($Setup) {
    Ensure-GitHubAutoDeploy
}

Write-Step "Deploying to Vercel..."
if ($Preview) {
    $output = npx vercel --yes 2>&1 | Out-String
} else {
    $output = npx vercel --prod --yes 2>&1 | Out-String
}
Write-Host $output

if ($LASTEXITCODE -ne 0) {
    throw "Deploy failed."
}

$url = [regex]::Match($output, "https://[a-z0-9\-]+\.vercel\.app").Value
Write-Host ""
Write-Host "Deploy finished." -ForegroundColor Green
if ($url) {
    Write-Host "Live site: $url" -ForegroundColor Green
}
Write-Host "Dashboard: https://vercel.com/nuke10" -ForegroundColor Green
Write-Host "After first deploy, add your Vercel domain in Firebase -> Authentication -> Authorized domains." -ForegroundColor Yellow
