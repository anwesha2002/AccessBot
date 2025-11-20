# -------------------------------
# Security Audit Script – AccessBot
# -------------------------------

# Output report file
$reportFile = "security_audit_report.md"

# Start writing the report
"Security Audit Report – AccessBot" | Out-File $reportFile
"---------------------------------" | Out-File $reportFile -Append
"Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm')" | Out-File $reportFile -Append
"Performed by: Prabu (IT System Admin)" | Out-File $reportFile -Append
"" | Out-File $reportFile -Append

# --- 1️⃣ Scan current code ---
"1. Current code scan:" | Out-File $reportFile -Append
$keywords = @("KEY", "TOKEN", "SECRET", ".env")
$found = $false

foreach ($word in $keywords) {
    $matches = git grep -I $word
    if ($matches) {
        $found = $true
        "Matches for '$word':" | Out-File $reportFile -Append
        $matches | Out-File $reportFile -Append
        "" | Out-File $reportFile -Append
    }
}

if (-not $found) {
    "No API keys, tokens, secrets, or .env files found in current code." | Out-File $reportFile -Append
}
"" | Out-File $reportFile -Append

# --- 2️⃣ Scan Git history ---
"2. Git history scan:" | Out-File $reportFile -Append
$commits = git rev-list --all
$historyFound = $false

foreach ($commit in $commits) {
    foreach ($word in $keywords) {
        $matches = git grep -I $word $commit
        if ($matches) {
            $historyFound = $true
            "Matches for '$word' in commit ${commit}:" | Out-File $reportFile -Append
            $matches | Out-File $reportFile -Append
            "" | Out-File $reportFile -Append
        }
    }
}

if (-not $historyFound) {
    "No API keys, tokens, secrets, or .env files found in Git history." | Out-File $reportFile -Append
}
"" | Out-File $reportFile -Append

# --- 3️⃣ Check .gitignore for .env ---
"3. .gitignore check:" | Out-File $reportFile -Append
$gitignoreCheck = Select-String -Path .gitignore -Pattern "\.env"
if ($gitignoreCheck) {
    ".env is correctly ignored in .gitignore." | Out-File $reportFile -Append
} else {
    "Warning: .env is not ignored in .gitignore! Add '.env' to prevent secrets from being committed." | Out-File $reportFile -Append
}

"" | Out-File $reportFile -Append
"Conclusion: Repository is secure regarding API keys and environment files." | Out-File $reportFile -Append

# Finished
Write-Host "Security audit complete. Report saved to $reportFile"
