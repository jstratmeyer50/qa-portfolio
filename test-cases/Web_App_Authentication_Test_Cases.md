# Test Case Suite: Web Application — User Authentication & Login

**Suite ID:** TC-AUTH-001  
**Application:** Project Management SaaS Platform  
**Module:** Authentication & Session Management  
**Test Data:** Available in QA database  
**Automation Status:** Partially automated (happy path); manual (edge cases)  
**Last Updated:** 2024-06-15

---

## Test Case Overview

| Test Case ID | Title | Complexity | Automation | Status |
|---|---|---|---|---|
| TC-AUTH-001 | Valid login with email/password | Low | ✅ | ✓ Pass |
| TC-AUTH-002 | Invalid password → error message | Low | ✅ | ✓ Pass |
| TC-AUTH-003 | Non-existent user → graceful error | Low | ✅ | ✓ Pass |
| TC-AUTH-004 | Password field is masked | Low | ❌ | ✓ Pass |
| TC-AUTH-005 | Remember me → persistent login | Medium | ❌ | ✓ Pass |
| TC-AUTH-006 | Session timeout after inactivity | Medium | ❌ | ⚠ Flaky |
| TC-AUTH-007 | Concurrent login — multiple devices | Medium | ❌ | ✓ Pass |
| TC-AUTH-008 | Account lockout after failed attempts | Medium | ✅ | ✓ Pass |
| TC-AUTH-009 | Forgot password flow | Medium | ✅ | ✓ Pass |
| TC-AUTH-010 | Social login: Google OAuth | High | ❌ | ✓ Pass |
| TC-AUTH-011 | SAML SSO (enterprise) | High | ❌ | ✓ Pass |
| TC-AUTH-012 | MFA — email code validation | High | ❌ | ⚠ Flaky |
| TC-AUTH-013 | Token refresh on API requests | High | ✅ | ✓ Pass |
| TC-AUTH-014 | CSRF protection — form token validation | Medium | ✅ | ✓ Pass |
| TC-AUTH-015 | Logout — token revocation | Low | ✅ | ✓ Pass |

---

## Detailed Test Cases

---

### TC-AUTH-001: Valid Login with Email/Password

**Objective:** Verify a user with valid credentials can successfully log in and access the application.

**Preconditions:**
- User exists in system (email: test.user@example.com, password: ValidPass123!)
- User is not locked out
- Browser cookies/cache are cleared
- User is on the login page

**Test Steps:**

| # | Step | Expected Result | Status |
|---|---|---|---|
| 1 | Enter email address: `test.user@example.com` in Email field | Field accepts input; no error shown | ✓ |
| 2 | Enter password: `ValidPass123!` in Password field | Field accepts input; dots/asterisks mask password | ✓ |
| 3 | Click "Sign In" button | Button becomes disabled; loading spinner appears | ✓ |
| 4 | Wait for API response (max 5 seconds) | No error message; page redirects to Dashboard | ✓ |
| 5 | Verify dashboard loads with user content | User name displays in top-right; projects list shows | ✓ |
| 6 | Verify session cookie created | `session_id` cookie present in browser; `HttpOnly` flag set | ✓ |
| 7 | Refresh page | Dashboard persists; no login required | ✓ |

**Expected Result:** ✅ User successfully logged in; dashboard accessible; session established.

**Actual Result:** ✅ Passed

**Browser/OS:** Chrome 123 / macOS Ventura  
**Automation Script:** `tests/auth/login_valid_credentials.spec.js`  
**Notes:** Test runs in CI/CD pipeline; execution time ~2 seconds.

---

### TC-AUTH-002: Invalid Password → Error Message

**Objective:** Verify the system displays an appropriate error when an incorrect password is provided.

**Preconditions:**
- User exists in system
- Valid email provided
- Incorrect password will be entered

**Test Steps:**

| # | Step | Expected Result | Status |
|---|---|---|---|
| 1 | Enter valid email: `test.user@example.com` | Email field accepts input | ✓ |
| 2 | Enter incorrect password: `WrongPass123!` | Password field accepts input; masked | ✓ |
| 3 | Click "Sign In" button | Loading spinner appears | ✓ |
| 4 | Wait for response | Error message appears: "Invalid email or password" | ✓ |
| 5 | Verify error styling | Error text in red; icon indicating error shown | ✓ |
| 6 | Verify user not logged in | Dashboard not accessible; login form still visible | ✓ |
| 7 | Attempt login again with correct password | Subsequent login succeeds (no lockout yet) | ✓ |

**Expected Result:** ✅ Error message displayed; user remains on login page; no session created.

**Actual Result:** ✅ Passed

**Browser/OS:** Chrome 123 / macOS Ventura  
**Automation Script:** `tests/auth/login_invalid_password.spec.js`  
**Notes:** Generic error message used to prevent user enumeration (security best practice).

---

### TC-AUTH-003: Non-Existent User → Graceful Error

**Objective:** Verify the system handles attempts to log in with a non-existent email gracefully.

**Preconditions:**
- Email does not exist in system: `nonexistent@example.com`
- Login form is displayed

**Test Steps:**

| # | Step | Expected Result | Status |
|---|---|---|---|
| 1 | Enter non-existent email: `nonexistent@example.com` | Email field accepts input | ✓ |
| 2 | Enter any password: `SomePassword123!` | Password field accepts input; masked | ✓ |
| 3 | Click "Sign In" button | Loading spinner appears | ✓ |
| 4 | Wait for response | Same error message as TC-002: "Invalid email or password" | ✓ |
| 5 | Verify no account created | System does not create account on failed login | ✓ |
| 6 | Verify not logged in | Dashboard not accessible | ✓ |

**Expected Result:** ✅ Generic error displayed (same as invalid password); no information leakage about whether email exists.

**Actual Result:** ✅ Passed

**Browser/OS:** Firefox 125 / Windows 11  
**Automation Script:** `tests/auth/login_nonexistent_user.spec.js`  
**Notes:** This prevents user enumeration attacks.

---

### TC-AUTH-004: Password Field is Masked

**Objective:** Verify the password input field masks characters (shows dots/asterisks instead of plain text).

**Preconditions:**
- Login page is displayed
- JavaScript is enabled

**Test Steps:**

| # | Step | Expected Result | Status |
|---|---|---|---|
| 1 | Locate the Password input field | Field is visible with placeholder text "Password" | ✓ |
| 2 | Click into the Password field | Field is focused; cursor visible | ✓ |
| 3 | Type password: `SecurePass123!` | Characters are masked as dots (•) or asterisks (*); not visible as plain text | ✓ |
| 4 | Verify field HTML attribute | Input `type="password"` confirmed in DevTools | ✓ |
| 5 | Inspect browser autocomplete | Password managers (1Password, LastPass) recognize field | ✓ |
| 6 | Verify on mobile | Password field masked on iOS Safari and Android Chrome | ✓ |

**Expected Result:** ✅ Password field masks all characters; no plain text visible.

**Actual Result:** ✅ Passed

**Browser/OS:** Chrome 123 / macOS; Safari 17 / iOS 17  
**Manual Test:** Yes — requires visual inspection  
**Notes:** Security measure to prevent shoulder-surfing attacks.

---

### TC-AUTH-005: Remember Me → Persistent Login

**Objective:** Verify the "Remember me" checkbox enables persistent login across browser sessions.

**Preconditions:**
- User not previously logged in
- "Remember me" checkbox is visible on login form

**Test Steps:**

| # | Step | Expected Result | Status |
|---|---|---|---|
| 1 | Enter valid credentials: `test.user@example.com` / `ValidPass123!` | Fields populated | ✓ |
| 2 | Check "Remember me" checkbox | Checkbox is checked; visual indicator shows | ✓ |
| 3 | Click "Sign In" button | Login succeeds; dashboard displayed | ✓ |
| 4 | Verify cookies set | Both `session_id` and `remember_token` cookies present | ✓ |
| 5 | Check cookie expiration | `session_id` expires in 1 hour; `remember_token` expires in 30 days | ✓ |
| 6 | Close browser completely | Browser and all tabs closed | ✓ |
| 7 | Reopen browser and navigate to app | Dashboard loads without login prompt; user authenticated | ✓ |
| 8 | Verify still logged in after 7 days | User can log in again after 7 days (token valid for 30 days) | ⚠ |

**Expected Result:** ✅ User remains logged in across browser sessions for up to 30 days.

**Actual Result:** ⚠ Mostly passes; TC-AUTH-008 (Account lockout) takes precedence for security.

**Browser/OS:** Chrome 123 / macOS Ventura  
**Manual Test:** Yes — requires waiting and browser close/reopen  
**Notes:** Session tokens refresh automatically if within 30-day window. Can be disabled via Settings > Security > "End all sessions."

---

### TC-AUTH-006: Session Timeout After Inactivity

**Objective:** Verify that user sessions automatically expire after a defined period of inactivity.

**Preconditions:**
- User is logged in
- Session timeout is set to 30 minutes in system configuration
- No API calls made to refresh session

**Test Steps:**

| # | Step | Expected Result | Status |
|---|---|---|---|
| 1 | Log in successfully | Dashboard displayed; user authenticated | ✓ |
| 2 | Verify session created | Session timestamp recorded in backend | ✓ |
| 3 | Wait 25 minutes (no user action) | User can still interact with app (session valid) | ⚠ |
| 4 | Wait additional 10 minutes (total 35 min inactivity) | Session expired; user redirected to login page | ⚠ |
| 5 | Attempt to access dashboard directly via URL | Redirected to login page | ⚠ |
| 6 | Log in again | Session reestablished; no data loss | ⚠ |
| 7 | Make API call after 30 min inactivity | API returns 401 Unauthorized; session refreshed and retried | ⚠ |

**Expected Result:** ✅ Session expires after 30 minutes of inactivity; user must re-authenticate.

**Actual Result:** ⚠ Flaky — sometimes timeout doesn't trigger; sometimes user is redirected unexpectedly. Issue: TC-BUG-047 (Session timeout not firing consistently).

**Browser/OS:** Chrome 123 / macOS Ventura  
**Manual Test:** Yes — requires 30+ minutes of waiting  
**Notes:** Timing is inconsistent due to background API calls refreshing session. Consider monitoring in QA environment before next release.

---

### TC-AUTH-008: Account Lockout After Failed Attempts

**Objective:** Verify that an account is locked after N consecutive failed login attempts (brute force protection).

**Preconditions:**
- User account exists
- Account is not currently locked
- System is configured to lock after 5 failed attempts

**Test Steps:**

| # | Step | Expected Result | Status |
|---|---|---|---|
| 1 | Attempt login with wrong password (attempt 1) | Error shown; user not locked out | ✓ |
| 2 | Attempt login with wrong password (attempts 2–4) | Error shown each time; no lockout | ✓ |
| 3 | Attempt login with wrong password (attempt 5) | Error shown; account is now locked | ✓ |
| 4 | Attempt login with correct password | Error message: "Account temporarily locked. Try again in 15 minutes." | ✓ |
| 5 | Verify lockout in backend | `account_locked` flag set in database; `locked_until` timestamp = now + 15 min | ✓ |
| 6 | Attempt login before 15 minutes elapse | Still locked; error shown | ✓ |
| 7 | Wait 15 minutes; attempt login with correct password | Account unlocked; login succeeds | ✓ |
| 8 | Verify lockout cleared | `account_locked` flag removed; `failed_attempts` counter reset to 0 | ✓ |

**Expected Result:** ✅ Account locked after 5 failed attempts; unlocked after 15 minutes.

**Actual Result:** ✅ Passed

**Browser/OS:** Chrome 123 / macOS Ventura  
**Automation Script:** `tests/auth/account_lockout.spec.js`  
**Notes:** Test uses system clock manipulation to skip 15-minute wait.

---

### TC-AUTH-009: Forgot Password Flow

**Objective:** Verify users can reset their password using the "Forgot Password" flow.

**Preconditions:**
- User account exists: `test.user@example.com`
- Email delivery is functional
- Reset token expiration: 1 hour

**Test Steps:**

| # | Step | Expected Result | Status |
|---|---|---|---|
| 1 | On login page, click "Forgot Password?" link | Redirected to password reset page | ✓ |
| 2 | Enter email: `test.user@example.com` | Email field populated | ✓ |
| 3 | Click "Send Reset Link" button | Success message: "Check your email for reset link" | ✓ |
| 4 | Verify email sent | Email arrives in test inbox within 1 minute | ✓ |
| 5 | Verify email content | Subject: "Reset Your Password"; contains unique reset link; no plain-text token | ✓ |
| 6 | Click reset link in email | Redirected to password reset form | ✓ |
| 7 | Enter new password: `NewSecurePass456!` | Field accepts input; password strength indicator shows | ✓ |
| 8 | Confirm password: `NewSecurePass456!` | Field accepts input | ✓ |
| 9 | Click "Reset Password" button | Success message shown; redirected to login page | ✓ |
| 10 | Attempt login with old password | Login fails (old password no longer valid) | ✓ |
| 11 | Attempt login with new password | Login succeeds; session established | ✓ |
| 12 | Try reset link again (same link) | Error: "Reset link has expired or been used" (one-time use) | ✓ |

**Expected Result:** ✅ User can reset password using email link; old password invalidated; link is one-time use.

**Actual Result:** ✅ Passed

**Browser/OS:** Chrome 123 / macOS Ventura  
**Automation Script:** `tests/auth/forgot_password.spec.js` (uses email API mock)  
**Notes:** Automated test uses mock email provider; manual verification of real email recommended before release.

---

### TC-AUTH-010: Social Login — Google OAuth

**Objective:** Verify users can log in using Google OAuth and that account linking works correctly.

**Preconditions:**
- Google OAuth application configured
- OAuth credentials in QA environment
- Test Google account available: `qa.test@gmail.com`

**Test Steps:**

| # | Step | Expected Result | Status |
|---|---|---|---|
| 1 | On login page, click "Sign in with Google" button | Redirected to Google OAuth consent screen | ✓ |
| 2 | Verify OAuth request parameters | `client_id`, `redirect_uri`, `scope` (email, profile) correct | ✓ |
| 3 | Select test Google account: `qa.test@gmail.com` | Google account selected | ✓ |
| 4 | Grant permission | Redirected back to app with OAuth code | ✓ |
| 5 | Verify authorization code exchanged for token | Backend successfully obtains `id_token` and `refresh_token` | ✓ |
| 6 | Verify first-time user flow | New account created with Google email and name | ✓ |
| 7 | Verify dashboard loads | User logged in; profile shows Google account info | ✓ |
| 8 | Log out and log back in | Login with "Sign in with Google" again; same account recognized | ✓ |
| 9 | Verify email is not changed | Email still linked to Google account; cannot be modified | ✓ |
| 10 | Verify scope permissions | Minimal scopes requested (email, profile only); no calendar/drive access requested | ✓ |

**Expected Result:** ✅ Google OAuth login works; account created/linked correctly; session established.

**Actual Result:** ✅ Passed

**Browser/OS:** Chrome 123 / macOS Ventura  
**Manual Test:** Yes — requires real Google account  
**Notes:** Automated tests use OAuth mock; manual verification with real Google account recommended. Scope audit passed (privacy compliant).

---

### TC-AUTH-013: Token Refresh on API Requests

**Objective:** Verify that expired access tokens are automatically refreshed on subsequent API requests.

**Preconditions:**
- User is logged in with valid session
- Access token will expire; refresh token is valid
- API endpoint configured to check token validity

**Test Steps:**

| # | Step | Expected Result | Status |
|---|---|---|---|
| 1 | Log in successfully | Access token issued (5-minute expiration) | ✓ |
| 2 | Verify token in memory | Token stored in app state/localStorage | ✓ |
| 3 | Wait 5+ minutes (simulate token expiration) | No automatic logout; token remains in app | ✓ |
| 4 | Make API request (e.g., fetch projects list) | API receives expired token | ✓ |
| 5 | API returns 401 Unauthorized | App detects 401 response | ✓ |
| 6 | App calls refresh token endpoint | Sends refresh token; backend validates | ✓ |
| 7 | Backend issues new access token | Returns new token with 5-minute expiration | ✓ |
| 8 | App stores new token and retries original request | Request succeeds with new token | ✓ |
| 9 | Verify projects list returned | API response 200 OK; data displayed to user | ✓ |
| 10 | Verify user experience seamless | No logout/re-login required; no error message shown to user | ✓ |

**Expected Result:** ✅ Access token automatically refreshed; original request retried; transparent to user.

**Actual Result:** ✅ Passed

**Browser/OS:** Chrome 123 / macOS Ventura  
**Automation Script:** `tests/auth/token_refresh.spec.js` (mocks API responses)  
**Notes:** Refresh token is longer-lived (30 days); if refresh fails, user logged out and redirected to login.

---

### TC-AUTH-014: CSRF Protection — Form Token Validation

**Objective:** Verify that forms are protected against Cross-Site Request Forgery (CSRF) attacks using token validation.

**Preconditions:**
- User is logged in
- CSRF token middleware is enabled
- User-Agent matches session

**Test Steps:**

| # | Step | Expected Result | Status |
|---|---|---|---|
| 1 | Load a form (e.g., Create Project form) | Form contains hidden CSRF token field: `<input type="hidden" name="_csrf_token" value="...">` | ✓ |
| 2 | Verify CSRF token in HTML | Token is unique per form; not exposed in URL | ✓ |
| 3 | Submit form with valid CSRF token | Request succeeds (200 OK) | ✓ |
| 4 | Attempt POST request without CSRF token | Request fails with 403 Forbidden | ✓ |
| 5 | Attempt POST request with invalid CSRF token | Request fails with 403 Forbidden | ✓ |
| 6 | Attempt POST request with token from different session | Request fails with 403 Forbidden | ✓ |
| 7 | Simulate CSRF attack from external site | External form cannot submit to app (different origin blocked) | ✓ |
| 8 | Verify SameSite cookie flag | Session cookie has `SameSite=Strict` or `SameSite=Lax` | ✓ |

**Expected Result:** ✅ CSRF protection enforced; invalid/missing tokens rejected; cross-origin requests blocked.

**Actual Result:** ✅ Passed

**Browser/OS:** Chrome 123 / macOS Ventura  
**Automation Script:** `tests/security/csrf_protection.spec.js`  
**Notes:** CSRF tokens regenerated on every login for maximum security.

---

### TC-AUTH-015: Logout — Token Revocation

**Objective:** Verify that logging out properly revokes the session and prevents further access.

**Preconditions:**
- User is logged in
- Session token exists in database

**Test Steps:**

| # | Step | Expected Result | Status |
|---|---|---|---|
| 1 | Click "Logout" button in header | Logout request sent to backend; UI shows loading state | ✓ |
| 2 | Backend revokes session token | Token marked as revoked in database | ✓ |
| 3 | User redirected to login page | Dashboard no longer accessible; login form displayed | ✓ |
| 4 | Verify session cookie cleared | Session cookie removed from browser (or expires immediately) | ✓ |
| 5 | Attempt to access dashboard via direct URL | Redirected to login page | ✓ |
| 6 | Attempt API request with old token | API returns 401 Unauthorized (token is revoked) | ✓ |
| 7 | Verify "Remember me" token also invalidated | Refresh browser; login required (30-day token cleared) | ✓ |
| 8 | Log in again with same account | New session established; old session completely forgotten | ✓ |

**Expected Result:** ✅ Logout revokes session; user must re-authenticate; old tokens rejected.

**Actual Result:** ✅ Passed

**Browser/OS:** Chrome 123 / macOS Ventura  
**Automation Script:** `tests/auth/logout.spec.js`  
**Notes:** Session revocation is immediate (no delay). All devices logged out if applicable.

---

## Summary

**Total Test Cases:** 15  
**Passed:** 13 ✓  
**Flaky:** 2 ⚠ (TC-006, TC-012 — under investigation)  
**Failed:** 0  

**Pass Rate:** 86.7% (consistent pass) + 13.3% (flaky)  
**Automation Coverage:** 60% (9 of 15 automated)  
**Manual Testing Required:** Edge cases, MFA, SSO, visual inspection

**Known Issues:**
- **TC-AUTH-006** — Session timeout not consistently firing (backend timer issue)
- **TC-AUTH-012** — MFA email delivery occasionally delayed (investigate email provider)

**Recommendation:** All test cases are production-ready. Address flaky tests before next release.

---

## Appendix: Test Data

| Email | Password | Status | 2FA | Role |
|---|---|---|---|---|
| test.user@example.com | ValidPass123! | Active | Email | User |
| test.admin@example.com | AdminPass123! | Active | TOTP | Admin |
| test.locked@example.com | LockedPass123! | Locked | None | User |
| test.inactive@example.com | InactivePass123! | Inactive | None | User |

---

## Appendix: Browser/Device Coverage

- ✅ Chrome 123 / Windows 11
- ✅ Chrome 123 / macOS Ventura
- ✅ Safari 17 / macOS Ventura
- ✅ Safari 17 / iOS 17
- ✅ Chrome / Android 14
- ✅ Firefox 125 / Windows 11
- ✅ Edge 123 / Windows 11

---

## Related Test Plans

- [Critical Regression Test Plan](../test-plans/03_Critical_Regression_Test_Plan.md) — Authentication system overhaul testing
- [End-to-End User Journey Test Plan](../test-plans/05_End_to_End_User_Journey_Test_Plan.md) — Login through purchase
