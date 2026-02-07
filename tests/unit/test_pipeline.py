"""Tests for the pipeline infrastructure."""

from astra.pipelines.base import PipelineStep
from astra.pipelines.middleware import MiddlewareChain
from astra.pipelines.registry import PipelineRegistry


class DummyStep(PipelineStep):
    @property
    def name(self) -> str:
        return "dummy"

    def execute(self, context):
        context["dummy_ran"] = True
        return context


class TestPipelineStep:
    def test_dummy_step(self):
        step = DummyStep()
        ctx = step.execute({})
        assert ctx["dummy_ran"] is True

    def test_should_skip_default(self):
        step = DummyStep()
        assert step.should_skip({}) is False


class TestMiddlewareChain:
    def test_empty_chain(self):
        chain = MiddlewareChain()
        core = lambda ctx: {**ctx, "done": True}
        result = chain.execute({"input": "test"}, core)
        assert result["done"] is True

    def test_middleware_wraps_core(self):
        chain = MiddlewareChain()

        def add_prefix(ctx, next_handler):
            ctx["prefix"] = "before"
            result = next_handler(ctx)
            result["suffix"] = "after"
            return result

        chain.add(add_prefix)
        core = lambda ctx: {**ctx, "core": True}
        result = chain.execute({}, core)

        assert result["prefix"] == "before"
        assert result["core"] is True
        assert result["suffix"] == "after"


class TestPipelineRegistry:
    def test_register_and_get(self):
        PipelineRegistry.register("test_step", DummyStep)
        cls = PipelineRegistry.get("test_step")
        assert cls is DummyStep

    def test_create_instance(self):
        PipelineRegistry.register("test_step_2", DummyStep)
        instance = PipelineRegistry.create("test_step_2")
        assert isinstance(instance, DummyStep)

    def test_unknown_step_raises(self):
        import pytest
        with pytest.raises(KeyError):
            PipelineRegistry.get("nonexistent_step")
