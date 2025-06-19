from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class User:
    id: int
    email: str
    password: str  # plaintext for demo only!
    name: str | None = None
