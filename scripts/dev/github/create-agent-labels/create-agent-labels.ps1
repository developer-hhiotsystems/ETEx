# Simple Agent Label Creator
# Copy-paste this entire script into PowerShell ISE or run directly

$repo = "developer-hhiotsystems/ETEx"

Write-Host "Creating 13 agent labels..." -ForegroundColor Cyan

$labels = @(
    @("agent: design", "9C27B0", "Created by Design Agent"),
    @("agent: coding", "2196F3", "Created by Coding Agent"),
    @("agent: review", "FF9800", "Created by Review Agent"),
    @("agent: explore", "4CAF50", "Created by Explore Agent"),
    @("type: design-issue", "E91E63", "Spec ambiguity or gap"),
    @("type: clarification", "FFC107", "Needs user decision"),
    @("type: question", "00BCD4", "Question about codebase"),
    @("type: observation", "9E9E9E", "Interesting finding"),
    @("type: blocked", "D73A4A", "Cannot proceed"),
    @("severity: critical", "B60205", "Must fix now"),
    @("severity: major", "D93F0B", "Should fix before merge"),
    @("severity: minor", "FBCA04", "Nice to fix"),
    @("severity: suggestion", "0E8A16", "Optional improvement")
)

$created = 0
$skipped = 0

foreach ($label in $labels) {
    $name = $label[0]
    $color = $label[1]
    $desc = $label[2]

    Write-Host "  $name... " -NoNewline

    try {
        gh label create $name --color $color --description $desc --repo $repo 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Created" -ForegroundColor Green
            $created++
        } else {
            Write-Host "Exists" -ForegroundColor Yellow
            $skipped++
        }
    } catch {
        Write-Host "Error" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Summary: $created created, $skipped skipped" -ForegroundColor Cyan
Write-Host "View at: https://github.com/$repo/labels" -ForegroundColor Cyan
