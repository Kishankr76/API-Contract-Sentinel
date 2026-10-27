from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, model_validator

from src.api_contract_sentinel.comparator import compare_specifications

app = FastAPI(
    title="API Contract Sentinel",
    description="Detect breaking changes between API specifications.",
    version="1.0.0",
)


class CompareRequest(BaseModel):
 old_spec: dict
 new_spec: dict


 @model_validator(mode="after")
 def validate_openapi_specs(self):
    for field_name, spec in [
        ("old_spec", self.old_spec),
        ("new_spec", self.new_spec),
    ]:
        if not spec:
            raise ValueError(f"{field_name} cannot be empty.")

        if "openapi" not in spec:
            raise ValueError(
                f"{field_name} must contain an 'openapi' field."
            )

        if not isinstance(spec.get("info"), dict):
            raise ValueError(
                f"{field_name} must contain an 'info' object."
            )

        if not isinstance(spec.get("paths"), dict):
            raise ValueError(
                f"{field_name} must contain a 'paths' object."
            )

    return self

@app.get("/")
def home():
    return {
        "message": "Welcome to API Contract Sentinel!",
        "status": "running",
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/compare")
def compare_apis(request: CompareRequest):
    try:
        report = compare_specifications(
            request.old_spec,
            request.new_spec,
        )
        return report
    except (KeyError, TypeError, AttributeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail=f"Could not compare API specifications: {error}",
        ) from error






