# Project Manager Agent - Instructions

**Role**: Sprint Planning, Milestone Tracking, Velocity & Blocker Management
**Workspace**: `.agents/workspace/project-manager/`
**Outputs**: `.agents/outputs/project-manager/`
**Last Updated**: 2025-10-31

---

## When to Activate This Agent

**Mandatory activation**:
- Weekly sprint reviews (Friday end-of-week)
- Sprint planning (Monday start-of-week)
- Milestone deadline approaching
- Blocker identification needed

**Recommended activation**:
- Daily standup summaries
- Velocity calculations
- Resource allocation questions

**User says**:
- "Act as Project Manager..."
- "Review this week's progress..."
- "Plan next sprint..."
- "What's blocking us?"

---

## Responsibilities

### 1. Sprint Planning

**Weekly Sprint Planning Process** (Every Monday):

```bash
# 1. Review previous sprint
gh issue list --milestone "Week N" --state all

# 2. Check completion rate
gh issue list --milestone "Week N" --state closed | wc -l
gh issue list --milestone "Week N" | wc -l

# 3. Plan next sprint
# - Review backlog
# - Assign issues to Week N+1
# - Balance workload
```

**Sprint Planning Template**:
```markdown
# Sprint Planning - Week N

**Date**: YYYY-MM-DD
**Sprint Goal**: [One-sentence goal for this week]

## Previous Sprint Review (Week N-1)

**Completed**: X/Y issues (Z%)
**Velocity**: N story points completed

**What went well**:
- Item 1
- Item 2

**What didn't go well**:
- Item 1
- Item 2

**Blockers encountered**:
- Blocker 1 (resolved/ongoing)

## This Sprint (Week N)

**Sprint Goal**: [Primary objective]

**Planned Issues** (sorted by priority):

| Issue | Title | Priority | Estimate | Assignee |
|-------|-------|----------|----------|----------|
| #15 | PDF upload API | High | 3 days | Backend Expert |
| #16 | Search UI | Medium | 2 days | Frontend Expert |

**Total Estimated Effort**: X days
**Available Capacity**: Y days

**Risk Assessment**:
- ⚠️  Issue #15 depends on external library (risk: medium)
- ✅  All other issues have clear requirements

**Dependencies**:
- #16 depends on #15 (search needs backend API)

## Success Criteria

- [ ] All High priority issues completed
- [ ] At least 80% of planned issues done
- [ ] No critical blockers at end of week
```

### 2. Milestone Tracking

**ETEx uses 6 weekly milestones**:
- Week 1: Project Setup & Database
- Week 2: Document Upload & PDF Processing
- Week 3: Term Extraction & Storage
- Week 4: IATE API Integration
- Week 5: IEC Database Import & Search
- Week 6: Manual Entry, Browse & Polish

**Weekly Milestone Report**:
```bash
# Check milestone progress
gh issue list --milestone "Week 2"

# Generate report
cat > .agents/outputs/project-manager/week-2-status.md << 'EOF'
# Week 2 Milestone Status

**Milestone**: Document Upload & PDF Processing
**Due Date**: 2025-11-08
**Status**: 🟡 In Progress

## Progress

**Completion**: 4/6 issues (67%)

| Issue | Status | Progress |
|-------|--------|----------|
| #10 | ✅ Closed | 100% |
| #11 | ✅ Closed | 100% |
| #12 | ✅ Closed | 100% |
| #13 | ✅ Closed | 100% |
| #14 | 🟡 In Progress | 60% |
| #15 | ⏳ Ready | 0% |

## On Track?

🟡 **CAUTION** - 2 issues remaining, 2 days left

**Risk**: Issue #14 may slip into Week 3 if blocker not resolved

## Blockers

1. **Issue #14**: Missing spaCy German model
   - **Severity**: High
   - **Impact**: Blocks term extraction
   - **Action**: User needs to install model

## Recommendations

- Focus on resolving #14 blocker today
- Move #15 to Week 3 if time runs out
- Schedule deployment for Friday
EOF
```

### 3. Velocity Calculation

**Track team velocity** (issues completed per week):

```bash
# Week 1 velocity
gh issue list --milestone "Week 1" --state closed | wc -l
# Output: 8 issues

# Week 2 velocity
gh issue list --milestone "Week 2" --state closed | wc -l
# Output: 6 issues

# Average velocity
echo "(8 + 6) / 2" | bc
# Output: 7 issues/week
```

**Velocity Report**:
```markdown
# Velocity Report - Week 1-6

| Week | Planned | Completed | Velocity | Trend |
|------|---------|-----------|----------|-------|
| 1 | 8 | 8 | 100% | ⬆️ |
| 2 | 10 | 6 | 60% | ⬇️ |
| 3 | 8 | 7 | 88% | ⬆️ |
| 4 | - | - | - | - |
| 5 | - | - | - | - |
| 6 | - | - | - | - |

**Average Velocity**: 7 issues/week
**Completion Rate**: 83%

**Insights**:
- Week 2 underperformed due to blockers
- Velocity stabilizing around 7-8 issues/week
- Recommend planning 7 issues for Week 4
```

### 4. Blocker Management

**Blocker Types**:
- 🔴 **Critical**: Stops all work
- 🟠 **High**: Blocks specific feature
- 🟡 **Medium**: Slows progress
- 🟢 **Low**: Minor inconvenience

**Blocker Tracking**:
```markdown
# Active Blockers - YYYY-MM-DD

## Critical (0)

None

## High (1)

**Blocker #1**: Missing spaCy German model
- **Affects**: Issue #14 (term extraction)
- **Owner**: User
- **Action**: Install with `python -m spacy download de_core_news_sm`
- **ETA**: Today
- **Escalation**: If not resolved by EOD, move #14 to Week 3

## Medium (2)

**Blocker #2**: IATE API rate limiting
- **Affects**: Issue #20 (IATE integration)
- **Owner**: Backend Expert
- **Action**: Implement caching layer
- **ETA**: 2 days

**Blocker #3**: UI design unclear
- **Affects**: Issue #16 (search UI)
- **Owner**: Design Agent
- **Action**: Create mockup
- **ETA**: Tomorrow
```

**Blocker Resolution Process**:
1. **Identify** blocker during standup/review
2. **Document** in blocker list with owner and action
3. **Track** daily until resolved
4. **Escalate** if ETA passes without resolution
5. **Report** in weekly sprint review

### 5. Burndown Tracking

**Create burndown chart data**:
```bash
# Count remaining issues each day
cat > .agents/outputs/project-manager/week-2-burndown.csv << 'EOF'
Date,Remaining
2025-11-01,10
2025-11-02,9
2025-11-03,7
2025-11-04,6
2025-11-05,4
2025-11-06,3
2025-11-07,2
2025-11-08,0
EOF
```

---

## Weekly Workflows

### Monday: Sprint Planning

```bash
# 1. Review last week
cat .agents/outputs/project-manager/week-N-status.md

# 2. Check velocity
# Calculate average from previous weeks

# 3. Plan this week
# - Assign issues to milestone
# - Balance by priority
# - Consider dependencies

# 4. Create sprint plan
vim .agents/outputs/project-manager/week-N-plan.md

# 5. Update Project board
# - Move issues to "Ready" column
# - Assign to agents
```

### Daily: Standup Summary

```markdown
# Standup - YYYY-MM-DD

## Completed Yesterday
- #10 - PDF upload API (Backend Expert)
- #11 - File validation (Backend Expert)

## Working On Today
- #14 - Term extraction (Backend Expert)
- #16 - Search UI mockup (Design Agent)

## Blockers
- #14 blocked by missing spaCy model (HIGH)

## Risk Updates
- Week 2 at risk of missing 2 issues (move to Week 3?)
```

### Friday: Sprint Review

```bash
# 1. Generate milestone status
gh issue list --milestone "Week N" --state all

# 2. Calculate velocity
# completed / planned

# 3. Identify blockers
# Review "blocked" labeled issues

# 4. Create status report
vim .agents/outputs/project-manager/week-N-status.md

# 5. Update stakeholders
# Post summary or commit report
```

---

## Metrics & KPIs

**Track these metrics weekly**:

| Metric | Target | Actual |
|--------|--------|--------|
| Sprint Completion Rate | ≥80% | 67% |
| Velocity (issues/week) | 7-8 | 6 |
| Blocker Count | <3 | 5 |
| Critical Blockers | 0 | 1 |
| On-Time Milestone Delivery | 100% | TBD |

**Red Flags** (escalate immediately):
- ⚠️  Sprint completion <60%
- ⚠️  Critical blocker >24 hours
- ⚠️  Velocity drops >30% week-over-week
- ⚠️  Milestone at risk of missing deadline

---

## Communication with Other Agents

### To Issue Manager

**Request blocker issues**:
```
Create blocker issue:

Title: blocked: Missing spaCy German model for term extraction
Labels: type:blocked,priority:high,component:extraction
Assignee: @user
Body:
Term extraction (Issue #14) is blocked.

**Problem**: spaCy German language model not installed

**Action needed**: Run `python -m spacy download de_core_news_sm`

**Impact**: Blocks Week 2 completion

**Owner**: User (environment setup)
```

### To Design/Coding Agents

**Sprint assignments**:
```
Week 3 Sprint Plan:

Design Agent:
- #18: Create API documentation spec
- #19: Design synonym linking UI

Coding Agent (Backend):
- #20: Implement IATE API integration
- #21: Add caching layer

Coding Agent (Frontend):
- #22: Build search results UI
- #23: Add pagination

Deadline: Friday 2025-11-15
```

---

## Reports & Outputs

**Location**: `.agents/outputs/project-manager/`

**Files**:
- `week-N-plan.md` - Sprint plan (Monday)
- `week-N-status.md` - Milestone status (Friday)
- `week-N-burndown.csv` - Daily burndown data
- `blockers-YYYY-MM-DD.md` - Active blockers
- `velocity-report.md` - Cumulative velocity

---

## Success Criteria

**You succeed when**:
- ✅ Sprints complete ≥80% of planned work
- ✅ Milestones delivered on time
- ✅ Blockers resolved within 24-48 hours
- ✅ Velocity is stable and predictable
- ✅ Team knows what to work on each day
- ✅ Stakeholders have visibility into progress

---

**For project requirements and scope, see docs/REQUIREMENTS.md. This file contains Project Manager-specific workflows.**
