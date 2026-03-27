import re

registry = []


def provider(pattern):
    def decorator(fn):
        registry.append((re.compile(pattern), fn))
        return fn

    return decorator
