# Defect Log

This defect log is completed from the two Lab4 evidence files:

- `docs/lab_report/EMS_Lab4_Unit_Test_Defect_Log.xls`
- `docs/lab_report/EMS_Lab4_System_Test_Defect_Log.xlsx`

## Unit Test Defects

| Defect ID | Date | Module | Type | Severity | Priority | Status | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UDEF-001 | 10/03/2026 | F01 register_user | Logic | High | High | Fixed | Email was not trimmed and lower-cased, allowing duplicate users for the same address. |
| UDEF-002 | 10/03/2026 | F01 register_user | Validation | Critical | High | Verified | Password with letters only was accepted instead of raising a validation error. |
| UDEF-003 | 11/03/2026 | F01 register_user | Boundary | Medium | Medium | Fixed | User exactly 13 years old was rejected because the birth date comparison was incorrect. |
| UDEF-004 | 11/03/2026 | F02 authenticate | Security | Critical | Critical | In Progress | Banned users could still log in because account status was not checked. |
| UDEF-005 | 12/03/2026 | F02 authenticate | Security | High | High | Open | Different authentication errors exposed whether an email existed. |
| UDEF-006 | 12/03/2026 | F03 register_for_event | Logic | Critical | Critical | Fixed | Ticket limit was not calculated across existing registrations and the new quantity. |
| UDEF-007 | 13/03/2026 | F03 register_for_event | Boundary | High | High | Verified | Capacity boundary with 1 seat remaining and quantity 2 was not blocked correctly. |
| UDEF-008 | 13/03/2026 | F03 register_for_event | Calculation | Critical | Critical | In Progress | Registration with zero balance still deducted money and created a payment transaction. |
| UDEF-009 | 14/03/2026 | F03 register_for_event | Logic | High | High | Open | Users could reserve tickets for pending events because approved status was not enforced. |
| UDEF-010 | 15/03/2026 | F04 cancel_registration | Boundary | High | High | Fixed | Refund at the 24-hour boundary returned 50% instead of 100%. |
| UDEF-011 | 15/03/2026 | F04 cancel_registration | Boundary | High | High | Verified | Refund at the 1-hour boundary returned 0% instead of 50%. |
| UDEF-012 | 16/03/2026 | F04 cancel_registration | Security | Critical | Critical | Reopened | A user could cancel another user's registration due to missing ownership validation. |
| UDEF-013 | 16/03/2026 | F05 top_up_wallet | Boundary | Low | Low | Fixed | Top-up amount 1 was rejected although the rule allowed amounts greater than 0. |
| UDEF-014 | 17/03/2026 | F05 top_up_wallet | Validation | High | High | Open | Extremely large top-up amount was not blocked and could cause transaction overflow. |
| UDEF-015 | 18/03/2026 | F06 confirm_top_up_wallet | Boundary | Medium | Medium | Fixed | Confirmation exactly at 30 seconds was rejected although the boundary should be inclusive. |
| UDEF-016 | 18/03/2026 | F06 confirm_top_up_wallet | Exception | High | High | Verified | Invalid reference raised `NameError` instead of `NotFoundError`, causing a 500 response. |
| UDEF-017 | 19/03/2026 | F07 moderate_owned_event | Boundary | Medium | Medium | Fixed | Reject review note with 4 characters was incorrectly rejected. |
| UDEF-018 | 20/03/2026 | F07 moderate_owned_event | Security | Critical | Critical | In Progress | Normal users could call moderation service directly because role guard only existed at route level. |
| UDEF-019 | 20/03/2026 | F08 reset_password | Validation | High | High | Open | Reset password accepted a new password identical to the current password. |
| UDEF-020 | 21/03/2026 | F08 reset_password | Security | Critical | Critical | Fixed | Password hash was updated even when date of birth did not match. |

## System Test Defects

| Defect ID | Date | Module | Type | Severity | Priority | Status | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SDEF-001 | 10/03/2026 | F1.1 Register account | Logic | High | High | Open | Registration accepted the same email with different casing and spaces as a new user. |
| SDEF-002 | 10/03/2026 | F1.1 Register account | Validation | Critical | High | Fixed | Password containing only letters was accepted although password rules require letters and numbers. |
| SDEF-003 | 12/03/2026 | F1.2 Login | Security | High | High | Verified | Login error message exposed whether the password was wrong instead of using a neutral message. |
| SDEF-004 | 12/03/2026 | F1.3 Reset password | Security | High | Medium | Open | Reset password displayed an email existence hint when date of birth did not match. |
| SDEF-005 | 14/03/2026 | F2.3 Reserve ticket | Validation | High | High | Fixed | Quantity 0 returned success and created a registration. |
| SDEF-006 | 14/03/2026 | F2.3 Reserve ticket | Concurrency | Critical | Critical | Fixed | Two users could both reserve the final remaining seat at the same time. |
| SDEF-007 | 14/03/2026 | F2.3 Reserve ticket | Logic | High | High | Verified | Total active tickets could exceed the 5-ticket limit after multiple reservations. |
| SDEF-008 | 17/03/2026 | F2.4 Cancel ticket | Calculation | Medium | Medium | Open | Refund rounding for the 1-24 hour window was inconsistent for decimal totals. |
| SDEF-009 | 17/03/2026 | F2.4 Cancel ticket | Logic | High | High | Fixed | Cancelling after event start restored capacity, creating exploitable free seats. |
| SDEF-010 | 19/03/2026 | F3.1 Top-up wallet | Logic | High | High | Fixed | QR top-up remained valid after 30 seconds due to incorrect timestamp comparison. |
| SDEF-011 | 19/03/2026 | F3.1 Top-up wallet | Logic | Medium | Medium | Verified | A second pending top-up could be created instead of rejecting the duplicate request. |
| SDEF-012 | 19/03/2026 | F3.2 Confirm top-up | Security | High | High | Open | Random top-up reference returned 500 and exposed internal stack trace information. |
| SDEF-013 | 21/03/2026 | F4.1 Owned event request | Validation | Medium | Medium | Fixed | Capacity 6000 was accepted although the limit is 1 to 5000. |
| SDEF-014 | 21/03/2026 | F4.1 Owned event request | Validation | Low | Low | Open | Invalid latitude and longitude were accepted and caused map rendering issues. |
| SDEF-015 | 21/03/2026 | F4.3 Admin moderate | Validation | High | High | Reopened | Admin could reject a request with an empty review note. |
| SDEF-016 | 24/03/2026 | F4.3 Admin moderate | Logic | Critical | Critical | Verified | Removing a participant cancelled the registration but did not refund the user's wallet. |
| SDEF-017 | 24/03/2026 | F5.1 Notifications | Retention | Medium | Low | Verified | Notifications older than 5 days were not purged on login, slowing notification page load. |
| SDEF-018 | 26/03/2026 | F5.2 Issue Report | Validation | Medium | Medium | Fixed | Description with exactly 10 characters was rejected due to an off-by-one boundary error. |
| SDEF-019 | 26/03/2026 | F5.3 Admin Analytics | Reporting | High | High | Open | Analytics revenue included cancelled registrations. |
| SDEF-020 | 28/03/2026 | F1.5 Profile / Avatar | Validation | Medium | Medium | Verified | JPG avatar larger than 2MB was accepted and stored. |
| SDEF-021 | 28/03/2026 | F1.1 Register account | Security | Critical | Critical | Open | Registration payload with `role=admin` created an admin account. |
| SDEF-022 | 28/03/2026 | F1.2 Login | Security | Critical | High | Fixed | Invalid session token could still return cached personal data from another user. |
| SDEF-023 | 31/03/2026 | F1.3 Reset password | Validation | High | High | Fixed | Reset password accepted a new password shorter than 8 characters. |
| SDEF-024 | 31/03/2026 | F1.4 Change password | Security | Critical | Critical | Open | Change password succeeded even when the current password was incorrect. |
| SDEF-025 | 02/04/2026 | F1.5 Update profile | Logic | Medium | Medium | Verified | Vietnamese phone normalization kept the leading zero after adding `+84`. |
| SDEF-026 | 02/04/2026 | F2.1 Event list | Access Control | High | High | Reopened | Dashboard showed pending and rejected future events to normal users. |
| SDEF-027 | 04/04/2026 | F2.2 Event detail | Access Control | High | High | Open | Normal users could open the direct URL of a pending event detail page. |
| SDEF-028 | 04/04/2026 | F2.2 Event detail | Calculation | Medium | Medium | Fixed | Decimal ticket prices were rounded to integers on the detail page. |
| SDEF-029 | 04/04/2026 | F2.3 Reserve ticket | Error Handling | Medium | Medium | Open | Unknown `ticket_label` caused a 500 response instead of falling back safely. |
| SDEF-030 | 07/04/2026 | F2.3 Reserve ticket | Accounting | High | High | Verified | Paid reservation deducted user balance but did not increase event escrow balance. |
| SDEF-031 | 07/04/2026 | F2.4 Cancel registration | Logic | High | High | Open | Checked-in registration could still be cancelled and refunded. |
| SDEF-032 | 09/04/2026 | F2.5 Registration history | Retention | Low | Low | Verified | Cancelled registrations older than 1 day still appeared in history. |
| SDEF-033 | 09/04/2026 | F3.1 Top-up wallet | Calculation | Medium | Medium | Fixed | Amount 123.456 was truncated to 123.45 instead of rounded to 123.46. |
| SDEF-034 | 11/04/2026 | F3.2 Confirm top-up | Concurrency | Critical | Critical | Closed | Double-clicking confirm top-up credited the same reference twice. |
| SDEF-035 | 11/04/2026 | F3.3 Wallet history | Logic | High | High | Open | Wallet history displayed incorrect `balance_after` after a top-up, charge, and refund sequence. |
| SDEF-036 | 11/04/2026 | F4.1 Submit event request | Validation | High | High | Fixed | Registration deadline after event start was accepted. |
| SDEF-037 | 14/04/2026 | F4.2 Edit/delete request | Workflow | Medium | Medium | Open | Editing a rejected request did not reset status to pending or notify admin. |
| SDEF-038 | 14/04/2026 | F4.3 Admin moderate | Logic | Critical | Critical | Reopened | Approving an already approved request created a duplicate event. |
| SDEF-039 | 16/04/2026 | F5.1 Notifications | Logic | Medium | Medium | Verified | Event reminders were duplicated on each login within the same 24-hour window. |
| SDEF-040 | 16/04/2026 | F5.3 Admin Analytics | Reporting | High | High | Fixed | Analytics counted registration rows instead of ticket quantity. |
| SDEF-041 | 18/04/2026 | F1.4 Change password | Validation | Medium | Medium | Fixed | New password identical to the current password was accepted. |
| SDEF-042 | 18/04/2026 | F2.1 Event list | Usability | Low | Medium | Closed | Invalid date filter range returned an empty list without a validation message. |
| SDEF-043 | 18/04/2026 | F2.2 Event detail | Usability | Medium | Medium | Fixed | Event detail page did not display `registration_deadline` even though the API returned it. |
| SDEF-044 | 21/04/2026 | F2.3 Reserve ticket | Transaction | Critical | Critical | Fixed | Registration was created before payment failure was handled for insufficient wallet balance. |
| SDEF-045 | 21/04/2026 | F2.4 Cancel registration | Concurrency | Critical | Critical | Verified | Double-clicking cancel created duplicate refund transactions. |
| SDEF-046 | 23/04/2026 | F3.1 Top-up wallet | Validation | High | High | Open | Top-up amount above the configured limit still created a pending QR request. |
| SDEF-047 | 23/04/2026 | F4.1 Submit event request | Validation | High | High | Fixed | Registration deadline equal to event start time was accepted. |
| SDEF-048 | 25/04/2026 | F4.2 Edit/delete request | Workflow | High | High | Closed | Owner could delete an approved request while the published event remained active. |
| SDEF-049 | 25/04/2026 | F5.1 Notifications | Access Control | Critical | Critical | Verified | Mark all as read updated notifications belonging to other users. |
| SDEF-050 | 25/04/2026 | F5.3 Admin Analytics | Reporting | Medium | Medium | Open | Invalid analytics date range reused cached chart data from the previous filter. |

## Summary

| Source | Open | In Progress | Fixed | Verified | Closed | Reopened | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Unit test defects | 4 | 3 | 8 | 4 | 0 | 1 | 20 |
| System test defects | 15 | 0 | 17 | 12 | 3 | 3 | 50 |
| Total | 19 | 3 | 25 | 16 | 3 | 4 | 70 |

## Severity Guide

- Blocker: demo cannot continue
- Critical: core requirement broken
- Major: important but workaround exists
- Minor: cosmetic or low business impact
