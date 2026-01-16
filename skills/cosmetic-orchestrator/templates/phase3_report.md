# Phase 3: Specialist Execution Report

## Session Information

- **Session ID**: {{session_id}}
- **Project Type**: {{project_type}}
- **Specialists Deployed**: {{specialists_count}}

---

## Execution Summary

| Metric | Value |
|--------|-------|
| Total Tasks | {{total_tasks}} |
| Completed | {{completed_tasks}} |
| Partial | {{partial_tasks}} |
| Failed | {{failed_tasks}} |
| Total Duration | {{total_duration_sec}} seconds |

---

## Specialist Agents Executed

{{#each specialists}}
### {{index}}. {{name}}

**Agent ID**: {{agent_id}}
**Status**: {{status}}
**Duration**: {{duration_sec}} seconds

#### Skills Used

| Skill | Category | Status |
|-------|----------|--------|
{{#each skills}}
| {{name}} | {{category}} | {{status}} |
{{/each}}

#### Tasks Completed

{{#each tasks}}
- {{#if completed}}✅{{else}}⏳{{/if}} **{{name}}**: {{description}}
  {{#if output}}
  - Output: {{output}}
  {{/if}}
{{/each}}

#### Key Results

{{results_summary}}

{{#if artifacts}}
#### Generated Artifacts

{{#each artifacts}}
- `{{path}}`: {{description}}
{{/each}}
{{/if}}

{{#if errors}}
#### Errors Encountered

{{#each errors}}
- ⚠️ {{message}} ({{severity}})
{{/each}}
{{/if}}

---

{{/each}}

## MCP Server Usage

| MCP Server | Operations | Status |
|------------|------------|--------|
{{#each mcp_usage}}
| {{server}} | {{operation_count}} | {{status}} |
{{/each}}

---

## Cross-Specialist Data Flow

```
{{data_flow_diagram}}
```

---

## Aggregated Outputs

### Formulation Data (if applicable)

{{#if formulation_data}}
```json
{{formulation_data}}
```
{{else}}
N/A - No formulation tasks in this session.
{{/if}}

### Safety Assessment (if applicable)

{{#if safety_data}}
| Parameter | Value | Status |
|-----------|-------|--------|
{{#each safety_data}}
| {{parameter}} | {{value}} | {{status}} |
{{/each}}
{{else}}
N/A - No safety tasks in this session.
{{/if}}

### Regulatory Check (if applicable)

{{#if regulatory_data}}
| Region | Status | Notes |
|--------|--------|-------|
{{#each regulatory_data}}
| {{region}} | {{status}} | {{notes}} |
{{/each}}
{{else}}
N/A - No regulatory tasks in this session.
{{/if}}

### Trend/Market Data (if applicable)

{{#if trend_data}}
{{trend_data}}
{{else}}
N/A - No trend analysis tasks in this session.
{{/if}}

---

## Execution Log

```
{{#each execution_log}}
[{{timestamp}}] [{{specialist}}] {{action}}: {{message}}
{{/each}}
```

---

## Notes for Phase 4

### Data Quality Indicators

| Indicator | Score | Notes |
|-----------|-------|-------|
| Completeness | {{completeness_indicator}}% | {{completeness_notes}} |
| Consistency | {{consistency_indicator}}% | {{consistency_notes}} |
| Coverage | {{coverage_indicator}}% | {{coverage_notes}} |

### Items Requiring Validation

{{#each validation_items}}
- [ ] {{this}}
{{/each}}

### Known Limitations

{{#each limitations}}
- {{this}}
{{/each}}

---

**Report Generated**: {{report_timestamp}}
**Duration**: {{phase_duration_sec}} seconds
