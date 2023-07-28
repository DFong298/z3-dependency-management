""" Script to parse versions of a package from spack package file """

from pathlib import Path
import sys
import re
import requests

def fetch_package_data(package_name) -> str:
    """fetch package details"""
    base_url = "https://raw.githubusercontent.com/spack/spack/develop/var/spack/repos/builtin/packages"
    package_url = f"{base_url}/{package_name}/package.py"
    print(f"Fetching data for package '{package_name}' from:")
    print(package_url)
    print("\n")
    return package_url


def parse_version(pkg_name: Path):
    """Parse the versions from package file"""
    package_url = fetch_package_data(pkg_name)

    r = requests.get(package_url)

    pattern = r'version\("(.*?)"'

    versions = re.findall(pattern, r.text)

    print("The listed versions are:\n")
    print(sorted(versions))
    return sorted(versions)


def print_help():
    """print usage help"""
    print("Usage: ./parse_version.py <file_path>")


def main():
    """Get package name"""

    if len(sys.argv) < 2:
        print("Error: Invalid number of args")
        print_help()
        sys.exit(1)
    package_name = sys.argv[1]

    parse_version(package_name)


if __name__ == "__main__":
    main()
