#!/bin/bash
# context-monitor.sh — 컨텍스트 사용량 추적 (PostToolUse hook)
# 장시간 작업 시 컨텍스트 한도 접근 경고

INPUT=$(cat)

# Track invocation count in a state file
STATE_DIR="${HOME}/.claude"
STATE_FILE="${STATE_DIR}/context-monitor-state.json"

mkdir -p "$STATE_DIR"

# Read current count
COUNT=0
if [ -f "$STATE_FILE" ]; then
  if command -v jq &> /dev/null; then
    COUNT=$(jq -r '.tool_call_count // 0' "$STATE_FILE" 2>/dev/null)
    [ "$COUNT" = "null" ] && COUNT=0
  fi
fi

# Increment
COUNT=$((COUNT + 1))

# Write state
cat > "$STATE_FILE" << EOF
{
  "tool_call_count": $COUNT,
  "last_updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "session_start": "$(jq -r '.session_start // empty' "$STATE_FILE" 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

# Warn at thresholds (proxy for context usage — tool calls correlate with token usage)
if [ "$COUNT" -eq 100 ]; then
  echo '{"continue": true, "message": "📊 context-monitor: 도구 호출 100회 도달. 컨텍스트 사용량이 높아지고 있습니다. 필요시 중간 요약을 고려하세요."}'
elif [ "$COUNT" -eq 150 ]; then
  echo '{"continue": true, "message": "⚠️ context-monitor: 도구 호출 150회 도달 — 컨텍스트 한도 80% 추정. 작업 요약 후 새 세션 시작을 권장합니다."}'
elif [ "$COUNT" -eq 200 ]; then
  echo '{"continue": true, "message": "🔴 context-monitor: 도구 호출 200회 초과! 즉시 현재 작업 상태를 저장하고 새 세션을 시작하세요."}'
else
  echo '{"continue": true}'
fi
exit 0
