# Test Data

This document describes every external dataset used by the framework and how it is loaded.

---

## 1. Data Directory

All external test data lives under **`testdata/`**:

```text
testdata/
├── Login.xlsx              # Excel workbook: valid_users, invalid_users, checkout_users
├── Products.xlsx           # Excel workbook: products
├── csv/
│   ├── users.csv           # Login/role rows
│   ├── products.csv        # Catalog rows (name, price, sku)
│   └── checkout.csv        # Checkout customer rows
└── json/
    ├── login_data.json     # valid_users, invalid_users, locked_users, empty_credentials
    ├── checkout_data.json  # valid_customers, negative_checkout
    ├── search_data.json    # search_scenarios
    └── products_data.json  # catalog_products
```

---

## 2. Data Loading API

### 2.1 `DataProvider.load_data(path, key_or_sheet=None)`

`src/utils/data_provider.py` — dispatches on file extension:

| File | Behavior |
|------|----------|
| `.json` | Returns the list under the given top-level key (`key_or_sheet`) |
| `.csv` | Returns a `list[dict]` of all rows (header → value) |
| `.xlsx` | Returns a `list[dict]` of all rows in the given sheet (`key_or_sheet`) |

### 2.2 `ExcelReader(path)`

`src/utils/excel_reader.py` — `get_sheet_data(sheet)` returns `list[dict]` for a workbook sheet using openpyxl.

---

## 3. Excel Data

### 3.1 `testdata/Login.xlsx`

| Sheet | Purpose | Sample columns |
|-------|---------|----------------|
| `valid_users` | Successful login users | `username`, `password` |
| `invalid_users` | Failed login users | `username`, `password` |
| `checkout_users` | Valid checkout customers | `first_name`, `last_name`, `postal_code` |

Used by: `tests/test_login.py`, `tests/test_logout.py`, `tests/test_cart.py`, `tests/test_checkout.py`, `tests/test_search.py`.

### 3.2 `testdata/Products.xlsx`

| Sheet | Purpose | Sample columns |
|-------|---------|----------------|
| `products` | Catalog items under test | `name`, `price` |

Used by: `tests/test_cart.py`, `tests/test_search.py`, `tests/test_checkout.py`.

---

## 4. JSON Data

### 4.1 `testdata/json/login_data.json`

| Key | Rows | Purpose |
|-----|------|---------|
| `valid_users` | 2 (`standard_user`, `problem_user`) | Successful login (drives DD-01) |
| `invalid_users` | 2 | Failed login with `expected_error` (drives DD-02) |
| `locked_users` | 1 | Locked-out user message |
| `empty_credentials` | 3 | Blank username / password / both |

### 4.2 `testdata/json/checkout_data.json`

| Key | Rows | Purpose |
|-----|------|---------|
| `valid_customers` | 2 | Successful checkout (drives DD-04) |
| `negative_checkout` | 4 | Missing fields + `expected_error` |

### 4.3 `testdata/json/search_data.json`

| Key | Rows | Purpose |
|-----|------|---------|
| `search_scenarios` | 6 | Query → `expected_match_count` + optional `expected_product_name` (drives DD-05) |

### 4.4 `testdata/json/products_data.json`

| Key | Rows | Purpose |
|-----|------|---------|
| `catalog_products` | 6 | Full catalog: `name`, `price`, `price_float`, `description` |

---

## 5. CSV Data

### 5.1 `testdata/csv/users.csv`

| Row | username | password | role | expected_result |
|-----|----------|----------|------|-----------------|
| 1 | standard_user | secret_sauce | standard | login_success |
| 2 | problem_user | secret_sauce | problem | login_success |
| 3 | visual_user | secret_sauce | visual | login_success |
| 4 | invalid_user | invalid_password | invalid | login_failure |
| 5 | locked_out_user | secret_sauce | locked | login_failure |

`test_ddt_login_csv` filters to `expected_result == "login_success"` → **3 cases** (DD-03).

### 5.2 `testdata/csv/products.csv`

6 catalog rows (`name`, `price`, `sku`) — mirrors the SauceDemo catalog and `Products.xlsx`.

### 5.3 `testdata/csv/checkout.csv`

| Row | first_name | last_name | postal_code | scenario |
|-----|-----------|-----------|-------------|----------|
| 1 | John | Doe | 10001 | valid_us |
| 2 | Emma | Watson | SW1A 1AA | valid_uk |
| 3 | Raj | Patel | 560001 | valid_in |
| 4 | (blank) | Doe | 10001 | missing_first_name |
| 5 | John | (blank) | 10001 | missing_last_name |
| 6 | John | Doe | (blank) | missing_postal_code |
| 7 | (blank) | (blank) | (blank) | empty_all |

---

## 6. In-Memory Database Data

The database suites create an **isolated in-memory SQLite** catalog inside each test (`:memory:`), so they require no external server:

| Column | Sample |
|--------|--------|
| `id` | 1–6 |
| `name` | Sauce Labs Backpack, Bike Light, Bolt T-Shirt, Fleece Jacket, Onesie, Test.allTheThings() T-Shirt (Red) |
| `price` | `$29.99`, `$9.99`, `$15.99`, `$49.99`, `$7.99`, `$15.99` |
| `price_float` | matching float values |
| `sku` | `SAUCE-BACKPACK-01` … `SAUCE-REDSHIRT-06` (unique) |
| `inventory_count` | 50, 40, 30, 20, 100, 15 |
| `is_active` | 1 for all |

---

## 7. Adding New Test Data

1. Place the file under `testdata/` (e.g., `testdata/json/my_data.json`).
2. Load it with `DataProvider.load_data(Path("testdata/json/my_data.json"), key_or_sheet="my_key")`.
3. To parameterize a UI test, decorate it with `@pytest.mark.parametrize` passing the loaded list — see `tests/ui/test_data_driven.py` for the pattern.

> **Excel note:** `.xlsx` files are committed to the repository. Do not store credentials beyond the demo `secret_sauce` value in any dataset.