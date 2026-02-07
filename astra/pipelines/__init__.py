"""Chat processing pipeline and middleware.

ChatPipeline import is lazy since it pulls in the full model stack.
"""

from astra.pipelines.registry import PipelineRegistry

__all__ = ["ChatPipeline", "PipelineRegistry"]


def __getattr__(name):
    if name == "ChatPipeline":
        from astra.pipelines.chat import ChatPipeline
        return ChatPipeline
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
