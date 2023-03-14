import sys
from os import listdir,system
import re

def f(txt):
    if re.match('anti[a-zA-Z]*', txt): return "group"
    else: return "none"

print(f("antibiotics"))