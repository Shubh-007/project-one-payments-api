---
name: Settlement Guard
description: Use when changing files under src/settlement. Enforces settlement-specific safety checks.
paths: "src/settlement/**"
---
 
# Settlement Guard
 
Before editing settlement code:
1. Identify settlement window, region, and monetary impact.
2. Check whether the change affects T+1/T+2 behavior.
3. Add or update tests for each affected region.
4. Explain rollback risk.
5. Do not touch src/legacy without an AUD ticket.
 
Return a settlement impact note before proposing code edits.
