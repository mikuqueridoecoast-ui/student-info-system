"""Unit tests. Run from the project root:  python -m unittest discover tests"""
import logging
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from models.student import Student
from services.student_service import (
    StudentService, StudentNotFoundError, DuplicateStudentError)
from utils import validators as v


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "students.json")
        self.service = StudentService(self.path, logging.getLogger("test"))
        self.s1 = Student(name="Ana Lopez", email="ana@example.com", course="Cloud", year_level=2, student_id="1")

    def tearDown(self):
        self.dir.cleanup()

    def test_add_and_persist(self):
        self.service.add(self.s1)
        reloaded = StudentService(self.path, logging.getLogger("test"))
        self.assertEqual(reloaded.get("1").name, "Ana Lopez")

    def test_duplicate_email(self):
        self.service.add(self.s1)
        other = Student(name="Ben Carter", email="ANA@example.com", course="Data", year_level=1)
        with self.assertRaises(DuplicateStudentError):
            self.service.add(other)

    def test_auto_id(self):
        self.assertEqual(len(Student(name="Zed", email="z@x.com", course="C", year_level=1).student_id), 8)

    def test_update(self):
        self.service.add(self.s1)
        self.service.update("1", year_level=3)
        self.assertEqual(self.service.get("1").year_level, 3)

    def test_delete(self):
        self.service.add(self.s1)
        self.service.delete("1")
        with self.assertRaises(StudentNotFoundError):
            self.service.get("1")

    def test_search(self):
        self.service.add(self.s1)
        self.assertEqual(len(self.service.search("cloud")), 1)

    def test_corrupt_file_recovery(self):
        with open(self.path, "w") as f:
            f.write("{bad json")
        recovered = StudentService(self.path, logging.getLogger("test"))
        self.assertEqual(recovered.get_all(), [])
        self.assertTrue(os.path.exists(self.path + ".bak"))


class ValidatorTests(unittest.TestCase):
    def test_year_level(self):
        self.assertEqual(v.validate_year_level("2"), 2)
        with self.assertRaises(ValueError):
            v.validate_year_level("abc")

    def test_gpa(self):
        self.assertEqual(v.validate_gpa(""), 0.0)
        with self.assertRaises(ValueError):
            v.validate_gpa("5")

    def test_email(self):
        with self.assertRaises(ValueError):
            v.validate_email("not-an-email")


if __name__ == "__main__":
    unittest.main()
