import json
import parse_version
from z3 import *
from collections import defaultdict

p1 = parse_version.PackageParser()
package = input("Enter package name: ")
x = p1.parse_child_pkgs(package)
p1.make_json("dependencies.json", x)

with open('dependencies.json') as f:
  data = json.load(f)

s = list(data.items())

versions = defaultdict(dict)

while s:
  name, u = s.pop()
  for version in u['versions']:
    versions[name][version] = len(versions[name]) + 1
  if 'child_pkgs' in u:
    for v in u['child_pkgs'].items():
      s.append(v)


symvars = []
solver = Solver()

for k, v in versions.items():
  solver.add(Int(k) >= list(v.items())[0][1], Int(k) <= list(v.items())[-1][1])

print(solver.check())
print(solver)
m = solver.model()
print(m)