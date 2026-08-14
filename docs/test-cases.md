# Test Cases

This document is the **source-derived test-case matrix** for the framework. Every test below maps 1:1 to a test method in `tests/`. The totals are verified by `pytest --collect-only -q`.

- **181 collected test cases**
- **171 test functions** (5 data-driven functions are parameterized and expand to 15 instances, adding 10 extra cases)

---

## 1. Totals by Suite

| Suite | File(s) | Cases |
|-------|---------|-------|
| Login | `tests/test_login.py` | 16 |
| Logout | `tests/test_logout.py` | 7 |
| Cart | `tests/test_cart.py` | 18 |
| Checkout | `tests/test_checkout.py` | 20 |
| Search / Catalog | `tests/test_search.py` | 15 |
| Home UI | `tests/ui/test_home.py` | 18 |
| Product UI | `tests/ui/test_product.py` | 10 |
| Negative scenarios | `tests/test_negative_scenarios.py` | 12 |
| API workflow | `tests/api/test_api_workflow.py` | 11 |
| API validation | `tests/api/test_api_validation.py` | 8 |
| API negative | `tests/api/test_api_negative.py` | 8 |
| DB validation | `tests/database/test_db_validation.py` | 6 |
| DB data integrity | `tests/database/test_data_integrity.py` | 6 |
| E2E journey | `tests/e2e/test_end_to_end_journey.py` | 2 |
| E2E purchase | `tests/e2e/test_purchase_workflow.py` | 2 |
| Regression | `tests/regression/test_regression_suite.py` | 5 |
| Cross-browser | `tests/ui/test_cross_browser.py` | 2 |
| Data-driven | `tests/ui/test_data_driven.py` | 15 (5 fns) |
| **Total** | | **181** |

---

## 2. Marker Coverage

| Marker | Count | Meaning |
|--------|-------|---------|
| `smoke` | 21 | Critical flows |
| `regression` | 144 | Full regression |
| `ui` | 135 | All Selenium UI tests |
| `api` | 32 | REST API tests |
| `db` / `database` | 14 | Database tests |
| `e2e` | 6 | End-to-end journeys |
| `negative` | 25 | Negative scenarios |
| `login` | 16 | Login suite |
| `cart` | 18 | Cart suite |
| `checkout` | 20 | Checkout suite |
| `search` | 15 | Search suite |
| `product` | 43 | Product-related (search+home+product) |
| `cross_browser` | 2 | Cross-browser |

---

## 3. Login — 16 cases (`tests/test_login.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| LOG-01 | `test_valid_user_login` | Standard user logs in with valid Excel credentials |
| LOG-02 | `test_invalid_username_shows_error` | Non-existent username shows "do not match" error |
| LOG-03 | `test_invalid_password_shows_error` | Wrong password shows error (Excel invalid user) |
| LOG-04 | `test_empty_username_shows_error` | Empty username → "Username is required" |
| LOG-05 | `test_empty_password_shows_error` | Empty password → "Password is required" |
| LOG-06 | `test_locked_out_user_error` | Locked-out user blocked with specific message |
| LOG-07 | `test_blank_credentials_error` | Blank form → "Username is required" |
| LOG-08 | `test_password_field_is_masked` | Password input has `type="password"` |
| LOG-09 | `test_login_button_state_and_behavior` | Login button enabled and responsive |
| LOG-10 | `test_browser_refresh_preserves_authenticated_session` | Session persists after page refresh |
| LOG-11 | `test_direct_navigation_to_protected_page_without_login` | /inventory.html redirects unauthenticated users |
| LOG-12 | `test_invalid_username_and_invalid_password_shows_error` | Both invalid → error message |
| LOG-13 | `test_login_error_message_dismissable` | Error banner closes via 'X' |
| LOG-14 | `test_login_error_disappears_after_valid_login` | Recovery from failed attempt |
| LOG-15 | `test_login_multiple_user_roles_excel` | Multiple valid users iterate via Excel |
| LOG-16 | `test_login_after_logout_succeeds` | Re-login works after logout in same session |

---

## 4. Logout — 7 cases (`tests/test_logout.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| LOGOUT-01 | `test_logout_returns_to_login_page` | Logout redirects to login and clears session |
| LOGOUT-02 | `test_protected_page_cannot_be_accessed_after_logout` | /inventory.html blocked after logout |
| LOGOUT-03 | `test_protected_cart_page_cannot_be_accessed_after_logout` | /cart.html blocked after logout |
| LOGOUT-04 | `test_protected_checkout_page_cannot_be_accessed_after_logout` | /checkout-step-one.html blocked after logout |
| LOGOUT-05 | `test_browser_back_button_after_logout` | Back button does not re-authenticate |
| LOGOUT-06 | `test_page_refresh_after_logout_stays_on_login` | Refresh after logout stays on login |
| LOGOUT-07 | `test_login_again_after_logout_in_same_session` | Immediate re-login works |

---

## 5. Cart — 18 cases (`tests/test_cart.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| CART-01 | `test_add_product_to_cart` | Add item; appears in cart list |
| CART-02 | `test_add_second_product_to_cart` | Two items → badge 2, both listed |
| CART-03 | `test_add_multiple_products_to_cart` | Three distinct items populate cart |
| CART-04 | `test_cart_badge_count_reflects_items` | Badge number equals item count |
| CART-05 | `test_cart_item_name_validation` | Cart name matches catalog |
| CART-06 | `test_cart_item_price_validation` | Cart price matches catalog |
| CART-07 | `test_cart_item_unit_prices_and_quantities` | Unit prices & quantities correct |
| CART-08 | `test_remove_product_from_cart` | Remove single item |
| CART-09 | `test_remove_multiple_products_from_cart` | Selective removal leaves remainder |
| CART-10 | `test_remove_all_products_from_cart` | Bulk removal → empty cart, badge 0 |
| CART-11 | `test_continue_shopping_returns_to_inventory` | Continue Shopping returns to catalog |
| CART-12 | `test_navigate_from_cart_to_checkout` | Checkout button → step one |
| CART-13 | `test_cart_persistence_after_browser_refresh` | Cart persists across refresh |
| CART-14 | `test_cart_subtotal_dynamic_calculation` | Subtotal = Σ(price×qty) |
| CART-15 | `test_cart_item_order_preserved` | Items keep add order |
| CART-16 | `test_add_remove_and_re_add_product_to_cart` | Add/remove/re-add cycle |
| CART-17 | `test_cart_badge_disappears_when_cart_is_empty` | Badge removed at 0 items |
| CART-18 | `test_cart_data_integrity_across_session_navigation` | Cart persists home↔details↔cart |

---

## 6. Checkout — 20 cases (`tests/test_checkout.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| CHK-01 | `test_complete_checkout_successfully` | Full checkout with valid data (smoke/e2e) |
| CHK-02 | `test_checkout_empty_form_validation` | Empty form → "First Name is required" |
| CHK-03 | `test_checkout_requires_first_name` | Missing first name error |
| CHK-04 | `test_checkout_requires_last_name` | Missing last name error |
| CHK-05 | `test_checkout_requires_postal_code` | Missing postal code error |
| CHK-06 | `test_checkout_first_name_whitespace_only` | Whitespace-only first name handled |
| CHK-07 | `test_checkout_last_name_special_characters` | Hyphen/apostrophe names accepted |
| CHK-08 | `test_checkout_postal_code_alphanumeric_formats` | International postcodes accepted |
| CHK-09 | `test_checkout_error_dismissal_behavior` | Error banner 'X' closes |
| CHK-10 | `test_checkout_overview_page_loaded` | Overview step 2 loads |
| CHK-11 | `test_checkout_overview_item_names` | Overview names match cart |
| CHK-12 | `test_checkout_overview_item_prices` | Overview prices match catalog |
| CHK-13 | `test_order_summary_subtotal_calculation` | Subtotal math verified |
| CHK-14 | `test_order_summary_tax_calculation` | Tax = 8% of subtotal |
| CHK-15 | `test_order_summary_pricing_calculation` | Total = subtotal + tax |
| CHK-16 | `test_complete_order_confirmation_header` | "Thank you for your order!" header |
| CHK-17 | `test_complete_order_description_text` | Dispatch description text |
| CHK-18 | `test_cart_is_empty_after_successful_checkout` | Cart reset after purchase (e2e) |
| CHK-19 | `test_cancel_checkout_step_one_returns_to_cart` | Cancel step 1 → cart |
| CHK-20 | `test_cancel_checkout_step_two_returns_to_inventory` | Cancel step 2 → inventory |

---

## 7. Search / Catalog — 15 cases (`tests/test_search.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| SRCH-01 | `test_product_is_listed_and_searchable_by_name` | Product present in listing |
| SRCH-02 | `test_search_partial_product_name` | Partial string match |
| SRCH-03 | `test_search_case_insensitive_matching` | Case-insensitive matches |
| SRCH-04 | `test_search_non_existent_product_returns_empty` | Unknown query → 0 matches |
| SRCH-05 | `test_search_special_characters_returns_no_matches` | Special chars → no crash, 0 matches |
| SRCH-06 | `test_search_empty_input_returns_all_products` | Empty query → all 6 products |
| SRCH-07 | `test_search_numeric_input_handling` | Numeric query handled safely |
| SRCH-08 | `test_catalog_displays_all_product_cards` | 6 cards, valid prices |
| SRCH-09 | `test_catalog_images_are_loaded_and_valid` | 6 valid image sources |
| SRCH-10 | `test_product_sorting_name_az` | A→Z sort |
| SRCH-11 | `test_product_sorting_name_za` | Z→A sort |
| SRCH-12 | `test_product_sorting_price_low_to_high` | Price ascending |
| SRCH-13 | `test_product_sorting_price_high_to_low` | Price descending |
| SRCH-14 | `test_open_product_details` | Detail view matches name & price |
| SRCH-15 | `test_product_price_and_desc_consistency_between_home_and_details` | Home↔detail consistency + back nav |

---

## 8. Home UI — 18 cases (`tests/ui/test_home.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| HOME-01 | `test_home_page_loads_successfully` | "Products" header after auth |
| HOME-02 | `test_product_inventory_is_displayed` | Inventory container visible |
| HOME-03 | `test_product_count_matches_expected` | Exactly 6 products |
| HOME-04 | `test_all_product_names_are_non_empty_and_valid` | Names non-empty, expected format |
| HOME-05 | `test_all_product_prices_are_positive_and_formatted` | `$` prefix + positive float |
| HOME-06 | `test_all_product_images_are_loaded` | 6 valid image sources |
| HOME-07 | `test_product_cards_structure_and_elements` | Card has title/desc/price/button |
| HOME-08 | `test_product_sorting_name_a_to_z` | A→Z with edge names |
| HOME-09 | `test_product_sorting_name_z_to_a` | Z→A with edge names |
| HOME-10 | `test_product_sorting_price_low_to_high` | Ascending price, 7.99→49.99 |
| HOME-11 | `test_product_sorting_price_high_to_low` | Descending price, 49.99→7.99 |
| HOME-12 | `test_navigate_to_product_detail_page` | Card → detail URL |
| HOME-13 | `test_product_detail_title_matches_catalog` | Detail title matches |
| HOME-14 | `test_product_detail_price_matches_catalog` | Detail price matches |
| HOME-15 | `test_product_detail_description_matches_catalog` | Description present/valid |
| HOME-16 | `test_product_detail_image_is_valid` | Hero image valid |
| HOME-17 | `test_navigate_back_from_product_detail` | Back → inventory.html |
| HOME-18 | `test_catalog_and_detail_info_consistency` | Name/price/desc consistency |

---

## 9. Product UI — 10 cases (`tests/ui/test_product.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| PROD-01 | `test_open_product_detail_view` | Card → detail URL |
| PROD-02 | `test_product_detail_title_validation` | Title matches |
| PROD-03 | `test_product_detail_price_validation` | Price string + float |
| PROD-04 | `test_product_detail_description_validation` | Description non-empty/accurate |
| PROD-05 | `test_product_detail_image_src_validation` | Valid image src |
| PROD-06 | `test_add_product_to_cart_from_detail_page` | Add → button becomes "Remove" |
| PROD-07 | `test_cart_badge_increments_from_detail_page` | Badge = 1 after add |
| PROD-08 | `test_remove_product_from_cart_on_detail_page` | Remove → "Add to cart" restored, badge 0 |
| PROD-09 | `test_navigate_back_to_catalog_from_detail` | Back to products → 6 items |
| PROD-10 | `test_product_detail_state_persistence_on_return` | Cart state persists on return |

---

## 10. Negative Scenarios — 12 cases (`tests/test_negative_scenarios.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| NEG-01 | `test_negative_login_locked_user_blocked` | Locked user blocked |
| NEG-02 | `test_negative_login_invalid_password` | Invalid password rejected |
| NEG-03 | `test_negative_login_empty_username_and_password` | Blank form rejected |
| NEG-04 | `test_negative_checkout_missing_postal_code` | Checkout without postal rejected |
| NEG-05 | `test_negative_checkout_missing_first_and_last_name` | Checkout without names rejected |
| NEG-06 | `test_negative_unauthorized_cart_access_after_logout` | /cart.html blocked after logout |
| NEG-07 | `test_negative_unauthorized_checkout_access_after_logout` | /checkout-step-one.html blocked after logout |
| NEG-08 | `test_negative_api_get_non_existent_resource_404` | GET unknown ID → 404 |
| NEG-09 | `test_negative_api_invalid_endpoint_404` | GET invalid endpoint → 404 |
| NEG-10 | `test_negative_api_empty_post_payload` | POST empty payload handled safely |
| NEG-11 | `test_negative_api_put_invalid_resource_404` | PUT unknown ID → 404/500 |
| NEG-12 | `test_negative_db_mismatch_assertion` | DB mismatch detected + clear assertion |

---

## 11. API Workflow — 11 cases (`tests/api/test_api_workflow.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| APIW-01 | `test_login_api_success` | Login API returns resource ID |
| APIW-02 | `test_get_users_list_validation` | GET list, status 200, non-empty |
| APIW-03 | `test_post_create_user` | POST creates record with ID |
| APIW-04 | `test_put_update_user` | PUT updates record |
| APIW-05 | `test_delete_user` | DELETE returns 200 |
| APIW-06 | `test_get_single_resource_and_schema_validation` | GET by ID + schema keys |
| APIW-07 | `test_get_invalid_endpoint_returns_404` | Invalid endpoint → 404 |
| APIW-08 | `test_get_invalid_resource_id_returns_404` | Unknown ID → 404 |
| APIW-09 | `test_api_response_headers_and_content_type` | Content-Type application/json |
| APIW-10 | `test_api_response_time_threshold` | Response < 3.0s SLA |
| APIW-11 | `test_bearer_token_authorization_header` | Bearer header formatting |

---

## 12. API Validation — 8 cases (`tests/api/test_api_validation.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| APIV-01 | `test_api_status_code_success_200` | GET valid resource → 200 |
| APIV-02 | `test_api_response_headers_content_type` | JSON content-type header |
| APIV-03 | `test_api_response_schema_required_keys` | Required schema keys present |
| APIV-04 | `test_api_field_data_types_validation` | Strict data types (int/str) |
| APIV-05 | `test_api_query_parameter_filtering` | Query filtering by userId |
| APIV-06 | `test_api_response_time_sla` | Response < 3.0s |
| APIV-07 | `test_api_post_creation_payload_echo` | POST echoes payload |
| APIV-08 | `test_api_put_update_payload_echo` | PUT returns updated content |

---

## 13. API Negative — 8 cases (`tests/api/test_api_negative.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| APIN-01 | `test_api_negative_get_non_existent_resource_404` | GET unknown ID → 404 |
| APIN-02 | `test_api_negative_get_invalid_endpoint_404` | Invalid URI → 404 |
| APIN-03 | `test_api_negative_post_empty_payload` | POST empty dict safe |
| APIN-04 | `test_api_negative_post_missing_required_fields` | POST missing fields handled |
| APIN-05 | `test_api_negative_post_invalid_data_type` | Invalid data types handled |
| APIN-06 | `test_api_negative_put_non_existent_resource` | PUT unknown ID → 404/500 |
| APIN-07 | `test_api_negative_delete_non_existent_resource` | DELETE unknown ID → 200/404 |
| APIN-08 | `test_api_negative_invalid_authorization_header` | Malformed auth header safe |

---

## 14. Database Validation — 6 cases (`tests/database/test_db_validation.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| DBV-01 | `test_ui_product_price_matches_database_record` | UI price vs DB record |
| DBV-02 | `test_database_catalog_record_count_and_existence` | 6 active catalog records + SKUs |
| DBV-03 | `test_database_required_fields_not_null` | No NULL required fields |
| DBV-04 | `test_database_no_duplicate_sku_records` | Unique SKUs |
| DBV-05 | `test_database_price_data_type_and_format` | Prices are positive floats |
| DBV-06 | `test_database_mismatch_raises_assertion_error` | Mismatch raises AssertionError |

---

## 15. Database Data Integrity — 6 cases (`tests/database/test_data_integrity.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| DBI-01 | `test_db_connection_health_check` | Engine connects, query executes |
| DBI-02 | `test_db_product_lookup_by_sku` | Lookup by unique SKU |
| DBI-03 | `test_db_inventory_counts_are_positive` | Stock count > 0 |
| DBI-04 | `test_db_active_status_constraint` | is_active flag in (0,1) |
| DBI-05 | `test_db_batch_ui_catalog_consistency` | Batch UI↔DB consistency |
| DBI-06 | `test_db_non_existent_product_returns_empty` | Unknown SKU → empty result |

---

## 16. E2E — 4 cases (`tests/e2e/`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| E2E-01 | `test_complete_e2e_shopping_journey` (`test_end_to_end_journey.py`) | Full journey: login→browse→details→cart→checkout→confirm→logout |
| E2E-02 | `test_e2e_multi_item_selective_removal_checkout` (`test_end_to_end_journey.py`) | Multi-item + selective removal + checkout |
| E2E-03 | `test_e2e_browse_detail_continue_shopping_workflow` (`test_purchase_workflow.py`) | Browse→detail→add→continue→checkout→logout |
| E2E-04 | `test_e2e_sorted_catalog_bundle_purchase` (`test_purchase_workflow.py`) | Sort→bundle (max+min price)→checkout |

---

## 17. Regression — 5 cases (`tests/regression/test_regression_suite.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| REG-01 | `test_regression_ui_auth_and_catalog_navigation` | Auth + catalog + sort sanity |
| REG-02 | `test_regression_ui_cart_and_checkout_integrity` | Cart math + checkout integrity |
| REG-03 | `test_regression_ui_session_termination_security` | Logout + protected-page redirect |
| REG-04 | `test_regression_api_service_lifecycle` | API GET/POST/PUT/DELETE lifecycle |
| REG-05 | `test_regression_database_catalog_consistency` | DB schema + catalog verification |

---

## 18. Cross-Browser — 2 cases (`tests/ui/test_cross_browser.py`)

| ID | Test Method | Purpose |
|----|-------------|---------|
| XB-01 | `test_cross_browser_login_and_catalog_render` | Login + 6-product render |
| XB-02 | `test_cross_browser_cart_and_checkout_flow` | Cart + checkout flow |

---

## 19. Data-Driven — 15 cases, 5 functions (`tests/ui/test_data_driven.py`)

| ID | Function | Parametrized Cases | Data Source |
|----|----------|--------------------|-------------|
| DD-01 | `test_ddt_valid_login_json` | 2 (valid users) | `testdata/json/login_data.json` |
| DD-02 | `test_ddt_invalid_login_json` | 2 (invalid users) | `testdata/json/login_data.json` |
| DD-03 | `test_ddt_login_csv` | 3 (login-success users) | `testdata/csv/users.csv` |
| DD-04 | `test_ddt_checkout_completion_json` | 2 (valid customers) | `testdata/json/checkout_data.json` |
| DD-05 | `test_ddt_search_and_discovery_json` | 6 (search scenarios) | `testdata/json/search_data.json` |

---

## 20. Verified Count

```bash
pytest --collect-only -q
# 181 tests collected
```
