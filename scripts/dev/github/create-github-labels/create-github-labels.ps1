# Create GitHub Labels for ETEx Project
# Run this script to create all labels defined in the workflow guide

Write-Host "Creating GitHub labels for ETEx..." -ForegroundColor Green

$repo = "developer-hhiotsystems/ETEx"

# Type Labels
Write-Host "`n[Type Labels]" -ForegroundColor Cyan
gh label create "type: feature" --color "0E8A16" --description "New functionality" --repo $repo
gh label create "type: bug" --color "D73A4A" --description "Something broken" --repo $repo
gh label create "type: docs" --color "0075CA" --description "Documentation only" --repo $repo
gh label create "type: refactor" --color "FFA500" --description "Code improvement" --repo $repo
gh label create "type: test" --color "FBCA04" --description "Testing improvements" --repo $repo
gh label create "type: chore" --color "CCCCCC" --description "Maintenance tasks" --repo $repo
gh label create "type: meta" --color "5319E7" --description "Meta/tracking issues" --repo $repo

# Priority Labels
Write-Host "`n[Priority Labels]" -ForegroundColor Cyan
gh label create "priority: critical" --color "B60205" --description "Blocks MVP, security issue" --repo $repo
gh label create "priority: high" --color "D93F0B" --description "Important for current week" --repo $repo
gh label create "priority: medium" --color "FBCA04" --description "Normal priority" --repo $repo
gh label create "priority: low" --color "0E8A16" --description "Nice to have" --repo $repo

# Phase Labels
Write-Host "`n[Phase Labels]" -ForegroundColor Cyan
gh label create "phase: mvp" --color "5319E7" --description "Must have for MVP (6 weeks)" --repo $repo
gh label create "phase: 2a" --color "C5DEF5" --description "Phase 2A (Internal docs)" --repo $repo
gh label create "phase: 2b" --color "C5DEF5" --description "Phase 2B (Deviation checking)" --repo $repo
gh label create "phase: 2c" --color "C5DEF5" --description "Phase 2C (DeepL integration)" --repo $repo
gh label create "phase: 2d" --color "C5DEF5" --description "Phase 2D (Additional languages)" --repo $repo
gh label create "phase: 2e" --color "C5DEF5" --description "Phase 2E (Synonym auto-detection)" --repo $repo
gh label create "phase: 2f" --color "C5DEF5" --description "Phase 2F (User accounts)" --repo $repo
gh label create "phase: future" --color "E4E669" --description "Ideas for later" --repo $repo

# Component Labels
Write-Host "`n[Component Labels]" -ForegroundColor Cyan
gh label create "component: backend" --color "1D76DB" --description "Python/FastAPI" --repo $repo
gh label create "component: frontend" --color "BFD4F2" --description "React/TypeScript" --repo $repo
gh label create "component: database" --color "006B75" --description "SQLite/Alembic" --repo $repo
gh label create "component: extraction" --color "7057FF" --description "PDF/term extraction" --repo $repo
gh label create "component: api-integration" --color "008672" --description "IATE/IEC integration" --repo $repo

# Status Labels (optional, can be managed by Project board)
Write-Host "`n[Status Labels]" -ForegroundColor Cyan
gh label create "status: planning" --color "D4C5F9" --description "Spec/design in progress" --repo $repo
gh label create "status: ready" --color "0E8A16" --description "Ready for coding" --repo $repo
gh label create "status: in-progress" --color "FBCA04" --description "Currently being worked on" --repo $repo
gh label create "status: review" --color "FFA500" --description "Code review needed" --repo $repo
gh label create "status: blocked" --color "D73A4A" --description "Waiting on external dependency" --repo $repo

Write-Host "`n✓ All labels created successfully!" -ForegroundColor Green
Write-Host "`nVerify at: https://github.com/$repo/labels" -ForegroundColor Cyan
