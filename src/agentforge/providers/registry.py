REGISTRY: dict[str, type] = {}

def register_provider(name: str):
    def _decorator(cls):
        REGISTRY[name.lower()] = cls
        return cls
    return _decorator
