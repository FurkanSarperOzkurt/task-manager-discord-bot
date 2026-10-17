"""
testleri calistirmak icin kisa yol
python run_tests.py diyince hepsini calistirir
"""

import subprocess
import sys


def main():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd=".",
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
