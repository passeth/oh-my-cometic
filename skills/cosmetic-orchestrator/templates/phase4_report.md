# Phase 4: Validation Report

## Session Information

- **Session ID**: {{session_id}}
- **Project Type**: {{project_type}}
- **Agent**: validation-agent

---

## Validation Summary

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| Completeness | {{completeness_score}}% | 90% | {{completeness_status}} |
| Consistency | {{consistency_score}}% | 95% | {{consistency_status}} |
| Coverage | {{coverage_score}}% | 85% | {{coverage_status}} |
| **Overall** | {{overall_score}}% | 90% | {{overall_status}} |

---

## Completeness Check

### Required Outputs

| Output | Present | Valid | Notes |
|--------|---------|-------|-------|
{{#each required_outputs}}
| {{name}} | {{#if present}}✅{{else}}❌{{/if}} | {{#if valid}}✅{{else}}⚠️{{/if}} | {{notes}} |
{{/each}}

### Missing Elements

{{#if missing_elements}}
{{#each missing_elements}}
- ❌ **{{name}}**: {{reason}}
  - Impact: {{impact}}
  - Recommendation: {{recommendation}}
{{/each}}
{{else}}
✅ All required elements are present.
{{/if}}

---

## Consistency Check

### Cross-Reference Validation

| Item A | Item B | Relationship | Status |
|--------|--------|--------------|--------|
{{#each cross_references}}
| {{item_a}} | {{item_b}} | {{relationship}} | {{#if consistent}}✅{{else}}⚠️ Conflict{{/if}} |
{{/each}}

### Contradictions Found

{{#if contradictions}}
{{#each contradictions}}
#### Contradiction {{index}}

- **Source A**: {{source_a}} ({{value_a}})
- **Source B**: {{source_b}} ({{value_b}})
- **Impact**: {{impact}}
- **Resolution**: {{resolution}}

{{/each}}
{{else}}
✅ No contradictions detected.
{{/if}}

### Calculation Verification

{{#if calculations}}
| Calculation | Expected | Actual | Status |
|-------------|----------|--------|--------|
{{#each calculations}}
| {{name}} | {{expected}} | {{actual}} | {{#if valid}}✅{{else}}❌{{/if}} |
{{/each}}
{{else}}
N/A - No calculations to verify.
{{/if}}

---

## Coverage Analysis

### Scope Coverage

| Scope Item | Addressed | Depth | Notes |
|------------|-----------|-------|-------|
{{#each scope_items}}
| {{name}} | {{#if addressed}}✅{{else}}❌{{/if}} | {{depth}} | {{notes}} |
{{/each}}

### Gap Analysis

{{#if gaps}}
{{#each gaps}}
#### Gap {{index}}: {{title}}

- **Category**: {{category}}
- **Severity**: {{severity}}
- **Description**: {{description}}
- **Impact**: {{impact}}
- **Recommended Action**: {{action}}

{{/each}}
{{else}}
✅ No significant gaps identified.
{{/if}}

---

## Issues Summary

### Critical Issues (Must Fix)

{{#if critical_issues}}
{{#each critical_issues}}
1. **{{title}}**
   - Description: {{description}}
   - Location: {{location}}
   - Impact: {{impact}}
   - Resolution: {{resolution}}
{{/each}}
{{else}}
✅ No critical issues found.
{{/if}}

### High Priority Issues

{{#if high_issues}}
{{#each high_issues}}
- ⚠️ **{{title}}**: {{description}}
  - Action: {{action}}
{{/each}}
{{else}}
✅ No high priority issues found.
{{/if}}

### Medium Priority Issues

{{#if medium_issues}}
{{#each medium_issues}}
- **{{title}}**: {{description}}
{{/each}}
{{else}}
✅ No medium priority issues found.
{{/if}}

### Low Priority Issues (Optional)

{{#if low_issues}}
{{#each low_issues}}
- {{title}}: {{description}}
{{/each}}
{{else}}
✅ No low priority issues found.
{{/if}}

---

## Data Quality Report

### Source Data Quality

| Data Source | Completeness | Accuracy | Freshness |
|-------------|--------------|----------|-----------|
{{#each data_sources}}
| {{name}} | {{completeness}}% | {{accuracy}}% | {{freshness}} |
{{/each}}

### Output Data Quality

| Output | Format Valid | Content Valid | Usable |
|--------|--------------|---------------|--------|
{{#each outputs}}
| {{name}} | {{#if format_valid}}✅{{else}}❌{{/if}} | {{#if content_valid}}✅{{else}}❌{{/if}} | {{#if usable}}✅{{else}}❌{{/if}} |
{{/each}}

---

## Revised Action Items

Based on validation results, the following action items are revised for Phase 5:

### Must Complete (Before Synthesis)

{{#each must_complete}}
1. **{{title}}**
   - Reason: {{reason}}
   - Owner: {{owner}}
{{/each}}

### Should Complete (If Time Permits)

{{#each should_complete}}
- {{this}}
{{/each}}

### Defer to Follow-up

{{#each defer_items}}
- {{this}}
{{/each}}

---

## Warnings

{{#if warnings}}
{{#each warnings}}
- ⚠️ {{this}}
{{/each}}
{{else}}
No warnings to report.
{{/if}}

---

## Validation Details

### Phase 1 (Context) Validation

- **Request Understanding**: {{phase1_request_score}}%
- **Keyword Extraction**: {{phase1_keyword_score}}%
- **Project Type Detection**: {{phase1_type_score}}%

### Phase 2 (Resources) Validation

- **Skill Discovery**: {{phase2_skill_score}}%
- **MCP Availability**: {{phase2_mcp_score}}%
- **Task Mapping**: {{phase2_mapping_score}}%

### Phase 3 (Execution) Validation

- **Task Completion**: {{phase3_task_score}}%
- **Output Quality**: {{phase3_output_score}}%
- **Error Handling**: {{phase3_error_score}}%

---

## Recommendations for Synthesis

### Key Points to Emphasize

{{#each key_points}}
- {{this}}
{{/each}}

### Areas Requiring Caution

{{#each caution_areas}}
- ⚠️ {{this}}
{{/each}}

### Suggested Report Structure

{{suggested_structure}}

---

**Report Generated**: {{report_timestamp}}
**Duration**: {{phase_duration_sec}} seconds
**Validation Rules Applied**: {{rules_count}}
