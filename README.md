# API Contract Sentinel 🛡️

A Python-based tool that compares two versions of an API specification and detects potentially breaking changes.

## 📌 Project Overview

APIs often change as applications evolve. However, an API change can break existing applications that depend on the previous API contract.

**API Contract Sentinel** compares an old and a new OpenAPI specification to identify selected compatibility issues and generate a structured report with explanations and suggested fixes.

## ✨ Features

* Detect removed API endpoints.
* Detect removed response fields.
* Detect changed response field data types.
* Detect newly required request fields.
* Classify detected changes as Breaking or Potentially Breaking.
* Generate a JSON comparison report.
* Validate JSON specification files.
* Handle missing files and invalid JSON.
* Run automated tests using pytest.

## 🛠️ Tech Stack

* **Language:** Python
* **Specification Format:** OpenAPI JSON
* **Testing:** pytest
* **Version Control:** Git and GitHub

## 📂 Project Structure

```text
API-Contract-Sentinel/
├── src/
│   └── api_contract_sentinel/
│       ├── __init__.py
│       └── comparator.py
├── tests/
│   ├── __init__.py
│   └── test_comparator.py
├── examples/
│   ├── old_api.json
│   └── new_api.json
├── docs/
│   └── comparison_report.json
├── check_comparator.py
├── .gitignore
└── README.md
```

## ⚙️ Requirements

* Python 3.13 or a compatible Python version
* Git

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Kishankr76/API-Contract-Sentinel.git
cd API-Contract-Sentinel
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install pytest

```bash
python -m pip install pytest
```

## ▶️ Usage

Run the comparison script from the project root directory:

```bash
python check_comparator.py
```

The tool compares the example specifications in the `examples/` directory and prints the detected changes.

The generated JSON report is saved to:

```text
docs/comparison_report.json
```

## 🧪 Run Tests

Execute the automated test suite:

```bash
python -m pytest -v
```

The tests cover change detection, error handling, report generation logic, and identical specifications.

## 🔍 Example Detected Changes

| Change                           | Classification       |
| -------------------------------- | -------------------- |
| API endpoint removed             | Breaking             |
| Response field removed           | Breaking             |
| Response field data type changed | Breaking             |
| Request field newly required     | Potentially Breaking |

## 📊 Example Output

```text
Old API Version: 1.0.0
New API Version: 2.0.0
Total Changes Detected: 4
```

The report also includes a description and suggested action for each detected change.

## ⚠️ Current Scope

This is an initial implementation focused on selected OpenAPI JSON compatibility checks.

The current implementation does not yet provide complete OpenAPI compatibility analysis. It focuses on the change types listed above.

## 🔮 Planned Improvements

* Add a FastAPI backend.
* Build a Streamlit user interface.
* Support YAML specifications.
* Add more schema compatibility checks.
* Integrate automated testing with GitHub Actions.
* Deploy the application for online access.

## 👨‍💻 Author

**Kishan Kumar**

GitHub: https://github.com/Kishankr76

## 📄 License

No license has been added yet. Licensing can be configured when the project is prepared for public reuse.
