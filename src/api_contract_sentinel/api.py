
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.api_contract_sentinel.comparator import compare_specifications


app = FastAPI(
    title="API Contract Sentinel",
    description="Detect breaking changes between API specifications.",
    version="1.0.0",
)


class CompareRequest(BaseModel):
    old_spec: dict
    new_spec: dict


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



