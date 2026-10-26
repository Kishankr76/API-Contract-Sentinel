
import json
from pathlib import Path



def load_specification(file_path: str) -> dict:
    """Load and validate an OpenAPI specification from a JSON file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Specification file not found: {path}"
        )

    try:
        with path.open("r", encoding="utf-8") as file:
            specification = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in specification file: {path}"
        ) from error

    if not isinstance(specification, dict):
        raise ValueError(
            "OpenAPI specification must be a JSON object."
        )

    return specification




def find_removed_response_fields(
    old_spec: dict,
    new_spec: dict,
) -> list[dict]:
    """Find response fields that existed before but are missing now."""
    changes = []

    old_paths = old_spec.get("paths", {})
    new_paths = new_spec.get("paths", {})

    for endpoint, old_operations in old_paths.items():
        new_operations = new_paths.get(endpoint, {})

        for method, old_operation in old_operations.items():
            new_operation = new_operations.get(method)

            if new_operation is None:
                continue

            old_responses = old_operation.get("responses", {})
            new_responses = new_operation.get("responses", {})

            for status_code, old_response in old_responses.items():
                new_response = new_responses.get(status_code)

                if new_response is None:
                    continue

                old_content = old_response.get("content", {})
                new_content = new_response.get("content", {})

                for media_type, old_media in old_content.items():
                    new_media = new_content.get(media_type)

                    if new_media is None:
                        continue

                    old_schema = old_media.get("schema", {})
                    new_schema = new_media.get("schema", {})

                    old_properties = old_schema.get("properties", {})
                    new_properties = new_schema.get("properties", {})

                    removed_fields = old_properties.keys() - new_properties.keys()

                    for field in sorted(removed_fields):
                        changes.append(
                            {
                                "endpoint": endpoint,
                                "method": method.upper(),
                                "status_code": status_code,
                                "field": field,
                                "severity": "Breaking",
                                "message": (
                                    f"Response field '{field}' was removed "
                                    f"from {method.upper()} {endpoint}."
                                ),
                                "suggestion": (
                                    f"Restore the '{field}' field or "
                                    "coordinate the change with API consumers."
                                ),
                            }
                        )

    return changes


def find_removed_endpoints(
    old_spec: dict,
    new_spec: dict,
) -> list[dict]:
    """Find API endpoints that existed before but are missing now."""
    changes = []

    old_paths = old_spec.get("paths", {})
    new_paths = new_spec.get("paths", {})

    for endpoint, old_operations in old_paths.items():
        new_operations = new_paths.get(endpoint, {})

        for method in old_operations:
            if method not in new_operations:
                changes.append(
                    {
                        "endpoint": endpoint,
                        "method": method.upper(),
                        "severity": "Breaking",
                        "message": (
                            f"Endpoint {method.upper()} {endpoint} "
                            "was removed."
                        ),
                        "suggestion": (
                            "Restore the endpoint or coordinate the "
                            "removal with API consumers."
                        ),
                    }
                )

    return changes


def find_changed_field_types(
    old_spec: dict,
    new_spec: dict,
) -> list[dict]:
    """Find response fields whose data types have changed."""
    changes = []

    old_paths = old_spec.get("paths", {})
    new_paths = new_spec.get("paths", {})

    for endpoint, old_operations in old_paths.items():
        new_operations = new_paths.get(endpoint, {})

        for method, old_operation in old_operations.items():
            new_operation = new_operations.get(method)

            if new_operation is None:
                continue

            old_responses = old_operation.get("responses", {})
            new_responses = new_operation.get("responses", {})

            for status_code, old_response in old_responses.items():
                new_response = new_responses.get(status_code)

                if new_response is None:
                    continue

                old_content = old_response.get("content", {})
                new_content = new_response.get("content", {})

                for media_type, old_media in old_content.items():
                    new_media = new_content.get(media_type)

                    if new_media is None:
                        continue

                    old_schema = old_media.get("schema", {})
                    new_schema = new_media.get("schema", {})

                    old_properties = old_schema.get("properties", {})
                    new_properties = new_schema.get("properties", {})

                    for field, old_details in old_properties.items():
                        if field not in new_properties:
                            continue

                        old_type = old_details.get("type")
                        new_type = new_properties[field].get("type")

                        if (
                            old_type is not None
                            and new_type is not None
                            and old_type != new_type
                        ):
                            changes.append(
                                {
                                    "endpoint": endpoint,
                                    "method": method.upper(),
                                    "status_code": status_code,
                                    "field": field,
                                    "old_type": old_type,
                                    "new_type": new_type,
                                    "severity": "Breaking",
                                    "message": (
                                        f"Response field '{field}' changed "
                                        f"type from '{old_type}' to '{new_type}'."
                                    ),
                                    "suggestion": (
                                        "Keep the original data type or "
                                        "coordinate the change with API consumers."
                                    ),
                                }
                            )

    return changes



def find_newly_required_fields(
    old_spec: dict,
    new_spec: dict,
) -> list[dict]:
    """Find request-body fields that have newly become required."""
    changes = []

    old_paths = old_spec.get("paths", {})
    new_paths = new_spec.get("paths", {})

    for endpoint, old_operations in old_paths.items():
        new_operations = new_paths.get(endpoint, {})

        for method, old_operation in old_operations.items():
            new_operation = new_operations.get(method)

            if new_operation is None:
                continue

            old_body = old_operation.get("requestBody", {})
            new_body = new_operation.get("requestBody", {})

            old_content = old_body.get("content", {})
            new_content = new_body.get("content", {})

            for media_type, old_media in old_content.items():
                new_media = new_content.get(media_type)

                if new_media is None:
                    continue

                old_schema = old_media.get("schema", {})
                new_schema = new_media.get("schema", {})

                old_required = set(old_schema.get("required", []))
                new_required = set(new_schema.get("required", []))

                newly_required = new_required - old_required

                for field in sorted(newly_required):
                    changes.append(
                        {
                            "endpoint": endpoint,
                            "method": method.upper(),
                            "field": field,
                            "severity": "Potentially Breaking",
                            "message": (
                                f"Request field '{field}' is now required "
                                f"for {method.upper()} {endpoint}."
                            ),
                            "suggestion": (
                                "Check whether existing clients send this "
                                "field before making it required."
                            ),
                        }
                    )

    return changes


def compare_specifications(
    old_spec: dict,
    new_spec: dict,
) -> dict:
    """Compare two API specifications and return a combined report."""

    removed_endpoints = find_removed_endpoints(old_spec, new_spec)
    removed_fields = find_removed_response_fields(old_spec, new_spec)
    changed_types = find_changed_field_types(old_spec, new_spec)
    newly_required = find_newly_required_fields(old_spec, new_spec)

    all_changes = (
        removed_endpoints
        + removed_fields
        + changed_types
        + newly_required
    )

    return {
        "old_version": old_spec.get("info", {}).get("version", "unknown"),
        "new_version": new_spec.get("info", {}).get("version", "unknown"),
        "total_changes": len(all_changes),
        "changes": all_changes,
    }

