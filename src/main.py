"""Student Information System: command line entry point.

Run from the project root:  python src/main.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.student import Student
from services.student_service import (
    StudentService, StudentNotFoundError, DuplicateStudentError)
from utils.config import load_config
from utils.logger import setup_logger
from utils import validators as v

MENU = """
=== Student Information System ===
1. Add Student
2. View All Students
3. View Student by ID
4. Update Student
5. Delete Student
6. Exit
7. Search Students
8. Export to CSV
"""


def ask(prompt, validator):
    """Ask until the input passes validation."""
    while True:
        try:
            return validator(input(prompt))
        except ValueError as err:
            print(f"  Invalid: {err}")


def show(students):
    if not students:
        print("No students found.")
        return
    print(f"{'ID':<10}{'Name':<20}{'Email':<26}{'Course':<18}{'Yr':<4}GPA")
    for s in students:
        print(f"{s.student_id:<10}{s.name:<20}{s.email:<26}{s.course:<18}"
              f"{s.year_level:<4}{s.gpa:.2f}")


def add_student(service):
    print("\n--- Add New Student ---")
    student = Student(
        name=ask("Name: ", v.validate_name),
        email=ask("Email: ", v.validate_email),
        course=ask("Course: ", v.validate_course),
        year_level=ask("Year Level (1-6): ", v.validate_year_level),
        gpa=ask("GPA (0.0-4.0, Enter to skip): ", v.validate_gpa),
    )
    service.add(student)
    print(f"Student added successfully! ID: {student.student_id}")


def view_student(service):
    student = service.get(input("Enter Student ID: ").strip())
    show([student])


def update_student(service):
    student_id = input("Enter Student ID to update: ").strip()
    service.get(student_id)
    print("Press Enter to keep the current value.")
    fields = {}
    for key, validator in [("name", v.validate_name), ("email", v.validate_email),
                           ("course", v.validate_course),
                           ("year_level", v.validate_year_level),
                           ("gpa", v.validate_gpa)]:
        raw = input(f"New {key}: ")
        if raw.strip():
            try:
                fields[key] = validator(raw)
            except ValueError as err:
                print(f"  Skipped {key}: {err}")
    service.update(student_id, **fields)
    print("Student updated.")


def delete_student(service):
    service.delete(input("Enter Student ID to delete: ").strip())
    print("Student deleted.")


def main():
    config = load_config("config/config.json")
    logger = setup_logger(config["log_file"], config["log_level"])
    service = StudentService(config["data_file"], logger)
    logger.info("Application started.")

    actions = {
        "1": lambda: add_student(service),
        "2": lambda: (print("\n--- All Students ---"), show(service.get_all())),
        "3": lambda: view_student(service),
        "4": lambda: update_student(service),
        "5": lambda: delete_student(service),
        "7": lambda: show(service.search(input("Search term: "))),
        "8": lambda: print("Exported to", service.export_csv(config["export_dir"])),
    }

    while True:
        print(MENU)
        try:
            choice = input("Enter your choice (1-8): ").strip()
        except EOFError:  # Input stream closed (Ctrl+D). Exit cleanly.
            logger.info("Input closed. Application stopped.")
            break
        if choice == "6":
            logger.info("Application closed.")
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Please try again.")
            continue
        try:
            action()
        except (StudentNotFoundError, DuplicateStudentError) as err:
            print(f"Error: {err}")
        except OSError as err:
            logger.error("File error: %s", err)
            print("File error. Check the log.")
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.")
        except Exception as err:  # Last resort. Keeps the menu running.
            logger.exception("Unexpected error: %s", err)
            print("Unexpected error. Check the log.")


if __name__ == "__main__":
    main()
