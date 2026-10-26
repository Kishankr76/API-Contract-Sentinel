
from pathlib import Path
import json

from src.api_contract_sentinel.comparator import (
    compare_specifications,
    load_specification,
)


BASE_DIR = Path(__file__).resolve().parent

old_spec = load_specification(
    str(BASE_DIR / "examples" / "old_api.json")
)

new_spec = load_specification(
    str(BASE_DIR / "examples" / "new_api.json")
)

report = compare_specifications(old_spec, new_spec)

print("===================================")
print("       API CONTRACT SENTINEL")
print("===================================")

print(f"Old API Version: {report['old_version']}")
print(f"New API Version: {report['new_version']}")
print(f"Total Changes Detected: {report['total_changes']}")

print("\n========== CHANGE REPORT ==========")

if not report["changes"]:
    print("No changes detected.")
else:
    for number, change in enumerate(report["changes"], start=1):
        print(f"\nChange #{number}")
        print(f"Severity: {change['severity']}")
        print(f"Endpoint: {change['method']} {change['endpoint']}")
        print(f"Message: {change['message']}")
        print(f"Suggestion: {change['suggestion']}")

        if "field" in change:
            print(f"Field: {change['field']}")

        if "old_type" in change and "new_type" in change:
            print(f"Old Type: {change['old_type']}")
            print(f"New Type: {change['new_type']}")

# Save the report as a JSON file.
report_path = BASE_DIR / "docs" / "comparison_report.json"

with report_path.open("w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print(f"\nFull JSON report saved to: {report_path}")




# from pathlib import Path

# from src.api_contract_sentinel.comparator import (
#     find_changed_field_types,
#     find_newly_required_fields,
#     find_removed_endpoints,
#     find_removed_response_fields,
#     load_specification,
# )

# BASE_DIR = Path(__file__).resolve().parent

# old_spec = load_specification(
#     str(BASE_DIR / "examples" / "old_api.json")
# )

# new_spec = load_specification(
#     str(BASE_DIR / "examples" / "new_api.json")
# )

# # Test 1: Find removed response fields
# field_changes = find_removed_response_fields(old_spec, new_spec)

# print("=== Removed Response Fields ===")

# if not field_changes:
#     print("No removed response fields detected.")
# else:
#     for change in field_changes:
#         print(f"\nSeverity: {change['severity']}")
#         print(f"Endpoint: {change['method']} {change['endpoint']}")
#         print(f"Removed field: {change['field']}")
#         print(f"Message: {change['message']}")
#         print(f"Suggestion: {change['suggestion']}")

# # Test 2: Find removed endpoints
# endpoint_changes = find_removed_endpoints(old_spec, new_spec)

# print("\n=== Removed API Endpoints ===")

# if not endpoint_changes:
#     print("No removed API endpoints detected.")
# else:
#     for change in endpoint_changes:
#         print(f"\nSeverity: {change['severity']}")
#         print(f"Endpoint: {change['method']} {change['endpoint']}")
#         print(f"Message: {change['message']}")
#         print(f"Suggestion: {change['suggestion']}")


# # Test 3: Find response fields with changed data types
# type_changes = find_changed_field_types(old_spec, new_spec)

# print("\n=== Changed Response Field Types ===")

# if not type_changes:
#     print("No changed response field types detected.")
# else:
#     for change in type_changes:
#         print(f"\nSeverity: {change['severity']}")
#         print(f"Endpoint: {change['method']} {change['endpoint']}")
#         print(f"Field: {change['field']}")
#         print(f"Old type: {change['old_type']}")
#         print(f"New type: {change['new_type']}")
#         print(f"Message: {change['message']}")
#         print(f"Suggestion: {change['suggestion']}")

# # Test 4: Find newly required request fields
# required_changes = find_newly_required_fields(old_spec, new_spec)

# print("\n=== Newly Required Request Fields ===")

# if not required_changes:
#     print("No newly required request fields detected.")
# else:
#     for change in required_changes:
#         print(f"\nSeverity: {change['severity']}")
#         print(f"Endpoint: {change['method']} {change['endpoint']}")
#         print(f"Newly required field: {change['field']}")
#         print(f"Message: {change['message']}")
#         print(f"Suggestion: {change['suggestion']}")