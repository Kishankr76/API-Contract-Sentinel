# API Contract Sentinel

### Detect API Breaking Changes Before They Break Your Application

API Contract Sentinel is a Python-based tool that compares two API specifications and identifies changes that may affect backward compatibility.

It helps developers understand what changed between an old and a new API contract by classifying detected changes according to their severity.

## Problem Statement

When an API changes, existing applications that depend on it may stop working correctly.

For example:

* An API endpoint is removed.
* A response field is deleted.
* A field's data type changes.
* A previously optional request field becomes required.

Detecting these changes before releasing a new API version can help reduce integration issues.

API Contract Sentinel automates the comparison process and generates a structured report of detected changes.

## Features

* **API Specification Comparison:** Compare old and new JSON API specifications.
* **Removed Endpoint Detection:** Identify endpoints that no longer exist in the new specification.
* **Removed Response Field Detection:** Find response fields removed from an existing endpoint.
* **Data Type Change Detection:** Detect changes such as `integer` to `string`.
* **Newly Required Field Detection:** Identify fields that have become mandatory.
* **Severity Classification:** Categorize detected changes as Breaking or Potentially Breaking.
* **Structured Reports:** Generate comparison results in JSON format.
* **Interactive Web Interface:** Upload specifications and view comparison results through Streamlit.
* **REST API:** Access the comparison functionality through a FastAPI backend.
* **Input Validation:** Validate incoming specifications and handle invalid requests.
* **Automated Testing:** Use pytest to test comparison logic and API endpoints.
* **Continuous Integration:** Run automated tests through GitHub Actions when code is pushed to the main branch or a pull request targets it.

## Technology Stack

| Technology     | Purpose                                                                         |
| -------------- | ------------------------------------------------------------------------------- |
| Python         | Core comparison logic                                                           |
| FastAPI        | Backend REST API                                                                |
| Streamlit      | Interactive frontend                                                            |
| Pydantic       | Request validation                                                              |
| Requests       | HTTP communication between frontend and backend                                 |
| JSON           | API specification input and comparison report format                            |
| PyYAML         | YAML-related dependency; full YAML specification support is not yet implemented |
| Pytest         | Automated testing                                                               |
| HTTPX          | Testing FastAPI endpoints                                                       |
| Git and GitHub | Version control and source code hosting                                         |
| GitHub Actions | Continuous integration                                                          |

## System Architecture

```text
              User
                |
                v
       Streamlit Frontend
          (app.py)
                |
                | HTTP POST /compare
                v
        FastAPI Backend
          (api.py)
                |
                v
       Comparison Engine
       (comparator.py)
                |
                v
      Compare Old and New
       API Specifications
                |
                v
       Detect API Changes
                |
                v
       Structured JSON Report
                |
                v
       Streamlit Results View
```

## How It Works

1. The user uploads the old and new API specification files through the Streamlit interface.
2. The frontend reads the uploaded JSON files.
3. The frontend sends both specifications to the FastAPI backend using an HTTP POST request.
4. The backend validates the request using Pydantic.
5. The comparison engine examines the specifications and identifies supported changes.
6. The engine classifies detected changes according to severity.
7. The backend returns the comparison report as JSON.
8. The frontend displays the results and allows the user to download the report.

## Project Structure

```text
API-Contract-Sentinel/
|
|-- .github/
|   `-- workflows/
|       `-- tests.yml
|
|-- docs/
|   `-- comparison_report.json
|
|-- examples/
|   |-- old_api.json
|   `-- new_api.json
|
|-- src/
|   `-- api_contract_sentinel/
|       |-- __init__.py
|       |-- api.py
|       `-- comparator.py
|
|-- tests/
|   |-- __init__.py
|   |-- test_api.py
|   `-- test_comparator.py
|
|-- app.py
|-- check_comparator.py
|-- requirements.txt
|-- README.md
`-- .gitignore
```

## Getting Started

### Prerequisites

* Python 3.13
* Git
* pip

### 1. Open the project directory

Open a terminal in the project root directory:

```powershell
cd C:\Users\dkaru\Documents\API-Contract-Sentinel
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

Run this command from the project root directory:

```powershell
python -m pip install -r requirements.txt
```


### 5. Run the FastAPI backend

Open the first terminal in the project root and run:

```powershell
python -m uvicorn src.api_contract_sentinel.api:app --reload
```

The backend will be available locally at:

* API base: `http://127.0.0.1:8000`
* Interactive API documentation: `http://127.0.0.1:8000/docs`
* Health check: `http://127.0.0.1:8000/health`

Keep this terminal running.

### Live Deployment

The application is deployed using the following services:

* **Frontend:** Streamlit Community Cloud
* **Backend:** Render
* **API Documentation:** FastAPI Swagger UI

Live links:

* Frontend: https://api-contract-sentinel.streamlit.app/
* Backend health check: https://api-contract-sentinel.onrender.com/health
* API documentation: https://api-contract-sentinel.onrender.com/docs

For local development, run both the FastAPI backend and Streamlit frontend as described above.

Note: The free hosting services may sleep during inactivity, so the first request can take longer while the backend starts.


### 6. Run the Streamlit frontend

Open a second terminal in the same project root. Activate the virtual environment if necessary, then run:

```powershell
python -m streamlit run app.py
```

Streamlit will display a local address in the terminal. Open that address in your browser.

**Note:** The frontend currently uses the local FastAPI backend. Both services must be running for the comparison workflow to work.

## API Endpoints

| Method | Endpoint   | Description                            |
| ------ | ---------- | -------------------------------------- |
| GET    | `/`        | Root endpoint                          |
| GET    | `/health`  | Health check                           |
| POST   | `/compare` | Compare old and new API specifications |

### Example Request

Send a POST request to `/compare` with a JSON body containing both specifications:

```json
{
  "old_spec": {
    "openapi": "3.0.0",
    "info": {
      "title": "Sample API",
      "version": "1.0.0"
    },
    "paths": {}
  },
  "new_spec": {
    "openapi": "3.0.0",
    "info": {
      "title": "Sample API",
      "version": "2.0.0"
    },
    "paths": {}
  }
}
```

This example demonstrates the request structure. Since both specifications contain empty paths, it does not demonstrate a detected breaking change.

## Running Tests

Run the automated test suite from the project root:

```powershell
python -m pytest -v
```

The tests cover the comparison engine and FastAPI endpoints, including supported change detection and request validation.

The project has **16 locally passing tests**, as verified during development.

## Continuous Integration

GitHub Actions is configured in:

```text
.github/workflows/tests.yml
```

The workflow runs when:

* Code is pushed to the `main` branch.
* A pull request targets the `main` branch.

The workflow checks out the repository, sets up Python, installs dependencies, and executes:

```powershell
python -m pytest -v
```

A successful workflow run displays a green check mark on GitHub.

## Current Limitations

* The comparison workflow currently accepts JSON API specifications only.
* Full OpenAPI specification validation is not implemented.
* Not every possible OpenAPI schema structure or compatibility rule is supported.
* YAML parsing is not yet integrated into the comparison workflow.
* Database persistence and authentication are not implemented.
* Detection accuracy depends on the API structures and change types supported by the comparison engine.
* The backend is hosted on Render and the frontend on Streamlit Community Cloud. Free hosting services may sleep during inactivity, causing delays on the first request.


## Future Improvements

* Add YAML specification parsing.
* Expand support for nested schemas and additional compatibility rules.
* Improve detection of safe and potentially breaking changes.
* Add automated tests for malformed inputs and complex API specifications.
* Improve report explanations and suggested fixes.
* Consider authentication and persistent comparison history if future requirements justify them.



## Learning Outcomes

Through this project, I practised:

* Python programming and modular code organization.
* API comparison and change-detection logic.
* Building REST endpoints using FastAPI.
* Request validation using Pydantic.
* Connecting a frontend to a backend using HTTP requests.
* Writing automated tests with pytest.
* Using Git and GitHub for version control.
* Setting up a GitHub Actions CI workflow.

## Author

**Kishan Kumar**

GitHub: Kishankr76

---

*API Contract Sentinel is a learning and development project designed to explore API compatibility, automated testing, and continuous integration.*
