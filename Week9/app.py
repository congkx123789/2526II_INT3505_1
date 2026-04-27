from fastapi import FastAPI, APIRouter, Response, Request, status, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI(
    title="Payment API v2 Lifecycle Demo",
    description="Interactive Dashboard for API Versioning.",
)

# --- GLOBAL STATE (CONTROLLED BY UI) ---
# Stages: "COEXIST", "DEPRECATED", "BROWNOUT", "SUNSET"
app.state.lifecycle_stage = "DEPRECATED"

# ==========================================
# MODELS
# ==========================================
class PaymentV1(BaseModel):
    amount: float
    order_id: str

class PaymentV2(BaseModel):
    amount: float
    currency: str
    payment_method: str
    order_id: str

class StageUpdate(BaseModel):
    stage: str

# ==========================================
# ADMIN ENDPOINT (FOR UI)
# ==========================================
@app.post("/api/admin/set-stage")
async def set_stage(data: StageUpdate):
    valid_stages = ["COEXIST", "DEPRECATED", "BROWNOUT", "SUNSET"]
    if data.stage not in valid_stages:
        raise HTTPException(status_code=400, detail="Invalid stage")
    app.state.lifecycle_stage = data.stage
    return {"message": f"Server stage updated to {data.stage}"}

@app.get("/api/admin/get-stage")
async def get_stage():
    return {"stage": app.state.lifecycle_stage}

# ==========================================
# V1 IMPLEMENTATION
# ==========================================
v1_router = APIRouter(prefix="/api/v1", tags=["V1 - Legacy"])

@v1_router.post("/payments")
async def create_payment_v1(payment: PaymentV1):
    stage = app.state.lifecycle_stage
    if stage == "BROWNOUT":
        raise HTTPException(status_code=503, detail="V1 Brownout Test Active")
    if stage == "SUNSET":
        return Response(status_code=410, content="API V1 Sunset complete")

    return {"status": "success", "data": payment.model_dump(), "version": "v1"}

# ==========================================
# V2 IMPLEMENTATION
# ==========================================
v2_router = APIRouter(prefix="/api/v2", tags=["V2 - Current"])

@v2_router.post("/payments")
async def create_payment_v2(payment: PaymentV2):
    return {"status": "success", "data": payment.model_dump(), "version": "v2"}

# ==========================================
# MIDDLEWARE
# ==========================================
@app.middleware("http")
async def api_lifecycle_middleware(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/api/v1"):
        stage = app.state.lifecycle_stage
        if stage in ["DEPRECATED", "BROWNOUT"]:
            response.headers["Deprecation"] = "true"
            response.headers["Link"] = '<http://localhost:8888/api/migration>; rel="sunset"'
            response.headers["Warning"] = '299 - "V1 is deprecated. Sunset: 2026-06-01."'
            response.headers["Sunset"] = "Mon, 01 Jun 2026 00:00:00 GMT"
    return response

# Assembly
app.include_router(v1_router)
app.include_router(v2_router)

# --- Serving the Frontend ---
app.mount("/static", StaticFiles(directory="Week9/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('Week9/static/index.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
