__version__ = "0.3.0"

# semver: bump minor for new features, patch for fixes
# we jumped to 0.3 after the full rewrite from the monolith
VERSION_TUPLE = tuple(int(x) for x in __version__.split("."))
