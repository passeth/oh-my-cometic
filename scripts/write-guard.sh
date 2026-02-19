#!/bin/bash
# write-guard.sh — 기존 파일 덮어쓰기 방지 (PreToolUse hook for Write|Edit)
# Reads JSON from stdin, checks if target file exists and is protected.

INPUT=$(cat)

# Extract file path from tool input
FILE_PATH=""
if command -v jq &> /dev/null; then
  FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // ""' 2>/dev/null)
fi

if [ -z "$FILE_PATH" ] || [ "$FILE_PATH" = "null" ]; then
  echo '{"continue": true}'
  exit 0
fi

# Protected paths
PROTECTED_PATTERNS=(
  ".claude/skills/"
  ".claude/agents/"
)

# Check if file is in a protected path
IS_PROTECTED=false
for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if echo "$FILE_PATH" | grep -q "$pattern"; then
    IS_PROTECTED=true
    break
  fi
done

# If file exists and is protected, warn
if [ "$IS_PROTECTED" = true ] && [ -f "$FILE_PATH" ]; then
  echo "{\"continue\": true, \"message\": \"⚠️ WRITE-GUARD: 보호 대상 파일입니다: $FILE_PATH\\n기존 내용이 덮어씌워질 수 있습니다. frontmatter model 필드만 수정하는 경우가 아니라면 주의하세요.\"}"
  exit 0
fi

# For any existing file, soft warning
if [ -f "$FILE_PATH" ]; then
  echo "{\"continue\": true, \"message\": \"📝 write-guard: 기존 파일 수정 감지 — $FILE_PATH\"}"
  exit 0
fi

echo '{"continue": true}'
exit 0
