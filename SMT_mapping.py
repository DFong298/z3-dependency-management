from z3 import *
import parse_version as pv

# We use butterflypack as an example for the code

package = input("Enter library name:")
v_list = pv.parse_version(package)

i = 0
mapping = {}

for version in reversed(v_list):
    mapping[version] = i
    i += 1


print(mapping)
# Suppose we want butterflypack version >1.2.0 and <2.1.1 of butterflypack
s = Solver()
x = Int('x') # maybe iterate through letters by using ord() for each package 

s.add( Or (x < mapping['1.2.0'], x > mapping['2.1.1']))
s.check()
m = s.model()

print(m[x].as_long()) # solved key integer 

print(list(mapping.keys())[int(m[x].as_long())]) # solved version