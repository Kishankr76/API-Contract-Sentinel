import json

import requests
import streamlit as st

# -------------------- Page Configuration --------------------

st.set_page_config(
page_title="API Contract Sentinel",
page_icon="🛡️",
layout="wide",
)

API_URL = "http://127.0.0.1:8000/compare"

# -------------------- Header --------------------

st.title("🛡️ API Contract Sentinel")
st.subheader("Detect Breaking Changes Between API Versions")

st.markdown(
"""
Compare two API specifications to identify changes that could
affect compatibility with existing clients.
"""
)

st.divider()

# -------------------- File Upload --------------------

st.header("📂 Upload API Specifications")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Old API Specification")


    old_file = st.file_uploader(
        "Choose the old API JSON file",
        type=["json"],
        key="old_api",
    )


with col2:
    st.subheader("New API Specification")


    new_file = st.file_uploader(
        "Choose the new API JSON file",
        type=["json"],
        key="new_api",
    )


# -------------------- Compare APIs --------------------

if st.button("🔍 Compare APIs", type="primary", use_container_width=True):
    if old_file is None or new_file is None:
        st.warning("Please upload both old and new API specification files.")

    else:
        try:
            old_spec = json.load(old_file)
            new_spec = json.load(new_file)

            with st.spinner("Comparing API specifications..."):
                response = requests.post(
                    API_URL,
                    json={
                        "old_spec": old_spec,
                        "new_spec": new_spec,
                    },
                    timeout=30,
                )

            if response.status_code == 200:
                report = response.json()
                changes = report.get("changes", [])

                st.success("API comparison completed successfully!")

                # Summary metrics
                st.header("📊 Comparison Summary")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Old API Version",
                    report.get("old_version", "Unknown"),
                )

                col2.metric(
                    "New API Version",
                    report.get("new_version", "Unknown"),
                )

                col3.metric(
                    "Total Changes",
                    report.get("total_changes", len(changes)),
                )

                # Categorize changes using backend severity values
                breaking_changes = [
                    change for change in changes
                    if change.get("severity") == "Breaking"
                ]

                potentially_breaking = [
                    change for change in changes
                    if change.get("severity") == "Potentially Breaking"
                ]

                safe_changes = [
                    change for change in changes
                    if change.get("severity") == "Safe"
                ]

                # Report sections
                st.divider()
                st.header("📋 Detailed Comparison Report")

                if not changes:
                    st.success("🎉 No changes detected between the two APIs.")

                else:
                    tab1, tab2, tab3, tab4 = st.tabs(
                        [
                            "🚨 Breaking",
                            "⚠️ Potentially Breaking",
                            "✅ Safe",
                            "📄 All Changes",
                        ]
                    )

                    with tab1:
                        if breaking_changes:
                            st.error(
                                f"{len(breaking_changes)} breaking change(s) detected."
                            )
                            st.dataframe(
                                breaking_changes,
                                use_container_width=True,
                            )
                        else:
                            st.success("No breaking changes detected.")

                    with tab2:
                        if potentially_breaking:
                            st.warning(
                                f"{len(potentially_breaking)} potentially "
                                "breaking change(s) detected."
                            )
                            st.dataframe(
                                potentially_breaking,
                                use_container_width=True,
                            )
                        else:
                            st.success("No potentially breaking changes detected.")

                    with tab3:
                        if safe_changes:
                            st.dataframe(
                                safe_changes,
                                use_container_width=True,
                            )
                        else:
                            st.info("No safe changes detected.")

                    with tab4:
                        st.dataframe(
                            changes,
                            use_container_width=True,
                        )

                # Download complete JSON report
                st.divider()

                st.download_button(
                    label="⬇️ Download Comparison Report (JSON)",
                    data=json.dumps(report, indent=2),
                    file_name="comparison_report.json",
                    mime="application/json",
                    use_container_width=True,
                )

            else:
                st.error(f"Backend returned an error: HTTP {response.status_code}")

                try:
                    error_details = response.json()
                    st.json(error_details)
                except ValueError:
                    st.write(response.text)

        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload valid JSON specifications.")

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the FastAPI backend. "
                "Please make sure the backend is running."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The comparison request timed out. Please try again."
            )

        except requests.exceptions.RequestException as error:
            st.error(f"Request failed: {error}")

        except (TypeError, KeyError, ValueError) as error:
            st.error(f"Could not process the comparison report: {error}")


# -------------------- Footer --------------------

st.divider()

st.caption(
"API Contract Sentinel | OpenAPI Change Detection Tool"
)



