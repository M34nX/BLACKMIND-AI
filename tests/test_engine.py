from app.engine import CodingEngine, CodingResult


class FakeProvider:
    def __init__(self):
        self.calls = []

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        self.calls.append((system_prompt, user_prompt))
        return f"stage-{len(self.calls)}"


async def test_engine_runs_three_stages_in_order():
    provider = FakeProvider()
    engine = CodingEngine(provider)

    result = await engine.solve(
        task="Create a function that adds two integers.",
        language="python",
        context="Use type hints.",
    )

    assert isinstance(result, CodingResult)
    assert result.plan == "stage-1"
    assert result.implementation == "stage-2"
    assert result.review == "stage-3"
    assert len(provider.calls) == 3
    assert "stage-1" in provider.calls[1][1]
    assert "stage-2" in provider.calls[2][1]
