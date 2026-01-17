# Phase 2: Resource Discovery Report

## Session Information

- **Session ID**: {{session_id}}
- **Project Type**: {{project_type}}
- **Agent**: resource-discovery-agent

---

## Available Skills Summary

| Category | Total | Implemented | Partial | Docs Only |
|----------|-------|-------------|---------|-----------|
| cosmetic-databases | {{db_total}} | {{db_impl}} | {{db_partial}} | {{db_docs}} |
| cosmetic-packages | {{pkg_total}} | {{pkg_impl}} | {{pkg_partial}} | {{pkg_docs}} |
| cosmetic-integrations | {{int_total}} | {{int_impl}} | {{int_partial}} | {{int_docs}} |
| cosmetic-thinking | {{think_total}} | {{think_impl}} | {{think_partial}} | {{think_docs}} |
| cosmetic-helpers | {{help_total}} | {{help_impl}} | {{help_partial}} | {{help_docs}} |
| **Total** | {{total_skills}} | {{total_impl}} | {{total_partial}} | {{total_docs}} |

---

## Skill Recommendations

### Primary Skills (Required)

| Skill | Category | Status | Purpose |
|-------|----------|--------|---------|
{{#each primary_skills}}
| {{name}} | {{category}} | {{status}} | {{purpose}} |
{{/each}}

### Secondary Skills (Optional)

| Skill | Category | Status | Purpose |
|-------|----------|--------|---------|
{{#each secondary_skills}}
| {{name}} | {{category}} | {{status}} | {{purpose}} |
{{/each}}

---

## Task-Skill Mapping

### For Project Type: {{project_type}}

```
{{task_skill_mapping}}
```

---

## Available MCP Servers

| MCP Server | Status | Relevant Tasks |
|------------|--------|----------------|
{{#each mcps}}
| {{name}} | {{status}} | {{tasks}} |
{{/each}}

### MCP Usage Plan

{{mcp_usage_plan}}

---

## Skill Dependency Graph

```
{{dependency_graph}}
```

---

## Resource Availability Check

### Scripts

| Skill | Script | Status |
|-------|--------|--------|
{{#each scripts}}
| {{skill}} | {{script_name}} | {{status}} |
{{/each}}

### Reference Materials

| Skill | References | Status |
|-------|------------|--------|
{{#each references}}
| {{skill}} | {{ref_count}} files | {{status}} |
{{/each}}

---

## Recommended Specialist Agents

Based on the analysis, the following specialist agents should be spawned in Phase 3:

1. **{{specialist_1_name}}**
   - Skills: {{specialist_1_skills}}
   - Tasks: {{specialist_1_tasks}}

2. **{{specialist_2_name}}**
   - Skills: {{specialist_2_skills}}
   - Tasks: {{specialist_2_tasks}}

{{#if specialist_3_name}}
3. **{{specialist_3_name}}**
   - Skills: {{specialist_3_skills}}
   - Tasks: {{specialist_3_tasks}}
{{/if}}

---

## Execution Order

```
1. {{execution_step_1}}
2. {{execution_step_2}}
3. {{execution_step_3}}
4. Parallel execution where possible
5. Aggregate results
```

---

## Warnings & Limitations

{{#each warnings}}
- ⚠️ {{this}}
{{/each}}

---

**Report Generated**: {{report_timestamp}}
**Duration**: {{phase_duration_sec}} seconds
