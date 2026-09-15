"""Illustrative formatting library; the exporter selects its backend."""

backend: str = "html"


def expr(value: object) -> object:
    """Return an already evaluated Python value unchanged.

    Args:
        value: Result of the Python expression passed to this identity function.
    """
    return value


def bold(text: str) -> str:
    """Return bold markup for the selected output format.

    Args:
        text: Plain example text without markup delimiters.
    """
    if backend == "latex":
        return r"\textbf{" + text + "}"
    elif backend == "html":
        return f"<strong>{text}</strong>"
    elif backend == "markdown":
        return f"**{text}**"
    raise ValueError(f"Unsupported backend: {backend}")
