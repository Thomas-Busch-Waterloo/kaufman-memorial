#!/usr/bin/env python3
"""
Validation script for data.json

This script validates the structure and content of data.json to ensure:
- Valid JSON syntax
- All required fields are present
- Field values are properly formatted
- Referenced image files exist
"""

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data.json"


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def load_json():
    """Load and parse the JSON file"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValidationError(f"File not found: {DATA_FILE}")
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON syntax: {e}")


def validate_file_exists(filepath, description="File"):
    """Check if a file exists"""
    full_path = ROOT / filepath
    if not full_path.exists():
        raise ValidationError(f"{description} not found: {filepath}")
    return True


def validate_person(data):
    """Validate the person object"""
    if "person" not in data:
        raise ValidationError("Missing required top-level key: 'person'")

    person = data["person"]
    required_fields = ["name", "subtitle", "profile_image", "header_note", "date_range"]

    for field in required_fields:
        if field not in person:
            raise ValidationError(f"Missing required field in person: '{field}'")
        if not isinstance(person[field], str) or not person[field].strip():
            raise ValidationError(f"Field 'person.{field}' must be a non-empty string")

    # Validate profile image exists
    validate_file_exists(person["profile_image"], "Person profile image")

    print("✓ Person object is valid")


def validate_background_object(bg, path="background"):
    """Validate a single background configuration object"""
    if not isinstance(bg, dict):
        raise ValidationError(f"{path} must be an object")

    required_fields = ["image", "size", "position"]
    for field in required_fields:
        if field not in bg:
            raise ValidationError(f"Missing required field in {path}: '{field}'")

    # Validate image file exists
    validate_file_exists(bg["image"], f"{path} image")

    # Validate size format
    size = bg["size"]
    valid_sizes = ["cover", "contain", "auto"]
    percentage_pattern = re.compile(r'^\d+%\s+\d+%$')

    if size not in valid_sizes and not percentage_pattern.match(size):
        raise ValidationError(
            f"{path}.size must be 'cover', 'contain', 'auto', or 'XX% XX%' format. Got: '{size}'"
        )

    # Validate position (basic check)
    if not isinstance(bg["position"], str) or not bg["position"].strip():
        raise ValidationError(f"{path}.position must be a non-empty string")


def validate_backgrounds(data):
    """Validate the backgrounds configuration"""
    if "backgrounds" not in data:
        raise ValidationError("Missing required top-level key: 'backgrounds'")

    backgrounds = data["backgrounds"]

    # Validate cover
    if "cover" not in backgrounds:
        raise ValidationError("Missing required field: backgrounds.cover")
    validate_background_object(backgrounds["cover"], "backgrounds.cover")

    # Validate pages or pages_list
    if "pages" in backgrounds:
        validate_background_object(backgrounds["pages"], "backgrounds.pages")

    if "pages_list" in backgrounds:
        if not isinstance(backgrounds["pages_list"], list):
            raise ValidationError("backgrounds.pages_list must be an array")

        for i, bg in enumerate(backgrounds["pages_list"]):
            validate_background_object(bg, f"backgrounds.pages_list[{i}]")

    print("✓ Backgrounds configuration is valid")


def validate_comments(data):
    """Validate the comments array"""
    if "comments" not in data:
        raise ValidationError("Missing required top-level key: 'comments'")

    comments = data["comments"]

    if not isinstance(comments, list):
        raise ValidationError("'comments' must be an array")

    if len(comments) == 0:
        raise ValidationError("'comments' array is empty")

    authors = []
    height_pattern = re.compile(r'^\d+px$')

    for i, comment in enumerate(comments):
        # Check required fields
        if "author" not in comment:
            raise ValidationError(f"Missing 'author' in comments[{i}]")
        if "message" not in comment:
            raise ValidationError(f"Missing 'message' in comments[{i}]")

        # Validate author
        author = comment["author"]
        if not isinstance(author, str) or not author.strip():
            raise ValidationError(f"comments[{i}].author must be a non-empty string")
        authors.append(author)

        # Validate message
        message = comment["message"]
        if not isinstance(message, str) or not message.strip():
            raise ValidationError(f"comments[{i}].message must be a non-empty string")

        # Validate optional profile_image
        if "profile_image" in comment:
            profile_img = comment["profile_image"]
            if profile_img:  # Only validate if not empty string
                try:
                    validate_file_exists(profile_img, f"comments[{i}].profile_image")
                except ValidationError as e:
                    raise ValidationError(f"Invalid profile_image for {author}: {e}")

        # Validate optional height
        if "height" in comment:
            height = comment["height"]
            if not height_pattern.match(height):
                raise ValidationError(
                    f"comments[{i}].height must be in format 'XXXpx'. Got: '{height}'"
                )

    # Check for duplicate authors (warning only)
    duplicates = [author for author in set(authors) if authors.count(author) > 1]
    if duplicates:
        print(f"⚠ Warning: Duplicate authors found: {', '.join(duplicates)}")

    print(f"✓ All {len(comments)} comments are valid")


def main():
    """Main validation function"""
    print("Validating data.json...")
    print()

    try:
        # Load JSON
        data = load_json()
        print("✓ JSON syntax is valid")

        # Run validations
        validate_person(data)
        validate_backgrounds(data)
        validate_comments(data)

        print()
        print("=" * 50)
        print("✅ All validations passed!")
        print("=" * 50)
        return 0

    except ValidationError as e:
        print()
        print("=" * 50)
        print(f"❌ Validation failed: {e}")
        print("=" * 50)
        return 1
    except Exception as e:
        print()
        print("=" * 50)
        print(f"❌ Unexpected error: {e}")
        print("=" * 50)
        return 1


if __name__ == "__main__":
    sys.exit(main())
