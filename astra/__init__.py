import os

# we only use PyTorch, not TensorFlow. the transformers library tries
# to import TF by default and the anaconda TF build is broken on macOS
# (segfaults in pyarrow). this kills it before it can cause problems.
os.environ.setdefault("USE_TF", "0")
os.environ.setdefault("USE_TORCH", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

from astra.version import __version__

__all__ = ["__version__"]
