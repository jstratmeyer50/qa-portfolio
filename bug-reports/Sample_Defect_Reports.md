# Bug Report Template & Examples

**Report Date:** 2024-06-20  
**Reported By:** Senior QA Analyst  
**System:** Project Management Platform

---

## BUG-047: Session Timeout Not Firing Consistently

**Severity:** HIGH  
**Priority:** P1 (blocking)  
**Status:** Under Investigation  
**Assigned To:** Backend Team Lead

---

### Summary

Users remain authenticated beyond the 30-minute session timeout threshold. Timeout is supposed to trigger after 30 minutes of inactivity, but it fires inconsistently or not at all. This can result in unauthorized access if a user leaves their device unattended.

**Security Impact:** ⚠️ MEDIUM — Could allow unauthorized access to unattended sessions on shared devices.

---

### Environment

| Field | Value |
|---|---|
| **Environment** | QA Staging (prod-like) |
| **OS/Browser** | macOS Ventura, Chrome 123 |
| **Date Found** | 2024-06-15 |
| **Reproducibility** | Intermittent (60% of attempts) |
| **Build/Version** | v2.3.1-beta |

---

### Steps to Reproduce

1. Log in with valid credentials (test.user@example.com / ValidPass123!)
2. Dashboard loads; user authenticated
3. Close all browser tabs; do NOT click logout
4. Wait exactly 30 minutes without any user action
5. Return to browser; open new tab and navigate to app URL
6. **Expected:** Redirected to login page (session expired)
7. **Actual:** Dashboard loads; user still authenticated ❌

### Detailed Reproduction

**Test 1 (Successful timeout — 20% of runs):**
```
14:00 - Login successful
14:30 - Inactivity threshold reached
14:30 - Attempt to access dashboard
14:30 - Redirected to login page ✓ (timeout worked)
```

**Test 2 (Failed timeout — 80% of runs):**
```
14:00 - Login successful
14:30 - Inactivity threshold reached
14:30 - Attempt to access dashboard
14:30 - Dashboard loads; still authenticated ❌ (timeout failed)
```

---

### Actual Behavior

- User session persists beyond 30-minute timeout
- No logout/redirect occurs
- Session remains valid for subsequent API requests
- No error message or warning shown to user

### Expected Behavior

- After 30 minutes of inactivity, session should expire
- User navigating to app should be redirected to login page
- API requests with expired token should return 401 Unauthorized
- Session data should be cleared from backend database

---

### Root Cause Analysis (Pending)

**Hypothesis 1:** Background API calls refreshing session timer
- App makes background calls (polling, sync) that reset the inactivity timer
- Investigation: Check network logs for unexpected API calls during "inactivity"

**Hypothesis 2:** Session timeout logic has race condition
- Multiple processes checking/updating session state simultaneously
- Investigation: Database lock contention or async/await timing issues

**Hypothesis 3:** Client-side session manager not honoring server-side expiration
- Server marks session as expired, but client doesn't check until API error
- Investigation: Review client token refresh logic

---

### Attachments

**Network Logs (Charles Proxy capture):** 
```
[14:00:05] POST /api/auth/login → 200 OK
[14:00:10] session_id=abc123def456 (set in cookies)
[14:15:00] GET /api/dashboard → 200 OK (unexpected API call during "inactivity")
[14:30:00] Attempted logout request (never sent)
```

**Database Query Results:**
```sql
-- Session table at 14:30
SELECT * FROM sessions WHERE user_id=123;
-- Result: session still exists; expires_at is in future (incorrect)
```

**Browser Console Errors:**
```
[No errors visible in console during timeout period]
```

---

### Impact Assessment

**Affected Users:** All users  
**Frequency:** Intermittent (60–80% of cases)  
**User Impact:** 
- Security risk on shared devices
- Potential data exposure if device left unattended
- User may not realize they're still logged in

**Business Impact:**
- Regulatory compliance risk (SOC2, GDPR)
- Potential customer escalation if sensitive data accessed
- Must be fixed before release

---

### Workaround

**For QA:** Log out manually instead of relying on timeout.  
**For Users:** No workaround; security vulnerability requires fix.

---

### Questions for Developer

1. Are background sync/polling calls updating the session timestamp?
2. Does the token refresh logic check server-side expiration?
3. Are there any race conditions in the session manager?
4. Is the session timeout configured correctly in both client and server?

---

### Acceptance Criteria for Fix

- [ ] Session expires after exactly 30 minutes of inactivity (no background calls)
- [ ] User redirected to login after timeout (100% reproducible)
- [ ] API requests with expired token return 401
- [ ] No race conditions in session refresh logic
- [ ] QA can reproduce 10 consecutive timeouts without failure
- [ ] Load test shows timeout works consistently under load

---

### Related Issues

- TC-AUTH-006: Session timeout after inactivity (flaky test)
- TC-BUG-042: API token refresh not working (possible related issue)

---

### Sign-Off

| Role | Name | Date | Sign-Off |
|---|---|---|---|
| QA Analyst | Jesse Stratmeyer | 2024-06-15 | ✓ |
| Dev Lead | [To Be Assigned] | — | — |
| Product Manager | [Optional] | — | — |

---

---

## BUG-089: Cart Offline Sync Fails When App Backgrounded

**Severity:** MEDIUM  
**Priority:** P2 (deferred to 1.1)  
**Status:** Confirmed  
**Assigned To:** Mobile Team Lead

---

### Summary

When a user modifies their shopping cart while offline and then re-enables network connectivity, the cart changes fail to sync to the server if the app is backgrounded during the sync attempt. This results in the local cart being out of sync with the server.

**Impact:** User's cart changes lost; must re-add items to cart.

---

### Environment

| Field | Value |
|---|---|
| **Platform** | iOS & Android |
| **OS Version** | iOS 17.1, Android 14 |
| **Devices** | iPhone 14 Pro, Pixel 7 |
| **Build** | v1.0.5 |
| **Date Found** | 2024-06-18 |
| **Reproducibility** | 100% (with specific steps) |

---

### Steps to Reproduce

1. Open app; add item to cart (Running Shoes, qty 1)
2. Enable Airplane Mode (go offline)
3. Update quantity: qty 1 → qty 3
4. Verify local cart shows qty 3 ✓
5. Disable Airplane Mode (go online)
6. **Immediately** background the app (tap home button or switch to another app)
7. Wait 5 seconds
8. Bring app back to foreground
9. **Expected:** Cart shows qty 3 and is synced to server
10. **Actual:** Cart shows qty 3 locally, but server still has qty 1 ❌

### Verification (Server-Side)

```sql
-- Check server-side cart
SELECT * FROM carts WHERE user_id=999;
-- Result: quantity = 1 (not synced to 3)
```

---

### Root Cause (Suspected)

Background sync job not completing before app backgrounded:
- App detects network reconnection → starts background sync
- User backgrounds app before sync completes
- iOS/Android suspends background task (after ~30 sec)
- Sync request never reaches server → local changes lost

---

### Workaround

Kill and reopen the app to force sync:
1. Close app completely
2. Wait 2 seconds
3. Reopen app
4. Cart syncs correctly on app launch

---

### Acceptance Criteria for Fix

- [ ] Cart syncs even if app backgrounded during reconnect
- [ ] Background sync completes within 30 seconds
- [ ] Conflict resolution: server-side cart takes precedence if mismatch
- [ ] User notification if sync fails (toast message on app reopen)
- [ ] Test with 10 consecutive offline→online transitions

---

---

## BUG-091: Checkout Page Exceeds 3-Second Load Target on LTE

**Severity:** MEDIUM  
**Priority:** P2 (performance, not blocking)  
**Status:** Confirmed  
**Assigned To:** Frontend Team

---

### Summary

The checkout page exceeds the 3-second load time target on LTE networks. Performance measured at ~3.2–3.4 seconds, which impacts user experience on slower mobile networks.

---

### Performance Metrics

| Network | LCP Time | FCP Time | TTI | Status |
|---|---|---|---|---|
| **4G** | 2.7s ✓ | 1.2s ✓ | 2.9s ✓ | PASS |
| **LTE (3.5G)** | 3.2s ❌ | 1.4s ✓ | 3.4s ❌ | FAIL |
| **3G** | 5.1s ❌ | 2.1s ❌ | 5.5s ❌ | FAIL |
| **WiFi** | 1.8s ✓ | 0.8s ✓ | 2.1s ✓ | PASS |

### LCP: Largest Contentful Paint; FCP: First Contentful Paint; TTI: Time to Interactive

---

### Bottlenecks (Lighthouse Analysis)

1. **Product thumbnail images (900ms)**
   - 3 images, 150KB each
   - Opportunity: WebP format (-30%), lazy-load below-fold images

2. **JavaScript bundle (650ms)**
   - Main app.js: 85KB minified
   - Opportunity: Code splitting, tree-shaking unused imports

3. **Third-party scripts (300ms)**
   - Google Analytics, tracking pixels
   - Opportunity: Async loading, defer non-critical

4. **API call to fetch order summary (250ms)**
   - Synchronous API call blocks rendering
   - Opportunity: Pre-fetch summary while user in cart view

---

### Root Cause

Images not optimized for mobile networks; large JavaScript bundle not split.

---

### Optimization Recommendations

**Quick Wins (1–2 hours):**
- Convert images to WebP format
- Lazy-load below-fold product images
- Defer non-critical third-party scripts

**Medium-term (1–2 sprints):**
- Split checkout JavaScript into separate bundle
- Pre-fetch order summary in previous step
- Implement service worker caching

**Performance Target:** <2.5s on LTE (achievable with above optimizations)

---

### Testing for Fix Verification

- [ ] Measure LCP on LTE: target <2.8s
- [ ] Measure FCP on LTE: target <1.5s
- [ ] Lighthouse score: target 85+
- [ ] Test on real devices with LTE throttling (not simulator)
- [ ] Monitor production with RUM (Real User Monitoring)

---

---

## Bug Report Summary

| Bug ID | Title | Severity | Status | Assigned |
|---|---|---|---|---|
| BUG-047 | Session timeout not firing | HIGH | Under Investigation | Backend |
| BUG-089 | Cart sync fails when backgrounded | MEDIUM | Confirmed | Mobile |
| BUG-091 | Checkout page slow on LTE | MEDIUM | Confirmed | Frontend |

**Total Open:** 3 bugs  
**Critical/Blocking:** 1 (BUG-047)  
**Deferred to 1.1:** 1 (BUG-089)  

---

## Bug Triage Guidelines

**Severity Levels:**
- **CRITICAL:** Product unusable, data loss, security breach → Fix immediately
- **HIGH:** Major functionality broken, workaround exists → Fix this sprint
- **MEDIUM:** Feature degraded, user impact moderate → Plan for next sprint
- **LOW:** Minor UX issue, cosmetic defect → Backlog or future sprint

**Priority Levels:**
- **P0:** Blocks release, security risk
- **P1:** High user impact, must fix this sprint
- **P2:** Medium impact, can defer to next sprint
- **P3:** Low priority, backlog

---

## How to Report a Bug

**Use this template for all defect reports:**

1. **Title:** One-line summary (BUG-###: Title)
2. **Severity/Priority:** Impact level
3. **Environment:** OS, browser, app version
4. **Steps to Reproduce:** Exact steps to recreate
5. **Expected vs. Actual:** What should happen vs. what happened
6. **Attachments:** Screenshots, logs, video recording
7. **Root Cause:** Suspected cause (if known)
8. **Acceptance Criteria:** What fix must accomplish

**Attach Evidence:**
- Screenshot/video of issue
- Network logs (if API-related)
- Console errors (DevTools screenshot)
- Database query results (if data issue)

**Helpful Resources:**
- [Test Plans](../test-plans/) — reference test scenario
- [Process Docs](../process-docs/04_Bug_Triage_Process.md) — triage guidelines
