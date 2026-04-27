# Exploratory Testing Session Notes

**Session ID:** EXP-2024-06-15-001  
**Date:** 2024-06-15  
**Tester:** Jesse Stratmeyer (Senior QA Analyst)  
**Application:** E-Commerce Platform v2.3.0  
**Module:** Shopping Cart & Checkout Flow  
**Duration:** 90 minutes  
**Mission/Charter:** Validate end-to-end purchase flow; discover edge cases and usability issues

---

## Session Charter

**Goal:** Uncover unexpected behaviors and usability issues in the shopping cart and checkout process that might not be caught by formal test cases.

**Scope:**
- Product browsing → cart → checkout → order confirmation
- Focus on user experience, edge cases, error handling
- Cross-browser validation (Chrome, Safari, Firefox)
- Mobile responsiveness (iOS Safari, Android Chrome)

**Approach:** User-centric exploration; simulate realistic customer behavior; try to break the flow intentionally.

---

## Exploration Timeline & Findings

### 1. Initial Reconnaissance (15 min)

**What I Did:**
- Loaded the product catalog page
- Browsed products in different categories
- Examined product detail pages
- Tested basic search functionality

**Observations:**
- ✅ Product images load quickly
- ✅ Product details clear and well-organized
- ✅ Search filters work intuitively
- ⚠️ "Sort by" dropdown sometimes slow to respond (initial load)
- ⚠️ Product images not responsive on small screens (cut off on mobile)

**Potential Issues:**
- Product image responsiveness needs checking
- Sort dropdown performance lag (might be dropdown library issue)

**Next:** Add items to cart and test cart operations.

---

### 2. Adding Items to Cart (20 min)

**What I Did:**
- Added single item (Running Shoes, size M, qty 1)
- Added multiple items (Socks qty 5, T-Shirt qty 2, etc.)
- Tested "Add to Cart" button states
- Attempted to add same item with different sizes
- Added item, then immediately removed it
- Added item to cart, continued shopping, added more items

**Key Findings:**

✅ **Working Well:**
- Add to cart toast notification appears and disappears smoothly
- Cart count badge updates immediately
- Can add multiple quantities of same item
- Cart persists when navigating away (good!)
- Touch targets large enough on mobile

⚠️ **Issues Found:**

**Issue #1: Size/Color Options Not Required**
- Expected: Should not allow adding item without selecting size/color
- Actual: Can add "Shoes" to cart without selecting size — defaults to "M"
- Impact: Users might receive wrong size
- Severity: HIGH (could cause returns)
- Possible Defect: TC-BUG-NEW-001 (Size not required in form validation)

**Issue #2: Quantity Spinner Inconsistent**
- Expected: Quantity selector +/- buttons should respect item stock
- Actual: Can set quantity to 999 (no stock check)
- Behavior: Let's see what happens at checkout (might be checked server-side)
- Severity: MEDIUM (might fail at checkout, but server-side validation is backup)

**Issue #3: "Add to Cart" Button Text Misleading**
- Button text changes to "Added ✓" but disappears after 1 sec
- Expected: User might not realize they can click again (or is it added?)
- Actual: Button returns to "Add to Cart"
- Confusion: Unclear if clicking again adds another item or does nothing
- Severity: LOW (UX friction, not a bug)

**Next:** Proceed to cart review and modify items.

---

### 3. Cart Review & Modifications (25 min)

**What I Did:**
- Reviewed cart contents and total calculation
- Updated quantities (increase, decrease, set to 0)
- Removed items via different methods (swipe, delete button)
- Applied promo code
- Observed price changes
- Tested with empty cart state

**Key Findings:**

✅ **Working Well:**
- Quantity updates reflected immediately
- Total price recalculated correctly
- Item removal works smoothly
- Empty cart message clear and helpful

⚠️ **Issues Found:**

**Issue #4: Promo Code Edge Case**
- Applied code "SUMMER20" → should give 20% discount
- Expected: $100 → $80 (with discount)
- Actual: Discount applied, but tooltip shows discount amount truncated
- Example: "Discount: $19.99999" shows instead of "$20.00"
- Severity: LOW (visual glitch, math is correct)

**Issue #5: Delete Item Confirmation Not Consistent**
- Delete button: removes item immediately (no confirmation)
- Swipe-to-delete: shows undo option for 3 seconds
- Expected: Consistent behavior across both methods
- Actual: Different UX patterns
- Severity: LOW (both approaches work, but inconsistent)

**Issue #6: Tax Not Applied in Cart View**
- Expected: Tax should be shown in cart (or at least mentioned)
- Actual: Total shown, but no line item for tax
- Confusion: "Total: $80.00" — but is this with or without tax?
- Reality: Tax calculated at checkout (OK, but should be clearer)
- Severity: MEDIUM (user surprised at checkout)

**Next:** Proceed to checkout flow.

---

### 4. Checkout Flow — Address & Shipping (20 min)

**What I Did:**
- Clicked "Proceed to Checkout"
- Filled in shipping address
- Selected shipping method
- Tested address validation
- Tried various address formats
- Tested with incomplete addresses

**Key Findings:**

✅ **Working Well:**
- Address form fields clearly labeled
- Validation provides helpful error messages
- State dropdown works intuitively
- Shipping options clearly displayed with prices

⚠️ **Issues Found:**

**Issue #7: Address Validation Too Strict**
- Tried address: "123 Main Street, Apt 456B"
- Error: "Address line 2 invalid" (but I didn't use line 2?)
- Actual: Form parsed my comma-separated input incorrectly
- Expected: Should handle apartment numbers gracefully
- Severity: MEDIUM (user confusion, but can work around)

**Issue #8: ZIP Code Format Not Validated Correctly**
- Entered ZIP: "97201-1234" (extended format)
- Expected: Should validate 5 or 9 digit ZIPs
- Actual: Accepted, but might not be found in system
- Severity: LOW (might fail at shipping calculation, but not user's fault)

**Issue #9: No Shipping Address Preview**
- After entering address and selecting shipping
- Expected: Show address and shipping method before final payment
- Actual: Must click through to payment screen to verify
- Severity: MEDIUM (late discovery of errors wastes time)

**Next:** Enter payment details and complete purchase.

---

### 5. Checkout — Payment & Completion (10 min)

**What I Did:**
- Entered payment card details
- Submitted payment
- Observed confirmation page
- Checked for confirmation email

**Key Findings:**

✅ **Working Well:**
- Payment form secure (no card details visible in console)
- Success page displays order number and summary
- Confirmation email arrives quickly
- Order details accessible in customer account

⚠️ **Issues Found:**

**Issue #10: Order Number Formatting Unclear**
- Order ID: "12345" (5 digits)
- Expected: Format like "ORD-20240615-12345" (more recognizable)
- Actual: Plain number (less professional)
- Severity: LOW (cosmetic, not functional)

**Issue #11: No Tracking Number Until Shipment**
- Expected: Should show expected delivery date
- Actual: "Tracking will be available once item ships"
- Positive: Honest message, but could show estimated date
- Severity: LOW (expected behavior, but could improve UX)

---

### 6. Cross-Browser Testing (15 min)

**What I Did:**
- Tested same flow in Safari (macOS)
- Tested in Firefox
- Observed rendering and functionality

**Key Findings:**

✅ **Chrome:** All issues found above (baseline)

⚠️ **Safari:**
- Issue #12: Quantity spinner buttons small and hard to tap
- Issue #13: Cart page scrolling janky (might be Safari rendering issue)

⚠️ **Firefox:**
- Issue #14: Promo code input field not focused properly (tab order)
- Issue #15: "Proceed to Checkout" button flash briefly on hover (CSS animation glitch)

---

### 7. Mobile Testing (10 min)

**What I Did:**
- Tested on iPhone 14 Pro simulator (Safari)
- Tested on Pixel 7 emulator (Chrome)
- Verified responsive layout
- Tested touch interactions

**Key Findings:**

✅ **Working Well:**
- Responsive layout adapts well to mobile
- Touch targets are large (≥44pt)
- Form fields readable without zooming

⚠️ **Issues Found:**
- Issue #16: Product image cut off on small screens (noted earlier)
- Issue #17: Quantity spinner buttons hard to tap (text too small on mobile)
- Issue #18: Cart summary "sticky" in mobile view, but overlaps content at bottom

---

## Issues Summary

### Critical Issues Found (Require Fix)

| Issue | Severity | Category | Recommendation |
|---|---|---|---|
| #1: Size not required | HIGH | Validation | Add form validation |
| #6: Tax not shown in cart | MEDIUM | UX | Add tax line item or clear notice |
| #7: Address validation too strict | MEDIUM | Validation | Improve regex or parsing |
| #9: No address preview before payment | MEDIUM | UX | Add confirmation screen |

### Minor Issues (Nice-to-Haves)

| Issue | Severity | Category | Recommendation |
|---|---|---|---|
| #2: Quantity unchecked | MEDIUM | Validation | Add stock check (server-side OK for now) |
| #3: Button text confusing | LOW | UX | Clarify "Add to Cart" button state |
| #4: Discount decimal rounding | LOW | Display | Format currency correctly |
| #5: Delete confirmation inconsistent | LOW | UX | Standardize across methods |
| #8: Extended ZIP format | LOW | Validation | Support 5+4 ZIP format |
| #10: Order number formatting | LOW | UX | Make order ID more recognizable |
| #11: No tracking ETA | LOW | UX | Show estimated delivery date |
| #12–18: Cross-browser/mobile issues | MEDIUM | UX | Address browser-specific rendering |

---

## Root Cause Analysis

**Why were these issues not found by formal testing?**

1. **Formal tests use happy path:** They test with perfect data (valid sizes, correct address format)
2. **Exploratory testing tries edge cases:** Real users might skip size selection, enter addresses wrong, use extended ZIP codes
3. **Real user behavior is unpredictable:** Formal tests don't account for typos, incomplete data, unusual formats
4. **Cross-browser testing incomplete:** Formal tests may focus on Chrome only; Safari/Firefox edge cases missed

---

## Testing Artifacts

**Screenshots Captured:**
- Product catalog layout issues
- Cart page with issue #5 (delete inconsistency)
- Address validation error (issue #7)
- Mobile rendering issues (issue #16–18)
- Browser-specific glitches (Safari quantity spinner, Firefox focus issue)

**Test Data Used:**
- Product: Running Shoes ($89.99)
- Promo Code: SUMMER20 (20% discount)
- Test Address: "123 Main Street, Apt 456B" (triggers validation error)
- Test ZIP: "97201-1234" (extended format)

---

## Recommendations

### For Next Release

1. **High Priority:**
   - Add size/color validation (don't allow adding without selection)
   - Display tax in cart view or clarify at checkout
   - Improve address validation to handle apartment numbers
   - Add address review screen before payment

2. **Medium Priority:**
   - Fix cross-browser rendering issues
   - Improve mobile touch targets
   - Standardize delete confirmation behavior
   - Format order numbers professionally

3. **Nice-to-Haves:**
   - Show estimated delivery date
   - Fix quantity spinner on mobile
   - Improve button state messaging
   - Support extended ZIP code format

### For Testing Process

1. **Include exploratory testing in every release:** Spend at least 2–4 hours per module exploring edge cases
2. **Test on real devices:** Don't rely solely on simulators/emulators
3. **Test with real user data:** Try incomplete addresses, special characters, edge cases
4. **Cross-browser testing:** Don't just test Chrome; verify Safari, Firefox, Edge
5. **Mobile-first approach:** Test mobile experience as primary concern

---

## Lessons Learned

1. **Formal test cases miss edge cases:** Real users don't fill out forms perfectly
2. **Address validation is tricky:** Different formats, special characters, abbreviations
3. **Mobile UX differs from desktop:** Touch targets, scrolling, viewport constraints
4. **Cross-browser matters:** Browser-specific rendering issues can hide in single-browser testing
5. **User experience testing valuable:** Features work technically, but UX friction reduces adoption

---

## Next Steps

1. **Debrief with team:** Share findings in next standup
2. **Create formal defect reports:** Convert issues to bug tickets
3. **Prioritize fixes:** Schedule fixes based on severity
4. **Plan follow-up testing:** Test fixes once implemented
5. **Document in test case library:** Create formal test cases for discovered edge cases

---

## Session Sign-Off

**Tester:** Jesse Stratmeyer  
**Date:** 2024-06-15  
**Time:** 14:00–15:30 (90 minutes)  
**Environment:** QA Staging (Chrome, Safari, Firefox; mobile simulators)

**Outcome:** ✅ **SUCCESSFUL SESSION**
- Found 18 issues (4 high/medium, 14 low/cosmetic)
- Validated core flow works (positive sign)
- Identified UX friction points
- Discovered cross-browser issues

**Value Delivered:**
- Discovered issues before production
- Provided detailed reproduction steps
- Recommended prioritized fixes
- Improved testing approach for future sessions

---

---

## Appendix: Exploratory Testing Best Practices

### Charter Development
1. Define clear mission/goal for session
2. Set time limit (2–4 hours is typical)
3. Focus on specific areas (don't try to test everything)
4. Avoid pre-written test cases (explore freely)
5. Document your approach as you go

### During Session
1. **Explore mindfully:** Ask "what could go wrong here?"
2. **Vary your approach:** Different data, different paths, different browsers
3. **Follow your intuition:** If something feels wrong, investigate
4. **Take notes:** Record what you're testing and what you find
5. **Capture evidence:** Screenshots, videos, logs help explain issues

### Issue Documentation
1. **Provide context:** What were you doing when you found this?
2. **Reproduce reliably:** Make sure issue is repeatable
3. **Be specific:** Include exact data, steps, expected vs. actual
4. **Show impact:** How does this affect users?
5. **Suggest fixes:** If obvious, provide recommendation

### Debrief & Follow-Up
1. Share findings with team promptly
2. Prioritize issues based on severity
3. Create formal defect tickets
4. Plan fixes and re-testing
5. Document lessons learned

### Chartering Template

```
SESSION CHARTER
================

Session ID: EXP-[YEAR]-[DATE]-[NUMBER]
Date: YYYY-MM-DD
Tester: [Name]
Application: [App Name]
Module: [Feature/Area]
Duration: [Time]

Mission: [One sentence goal]
Scope: [What are we testing]
Approach: [How will we test]
Questions: [What do we want to learn]
Areas to Explore: [Specific areas to focus on]
```

---

## Related Documentation

- [Test Plans](../test-plans/) — Formal test planning
- [Test Cases](../test-cases/) — Scripted test cases
- [Bug Reports](../bug-reports/) — How to document findings
- [Process Docs](../process-docs/) — QA workflows
