"""Input validation. Each function returns a clean value or raises ValueError."""
import re

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


def validate_name(value):
    value = value.strip()
    if len(value) < 2:
        raise ValueError("Name must have at least 2 characters.")
    return value


def validate_email(value):
    value = value.strip()
    if not EMAIL_PATTERN.match(value):
        raise ValueError("Email format is invalid.")
    return value


def validate_course(value):
    value = value.strip()
    if not value:
        raise ValueError("Course cannot be empty.")
    return value


def validate_year_level(value):
    try:
        year = int(value)
    except (TypeError, ValueError):
        raise ValueError("Year level must be a whole number.")
    if not 1 <= year <= 6:
        raise ValueError("Year level must be between 1 and 6.")
    return year


def validate_gpa(value):
    if str(value).strip() == "":
        return 0.0
    try:
        gpa = float(value)
    except ValueError:
        raise ValueError("GPA must be a number.")
    if not 0.0 <= gpa <= 4.0:
        raise ValueError("GPA must be between 0.0 and 4.0.")
    return gpa
