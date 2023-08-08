""" Script to parse versions of a package from spack package file """

from pathlib import Path
import sys
import re
import json
import pprint
import requests


class Package:
    def __init__(self, name, versions):
        self.name = name
        self.versions = versions


class PackageParser:
    """Package Parsing"""

    def pkg_url(self, pkg_name) -> str:
        """parse pkg url"""

        base_url = "https://raw.githubusercontent.com/spack/spack/develop/var/spack/repos/builtin/packages"
        package_url = f"{base_url}/{pkg_name}/package.py"
        return package_url

    def fetch_pkg(self, pkg_name):
        """fetch pkg contents"""
        url = self.pkg_url(pkg_name)
        return requests.get(url, timeout=5).text

    def parse_version(self, pkg_name):
        """Parse the versions from package file"""

        pkg_contents = self.fetch_pkg(pkg_name)

        version_pat = r'version\("(.*?)"'

        versions = re.findall(version_pat, pkg_contents)

        return versions

    def parse_child_pkgs(self, pkg_name, visited_packages=None):
        """Parse the versions from the package file and its child packages recursively"""
        if visited_packages is None:
            visited_packages = set()

        if pkg_name in visited_packages:
            return {}  # Avoid circular dependencies

        visited_packages.add(pkg_name)
        pkg_contents = self.fetch_pkg(pkg_name)
        child_pkg_pat = r'depends_on\("(\w+)"'
        child_pkgs = re.findall(child_pkg_pat, pkg_contents)

        # virtual_pkg_mapping.json contains the mapping of virtual packages and their providers
        # virtual pkgs and the url for fetching `package.py` have different naming for
        # virtual pkgs,hence this workaround

        # TODO: All the virtual packages in the json file below is *not* mapped to their providers,
        # Map all of them.

        with open("./virtual_pkg_mapping.json", "r", encoding="utf-8") as f_handle:
            data = json.load(f_handle)
            for i, child_pkg in enumerate(child_pkgs):
                if child_pkg in data:
                    child_pkgs[i] = data[child_pkg]

        if pkg_name is not None:
            pkgs = {}
            for child_pkg in child_pkgs:
                versions = self.parse_version(child_pkg)
                child_pkgs_recursive = self.parse_child_pkgs(
                    child_pkg, visited_packages
                )
                pkgs[child_pkg] = {
                    "versions": versions,
                    "child_pkgs": child_pkgs_recursive,
                }
            return pkgs
        
    def make_json(self, filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f)


# p1 = PackageParser()
# x = p1.parse_child_pkgs("butterflypack")
# pprint.pprint(x)
# p1.make_json("func.json", x)

# with open('output.json', 'w') as f:
#     json.dump(x, f)