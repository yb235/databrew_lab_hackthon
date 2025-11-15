# 📅 Sprint Planning Template

**Sprint Planning Guide for DataBrew Lab**  
**Last Updated**: November 15, 2025

---

## 📋 Table of Contents

1. [Sprint Planning Overview](#sprint-planning-overview)
2. [Pre-Planning Preparation](#pre-planning-preparation)
3. [Sprint Planning Meeting Agenda](#sprint-planning-meeting-agenda)
4. [Task Estimation Guidelines](#task-estimation-guidelines)
5. [Sprint Planning Template](#sprint-planning-template)
6. [Post-Planning Activities](#post-planning-activities)
7. [Best Practices](#best-practices)

---

## 🎯 Sprint Planning Overview

### Purpose
Sprint planning is where the team:
- Reviews the previous sprint
- Sets goals for the upcoming sprint
- Selects work from the backlog
- Estimates and assigns tasks
- Commits to a sprint backlog

### Attendees
**Required**:
- Scrum Master (facilitator)
- Product Owner (priorities and goals)
- Development Team (all developers, QA, designers)
- Technical Lead (technical guidance)

**Optional**:
- Project Manager
- Stakeholders (for goal setting only)

### Duration
- **2 weeks sprint**: 2-hour meeting
- **1 week sprint**: 1-hour meeting

### Schedule
- **When**: Last day of current sprint
- **Time**: After sprint review and retrospective
- **Frequency**: Every 1-2 weeks (matches sprint length)

---

## 📝 Pre-Planning Preparation

### 1 Week Before Sprint Planning

#### Product Owner Tasks
- [ ] Review and prioritize backlog in [PENDING_WORK.md](./PENDING_WORK.md)
- [ ] Define sprint goal candidates
- [ ] Ensure top stories have acceptance criteria
- [ ] Check dependencies are resolved
- [ ] Communicate with stakeholders about priorities

#### Scrum Master Tasks
- [ ] Review current sprint progress
- [ ] Check team velocity from previous sprints
- [ ] Calculate team capacity for next sprint
- [ ] Prepare sprint planning meeting agenda
- [ ] Book meeting room/video call
- [ ] Send calendar invites

#### Technical Lead Tasks
- [ ] Review technical dependencies
- [ ] Identify any technical risks
- [ ] Prepare technical context for complex tasks
- [ ] Review architecture decisions needed
- [ ] Check infrastructure readiness

#### Development Team Tasks
- [ ] Review [PENDING_WORK.md](./PENDING_WORK.md) priorities
- [ ] Clarify questions about upcoming work
- [ ] Complete current sprint tasks
- [ ] Update task status in [PROJECT_TRACKER.md](./PROJECT_TRACKER.md)

### 2 Days Before Sprint Planning

#### Review Metrics
```markdown
Current Sprint Metrics to Review:
- Completed tasks: X/Y
- Velocity: X tasks/week
- Burndown status: On track / Behind / Ahead
- Quality metrics: Test coverage, bug count
- Blockers encountered: List and resolutions
```

#### Prepare Documents
- [ ] [PROJECT_STATUS.md](./PROJECT_STATUS.md) - Current state
- [ ] [BUGS_AND_ISSUES.md](./BUGS_AND_ISSUES.md) - Critical bugs
- [ ] [PENDING_WORK.md](./PENDING_WORK.md) - Prioritized backlog
- [ ] [PROJECT_TRACKER.md](./PROJECT_TRACKER.md) - Sprint history

### 1 Day Before Sprint Planning

#### Team Capacity Calculation
```markdown
Team Member | Role | Days Available | Hours/Day | Total Hours | % Available
------------|------|----------------|-----------|-------------|-------------
Member 1    | Dev  | 10 days        | 6h        | 60h         | 75%
Member 2    | Dev  | 10 days        | 8h        | 80h         | 100%
Member 3    | QA   | 8 days         | 6h        | 48h         | 60%
------------|------|----------------|-----------|-------------|-------------
TOTAL       |      |                |           | 188h        | 78%

Factors reducing capacity:
- Holidays: [List]
- PTO: [List]
- Training/Meetings: [Estimate hours]
- Support/Maintenance: [Estimate 10-20%]
```

**Formula**:
```
Available Capacity = (Team Size × Days × Hours/Day) × Availability %
Planned Capacity = Available Capacity × 0.8  (80% for safety buffer)
```

---

## 🏛️ Sprint Planning Meeting Agenda

### Part 1: Sprint Review & Retrospective (45-60 minutes)

#### 1.1 Sprint Review (20-30 min)
**Review completed work**

```markdown
Sprint [Number] Review

Sprint Goal: [Goal from last sprint]
Status: ✅ Achieved / 🟡 Partially / ❌ Not Achieved

Completed Work:
- [x] Task 1 - Description
- [x] Task 2 - Description
- [x] Task 3 - Description

Incomplete Work:
- [ ] Task 4 - Reason for incompletion
- [ ] Task 5 - Reason for incompletion

Metrics:
- Planned: X tasks
- Completed: Y tasks
- Completion Rate: Z%
- Velocity: X tasks/week
- Quality: [Test coverage, bugs found]

Demo:
- [Feature 1 demo notes]
- [Feature 2 demo notes]
```

**Actions**:
1. Scrum Master presents sprint metrics
2. Team demos completed features
3. Product Owner accepts/rejects work
4. Discuss incomplete work (rollover or drop)

#### 1.2 Sprint Retrospective (25-30 min)
**Reflect on process**

**Format**: Start/Stop/Continue

```markdown
What Went Well (Continue):
- [Thing 1]
- [Thing 2]
- [Thing 3]

What Didn't Go Well (Stop):
- [Thing 1]
- [Thing 2]

What To Improve (Start):
- [Thing 1]
- [Thing 2]

Action Items:
- [ ] Action 1 - Owner: [Name] - Deadline: [Date]
- [ ] Action 2 - Owner: [Name] - Deadline: [Date]
```

**Activities**:
1. Each team member shares observations (5 min)
2. Group similar items (5 min)
3. Vote on top items to address (5 min)
4. Create action items (10 min)
5. Assign owners and deadlines (5 min)

### Part 2: Next Sprint Planning (60 minutes)

#### 2.1 Set Sprint Goal (10 min)
**Define the objective**

```markdown
Sprint [Number] Goal:
[One clear, concise sentence describing what the sprint will achieve]

Example: "Complete Phase 1 Storage Service implementation with >85% test coverage"

Success Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

Value to Stakeholders:
[Why this sprint goal matters]
```

**Tips**:
- Make it specific and measurable
- Ensure it delivers value
- Get team buy-in
- Align with project milestones

#### 2.2 Select Backlog Items (20 min)
**Choose work from [PENDING_WORK.md](./PENDING_WORK.md)**

**Process**:
1. Product Owner presents top priority items
2. Technical Lead provides context
3. Team asks clarifying questions
4. Group discusses feasibility
5. Reach consensus on selection

**Criteria for Selection**:
- ✅ Aligns with sprint goal
- ✅ Dependencies resolved
- ✅ Acceptance criteria clear
- ✅ Fits in available capacity
- ✅ Provides value

#### 2.3 Task Breakdown & Estimation (20 min)
**Break down and estimate work**

**Process**:
1. Break large items into tasks (max 8 hours each)
2. Discuss technical approach
3. Estimate using planning poker
4. Adjust if estimates exceed capacity

See [Task Estimation Guidelines](#task-estimation-guidelines) below.

#### 2.4 Task Assignment (10 min)
**Assign tasks to team members**

```markdown
Task Assignment:
- Task ID: SE-XXX
- Description: [Task description]
- Assigned To: [Team Member]
- Est. Hours: Xh
- Priority: P0/P1/P2/P3
- Dependencies: [List]
```

**Considerations**:
- Team member expertise
- Workload balance
- Learning opportunities
- Pairing needs

---

## 📏 Task Estimation Guidelines

### Estimation Techniques

#### 1. Planning Poker
**Most common method for DataBrew Lab**

**Fibonacci Scale**: 1, 2, 3, 5, 8, 13, 21 (hours)

**Process**:
```markdown
1. Product Owner describes task
2. Team asks clarifying questions
3. Each member privately selects estimate
4. All reveal simultaneously
5. Discuss outliers
6. Re-estimate if needed
7. Reach consensus
```

**Guidelines**:
- 1-2 hours: Simple, well-understood task
- 3-5 hours: Moderate complexity
- 8 hours: Complex task (should be 1 day max)
- 13+ hours: Too large, break down further

#### 2. T-Shirt Sizing (Alternative)
**For rough estimates**

- XS (1-2h): Trivial change
- S (3-5h): Simple feature
- M (8-13h): Moderate feature
- L (21-34h): Complex feature (break down!)
- XL (55h+): Epic (definitely break down!)

### Estimation Best Practices

**Do**:
- ✅ Include time for testing
- ✅ Include time for code review
- ✅ Include time for documentation
- ✅ Add buffer for unknowns (20-30%)
- ✅ Consider team expertise
- ✅ Reference similar past tasks

**Don't**:
- ❌ Estimate without understanding requirements
- ❌ Estimate based on "best case" scenario
- ❌ Ignore dependencies
- ❌ Forget about meetings/interruptions
- ❌ Let one person dominate estimation
- ❌ Estimate for others without their input

### Example Estimation

```markdown
Task: Implement SQLite storage adapter (SE-116)

Breakdown:
- Design schema: 1h
- Implement connection: 2h
- Implement CRUD ops: 3h
- Error handling: 1h
- Write tests: 2h
- Code review: 1h
- Documentation: 1h
- Buffer (20%): 2h
-----------------------
Total: 13h

Estimate: 13 hours (2 days)
Assigned to: Backend Dev with SQLite experience
Risk: Medium (new to team, but familiar tech)
```

---

## 📄 Sprint Planning Template

### Sprint [Number] Planning

**Date**: [Date]  
**Sprint Duration**: [X weeks]  
**Sprint Start**: [Date]  
**Sprint End**: [Date]

---

#### Sprint Goal
```markdown
[One clear sentence describing the sprint objective]

Success Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

---

#### Team Capacity

| Team Member | Role | Available Days | Hours/Day | Total Hours | Notes |
|-------------|------|----------------|-----------|-------------|-------|
| [Name] | Dev | X | X | Xh | [PTO, etc.] |
| [Name] | QA | X | X | Xh | |
| **TOTAL** | | | | **Xh** | |

**Planned Capacity**: [Total × 0.8]h (with 20% buffer)

---

#### Selected Work

##### High Priority (P0) - Must Have
| ID | Task | Owner | Est. | Dependencies |
|----|------|-------|------|--------------|
| SE-XXX | [Description] | [Name] | Xh | [List] |
| SE-XXX | [Description] | [Name] | Xh | [List] |

##### Medium Priority (P1) - Should Have
| ID | Task | Owner | Est. | Dependencies |
|----|------|-------|------|--------------|
| SE-XXX | [Description] | [Name] | Xh | [List] |

##### Low Priority (P2) - Nice to Have
| ID | Task | Owner | Est. | Dependencies |
|----|------|-------|------|--------------|
| SE-XXX | [Description] | [Name] | Xh | [List] |

---

#### Sprint Metrics

- **Total Tasks**: X
- **Total Estimated Hours**: Xh
- **Team Capacity**: Xh
- **Capacity Utilization**: X%
- **Target Velocity**: X tasks/week

---

#### Risks & Dependencies

**Risks**:
- [ ] Risk 1 - Mitigation: [Strategy]
- [ ] Risk 2 - Mitigation: [Strategy]

**Dependencies**:
- [ ] Dependency 1 - Status: [Status]
- [ ] Dependency 2 - Status: [Status]

**Blockers**:
- [ ] Blocker 1 - Resolution Plan: [Plan]

---

#### Definition of Done

**Task is "Done" when**:
- [ ] Code complete and tested locally
- [ ] Unit tests written and passing (>85% coverage)
- [ ] Integration tests passing (if applicable)
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] No critical bugs
- [ ] Merged to main branch
- [ ] Stakeholder acceptance (if needed)

---

#### Meeting Notes

**Attendees**: [List]

**Decisions Made**:
- Decision 1: [Description]
- Decision 2: [Description]

**Action Items**:
- [ ] Action 1 - Owner: [Name] - Due: [Date]
- [ ] Action 2 - Owner: [Name] - Due: [Date]

**Questions/Concerns**:
- Question 1: [Answer/Resolution]
- Question 2: [Answer/Resolution]

---

## ✅ Post-Planning Activities

### Immediately After Meeting (Same Day)

#### Scrum Master
- [ ] Update [PROJECT_TRACKER.md](./PROJECT_TRACKER.md):
  - New sprint overview
  - Updated Kanban board
  - Team assignments
  - Sprint goals
  - Burndown chart baseline
- [ ] Create GitHub project board (if using)
- [ ] Send sprint summary email to team
- [ ] Schedule daily standups for sprint

#### Product Owner
- [ ] Update [PROJECT_STATUS.md](./PROJECT_STATUS.md):
  - Current sprint goals
  - Updated progress metrics
- [ ] Update [PENDING_WORK.md](./PENDING_WORK.md):
  - Move planned items from backlog
  - Adjust priorities
- [ ] Communicate sprint goals to stakeholders

#### Development Team
- [ ] Review assigned tasks in [PROJECT_TRACKER.md](./PROJECT_TRACKER.md)
- [ ] Set up development environment for sprint work
- [ ] Review technical dependencies
- [ ] Clarify any remaining questions

### First Day of Sprint

#### Team
- [ ] First daily standup
- [ ] Begin work on P0 (highest priority) tasks
- [ ] Update task status as work begins
- [ ] Communicate any immediate blockers

---

## 🎯 Best Practices

### Before Planning

**Do**:
- ✅ Prepare and prioritize backlog ahead of time
- ✅ Ensure acceptance criteria are clear
- ✅ Calculate team capacity accurately
- ✅ Review previous sprint velocity
- ✅ Resolve major blockers before planning

**Don't**:
- ❌ Plan without capacity calculation
- ❌ Include tasks with unresolved dependencies
- ❌ Over-commit based on optimistic estimates
- ❌ Skip retrospective learnings
- ❌ Start planning without a clear goal

### During Planning

**Do**:
- ✅ Time-box discussions (use timer)
- ✅ Encourage everyone to participate
- ✅ Focus on value and priorities
- ✅ Ask clarifying questions
- ✅ Challenge estimates respectfully
- ✅ Document decisions and action items

**Don't**:
- ❌ Let meetings run over time
- ❌ Dive too deep into technical details
- ❌ Commit to more than capacity allows
- ❌ Make assumptions without clarification
- ❌ Ignore team concerns or risks
- ❌ Skip task assignments

### After Planning

**Do**:
- ✅ Update all project management docs immediately
- ✅ Communicate sprint goals clearly
- ✅ Start working on highest priority first
- ✅ Review sprint board daily
- ✅ Track progress against capacity
- ✅ Adjust if needed (but avoid scope creep)

**Don't**:
- ❌ Delay documentation updates
- ❌ Start work before assignments are clear
- ❌ Add tasks mid-sprint without team agreement
- ❌ Ignore burndown trends
- ❌ Hide blockers from the team
- ❌ Change sprint goal mid-sprint

---

## 📊 Sprint Planning Checklist

### Pre-Planning ✅
- [ ] Backlog prioritized and ready
- [ ] Team capacity calculated
- [ ] Previous sprint metrics reviewed
- [ ] Dependencies identified and resolved
- [ ] Sprint goal candidates prepared
- [ ] Meeting scheduled with all attendees

### During Planning ✅
- [ ] Sprint review completed
- [ ] Retrospective conducted
- [ ] Sprint goal set and agreed
- [ ] Backlog items selected
- [ ] Tasks broken down (<8h each)
- [ ] All tasks estimated
- [ ] Tasks assigned to team members
- [ ] Risks and dependencies documented
- [ ] Team commitment secured

### Post-Planning ✅
- [ ] PROJECT_TRACKER.md updated
- [ ] PROJECT_STATUS.md updated
- [ ] PENDING_WORK.md updated
- [ ] Sprint summary sent to team
- [ ] Stakeholders informed
- [ ] Daily standups scheduled
- [ ] Team ready to start work

---

## 📞 Need Help?

**Scrum Master**: Lead sprint planning, update tracker  
**Product Owner**: Prioritize work, define goals  
**Technical Lead**: Provide technical guidance  
**Project Manager**: Resource allocation, stakeholder communication

**Questions? Issues?**
- Raise in daily standup
- Discuss in retrospective
- Create process improvement issue
- Contact Scrum Master

---

**Last Updated**: November 15, 2025  
**Template Version**: 1.0  
**Maintained By**: Scrum Master

---

<div align="center">

**Plan Well, Execute Better! 🚀**

</div>
