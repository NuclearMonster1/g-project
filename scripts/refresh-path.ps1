# Refresh PATH so Node.js/npm work in terminals opened before Node was installed.
$machine = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$user = [System.Environment]::GetEnvironmentVariable("Path", "User")
$env:Path = "$machine;$user"

$nodeDir = "C:\Program Files\nodejs"
if ((Test-Path $nodeDir) -and ($env:Path -notlike "*$nodeDir*")) {
    $env:Path = "$nodeDir;$env:Path"
}

function Test-NodeReady {
    $node = Get-Command node -ErrorAction SilentlyContinue
    $npm = Get-Command npm -ErrorAction SilentlyContinue
    return ($null -ne $node -and $null -ne $npm)
}

if (-not (Test-NodeReady)) {
    Write-Host "Node.js not found. Installing Node.js LTS..." -ForegroundColor Yellow
    winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
    $machine = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    $user = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path = "$machine;$user"
    if ((Test-Path $nodeDir) -and ($env:Path -notlike "*$nodeDir*")) {
        $env:Path = "$nodeDir;$env:Path"
    }
}

if (-not (Test-NodeReady)) {
    throw "Node.js is still not available. Close Cursor completely, reopen it, then try again."
}

# Use .cmd shims so PowerShell does not try to run npx.ps1/npm.ps1 (blocked by execution policy).
function Invoke-Vercel {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $output = & (Join-Path $nodeDir "npx.cmd") @Args 2>&1 | Out-String
    $exit = $LASTEXITCODE
    $ErrorActionPreference = $prev
    return @{ Output = $output; ExitCode = $exit }
}

function npx {
    $result = Invoke-Vercel @args
    if ($result.Output) { Write-Host $result.Output.TrimEnd() }
    $global:LASTEXITCODE = $result.ExitCode
    if ($result.ExitCode -ne 0) { return $result.Output }
}

function npm {
    & (Join-Path $nodeDir "npm.cmd") @args
}
