from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator

from app.config import settings
from app.context import ProjectFile as ContextFile
from app.context import build_project_context, validate_project_file
from app.engine import CodingEngine, ModelError, OpenAICompatibleProvider

app = FastAPI(
    title=settings.app_name,
    description="A multi-stage AI assistant for software engineering.",
    version="0.2.0",
)

engine = CodingEngine(OpenAICompatibleProvider(settings))


class ProjectFileInput(BaseModel):
    path: str = Field(min_length=1, max_length=240)
    content: str = Field(max_length=16000)

    @model_validator(mode="after")
    def validate_virtual_file(self):
        validate_project_file(self.path, self.content)
        return self


class CodeRequest(BaseModel):
    task: str = Field(min_length=5, max_length=12000)
    language: str = Field(default="python", min_length=1, max_length=60)
    context: str = Field(default="", max_length=12000)
    project_files: list[ProjectFileInput] = Field(default_factory=list, max_length=30)

    @model_validator(mode="after")
    def validate_project_context_size(self):
        files = [
            ContextFile(path=item.path, content=item.content)
            for item in self.project_files
        ]
        build_project_context(files)
        return self


class CodeResponse(BaseModel):
    plan: str
    implementation: str
    review: str


@app.get("/")
async def root():
    return {"name": settings.app_name, "version": "0.2.0", "docs": "/docs"}


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model_configured": bool(settings.model_api_key),
        "workflow": ["project_context", "planner", "engineer", "reviewer"],
    }


@app.post("/v1/code", response_model=CodeResponse)
async def generate_code(request: CodeRequest):
    project_context = build_project_context([
        ContextFile(path=item.path, content=item.content)
        for item in request.project_files
    ])
    combined_context = "\n\n".join(
        part for part in (request.context, project_context) if part
    )

    try:
        result = await engine.solve(
            task=request.task,
            language=request.language,
            context=combined_context,
        )
        return CodeResponse(
            plan=result.plan,
            implementation=result.implementation,
            review=result.review,
        )
    except ModelError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
