
from pathlib import Path

from src.api_contract_sentinel.comparator import (
    find_removed_response_fields,
    load_specification,
)


BASE_DIR = Path(__file__).resolve().parent.parent


def test_removed_response_field_is_detected():
    old_spec = load_specification(
        str(BASE_DIR / "examples" / "old_api.json")
    )

    new_spec = load_specification(
        str(BASE_DIR / "examples" / "new_api.json")
    )

    changes = find_removed_response_fields(old_spec, new_spec)

    removed_fields = [change["field"] for change in changes]

    assert "email" in removed_fields


def test_removed_endpoint_is_detected():
    old_spec = load_specification(
        str(BASE_DIR / "examples" / "old_api.json")
    )

    new_spec = load_specification(
        str(BASE_DIR / "examples" / "new_api.json")
    )

    from src.api_contract_sentinel.comparator import find_removed_endpoints

    changes = find_removed_endpoints(old_spec, new_spec)

    removed_endpoints = [
        (change["method"], change["endpoint"])
        for change in changes
    ]

    assert ("GET", "/products") in removed_endpoints


def test_changed_response_field_type_is_detected():
    old_spec = load_specification(
        str(BASE_DIR / "examples" / "old_api.json")
    )

    new_spec = load_specification(
        str(BASE_DIR / "examples" / "new_api.json")
    )

    from src.api_contract_sentinel.comparator import find_changed_field_types

    changes = find_changed_field_types(old_spec, new_spec)

    changed_fields = [
        (change["field"], change["old_type"], change["new_type"])
        for change in changes
    ]

    assert ("id", "integer", "string") in changed_fields


def test_newly_required_request_field_is_detected():
    old_spec = load_specification(
        str(BASE_DIR / "examples" / "old_api.json")
    )

    new_spec = load_specification(
        str(BASE_DIR / "examples" / "new_api.json")
    )

    from src.api_contract_sentinel.comparator import find_newly_required_fields

    changes = find_newly_required_fields(old_spec, new_spec)

    newly_required_fields = [
        (change["method"], change["endpoint"], change["field"])
        for change in changes
    ]

    assert ("POST", "/users", "email") in newly_required_fields


import pytest

from src.api_contract_sentinel.comparator import load_specification


def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError, match="Specification file not found"):
        load_specification("this_file_does_not_exist.json")


def test_invalid_json_raises_error(tmp_path):
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{invalid json}", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_specification(str(invalid_file))


def test_compare_specifications_returns_all_changes():
    from src.api_contract_sentinel.comparator import compare_specifications

    old_spec = load_specification(
        str(BASE_DIR / "examples" / "old_api.json")
    )

    new_spec = load_specification(
        str(BASE_DIR / "examples" / "new_api.json")
    )

    report = compare_specifications(old_spec, new_spec)

    assert report["old_version"] == "1.0.0"
    assert report["new_version"] == "2.0.0"
    assert report["total_changes"] == 4
    assert len(report["changes"]) == 4


def test_identical_specifications_return_no_changes():
    from src.api_contract_sentinel.comparator import compare_specifications

    specification = {
        "openapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0"
        },
        "paths": {
            "/users": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Success"
                        }
                    }
                }
            }
        }
    }

    report = compare_specifications(specification, specification)

    assert report["total_changes"] == 0
    assert report["changes"] == []



