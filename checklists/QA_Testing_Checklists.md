# QA Checklists & Testing Artifacts

This directory contains practical checklists used throughout the testing lifecycle. Each checklist can be copied and customized for specific releases or features.

---

## 1. Smoke Testing Checklist

**Purpose:** Quick validation after each build/deploy to ensure critical functionality works.  
**Duration:** 15–30 minutes  
**Frequency:** After every build in CI/CD; before regression testing

---

### Smoke Test Checklist — Project Management Platform (v2.3.1)

**Date:** 2024-06-20  
**Tester:** QA Team  
**Build:** v2.3.1-beta  
**Environment:** QA Staging

#### Core Functionality

| # | Functionality | Expected | Status | Notes |
|---|---|---|---|---|
| 1 | **User Authentication** |  |  |  |
| | Login with valid credentials | Dashboard loads | ✅ | Took 2.1 sec |
| | Logout | Redirected to login page | ✅ | Session cleared |
| | Invalid password | Error message shown | ✅ | Generic error (good security) |
| 2 | **Dashboard** |  |  |  |
| | Dashboard loads | Projects list visible | ✅ | 3 projects shown |
| | No console errors | No red errors in DevTools | ✅ | Clean console |
| | Page responsive | Mobile/tablet view works | ✅ | Tested on iPhone simulator |
| 3 | **Project CRUD** |  |  |  |
| | Create new project | Project appears in list | ✅ | Name: "Test Project" |
| | Edit project details | Changes saved | ✅ | Updated description |
| | Delete project | Removed from list | ✅ | Confirmation shown |
| 4 | **Task Management** |  |  |  |
| | Create task | Task added to project | ✅ | Title: "Test Task" |
| | Update task status | Status changes (todo → in progress → done) | ✅ | Visual indicator updates |
| | Assign task to user | Assignment shows in task detail | ✅ | Assigned to: Test User |
| 5 | **Notifications** |  |  |  |
| | Notification bell icon | Displays count of unread | ✅ | Shows "2" unread |
| | Click notification | Opens correct item | ✅ | Clicked task notification → navigated to task |
| 6 | **API Endpoints** |  |  |  |
| | GET /api/projects | Returns JSON, 200 OK | ✅ | 3 projects returned |
| | POST /api/projects | Creates new project, 201 Created | ✅ | Project ID: 456 |
| | GET /api/tasks?project_id=123 | Returns tasks, 200 OK | ✅ | 5 tasks returned |

#### Performance Checks

| # | Metric | Target | Actual | Status |
|---|---|---|---|---|
| 1 | Dashboard load time | <2 sec | 1.8 sec | ✅ |
| 2 | Task list rendering (100 items) | <1 sec | 0.9 sec | ✅ |
| 3 | Create project time-to-save | <3 sec | 1.2 sec | ✅ |

#### Integration Points

| # | Integration | Status | Notes |
|---|---|---|---|
| 1 | Email delivery (notifications) | ✅ | Notification email received |
| 2 | OAuth login (Google) | ✅ | Logged in with Google account |
| 3 | Slack integration (task notifications) | ✅ | Slack message posted on task creation |

#### Browser/Device Coverage

| # | Browser/Device | Status | Notes |
|---|---|---|---|
| 1 | Chrome (macOS) | ✅ | All features working |
| 2 | Safari (macOS) | ✅ | All features working |
| 3 | Firefox (Windows) | ✅ | All features working |
| 4 | Safari (iOS) | ✅ | Mobile responsive, touch works |
| 5 | Chrome (Android) | ✅ | Mobile responsive, touch works |

#### Regression Checks

| # | Feature | Previous Version | Current Version | Status |
|---|---|---|---|---|
| 1 | Create project | ✅ | ✅ | No regression |
| 2 | Edit task | ✅ | ✅ | No regression |
| 3 | Delete project (with confirmation) | ✅ | ✅ | No regression |
| 4 | Project search/filter | ✅ | ✅ | No regression |

#### Issues Found

| # | Issue | Severity | Assigned | Status |
|---|---|---|---|---|
| 1 | "Create task" button slightly off-center in mobile view | LOW | Frontend | Assigned to Sprint 24 |

#### Sign-Off

- **Tester:** Sarah Chen, Senior QA Analyst
- **Date:** 2024-06-20
- **Time:** 14:30–15:00 (30 minutes)
- **Result:** ✅ **PASSED** — Build approved for regression testing

---

---

## 2. Regression Testing Checklist

**Purpose:** Verify that new changes don't break existing functionality.  
**Duration:** 4–8 hours (depends on scope)  
**Frequency:** Before each release; after major feature additions

---

### Regression Test Checklist — Payment Integration Release (v2.3.1)

**Date:** 2024-06-20  
**Scope:** Payment system changes; authentication unchanged  
**Test Environment:** QA Staging  
**Build:** v2.3.1  

#### Feature: User Authentication (No Changes Expected)

| # | Test Case | Expected | Status | Notes |
|---|---|---|---|---|
| 1 | TC-AUTH-001: Valid login | Login succeeds | ✅ | Pass |
| 2 | TC-AUTH-002: Invalid password | Error shown | ✅ | Pass |
| 3 | TC-AUTH-005: Remember me | Persistent login | ✅ | Pass |
| 4 | TC-AUTH-009: Forgot password | Password reset works | ✅ | Pass |
| 5 | TC-AUTH-010: Google OAuth | OAuth login works | ✅ | Pass |
| **Subtotal** | **5 test cases** | **5 passed** | **✅ 100%** | No regressions |

#### Feature: Dashboard & Project Management (No Changes Expected)

| # | Test Case | Expected | Status | Notes |
|---|---|---|---|---|
| 1 | Create project | Project created | ✅ | Pass |
| 2 | Edit project name | Name updated | ✅ | Pass |
| 3 | Delete project | Project removed | ✅ | Pass |
| 4 | View project tasks | Task list displays | ✅ | Pass |
| 5 | Search/filter projects | Filtered results shown | ✅ | Pass |
| **Subtotal** | **5 test cases** | **5 passed** | **✅ 100%** | No regressions |

#### Feature: Payment Processing (New Feature — Main Focus)

| # | Test Case | Expected | Status | Notes |
|---|---|---|---|---|
| 1 | TC-CART-109: Enter payment details | Payment form loads | ✅ | Pass |
| 2 | TC-CART-110: Complete purchase | Payment succeeds | ✅ | Pass |
| 3 | Refund processing | Refund successful | ✅ | Pass |
| 4 | Payment webhook | Order status updates | ✅ | Pass |
| 5 | Failed payment retry | Retry succeeds | ✅ | Pass |
| 6 | Idempotency: Duplicate payment | Single charge only | ✅ | Pass |
| 7 | Test card scenarios | All test cards work as expected | ✅ | Pass |
| **Subtotal** | **7 test cases** | **7 passed** | **✅ 100%** | All payment tests pass |

#### Cross-Browser Testing

| Browser | Version | OS | Status | Notes |
|---|---|---|---|---|
| Chrome | 123 | macOS Ventura | ✅ | All tests pass |
| Safari | 17 | macOS Ventura | ✅ | All tests pass |
| Firefox | 125 | Windows 11 | ✅ | All tests pass |
| Edge | 123 | Windows 11 | ✅ | All tests pass |
| Chrome | Latest | iOS 17.1 | ✅ | Mobile responsive |
| Safari | Latest | iOS 17.1 | ✅ | Mobile responsive |

#### Mobile Testing

| Device | OS | Status | Notes |
|---|---|---|---|
| iPhone 14 Pro (simulator) | iOS 17.1 | ✅ | Responsive, touch works |
| iPhone SE (simulator) | iOS 17.1 | ✅ | Small screen compatible |
| Pixel 7 (emulator) | Android 14 | ✅ | Responsive, touch works |
| Galaxy Tab (emulator) | Android 14 | ✅ | Tablet layout correct |

#### API Testing

| Endpoint | Method | Expected | Actual | Status |
|---|---|---|---|---|
| `/api/payments/create` | POST | 200 OK | 200 OK | ✅ |
| `/api/payments/status/:id` | GET | 200 OK | 200 OK | ✅ |
| `/api/payments/refund` | POST | 200 OK | 200 OK | ✅ |
| `/api/webhooks/stripe` | POST | 200 OK | 200 OK | ✅ |

#### Data Integrity Checks

| Check | Expected | Status | Notes |
|---|---|---|---|
| Order created in database | Order exists | ✅ | Order ID: 12345 |
| Order total correct | Total = $99.99 | ✅ | Calculated correctly |
| Payment recorded | Stripe charge ID in DB | ✅ | stripe_charge_id: ch_1234567890 |
| Refund recorded | Refund entry in DB | ✅ | Refund ID: re_1234567890 |
| Email sent | Confirmation in inbox | ✅ | Received within 1 minute |

#### Performance Metrics

| Metric | Target | Actual | Status |
|---|---|---|---|
| Checkout page load | <3 sec | 2.8 sec | ✅ |
| Payment processing | <10 sec | 4.2 sec | ✅ |
| Order confirmation page | <2 sec | 1.9 sec | ✅ |

#### Compatibility Matrix

| Feature | v2.2.0 | v2.3.1 | Regression? |
|---|---|---|---|
| Login | ✅ | ✅ | No |
| Projects | ✅ | ✅ | No |
| Tasks | ✅ | ✅ | No |
| **Payments** | ❌ N/A | ✅ | N/A (new feature) |

#### Issues Found During Regression

| # | Issue | Severity | Status | Bug ID |
|---|---|---|---|---|
| None | — | — | — | — |

#### Sign-Off

- **QA Lead:** Jesse Stratmeyer
- **Date:** 2024-06-20
- **Duration:** 6 hours
- **Test Cases Executed:** 22
- **Pass Rate:** 100% ✅
- **Approval:** ✅ **REGRESSION TESTING PASSED** — Build approved for UAT

---

---

## 3. Release Readiness Checklist

**Purpose:** Final gate before production release.  
**Duration:** 4–6 hours  
**Frequency:** Once before each production release

---

### Release Readiness Checklist — v2.3.1 Production Release

**Target Release Date:** 2024-06-23  
**Release Type:** Minor feature (payments), bug fixes  
**Environments:** Staging → Production

#### Pre-Release Validation

| # | Item | Checked | Owner | Status |
|---|---|---|---|---|
| 1 | All test cases executed | Yes, 100% pass rate | QA | ✅ |
| 2 | No open P0/P1 bugs | Yes, all fixed or deferred | Dev | ✅ |
| 3 | Known issues documented | Yes, in release notes | QA | ✅ |
| 4 | Smoke test passed | Yes, all checks passed | QA | ✅ |
| 5 | Regression test passed | Yes, 100% pass | QA | ✅ |
| 6 | UAT approved | Yes, signed off | Product | ✅ |
| 7 | Performance acceptable | Yes, all metrics met | QA/DevOps | ✅ |
| 8 | Security review passed | Yes, no vulnerabilities | Security | ✅ |

#### Code & Documentation

| # | Item | Checked | Owner | Status |
|---|---|---|---|---|
| 1 | Code review completed | Yes, 2 approvals | Dev | ✅ |
| 2 | Unit tests passing | Yes, 100% | Dev | ✅ |
| 3 | Integration tests passing | Yes, all green | Dev | ✅ |
| 4 | Documentation updated | Yes, API docs, user guide | Tech Writer | ✅ |
| 5 | CHANGELOG updated | Yes, v2.3.1 entry added | Product | ✅ |
| 6 | Release notes ready | Yes, customer-facing | Marketing | ✅ |
| 7 | Migration scripts (if needed) | N/A | Dev | ✅ |

#### Infrastructure & Deployment

| # | Item | Checked | Owner | Status |
|---|---|---|---|---|
| 1 | Production environment ready | Yes, tested | DevOps | ✅ |
| 2 | Database backups verified | Yes, backup taken | DevOps | ✅ |
| 3 | Rollback procedure documented | Yes, in runbook | DevOps | ✅ |
| 4 | Monitoring/alerting configured | Yes, all metrics | DevOps | ✅ |
| 5 | Log aggregation working | Yes, CloudWatch operational | DevOps | ✅ |
| 6 | Load testing completed (if major changes) | N/A (minor feature) | DevOps | ✅ |
| 7 | Canary deployment plan | Yes, 10% → 50% → 100% | DevOps | ✅ |

#### Third-Party Integrations

| # | Integration | Tested | Status | Notes |
|---|---|---|---|---|
| 1 | Stripe (payments) | Yes, sandbox & prod | ✅ | Credential rotation verified |
| 2 | Google OAuth | Yes, QA & prod accounts | ✅ | OAuth flow works |
| 3 | Email delivery (SendGrid) | Yes, test & prod | ✅ | Sending operational |
| 4 | Slack (notifications) | Yes, webhook working | ✅ | Notifications firing |
| 5 | Analytics (Mixpanel) | Yes, events tracking | ✅ | Event payload correct |

#### User Communication

| # | Item | Checked | Owner | Status |
|---|---|---|---|---|
| 1 | Release announcement ready | Yes, draft sent | Marketing | ✅ |
| 2 | In-app notification prepared | Yes, copy approved | Product | ✅ |
| 3 | Support team briefed | Yes, training completed | Support | ✅ |
| 4 | Known issues communicated | Yes, documented | QA | ✅ |
| 5 | Support documentation updated | Yes, FAQ & troubleshooting | Tech Support | ✅ |

#### Data Migration & Backward Compatibility

| # | Check | Result | Status |
|---|---|---|---|
| 1 | Existing orders not affected by payment system changes | No schema changes to orders table | ✅ |
| 2 | API backward compatibility | Old API endpoints still work | ✅ |
| 3 | Database migration tested | Migration script successful on staging | ✅ |
| 4 | Rollback tested | Rollback script reverses changes | ✅ |

#### Final Sign-Off

| Role | Name | Date | Approval |
|---|---|---|---|
| QA Lead | Jesse Stratmeyer | 2024-06-20 | ✅ **APPROVED** |
| Dev Lead | [Dev Lead Name] | 2024-06-20 | ✅ **APPROVED** |
| Product Manager | [PM Name] | 2024-06-20 | ✅ **APPROVED** |
| DevOps Lead | [DevOps Name] | 2024-06-20 | ✅ **APPROVED** |
| Security Lead | [Security Name] | 2024-06-20 | ✅ **APPROVED** |

#### Release Decision

✅ **APPROVED FOR PRODUCTION RELEASE**  
**Target Date:** 2024-06-23  
**Deployment Window:** 2 PM–4 PM UTC  
**Deployment Strategy:** Canary (10% → 50% → 100%)

---

---

## 4. UAT (User Acceptance Testing) Checklist

**Purpose:** Validate that new features meet business requirements.  
**Duration:** 2–3 days  
**Participants:** Product Manager, Stakeholders, QA Facilitator

---

### UAT Checklist — Payment Feature (v2.3.1)

**Date:** 2024-06-19  
**Participants:** Finance Manager (Carol), Product Manager (Alex), QA (Jesse)

#### Business Requirements Validation

| # | Requirement | Acceptance Criteria | Test Result | Sign-Off |
|---|---|---|---|---|
| 1 | Customers can pay by credit card | User can complete purchase with Visa/MC/Amex | ✅ Pass | Carol ✓ |
| 2 | Order confirmations sent via email | Customer receives email within 1 min | ✅ Pass | Carol ✓ |
| 3 | Refunds can be processed manually | Admin can refund via UI | ✅ Pass | Alex ✓ |
| 4 | Payment fees calculated correctly | Fee: 2.9% + $0.30 per transaction | ✅ Pass | Carol ✓ |
| 5 | Invoices generated automatically | Invoice created post-payment | ✅ Pass | Carol ✓ |
| 6 | Payment data secure (PCI compliant) | Card data not stored locally | ✅ Pass | Alex ✓ |
| 7 | Failed payments handled gracefully | Error message shown; user can retry | ✅ Pass | Alex ✓ |

#### Real-World Scenario Testing

| # | Scenario | Action | Result | Status |
|---|---|---|---|---|
| 1 | Customer pays with Visa | Complete purchase with Visa card | Order created, email sent | ✅ |
| 2 | Customer pays with Amex | Complete purchase with Amex card | Order created, email sent | ✅ |
| 3 | Card declines (insufficient funds) | Attempt payment with test decline card | Error shown, can retry | ✅ |
| 4 | Refund request (full) | Process refund in admin panel | Refund successful, customer notified | ✅ |
| 5 | Refund request (partial) | Refund 50% of order | Partial refund successful | ✅ |

#### User Experience Validation

| # | Question | Feedback | Score |
|---|---|---|---|
| 1 | Is the checkout flow intuitive? | Yes, clear step-by-step process | ✅ 5/5 |
| 2 | Is the payment form easy to use? | Yes, form fields labeled clearly | ✅ 5/5 |
| 3 | Are error messages helpful? | Yes, tells user what went wrong | ✅ 4/5 |
| 4 | Is payment processing speed acceptable? | Yes, completes in ~4 seconds | ✅ 5/5 |
| 5 | Do confirmation emails look professional? | Yes, well-formatted, includes receipt | ✅ 5/5 |

#### UAT Sign-Off

- **Finance Manager (Carol):** ✅ Approve for release
- **Product Manager (Alex):** ✅ Approve for release
- **QA Facilitator (Jesse):** ✅ Approve for release

**Overall Result:** ✅ **UAT PASSED** — Feature ready for production

---

## Summary of Checklists

Use these templates for your testing activities:

1. **Smoke Testing:** Quick build validation (15–30 min)
2. **Regression Testing:** Verify no breakage after changes (4–8 hours)
3. **Release Readiness:** Final gate before production (4–6 hours)
4. **UAT:** Business requirements validation (2–3 days)

All checklists are **customizable** — adapt them to your specific project and release scope.
