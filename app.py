import json

import requests
import streamlit as st

st.set_page_config(
page_title="API Contract Sentinel",
page_icon="🛡️",
layout="wide",
)

API_URL = "http://127.0.0.1:8000/compare"

st.title("🛡️ API Contract Sentinel")
st.subheader("Detect Breaking Changes Between API Versions")

st.write(
"Upload two API specification files to identify "
"breaking changes before releasing a new API version."
)

st.header("Upload API Specifications")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Old API Specification")
    old_file = st.file_uploader(
        "Upload old API JSON file",
        type=["json"],
        key="old_api",
    )


with col2:
    st.subheader("New API Specification")
    new_file = st.file_uploader(
        "Upload new API JSON file",
        type=["json"],
        key="new_api",
    )

if st.button("Compare APIs", type="primary"):
    if old_file is None or new_file is None:
        st.warning("Please upload both API specification files.")
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

                st.success("API comparison completed!")

                col1, col2, col3 = st.columns(3)

                col1.metric("Old Version", report["old_version"])
                col2.metric("New Version", report["new_version"])
                col3.metric("Total Changes", report["total_changes"])

                st.subheader("Comparison Report")

                if report["changes"]:
                    st.dataframe(
                        report["changes"],
                        use_container_width=True,
                    )

                    st.download_button(
                        label="Download Report (JSON)",
                        data=json.dumps(report, indent=2),
                        file_name="comparison_report.json",
                        mime="application/json",
                    )
                else:
                    st.success("No changes detected!")
            else:
                st.error(f"Backend error ({response.status_code})")

                try:
                    st.json(response.json())
                except ValueError:
                    st.write(response.text)

        except json.JSONDecodeError:
            st.error("The uploaded file is not valid JSON.")
        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to FastAPI. "
                "Please ensure the backend is running."
            )
        except requests.exceptions.Timeout:
            st.error("The backend request timed out. Please try again.")
        except requests.exceptions.RequestException as error:
            st.error(f"Request failed: {error}")


