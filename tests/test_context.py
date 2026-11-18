import pytest

from app.context import (
    MAX_FILE_CHARS,
    MAX_PROJECT_CHARS,
    ProjectFile,
    build_project_context,
    validate_project_file,
)


def test_validate_project_file_accepts_relative_source_path():
    item = validate_project_file("src/utils.py", "def add(a, b):\n    return a + b\n")
    assert item == ProjectFile(
        path="src/utils.py",
        content="def add(a, b):\n    return a + b\n",
    )


@pytest.mark.parametrize(
    "path",
    ["../outside.py", "/etc/passwd", "src/../../outside.py", r"src\\app.py"],
)
def test_validate_project_file_rejects_unsafe_paths(path):
    with pytest.raises(ValueError):
        validate_project_file(path, "print('hello')")


@pytest.mark.parametrize(
    "path",
    [".env", "config/.env.local", "private.pem", "certs/server.key", ".git/config"],
)
def test_validate_project_file_rejects_secrets_and_vcs_paths(path):
    with pytest.raises(ValueError):
        validate_project_file(path, "sensitive")


def test_validate_project_file_rejects_oversized_and_binary_content():
    with pytest.raises(ValueError):
        validate_project_file("large.py", "x" * (MAX_FILE_CHARS + 1))
    with pytest.raises(ValueError):
        validate_project_file("binary.dat", "abc\x00def")


def test_build_project_context_includes_file_boundaries():
    context = build_project_context([
        ProjectFile(path="app.py", content="print('ok')"),
        ProjectFile(path="tests/test_app.py", content="def test_app(): pass"),
    ])
    assert "--- FILE: app.py ---" in context
    assert "--- END FILE ---" in context
    assert "--- FILE: tests/test_app.py ---" in context


def test_build_project_context_enforces_total_size():
    with pytest.raises(ValueError):
        build_project_context([
            ProjectFile(path="a.py", content="x" * MAX_PROJECT_CHARS),
            ProjectFile(path="b.py", content="y"),
        ])
