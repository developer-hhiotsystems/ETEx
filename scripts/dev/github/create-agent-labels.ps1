# Create Agent-Specific GitHub Labels for ETEx
# Safe version with error handling and verification
# Run this after creating the 9 essential labels

param(
    [string]$repo = "developer-hhiotsystems/ETEx",
    [switch]$DryRun
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ETEx Agent Label Creation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "[DRY RUN MODE] - No labels will be created" -ForegroundColor Yellow
    Write-Host ""
}

# Check if gh CLI is available
Write-Host "[1/4] Checking GitHub CLI..." -ForegroundColor Cyan
try {
    $ghVersion = gh --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ GitHub CLI found: $($ghVersion | Select-Object -First 1)" -ForegroundColor Green
    } else {
        throw "gh command failed"
    }
} catch {
    Write-Host "  ✗ GitHub CLI not found or not authenticated" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install GitHub CLI:" -ForegroundColor Yellow
    Write-Host "  winget install GitHub.cli" -ForegroundColor White
    Write-Host ""
    Write-Host "Then authenticate:" -ForegroundColor Yellow
    Write-Host "  gh auth login" -ForegroundColor White
    exit 1
}

# Check authentication
Write-Host "[2/4] Checking authentication..." -ForegroundColor Cyan
try {
    $authStatus = gh auth status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Authenticated to GitHub" -ForegroundColor Green
    } else {
        throw "Not authenticated"
    }
} catch {
    Write-Host "  ✗ Not authenticated to GitHub" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run: gh auth login" -ForegroundColor Yellow
    exit 1
}

Write-Host "[3/4] Repository: $repo" -ForegroundColor Cyan
Write-Host ""

# Define agent labels
$agentLabels = @(
    # Agent Role Labels (4)
    @{name="agent: design"; color="9C27B0"; description="Created by Design Agent"},
    @{name="agent: coding"; color="2196F3"; description="Created by Coding Agent"},
    @{name="agent: review"; color="FF9800"; description="Created by Review Agent"},
    @{name="agent: explore"; color="4CAF50"; description="Created by Explore Agent"},

    # Agent Finding Types (5)
    @{name="type: design-issue"; color="E91E63"; description="Spec ambiguity or gap"},
    @{name="type: clarification"; color="FFC107"; description="Needs user decision"},
    @{name="type: question"; color="00BCD4"; description="Question about codebase"},
    @{name="type: observation"; color="9E9E9E"; description="Interesting finding to note"},
    @{name="type: blocked"; color="D73A4A"; description="Cannot proceed without action"},

    # Review Severity Labels (4)
    @{name="severity: critical"; color="B60205"; description="Must fix now (security, broken)"},
    @{name="severity: major"; color="D93F0B"; description="Should fix before merge"},
    @{name="severity: minor"; color="FBCA04"; description="Nice to fix"},
    @{name="severity: suggestion"; color="0E8A16"; description="Optional improvement"}
)

Write-Host "[4/4] Creating $($agentLabels.Count) agent labels..." -ForegroundColor Cyan
Write-Host ""

$successCount = 0
$skipCount = 0
$errorCount = 0

foreach ($label in $agentLabels) {
    $labelName = $label.name
    $labelColor = $label.color
    $labelDescription = $label.description

    Write-Host "  Creating: " -NoNewline
    Write-Host "$labelName" -ForegroundColor White -NoNewline
    Write-Host " (#$labelColor)" -ForegroundColor DarkGray

    if ($DryRun) {
        Write-Host "    [DRY RUN] Would create label" -ForegroundColor Yellow
        $successCount++
        continue
    }

    try {
        # Attempt to create label
        $output = gh label create $labelName --color $labelColor --description $labelDescription --repo $repo 2>&1

        if ($LASTEXITCODE -eq 0) {
            Write-Host "    ✓ Created successfully" -ForegroundColor Green
            $successCount++
        } else {
            # Check if label already exists
            if ($output -match "already exists") {
                Write-Host "    ⊙ Already exists (skipped)" -ForegroundColor Yellow
                $skipCount++
            } else {
                Write-Host "    ✗ Error: $output" -ForegroundColor Red
                $errorCount++
            }
        }
    } catch {
        Write-Host "    ✗ Exception: $_" -ForegroundColor Red
        $errorCount++
    }

    # Small delay to avoid rate limiting
    Start-Sleep -Milliseconds 200
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✓ Created:       $successCount" -ForegroundColor Green
Write-Host "  ⊙ Already exist: $skipCount" -ForegroundColor Yellow
Write-Host "  ✗ Errors:        $errorCount" -ForegroundColor Red
Write-Host "  ─ Total:         $($agentLabels.Count)" -ForegroundColor White
Write-Host ""

if ($errorCount -eq 0) {
    Write-Host "✓ All agent labels ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "View labels at:" -ForegroundColor Cyan
    Write-Host "  https://github.com/$repo/labels" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Verify labels on GitHub" -ForegroundColor White
    Write-Host "  2. Create your first issue with agent labels" -ForegroundColor White
    Write-Host "  3. Start Week 1 implementation" -ForegroundColor White
} else {
    Write-Host "⚠ Some labels failed to create" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  • Insufficient permissions - Re-run: gh auth refresh -h github.com -s repo" -ForegroundColor White
    Write-Host "  • Network error - Check internet connection and retry" -ForegroundColor White
    Write-Host "  • Rate limit - Wait a few minutes and retry" -ForegroundColor White
}

Write-Host ""
