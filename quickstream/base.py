import re

registry = []
test_registry = {}


def provider(pattern, tests={}):
    def decorator(fn):
        registry.append((re.compile(pattern), fn))
        test_registry.update(tests)
        return fn

    return decorator
