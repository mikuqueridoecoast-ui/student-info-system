"""Student model."""
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime


def _now():
    return datetime.now().isoformat()


@dataclass
class Student:
    """A single student record. The ID is generated when left empty."""
    name: str
    email: str
    course: str
    year_level: int
    gpa: float = 0.0
    student_id: str = ""
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def __post_init__(self):
        if not self.student_id:
            self.student_id = str(uuid.uuid4())[:8]

    def to_dict(self):
        """Convert the record to a dictionary for JSON storage."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        """Build a record from a dictionary. Raises KeyError on missing fields."""
        return cls(
            name=data["name"],
            email=data["email"],
            course=data["course"],
            year_level=int(data["year_level"]),
            gpa=float(data.get("gpa", 0.0)),
            student_id=str(data["student_id"]),
            created_at=data.get("created_at", _now()),
            updated_at=data.get("updated_at", _now()),
        )
