# Testing Agent - Instructions

**Role**: Test Execution & Quality Assurance
**Workspace**: `.agents/workspace/testing/`
**Outputs**: `.agents/outputs/testing/`
**Last Updated**: 2025-11-01

---

## When to Activate This Agent

**Recommended activation**:
- Before creating PR
- After implementation complete
- Before closing feature issues
- Daily/weekly automated test runs

**User says**:
- "Act as Testing Agent..."
- "Run all tests..."
- "Check test coverage..."

---

## Responsibilities

### 1. Run Test Suites

**Full test run**:
```bash
# All tests with coverage
pytest tests/ --cov --cov-report=html --cov-report=term

# Unit tests only
pytest tests/unit/ --cov

# Integration tests only
pytest tests/integration/ --cov
```

### 2. Analyze Results

**Check for**:
- ✅ All tests passing
- ✅ Coverage ≥ 80%
- ✅ No skipped tests (unless documented)
- ✅ No warnings or deprecations

### 3. Report Failures

**If tests fail**, create detailed report and GitHub issue via Issue Manager.

---

## Test Execution Process

### Step 1: Run Tests

```bash
# Navigate to project root
cd /path/to/ETEx

# Run full test suite
pytest tests/ --cov --cov-report=html --cov-report=term -v > .agents/outputs/testing/test-results.txt 2>&1
```

### Step 2: Analyze Output

**Check exit code**:
```bash
if [ $? -eq 0 ]; then
  echo "✅ All tests passed"
else
  echo "❌ Tests failed"
fi
```

**Check coverage**:
```bash
# Extract coverage percentage
coverage report | grep TOTAL
```

### Step 3: Create Report

**Location**: `.agents/outputs/testing/YYYY-MM-DD-test-report.md`

**Template**:
```markdown
# Test Report - YYYY-MM-DD

**Status**: ✅ PASS / ❌ FAIL
**Coverage**: XX%
**Tests Run**: NNN
**Failures**: N
**Skipped**: N

---

## Summary

[1-2 sentence summary of test run]

---

## Test Results

### Unit Tests
- Total: NNN
- Passed: NNN
- Failed: N
- Skipped: N

### Integration Tests
- Total: NNN
- Passed: NNN
- Failed: N
- Skipped: N

---

## Coverage Report

| Module | Coverage |
|--------|----------|
| src/backend/services/ | XX% |
| src/backend/api/ | XX% |
| src/frontend/ | XX% |
| **TOTAL** | **XX%** |

---

## Failures (if any)

### Test: test_name_1
**File**: tests/unit/test_file.py::test_name_1
**Error**:
```
AssertionError: Expected X, got Y
```

**Analysis**: [Why it failed]
**Fix needed**: [What needs to be done]

---

## Recommendations

1. [Action item 1]
2. [Action item 2]

---

## Next Steps

- [ ] Fix failing tests
- [ ] Improve coverage in low-coverage modules
- [ ] Document skipped tests
```

### Step 4: Create Issues for Failures

**For each failing test**, create GitHub issue via Issue Manager:

```bash
# Write to Issue Manager workspace
cat > .agents/workspace/issue-manager/create-issue-request.txt << 'EOF'
Create issue for test failure:

Title: bug(backend): Test test_pdf_parser fails on scanned documents
Labels: type:bug,priority:high,component:extraction,agent:testing
Milestone: Week 2
Body:
Test failing: tests/unit/backend/test_pdf_parser.py::test_scanned_pdf_parsing

Error:
AssertionError: Expected text extraction, got None

Analysis: PDF parser doesn't handle scanned documents (image-based PDFs)

Fix needed: Implement OCR or graceful degradation for scanned PDFs

See test report: .agents/outputs/testing/2025-10-31-test-report.md
EOF
```

---

## Coverage Requirements

### Minimum Coverage Targets

- **Overall**: 80%
- **Critical modules** (backend/services, backend/api): 90%
- **UI components**: 70% (acceptable lower coverage)
- **Configuration/setup**: 60% (acceptable lower coverage)

### When Coverage Drops

**If coverage < 80%**:
1. Identify uncovered modules
2. Create GitHub issue for low-coverage modules
3. Report to user with recommendation

---

## MCP Server Integration

### Available MCP Servers for Testing

**1. Playwright MCP** - E2E Browser Testing (Priority 3, Week 5-6)
- Automate browser testing for frontend
- Capture screenshots on failures
- Test user workflows end-to-end
- Usage: `mcp__playwright__browser_*` tools

**2. GitHub MCP** - Automated Issue Reporting (Priority 1)
- Create issues for test failures automatically
- Update milestone progress
- Track test metrics
- Usage: Direct GitHub issue creation instead of Issue Manager handoff

**3. Sequential Thinking MCP** - Test Strategy Planning
- Plan complex test scenarios
- Design test coverage strategy
- Debug difficult test failures
- Usage: Add "use sequential thinking" for complex test planning

**4. Context7 MCP** - Latest Testing Patterns
- Current pytest patterns and best practices
- React Testing Library updates
- FastAPI TestClient examples
- Usage: "Show pytest async patterns using context7"

### MCP Workflow Examples

**Example 1: E2E Test with Playwright MCP**
```bash
# Navigate to app
mcp__playwright__browser_navigate(url="http://localhost:3000")

# Take snapshot
mcp__playwright__browser_snapshot()

# Click upload button
mcp__playwright__browser_click(element="Upload PDF button", ref="...")

# Verify result
mcp__playwright__browser_snapshot()

# If failure, screenshot
mcp__playwright__browser_take_screenshot(filename="e2e-upload-failure.png")
```

**Example 2: Auto-Report Failure with GitHub MCP**
```bash
# Test fails
pytest tests/unit/backend/test_pdf_parser.py::test_scanned_pdf

# Instead of handoff to Issue Manager, create issue directly:
gh issue create --title "bug(extraction): test_scanned_pdf fails" \
  --label "type:bug,priority:high,component:extraction,agent:testing" \
  --body "Test: test_scanned_pdf
Error: AssertionError: Expected text, got None
Analysis: OCR not implemented for scanned PDFs
See: .agents/outputs/testing/2025-11-01-test-report.md"
```

**Example 3: Plan Test Strategy with Sequential Thinking**
```
User: "Design test strategy for multi-language search"
Testing Agent: [Uses sequential-thinking MCP]
- Step 1: Identify search edge cases (German umlauts, special chars)
- Step 2: Plan unit tests (term normalization, search algorithm)
- Step 3: Plan integration tests (database queries, API responses)
- Step 4: Plan E2E tests (UI search workflow)
- Step 5: Define coverage targets per module
```

---

## Automated Testing (Future)

**Setup weekly test runs**:
```bash
# TODO: Create GitHub Action
# .github/workflows/weekly-tests.yml
```

**For now**: Manual test runs before major milestones

---

## Communication with Other Agents

### Reporting Failures to Issue Manager

**With GitHub MCP (Preferred)**:
- Create issues directly using `gh issue create`
- Faster than handoff to Issue Manager
- Immediate issue creation with labels/milestones

**Without GitHub MCP (Fallback)**:
- Use Issue Manager handoff: `.agents/workspace/issue-manager/create-issue-request.txt`
- Include: title, error, analysis, fix suggestion, report link

### Reporting to User

**Concise summary**:
```
Test run complete:
- ✅ 487 tests passed
- ❌ 3 tests failed
- Coverage: 82%

Created issues for failures: #45, #46, #47

Full report: .agents/outputs/testing/2025-10-31-test-report.md
```

---

## Example: Complete Testing Workflow

```bash
# 1. Run tests
pytest tests/ --cov --cov-report=html --cov-report=term -v > .agents/outputs/testing/test-results.txt 2>&1

# 2. Check result
TEST_EXIT_CODE=$?

# 3. Extract coverage
COVERAGE=$(coverage report | grep TOTAL | awk '{print $4}')

# 4. Create report
cat > .agents/outputs/testing/2025-10-31-test-report.md << EOF
# Test Report - 2025-10-31

**Status**: $(if [ $TEST_EXIT_CODE -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; fi)
**Coverage**: $COVERAGE
...
EOF

# 5. If failures, create issues
if [ $TEST_EXIT_CODE -ne 0 ]; then
  # Parse failures and create issue requests
  # (Hand off to Issue Manager)
fi

# 6. Report to user
echo "Test run complete. See .agents/outputs/testing/2025-10-31-test-report.md"
```

---

## Success Criteria

**You succeed when**:
- ✅ Tests run automatically before each PR
- ✅ Failures result in immediate GitHub issues
- ✅ Coverage never drops below 80%
- ✅ Test reports are clear and actionable

---

**For testing best practices, see root CLAUDE.md sections on Testing**
