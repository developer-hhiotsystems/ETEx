# Create Agent-Specific GitHub Labels for ETEx
# Run this after creating the 9 essential labels

Write-Host "Creating agent-specific labels for ETEx..." -ForegroundColor Green

$repo = "developer-hhiotsystems/ETEx"

# Agent Role Labels
Write-Host "`n[Agent Role Labels]" -ForegroundColor Cyan
gh label create "agent: design" --color "9C27B0" --description "Created by Design Agent" --repo $repo
gh label create "agent: coding" --color "2196F3" --description "Created by Coding Agent" --repo $repo
gh label create "agent: review" --color "FF9800" --description "Created by Review Agent" --repo $repo
gh label create "agent: explore" --color "4CAF50" --description "Created by Explore Agent" --repo $repo

# Agent Finding Types
Write-Host "`n[Agent Finding Types]" -ForegroundColor Cyan
gh label create "type: design-issue" --color "E91E63" --description "Spec ambiguity or gap" --repo $repo
gh label create "type: clarification" --color "FFC107" --description "Needs user decision" --repo $repo
gh label create "type: question" --color "00BCD4" --description "Question about codebase" --repo $repo
gh label create "type: observation" --color "9E9E9E" --description "Interesting finding to note" --repo $repo
gh label create "type: blocked" --color "D73A4A" --description "Cannot proceed without action" --repo $repo

# Review Severity Labels
Write-Host "`n[Review Severity Labels]" -ForegroundColor Cyan
gh label create "severity: critical" --color "B60205" --description "Must fix now (security, broken)" --repo $repo
gh label create "severity: major" --color "D93F0B" --description "Should fix before merge" --repo $repo
gh label create "severity: minor" --color "FBCA04" --description "Nice to fix" --repo $repo
gh label create "severity: suggestion" --color "0E8A16" --description "Optional improvement" --repo $repo

Write-Host "`n✓ All agent labels created successfully!" -ForegroundColor Green
Write-Host "`nTotal labels: 13 agent-specific + 9 essential = 22 labels" -ForegroundColor Cyan
Write-Host "`nVerify at: https://github.com/$repo/labels" -ForegroundColor Cyan
