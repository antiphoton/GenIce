"""
Test for generating water positions from cage positions
"""


cages="""
12 0.5 0.5 0.5
14 0.5 0.0 -0.25
14 0.0 0.25 0.5
14 0.75 0.5 0.0
14 0.5 0.0 0.25
12 0.0 0.0 0.0
14 0.25 0.5 0.0
14 0.0 -0.25 0.5
"""



celltype = 'rect'

cell = """
12.747893943706936 12.747893943706936 12.747893943706936
"""

from genice import libgenice, FrankKasper
cagepos, cagetype = libgenice.parse_cages(cages)
cell9             = libgenice.parse_cell(cell, celltype)
waters = [w for w in FrankKasper.toWater(cagepos, cell9)]
coord = "relative"
density = FrankKasper.estimate_density(waters, cell9, 2.76)
bondlen = 2.76 * 1.2