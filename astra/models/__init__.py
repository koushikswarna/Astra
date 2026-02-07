"""Model loading and text generation.

Imports are lazy to avoid pulling in torch/transformers
just because someone imported the astra package.
"""

__all__ = ["TextGenerator", "ModelLoader"]


def __getattr__(name):
    if name == "TextGenerator":
        from astra.models.generator import TextGenerator
        return TextGenerator
    if name == "ModelLoader":
        from astra.models.loader import ModelLoader
        return ModelLoader
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
