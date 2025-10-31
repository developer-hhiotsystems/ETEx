# GitHub Project Board Setup Guide

**Purpose**: Step-by-step guide to setup GitHub Projects board with Kanban, Timeline, and Table views
**Last Updated**: 2025-10-31
**Version**: 1.0

---

## Overview

**What is GitHub Projects?**
- Visual project management tool built into GitHub
- Track issues, pull requests, and notes
- Multiple views: Kanban board, Timeline (roadmap), Table (spreadsheet)
- Automation: Auto-move items based on status

**For ETEx MVP:**
- Track Week 1-6 implementation
- Visualize progress (Kanban view)
- See timeline/roadmap (Timeline view)
- Filter and sort (Table view)

---

## Quick Setup (5 minutes)

### Step 1: Create Project

1. **Go to**: https://github.com/developer-hhiotsystems?tab=projects
2. **Click**: "New project" (green button, top right)
3. **Choose**: "Board" template (Kanban layout)
4. **Name**: `ETEx MVP - 6 Week Sprint`
5. **Description**: `Track Week 1-6 MVP implementation with Kanban, Timeline, and Table views`
6. **Click**: "Create project"

---

### Step 2: Configure Kanban View (Default)

**Rename columns** (click column title → rename):

```
Todo → 📋 Backlog
In Progress → 👨‍💻 In Progress
Done → ✅ Done
```

**Add missing columns** (click "+ Add column"):

```
📐 Design
🚀 Ready
👀 Review
```

**Final column order**:
```
📋 Backlog → 📐 Design → 🚀 Ready → 👨‍💻 In Progress → 👀 Review → ✅ Done
```

---

### Step 3: Add Timeline View

1. **Click**: "+" next to "View 1" tab
2. **Choose**: "New view"
3. **Select**: "Timeline" (calendar/roadmap view)
4. **Name**: `Timeline (Roadmap)`
5. **Click**: "Create"

**Configure Timeline**:
- **Group by**: Milestone (shows Week 1, Week 2, etc.)
- **Zoom level**: Week (shows weekly breakdown)
- **Date field**: Target date (due date from milestone)

---

### Step 4: Add Table View

1. **Click**: "+" next to views
2. **Choose**: "Table" (spreadsheet view)
3. **Name**: `Table (All Issues)`
4. **Click**: "Create"

**Add custom fields** (click "+" → "New field"):

| Field Name | Type | Values |
|------------|------|--------|
| **Week** | Single select | Week 1, Week 2, ..., Week 6, Post-MVP |
| **Effort** | Single select | 🔹 Small, 🔸 Medium, 🔶 Large, 🔺 XL |
| **Component** | Single select | Backend, Frontend, Database, Extraction, API Integration |

**Show columns** (click column header → show/hide):
- ☑ Title
- ☑ Status
- ☑ Assignees
- ☑ Labels
- ☑ Milestone
- ☑ Week (custom field)
- ☑ Effort (custom field)
- ☑ Component (custom field)

---

### Step 5: Link Repository

1. **In project**, click **"⚙️ Settings"** (top right)
2. **Scroll to**: "Manage access"
3. **Click**: "Add repository"
4. **Select**: `developer-hhiotsystems/ETEx`
5. **Click**: "Add"

Now issues from ETEx repository can be added to the project!

---

### Step 6: Setup Automation (Optional)

**Auto-move items based on status**:

1. **In project**, click **"⚙️ Settings"**
2. **Click**: "Workflows"
3. **Enable**:
   - "Item opened" → Move to **Backlog**
   - "Item closed" → Move to **Done**
   - "Pull request opened" → Move to **Review**
   - "Pull request merged" → Move to **Done**

**Create custom workflow**:
- **When**: Label "status: in-progress" is added
- **Then**: Move to "In Progress" column

---

## Adding Issues to Project

### Method 1: From Issue Page

1. Open issue (e.g., #1)
2. In right sidebar, find "Projects"
3. Click "Add to project"
4. Select "ETEx MVP - 6 Week Sprint"
5. Issue appears in Backlog column

### Method 2: From Project Board

1. Open project board
2. Click "+" in any column
3. Search for issue by number or title
4. Click issue to add

### Method 3: Via CLI

```powershell
# Add issue #1 to project
gh project item-add <PROJECT_NUMBER> --owner developer-hhiotsystems --content-id <ISSUE_ID>
```

**Note**: GitHub CLI support for Projects (Beta) is limited. Web interface is easier.

---

## Using the Views

### Kanban View (Daily Work)

**Use this view for**:
- Daily standup (what's in progress?)
- Moving issues between stages
- Quick status overview

**Workflow**:
```
📋 Backlog → 📐 Design → 🚀 Ready → 👨‍💻 In Progress → 👀 Review → ✅ Done
```

**Example**:
1. Issue #1 (Database schema) starts in **Backlog**
2. Design agent starts spec → move to **Design**
3. Spec complete → move to **Ready**
4. Coding starts → move to **In Progress**
5. PR opened → move to **Review**
6. PR merged → move to **Done**

---

### Timeline View (Roadmap/Planning)

**Use this view for**:
- Weekly planning (what's this week vs next week?)
- Seeing timeline at a glance
- Identifying bottlenecks

**Group by Milestone**:
```
Week 1: Project Setup & Database [Nov 1-7]
├─ Issue #1: Database schema
├─ Issue #2: Alembic migrations
└─ Issue #3: Pydantic schemas

Week 2: Document Upload & PDF Processing [Nov 8-14]
├─ Issue #4: PDF upload endpoint
└─ Issue #5: File upload UI
```

**Zoom levels**:
- **Month**: High-level overview (all 6 weeks)
- **Week**: Detailed view (current week tasks)
- **Day**: Fine-grained (daily tasks)

---

### Table View (Filtering/Analysis)

**Use this view for**:
- Filtering issues (show only backend)
- Sorting by priority or effort
- Bulk editing custom fields
- Exporting to CSV

**Common filters**:
- **Backend only**: Component = "Backend"
- **This week**: Milestone = "Week 1"
- **High priority**: Priority = "High"
- **In progress**: Status = "In Progress"
- **Agent-generated**: Labels contains "agent:"

**Sort by**:
- Priority (critical → low)
- Effort (XL → small)
- Week (1 → 6)

---

## Week 1-6 Workflow Example

### Week 1 Planning (Monday)

**Kanban View**:
1. Create 5 issues for Week 1 tasks
2. All start in **Backlog**
3. Assign to "Week 1" milestone
4. Set **Effort** custom field

**Timeline View**:
1. See Week 1 issues grouped together
2. Due date: Friday Nov 7
3. Visual progress bar

**Table View**:
1. Filter: Milestone = "Week 1"
2. Sort by: Priority (high first)
3. Check: All have assignees

---

### Week 1 Execution (Daily)

**Monday AM** (Kanban View):
- Move #1 (Database schema) to **In Progress**
- Assign to yourself

**Tuesday PM**:
- #1 complete → create PR
- Move #1 to **Review**
- Move #2 (Alembic) to **In Progress**

**Wednesday**:
- PR #1 merged → #1 moves to **Done** (auto)
- #2 complete → PR created → **Review**
- Start #3 → **In Progress**

**Friday** (Timeline View):
- Check: Week 1 milestone progress (60% complete)
- See: Week 2 tasks coming up

---

### Week 1 Review (Friday)

**Table View**:
1. Filter: Milestone = "Week 1"
2. Check: All issues in "Done"?
3. If not: Move incomplete to Week 2

**Kanban View**:
1. Celebrate: Week 1 **Done** column filled!
2. Plan: Week 2 **Ready** column populated

**Timeline View**:
1. Week 1 milestone marked complete
2. Week 2 milestone active

---

## Advanced Features

### Custom Fields

**Use custom fields for**:
- **Week**: Track which week (easier than milestones for quick view)
- **Effort**: Size estimation (planning)
- **Component**: Filter by backend/frontend
- **Reviewed By**: Track who reviewed (accountability)

**Add custom field**:
1. Table view → "+" → "New field"
2. Name: "Reviewed By"
3. Type: "Text"
4. Fill in as reviews complete

---

### Saved Filters

**Create filter** (Table view):
1. Apply filters (e.g., Component = "Backend" AND Status = "In Progress")
2. Click "Save view"
3. Name: "Backend - In Progress"

**Reuse filter**:
- Click view tab
- Instant filtered view

---

### Insights (Future)

**Once you have data** (Week 2+):
1. Project → "Insights" tab
2. See:
   - Velocity (issues closed per week)
   - Cycle time (hours in "In Progress")
   - Burndown chart

---

## Integration with Milestones

### Create Milestones (Via Script)

```powershell
.\scripts\dev\github\create-milestones.ps1 -startDate "2025-11-01"
```

**Creates**:
- Week 1: Due Nov 7
- Week 2: Due Nov 14
- Week 3: Due Nov 21
- Week 4: Due Nov 28
- Week 5: Due Dec 5
- Week 6: Due Dec 12

### Assign Issues to Milestones

**Via web**:
1. Open issue
2. Right sidebar → "Milestone"
3. Select "Week 1: Project Setup & Database"

**Via CLI**:
```powershell
gh issue edit 1 --milestone "Week 1: Project Setup & Database"
```

---

## Best Practices

### 1. Update Status Regularly

**Daily**:
- Move issues between columns as you work
- Add comments on blockers

**Weekly**:
- Review milestone progress (Friday)
- Plan next week (Monday)

---

### 2. Use Consistent Labels

**Always add**:
- Type (feature/bug/docs)
- Priority (high/medium/low)
- Component (backend/frontend)

**This enables**:
- Filtering in Table view
- Grouping in Timeline view
- Clear categorization

---

### 3. Link Issues to PRs

**In PR description**:
```markdown
Closes #15
Related to #12
```

**Benefits**:
- Issue auto-moves to Done when PR merged
- Traceability (what PR fixed what issue)

---

### 4. Archive Completed Weeks

**After Week 1 complete**:
1. Milestone "Week 1" → Close
2. Filter issues: Milestone = "Week 1"
3. Verify all Done
4. Move focus to Week 2

---

## Troubleshooting

### Problem: Can't add repository to project

**Cause**: Project is user-level, not org-level

**Solution**:
- Project must be created under user account
- Then link repository via Settings → Manage access

---

### Problem: Issues don't auto-move to Done

**Cause**: Automation not enabled

**Solution**:
1. Project → Settings → Workflows
2. Enable "Item closed" → "Move to Done"

---

### Problem: Timeline view shows wrong dates

**Cause**: Issues missing milestone or due date

**Solution**:
- Assign issues to milestones
- Milestones have due dates
- Timeline uses milestone due date

---

### Problem: Can't filter by custom field

**Cause**: Custom field not set on issues

**Solution**:
1. Table view
2. Bulk select issues
3. Set custom field value

---

## Quick Reference

### Project URL
```
https://github.com/developer-hhiotsystems?tab=projects
```

### Milestones URL
```
https://github.com/developer-hhiotsystems/ETEx/milestones
```

### Key Shortcuts
- `c` - Create issue
- `/` - Focus search
- `?` - Show keyboard shortcuts

---

## Related Documentation

- **Workflow Guide**: [github-workflow-guide.md](github-workflow-guide.md)
- **Issue Creation**: [create-week1-issues.md](create-week1-issues.md)
- **Scripts**: [scripts/dev/github/README.md](../../scripts/dev/github/README.md)

---

**For complete GitHub Projects documentation, see**: https://docs.github.com/en/issues/planning-and-tracking-with-projects

**Last Updated**: 2025-10-31
**Version**: 1.0
