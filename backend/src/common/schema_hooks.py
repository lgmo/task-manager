from typing import Any


def preprocessing_filter_spec(
    endpoints: list[tuple[str, Any, Any, Any]],
) -> list[tuple[str, Any, Any, Any]]:
    filtered: list[tuple[str, Any, Any, Any]] = []
    for path, path_regex, method, callback in endpoints:
        if path != "/api/schema/":
            filtered.append((path, path_regex, method, callback))
    return filtered
