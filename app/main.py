from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.config import settings
from app.engine import CodingEngine, ModelError, OpenAICompatibleProvider

app = FastAPI(
    title=settings.app_name,
    description="A multi-stage AI assistant for software engineering.",
    version="0.1.0",
)

engine = CodingEngine(OpenAICompatibleProvider(settings))


class CodeRequest(BaseModel):
    task: str = Field(min_length=5, max_length=12000)
    language: str = Field(default="python", min_length=1, max_length=60)
    context: str = Field(default="", max_length=12000)


class CodeResponse(BaseModel):
    plan: str
    implementation: str
    review: str


@app.get("/")
async def root():
    return {"name": settings.app_name, "version": "0.1.0", "docs": "/docs"}


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model_configured": bool(settings.model_api_key),
        "workflow": ["planner", "engineer", "reviewer"],
    }


@app.post("/v1/code", response_model=CodeResponse)
async def generate_code(request: CodeRequest):
    try:
        result = await engine.solve(
            task=request.task,
            language=request.language,
            context=request.context,
        )
        return CodeResponse(
            plan=result.plan,
            implementation=result.implementation,
            review=result.review,
        )
    except ModelError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
