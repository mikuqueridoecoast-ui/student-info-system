"""Student service: CRUD, search, and export with JSON persistence."""
import csv
import json
import os
import shutil
from datetime import datetime

from models.student import Student


class StudentNotFoundError(Exception):
    """Raised when a student ID does not exist."""


class DuplicateStudentError(Exception):
    """Raised when a student ID or email already exists."""


class StudentService:
    def __init__(self, data_file, logger):
        self.data_file = data_file
        self.logger = logger
        self.students = {}
        self._load()

    # ---------- persistence ----------
    def _load(self):
        """Read students from disk. Back up and reset a corrupt file."""
        if not os.path.exists(self.data_file):
            self.logger.info("Data file missing. Starting empty.")
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                records = json.load(f)
            for item in records:
                student = Student.from_dict(item)
                self.students[student.student_id] = student
            self.logger.info("Loaded %d students.", len(self.students))
        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            backup = self.data_file + ".bak"
            shutil.copy(self.data_file, backup)
            self.students = {}
            self.logger.error("Data file corrupt. Backup saved to %s.", backup)

    def _save(self):
        """Write to a temp file, then replace. Prevents half-written data."""
        os.makedirs(os.path.dirname(self.data_file) or ".", exist_ok=True)
        temp = self.data_file + ".tmp"
        try:
            with open(temp, "w", encoding="utf-8") as f:
                json.dump([s.to_dict() for s in self.students.values()], f, indent=2)
            os.replace(temp, self.data_file)
        except OSError as err:
            self.logger.error("Save failed: %s", err)
            raise

    # ---------- CRUD ----------
    def add(self, student):
        while student.student_id in self.students:  # Regenerate on the rare ID clash.
            student.student_id = Student(
                name="x", email="x", course="x", year_level=1).student_id
        if any(s.email.lower() == student.email.lower() for s in self.students.values()):
            raise DuplicateStudentError("Email already in use.")
        self.students[student.student_id] = student
        self._save()
        self.logger.info("Added student %s.", student.student_id)

    def get_all(self):
        return sorted(self.students.values(), key=lambda s: s.student_id)

    def get(self, student_id):
        if student_id not in self.students:
            raise StudentNotFoundError(f"No student with ID {student_id}.")
        return self.students[student_id]

    def update(self, student_id, **fields):
        student = self.get(student_id)
        for key, value in fields.items():
            if value is not None and hasattr(student, key):
                setattr(student, key, value)
        student.updated_at = datetime.now().isoformat()
        self._save()
        self.logger.info("Updated student %s.", student_id)
        return student

    def delete(self, student_id):
        self.get(student_id)
        del self.students[student_id]
        self._save()
        self.logger.info("Deleted student %s.", student_id)

    # ---------- bonus ----------
    def search(self, term):
        term = term.lower()
        return [s for s in self.get_all()
                if term in s.name.lower() or term in s.course.lower()
                or term in s.email.lower() or term == s.student_id.lower()]

    def export_csv(self, export_dir):
        os.makedirs(export_dir, exist_ok=True)
        path = os.path.join(export_dir, "students.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["student_id", "name", "email", "course",
                               "year_level", "gpa", "created_at", "updated_at"])
            writer.writeheader()
            for s in self.get_all():
                writer.writerow(s.to_dict())
        self.logger.info("Exported %d students to %s.", len(self.students), path)
        return path
