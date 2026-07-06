"""
Test Runner Script
Run all tests with coverage reporting

Following documentation: Running Tests and Interpreting Results
"""

import sys
import subprocess
from pathlib import Path


def run_tests():
    """Run all tests with coverage"""
    print("=" * 60)
    print("🧪 Running Tests for Personalized Networking Assistant")
    print("=" * 60)
    print()
    
    # Ensure we're in the project root
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    
    # Run pytest with coverage
    cmd = [
        "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=app",
        "--cov-report=html",
        "--cov-report=term",
        "--cov-report=term-missing",
        "--maxfail=1"
    ]
    
    print("📌 Running: " + " ".join(cmd))
    print()
    
    try:
        result = subprocess.run(cmd, cwd=project_root)
        return result.returncode
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


def run_specific_test(test_file: str):
    """Run a specific test file"""
    cmd = [
        "pytest",
        f"tests/{test_file}",
        "-v",
        "--cov=app",
        "--cov-report=term"
    ]
    
    try:
        result = subprocess.run(cmd, cwd=project_root)
        return result.returncode
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


if __name__ == "__main__":
    # Parse arguments
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        if not test_file.endswith(".py"):
            test_file += ".py"
        print(f"📌 Running specific test: {test_file}")
        sys.exit(run_specific_test(test_file))
    else:
        sys.exit(run_tests())