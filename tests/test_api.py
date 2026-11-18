from fastapi.testclient import TestClient

import app.main as main
from app.engine import CodingResult


def test_code_endpoint_passes_project_files_to_engine(monkeypatch):
    captured = {}

    async def fake_solve(task, language, context=""):
        captured["task"] = task
        captured["language"] = language
        captured["context"] = context
        return CodingResult(
            plan="Plan",
            implementation="def answer(): return 42",
            review="Looks good",
        )

    monkeypatch.setattr(main.engine, "solve", fake_solve)
    client = TestClient(main.app)
    response = client.post(
        "/v1/code",
        json={
            "task": "Explain and improve this module.",
            "language": "python",
            "project_files": [
                {"path": "src/app.py", "content": "def answer(): return 42"}
            ],
        },
    )

    assert response.status_code == 200
    assert response.json()["implementation"] == "def answer(): return 42"
    assert "FILE: src/app.py" in captured["context"]
    assert "def answer(): return 42" in captured["context"]


def test_code_endpoint_rejects_environment_files():
    client = TestClient(main.app)
    response = client.post(
        "/v1/code",
        json={
            "task": "Review this project.",
            "project_files": [{"path": "config/.env.development", "content": "TOKEN=x"}],
        },
    )
    assert response.status_code == 422


def test_code_endpoint_rejects_path_traversal():
    client = TestClient(main.app)
    response = client.post(
        "/v1/code",
        json={
            "task": "Review this project.",
            "project_files": [{"path": "../outside.py", "content": "print('x')"}],
        },
    )
    assert response.status_code == 422
