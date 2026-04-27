# Test Case Suite: Mobile Application — Shopping Cart & Checkout

**Suite ID:** TC-CART-MOBILE-001  
**Application:** E-Commerce iOS/Android App  
**Module:** Shopping Cart, Checkout, Payment  
**Test Data:** Available in QA backend  
**Automation Status:** Partially automated (API validation); mostly manual (UI)  
**Last Updated:** 2024-06-20

---

## Test Case Overview

| Test Case ID | Title | Platform | Automation | Status |
|---|---|---|---|---|
| TC-CART-101 | Add product to cart | iOS, Android | ❌ | ✓ Pass |
| TC-CART-102 | Update product quantity in cart | iOS, Android | ❌ | ✓ Pass |
| TC-CART-103 | Remove item from cart | iOS, Android | ❌ | ✓ Pass |
| TC-CART-104 | Apply promo code | iOS, Android | ❌ | ✓ Pass |
| TC-CART-105 | Cart persists after app close | iOS, Android | ✅ | ✓ Pass |
| TC-CART-106 | Offline cart → sync on reconnect | iOS, Android | ❌ | ⚠ Issue |
| TC-CART-107 | Checkout: Enter shipping address | iOS, Android | ❌ | ✓ Pass |
| TC-CART-108 | Checkout: Select shipping method | iOS, Android | ❌ | ✓ Pass |
| TC-CART-109 | Checkout: Enter payment details | iOS, Android | ✅ | ✓ Pass |
| TC-CART-110 | Complete purchase — success | iOS, Android | ✅ | ✓ Pass |
| TC-CART-111 | Payment failure → retry | iOS, Android | ❌ | ✓ Pass |
| TC-CART-112 | Accessibility: VoiceOver checkout | iOS | ❌ | ✓ Pass |
| TC-CART-113 | Performance: Checkout <3s load | iOS, Android | ✅ | ⚠ Flaky |

---

## Detailed Test Cases

---

### TC-CART-101: Add Product to Cart

**Objective:** Verify users can add a product to their shopping cart from the product detail view.

**Preconditions:**
- App installed and user logged in
- Product catalog loaded
- User on product detail page (e.g., "Running Shoes - $89.99")

**Platform:** iOS & Android

**Test Steps:**

| # | Step | iOS Expected | Android Expected | Status |
|---|---|---|---|---|
| 1 | View product detail page | Product image, title, price, description visible | Same | ✓ |
| 2 | Verify size/color options visible (if applicable) | Selection dropdowns or radio buttons shown | Same | ✓ |
| 3 | Select product options (size: M, color: Blue) | Options highlighted/selected | Same | ✓ |
| 4 | Tap "Add to Cart" button | Button changes to "Added ✓" or loading spinner shows | Same | ✓ |
| 5 | Wait for cart update (API call) | Success message: "Added to Cart" toast appears (top of screen, 2 sec) | Same | ✓ |
| 6 | Verify cart count updated | Cart icon in bottom navbar shows "1" badge | Same | ✓ |
| 7 | Verify product in cart | Tap cart icon → product listed with correct size/color/price | Same | ✓ |
| 8 | Verify price calculation | Cart total = $89.99 (no tax shown until checkout) | Same | ✓ |

**Expected Result:** ✅ Product successfully added to cart; toast notification shown; cart count incremented.

**Actual Result:** ✅ Passed on both iOS and Android

**Devices Tested:**
- **iOS:** iPhone 14 Pro (6.1"), iOS 17.1
- **Android:** Pixel 7 (6.3"), Android 14

**Automation Script:** N/A — manual UI testing  
**API Verification:** POST `/api/cart/add` — response 200 OK; product_id, size, color in request

**Notes:**
- Toast notification dismisses automatically after 2 seconds
- "Added ✓" button state reverts after 1 second for reusability
- Cart is stored locally on device and synced to backend

---

### TC-CART-105: Cart Persists After App Close

**Objective:** Verify shopping cart contents are retained when the app is closed and reopened.

**Preconditions:**
- Product added to cart (TC-CART-101 completed)
- Cart contains: Running Shoes (size M, qty 1) — $89.99

**Platform:** iOS & Android

**Test Steps:**

| # | Step | iOS Expected | Android Expected | Status |
|---|---|---|---|---|
| 1 | Verify cart contains product | Cart icon shows "1" badge | Same | ✓ |
| 2 | Close app completely (swipe up / force stop) | App process terminated | Same | ✓ |
| 3 | Wait 2 seconds | Ensure app fully closed | Same | ✓ |
| 4 | Reopen app | App launches; splash screen shown | Same | ✓ |
| 5 | Navigate to cart | Tap cart icon in bottom navbar | Same | ✓ |
| 6 | Verify product still in cart | Running Shoes (size M, qty 1) displayed | Same | ✓ |
| 7 | Verify quantity unchanged | Quantity spinner shows "1" | Same | ✓ |
| 8 | Verify price unchanged | Cart total still $89.99 | Same | ✓ |
| 9 | Verify product can be purchased | Proceed to checkout and complete purchase | Same | ✓ |

**Expected Result:** ✅ Cart contents fully persisted across app close/reopen.

**Actual Result:** ✅ Passed on both platforms

**Devices Tested:**
- **iOS:** iPhone 14 Pro (6.1"), iOS 17.1
- **Android:** Pixel 7 (6.3"), Android 14

**Automation Script:** `tests/mobile/cart_persistence.spec.js` (uses emulator/simulator)

**Backend Verification:**
- Local device storage: SQLite database (iOS) or SharedPreferences (Android)
- Backend sync: Cart synced within 30 seconds of app launch
- Conflict resolution: Server-side cart takes precedence if out of sync

**Notes:**
- Cart is stored locally for offline access; background sync occurs when network available
- If product price changed on server, user alerted during checkout

---

### TC-CART-106: Offline Cart → Sync on Reconnect

**Objective:** Verify cart updates while offline are synced to server when network reconnects.

**Preconditions:**
- Cart contains 1 item (Running Shoes, qty 1)
- Network connectivity will be toggled (Wi-Fi off)

**Platform:** iOS & Android

**Test Steps:**

| # | Step | iOS Expected | Android Expected | Issue |
|---|---|---|---|---|
| 1 | Verify online (network status shown) | WiFi icon visible in status bar | Same | — |
| 2 | Disable WiFi and mobile data (Airplane Mode) | Device offline; network icon removed | Same | — |
| 3 | Navigate to cart | Cart displays offline content (cached) | Same | — |
| 4 | Update quantity: 1 → 3 (Running Shoes) | Quantity spinner updated; cart total updated locally | Same | ⚠ |
| 5 | Verify local update reflected immediately | Cart shows qty 3, total = $269.97 | Same | ⚠ |
| 6 | Attempt checkout | Error message: "Offline. Cannot complete purchase." | Same | ⚠ |
| 7 | Re-enable WiFi (turn off Airplane Mode) | Network connectivity restored | Same | — |
| 8 | Wait 5 seconds (sync background job) | App syncs cart to server silently | Same | ⚠ |
| 9 | Verify server-side cart updated | Backend shows qty 3 for Running Shoes | Same | ⚠ |
| 10 | Verify no conflict notification | User not notified of sync (seamless) | Same | ⚠ |
| 11 | Proceed to checkout | Checkout succeeds with qty 3 | Same | ⚠ |

**Expected Result:** ✅ Cart updates sync seamlessly when network restored; no data loss.

**Actual Result:** ⚠ Issue found — sync sometimes fails silently; user unaware of failure.

**Devices Tested:**
- **iOS:** iPhone 14 Pro (6.1"), iOS 17.1
- **Android:** Pixel 7 (6.3"), Android 14

**Defect:** TC-BUG-089 — Cart offline sync fails when app backgrounded during reconnect  
**Workaround:** Kill and restart app to force sync

**Notes:**
- Offline cart stored in local database; changes queued for sync
- Sync uses exponential backoff (retry after 5s, 10s, 30s, 1min, etc.)
- If server-side cart differs from local, conflict resolution needed (currently: server wins)

---

### TC-CART-109: Checkout — Enter Payment Details

**Objective:** Verify users can enter payment details securely and payment is processed correctly.

**Preconditions:**
- Cart contains items (Running Shoes qty 3, total $269.97)
- User on checkout payment screen
- Payment processor (Stripe) configured in QA environment

**Platform:** iOS & Android

**Test Steps:**

| # | Step | iOS Expected | Android Expected | Status |
|---|---|---|---|---|
| 1 | Navigate to checkout (from cart) | Checkout flow starts; address form shown | Same | ✓ |
| 2 | Fill address & shipping (already tested) | Address validated; shipping method selected | Same | ✓ |
| 3 | Proceed to payment screen | Payment form displayed | Same | ✓ |
| 4 | Verify payment form fields | Card number, expiration, CVC, name fields visible | Same | ✓ |
| 5 | Enter test card: 4242 4242 4242 4242 | 16 digits accepted; spaces/dashes auto-formatted | Same | ✓ |
| 6 | Enter expiration: 12/25 | Month/year dropdowns or text field accepted | Same | ✓ |
| 7 | Enter CVC: 123 | 3-digit field accepts input; value masked | Same | ✓ |
| 8 | Enter cardholder name: John Doe | Text field accepted | Same | ✓ |
| 9 | Verify keyboard: numeric for card field | Card field shows numeric keyboard (iOS/Android numeric input) | Same | ✓ |
| 10 | Verify card details not logged | App does not log/store card details (PCI compliance) | Same | ✓ |
| 11 | Verify secure transmission (Stripe.js) | Payment details sent directly to Stripe; not to our server | Same | ✓ |
| 12 | Review order summary | Cart total: $269.97; shipping: $0 (free); tax: $0 (QA env) | Same | ✓ |
| 13 | Tap "Complete Purchase" | Loading spinner shows; API call to backend | Same | ✓ |

**Expected Result:** ✅ Payment details accepted; form validation passes; secure transmission verified.

**Actual Result:** ✅ Passed on both platforms

**Devices Tested:**
- **iOS:** iPhone 14 Pro (6.1"), iOS 17.1
- **Android:** Pixel 7 (6.3"), Android 14

**Automation Script:** `tests/mobile/checkout_payment.spec.js` (uses Stripe test card mock)

**Security Verification:**
- ✓ Payment details not logged in app console or backend
- ✓ HTTPS encryption verified (network traffic inspection with Charles Proxy)
- ✓ Stripe.js library loading from Stripe CDN (no local copy)
- ✓ PCI DSS compliance: our server never touches raw card data

**Notes:**
- Test card 4242 4242 4242 4242 simulates successful charge in Stripe sandbox
- Other test cards available: 4000000000000002 (decline), 4000002500003155 (3D Secure), etc.

---

### TC-CART-110: Complete Purchase — Success

**Objective:** Verify the complete purchase flow from cart to order confirmation.

**Preconditions:**
- Cart filled: Running Shoes qty 3 ($269.97)
- Address entered: 123 Main St, Portland, OR 97201
- Shipping selected: Standard (free)
- Payment entered: Valid test card

**Platform:** iOS & Android

**Test Steps:**

| # | Step | iOS Expected | Android Expected | Status |
|---|---|---|---|---|
| 1 | Review order summary page | All items, address, shipping, total visible | Same | ✓ |
| 2 | Tap "Complete Purchase" button | Loading indicator; API call to backend (/api/orders/create) | Same | ✓ |
| 3 | Wait for payment processing (max 10 sec) | Loading indicator persists while Stripe processes | Same | ✓ |
| 4 | Verify payment succeeds | Stripe returns charge success response to backend | Same | ✓ |
| 5 | Verify order created in database | Backend creates order record with status "paid" | Same | ✓ |
| 6 | Verify order confirmation screen | Confirmation page displays with order number (e.g., #ORD-20240620-0001) | Same | ✓ |
| 7 | Display order details | Order number, items (qty/price), total, shipping address, estimated delivery date | Same | ✓ |
| 8 | Verify success messaging | "Thank you for your purchase!" message displayed prominently | Same | ✓ |
| 9 | Verify cart cleared | Cart icon shows "0" badge (cart now empty) | Same | ✓ |
| 10 | Verify confirmation email sent | Email arrives in inbox within 1 minute (order receipt, tracking details when available) | Same | ✓ |
| 11 | Verify "View Order Status" button | User can tap to see order details and tracking | Same | ✓ |
| 12 | Verify "Continue Shopping" button | Returns to product list; user can add more items | Same | ✓ |

**Expected Result:** ✅ Purchase completed successfully; confirmation shown; email sent; cart cleared.

**Actual Result:** ✅ Passed on both platforms

**Devices Tested:**
- **iOS:** iPhone 14 Pro (6.1"), iOS 17.1
- **Android:** Pixel 7 (6.3"), Android 14

**Automation Script:** `tests/mobile/complete_purchase.spec.js`

**Backend Verification:**
- Order created in `orders` table with all details
- Line items in `order_items` table (qty, price, product_id)
- Payment recorded in `payments` table with Stripe charge ID
- Order status: "paid" (not "pending" or "failed")
- Confirmation email sent via email service

**Email Verification:**
- Subject: "Order Confirmation: #ORD-20240620-0001"
- Content: Order number, items, total, shipping address, estimated delivery
- Links: "View Order" (deep link to order status page), "Need Help?" (support contact)

**Notes:**
- Purchase is synchronous (user waits for confirmation)
- If payment fails (declined card), error message shown; user returns to checkout
- Order confirmation available in "Orders" section of app (order history)

---

### TC-CART-112: Accessibility — VoiceOver Checkout

**Objective:** Verify the checkout flow is navigable using VoiceOver (iOS screen reader) and all controls are labeled.

**Preconditions:**
- iOS device (iPhone 14 Pro, iOS 17.1)
- VoiceOver enabled (Settings > Accessibility > VoiceOver)
- Cart contains items
- On checkout flow

**Platform:** iOS only

**Test Steps:**

| # | Step | Expected Behavior | Status |
|---|---|---|---|
| 1 | Enable VoiceOver | Screen reader active; all UI elements announced | ✓ |
| 2 | Navigate form fields with swipe (left/right) | Each field announced with label and state (e.g., "Card number field, empty") | ✓ |
| 3 | Tap card number field | Field focused; "Card number field" announced | ✓ |
| 4 | Enter test card: 4242 4242 4242 4242 | VoiceOver announces "1 entered", "2 entered", etc., as each digit typed | ⚠ Verbose |
| 5 | Verify field labels read correctly | "Card number field", "Expiration date field", "CVC field", "Cardholder name field" all announced | ✓ |
| 6 | Tab through fields in order (card → exp → CVC → name) | Tab order logical and sequential | ✓ |
| 7 | Verify buttons are announced | "Complete purchase button" announced with double-tap instruction | ✓ |
| 8 | Double-tap "Complete Purchase" | Button activated; loading state announced ("Processing, please wait") | ✓ |
| 9 | Wait for confirmation screen | Confirmation screen announced: "Order confirmed, order number ORD-20240620-0001" | ✓ |
| 10 | Verify error messages readable | If any error, error text announced and linked to problematic field | ✓ |
| 11 | Verify focus indicators visible | Focus outline visible around form fields (even with VoiceOver) | ✓ |
| 12 | Test with minimum touch target size | Buttons ≥44×44pt; form fields ≥44pt tall | ✓ |

**Expected Result:** ✅ Checkout fully navigable with VoiceOver; all elements labeled and announced; no hidden controls.

**Actual Result:** ✅ Passed (minor: digit entry verbosity could be reduced)

**Device Tested:**
- **iOS:** iPhone 14 Pro (6.1"), iOS 17.1

**Manual Test:** Yes — requires visual and auditory verification  
**Standard:** WCAG 2.1 Level AA  

**Notes:**
- Digit-by-digit announcement during card entry is verbose; consider grouping (every 4 digits)
- "Expiration date" format announced clearly (MM/YY)
- Error messages linked to problematic fields for quick navigation
- Accessibility audit score: 95/100 (excellent)

---

### TC-CART-113: Performance — Checkout Load Time <3 Seconds

**Objective:** Verify checkout page loads in under 3 seconds on typical mobile network conditions.

**Preconditions:**
- Network throttled to 4G (typical mobile speed)
- Cart contains items
- Navigating to checkout from cart view

**Platform:** iOS & Android

**Test Steps:**

| # | Step | iOS Expected | Android Expected | Status |
|---|---|---|---|---|
| 1 | Throttle network to 4G (25 Mbps down, 10 Mbps up) | Network profiler set; Charles Proxy or Xcode network link conditioner active | Same | ✓ |
| 2 | Tap "Proceed to Checkout" from cart | Navigation begins; start timer | Same | ✓ |
| 3 | Wait for checkout page to fully load | All form fields, buttons, and summary visible; images loaded | Same | ⚠ |
| 4 | Measure load time from navigation to render complete | Time measured: <3 seconds (target) | Same | ⚠ |
| 5 | Record actual times (multiple runs) | Run 1: 2.8s, Run 2: 3.1s, Run 3: 2.9s (average: 2.93s) | Same | ⚠ |
| 6 | Verify all resources loaded | Lighthouse audit: all images, CSS, JavaScript loaded; no 404 errors | Same | ⚠ |
| 7 | Verify form is interactive | User can tap fields and enter text without lag | Same | ⚠ |
| 8 | Repeat on LTE network (slower) | LTE: Run 1: 3.2s, Run 2: 3.4s (exceeds target) | Same | ⚠ |

**Expected Result:** ✅ Checkout loads in <3 seconds on 4G; acceptable on LTE.

**Actual Result:** ⚠ Flaky — Average ~2.93s on 4G (meets target by small margin); exceeds on slower LTE.

**Devices Tested:**
- **iOS:** iPhone 14 Pro (6.1"), iOS 17.1
- **Android:** Pixel 7 (6.3"), Android 14

**Network Profiling Tool:** Charles Proxy, XCode Network Link Conditioner, Chrome DevTools Throttling

**Performance Details:**
- **Initial page load:** 1.2s (HTML + CSS)
- **Images load:** 1.1s (product thumbnail, logo)
- **JavaScript execution:** 0.4s (form initialization)
- **Total:** 2.7s (average)

**Optimization Opportunities:**
- Lazy-load product thumbnails (load below fold only when scrolled)
- Minify JavaScript bundle (currently 85KB; target: <50KB)
- Use WebP images instead of PNG (save 30% on image size)
- Cache checkout form between sessions

**Defect:** TC-BUG-091 — Checkout exceeds 3s target on LTE networks; needs optimization  
**Priority:** P2 (not critical, but impacts user experience on slow networks)

**Notes:**
- Target metric: First Contentful Paint (FCP) <2s, Largest Contentful Paint (LCP) <3s
- Measured on actual devices with network throttling (not just simulator)
- Lighthouse audit shows 92/100 performance score

---

## Summary

**Total Test Cases (Cart & Checkout):** 13  
**Passed:** 11 ✓  
**Flaky/Warnings:** 2 ⚠  
**Failed:** 0  

**Pass Rate:** 85%  
**Automation Coverage:** 30% (4 of 13 automated)  
**Manual Testing Required:** UI flow, accessibility, network edge cases

**Known Issues:**
- **TC-CART-106** — Offline sync fails when app backgrounded (TC-BUG-089)
- **TC-CART-113** — Checkout exceeds 3s on LTE networks (TC-BUG-091)

**Recommendation:** Address synchronization issue before next release. LTE performance degradation acceptable for 1.0 release (plan optimization for 1.1).

---

## Related Test Cases

- [Web App Authentication Test Cases](01_Web_App_Authentication_Test_Cases.md)
- [End-to-End User Journey Test Plan](../test-plans/05_End_to_End_User_Journey_Test_Plan.md)
