#!/usr/bin/env python3
# -*- python -*-

from __future__ import print_function
import os
import sys
import numpy     as np
import argparse  as ap
import logging
import importlib
import networkx as nx

from genice import rigid
from genice import yaplot as yp
from genice.libgenice import safe_import

def oxygenize(coord, cell, name):
    atoms = []
    for node in range(len(coord)):
        abscom = np.dot(coord[node],cell)  # relative to absolute
        atoms.append([0,name, "O", abscom])
    return atoms





def format_yaplot(atoms, cell, celltype):
    logger = logging.getLogger()
    logger.info("Output in Yaplot format.")
    s = ""
    H = []
    O  = ""
    for i in range(len(atoms)):
        resno, resname, atomname, position = atoms[i]
        if resno == 0:
            if O is not "":
                s += yp.Color(3)
                s += yp.Size(0.02)
                s += yp.Circle(O)
                if len(H):
                    s += yp.Line(O,H[0])
                    s += yp.Line(O,H[1])
            H = []
            O = ""
        if "O" in atomname:
            O = position
        elif "H" in atomname:
            H.append(position)
        else:
            s += yp.Color(4)
            s += yp.Size(0.04)
            s += yp.Circle(position)
    if O is not "":
        s += yp.Circle(O)
        if len(H):
            s += yp.Line(O,H[0])
            s += yp.Line(O,H[1])
    return s



def format_euler(positions, cell, rotmatrices, celltype):
    logger = logging.getLogger()
    logger.info("Output water molecules as rigid rotors (Euler).")
    s = ""
    if celltype == "rect":
        s += "@BOX3\n"
        s += "{0} {1} {2}\n".format(cell[0,0]*10,cell[1,1]*10,cell[2,2]*10)
    else:
        s += "@BOX9\n"
        for d in range(3):
            s += "{0} {1} {2}\n".format(cell[0,d]*10,cell[1,d]*10,cell[2,d]*10)
    s += "@NX3A\n"
    s += "{0}\n".format(len(positions))
    for i in range(len(positions)):
        position = np.dot(positions[i],cell)*10   #in Angstrom
        euler = rigid.quat2euler(rigid.rotmat2quat(rotmatrices[i].transpose()))
        s += "{0:9.4f} {1:9.4f} {2:9.4f}  {3:9.4f} {4:9.4f} {5:9.4f}\n".format(position[0],
                                                                               position[1],
                                                                               position[2],
                                                                               euler[0],
                                                                               euler[1],
                                                                               euler[2])
    return s


def format_quaternion(positions, cell, rotmatrices, celltype):
    logger = logging.getLogger()
    logger.info("Output water molecules as rigid rotors (Quaternion).")
    s = ""
    if celltype == "rect":
        s += "@BOX3\n"
        s += "{0} {1} {2}\n".format(cell[0,0]*10,cell[1,1]*10,cell[2,2]*10)
    else:
        s += "@BOX9\n"
        for d in range(3):
            s += "{0} {1} {2}\n".format(cell[0,d]*10,cell[1,d]*10,cell[2,d]*10)
    s += "@NX4A\n"
    s += "{0}\n".format(len(positions))
    for i in range(len(positions)):
        position = np.dot(positions[i],cell)*10   #in Angstrom
        quat     = rigid.rotmat2quat(rotmatrices[i].transpose())
        s += "{0:9.4f} {1:9.4f} {2:9.4f}  {3:9.4f} {4:9.4f} {5:9.4f} {6:9.4f}\n".format(position[0],
                                                                               position[1],
                                                                               position[2],
                                                                               quat[0],
                                                                               quat[1],
                                                                               quat[2],
                                                                               quat[3])
    return s


def format_com(positions, cell, celltype):
    logger = logging.getLogger()
    logger.info("Output centers of mass of water molecules.")
    s = ""
    if celltype == "rect":
        s += "@BOX3\n"
        s += "{0} {1} {2}\n".format(cell[0,0]*10,cell[1,1]*10,cell[2,2]*10)
    else:
        s += "@BOX9\n"
        for d in range(3):
            s += "{0} {1} {2}\n".format(cell[0,d]*10,cell[1,d]*10,cell[2,d]*10)
    s += "@AR3A\n"
    s += "{0}\n".format(len(positions))
    for i in range(len(positions)):
        position = np.dot(positions[i],cell)*10   #in Angstrom
        s += "{0:9.4f} {1:9.4f} {2:9.4f}\n".format(position[0],
                                                   position[1],
                                                   position[2])
    return s


def format_rcom(positions, cell, celltype):
    logger = logging.getLogger()
    logger.info("Output centers of mass of water molecules.")
    s = ""
    if celltype == "rect":
        s += "@BOX3\n"
        s += "{0} {1} {2}\n".format(cell[0,0]*10,cell[1,1]*10,cell[2,2]*10)
    else:
        s += "@BOX9\n"
        for d in range(3):
            s += "{0} {1} {2}\n".format(cell[0,d]*10,cell[1,d]*10,cell[2,d]*10)
    s += "@AR3R\n"
    s += "{0}\n".format(len(positions))
    for i in range(len(positions)):
        position = positions[i]
        s += "{0:9.4f} {1:9.4f} {2:9.4f}\n".format(position[0],
                                                   position[1],
                                                   position[2])
    return s


def format_python(positions, cell, celltype, bondlen):
    logger = logging.getLogger()
    logger.info("Output water molecules as a Python module.")
    s = ""
    s += "bondlen={0}\n".format(bondlen)
    s += "celltype='{0}'\n".format(celltype)
    s += "coord='relative'\n"
    if celltype != "rect":
        sys.exit(1)
    NB   = 6.022e23
    density = 18.0 * len(positions) / (cell[0,0]*cell[1,1]*cell[2,2]*1e-24*NB) * 1e-3
    s += "density={0}\n".format(density)
    s += "cell='{0} {1} {2}'\n".format(cell[0,0],cell[1,1],cell[2,2])
    s += "waters=\"\"\"\n"
    for i in range(len(positions)):
        position = positions[i]
        s += "{0:9.4f} {1:9.4f} {2:9.4f}\n".format(position[0],position[1],position[2])
    s += "\"\"\"\n\n"
    return s


def format_digraph(graph, positions):
    logger = logging.getLogger()
    logger.info("Output the hydrogen bond network.")
    from genice import digraph
    
    s = ""
    s += "@NGPH\n"
    s += "{0}\n".format(len(positions))
    for i,j,k in graph.edges_iter(data=True):
        s += "{0} {1}\n".format(i,j)
    s += "-1 -1\n"
    return s


                     
def format_openscad2(graph, positions, cell, celltype, rep, scale=50, roxy=0.07, rbond=0.06):
    """
    cell is in nm

    openscad2 comes up with OO style
    """
    logger = logging.getLogger()
    logger.info("Output water molecules in OpenSCAD format revised.")
    from genice import openscad2
    #logger = logging.getLogger()
    rep = np.array(rep)
    trimbox    = cell *np.array([(rep[i]-2)/rep[i] for i in range(3)])
    trimoffset = (cell[0]+cell[1]+cell[2])/rep

    margin = 0.2 # expansion relative to the cell size
    lower = (1.0 - margin) / rep
    upper = (rep - 1.0 + margin) / rep
    
    bonds = []
    for i,j in graph.edges_iter(data=False):
        s1 =positions[i]
        s2 =positions[j]
        d = s2-s1
        d -= np.floor( d + 0.5 )
        logger.debug("Len {0}-{1}={2}".format(i,j,np.linalg.norm(d)))
        s2 = s1 + d
        if ( (lower[0] < s1[0] < upper[0] and lower[1] < s1[1] < upper[1] and lower[2] < s1[2] < upper[2] ) or
             (lower[0] < s2[0] < upper[0] and lower[1] < s2[1] < upper[1] and lower[2] < s2[2] < upper[2] ) ):
            bonds.append( (np.dot(s1,cell), np.dot(s2,cell)))
        
    nodes = []
    for s1 in positions:
        if lower[0] < s1[0] < upper[0] and lower[1] < s1[1] < upper[1] and lower[2] < s1[2] < upper[2]:
            nodes.append( np.dot(s1, cell) )
        
    o = openscad2.OpenScad()
    objs = [o.sphere(r="Roxy").translate(node) for node in nodes] + [o.bond(s1,s2,r="Rbond") for s1,s2 in bonds]
    #operations
    ops = [openscad2.bondfunc,
        o.defvar("$fn", 20),
        o.defvar("Roxy", roxy),
        o.defvar("Rbond", rbond),
        ( o.rhomb(trimbox).translate(trimoffset) & o.add(*objs) ).translate(-trimoffset).scale([scale,scale,scale])]
    return o.encode(*ops)
                     
def format_yaplot0(graph, positions, cell, celltype):
    """
    cell is in nm
    HBN in yaplot 
    """
    logger = logging.getLogger()
    logger.info("Output HBN in Yaplot format.")

    undir = graph.to_undirected()
    #for i in graph.nodes_iter():
    #    if len(nx.neighbors(i)) ==
        
    s = ""
    s += yp.Size(0.06)
    for i in graph.nodes_iter():
        pos = np.dot( positions[i], cell )
        if 4 == len(undir.neighbors(i)):
            s += yp.Color(3)
        else:
            logger.debug("Z({1})={0}".format(undir.neighbors(i),i))
            s += yp.Color(5)
        s += yp.Circle(pos)
    s += yp.Color(2)
    for i,j in graph.edges_iter(data=False):
        s1 =positions[i]
        s2 =positions[j]
        d = s2-s1
        d -= np.floor( d + 0.5 )
        s2 = s1 + d
        #if np.dot(d,d) < 0.0000001:
        #    logger.debug("{1}={0}".format(i,j))
        s += yp.Line(np.dot(s1,cell),np.dot(s2,cell))
    return s




def getoptions():
    parser = ap.ArgumentParser(description='')
    parser.add_argument('--rep',  '-r', nargs = 3, type=int,   dest='rep',  default=[2,2,2],
                        help='Repeat the unit cell in x,y, and z directions. [2,2,2]')
    parser.add_argument('--dens', '-d', nargs = 1, type=float, dest='dens', default=(-1,),
                        help='Specify the ice density in g/cm3')
    parser.add_argument('--seed', '-s', nargs = 1, type=int,   dest='seed', default=(1000,),
                        help='Random seed [1000]')
    parser.add_argument('--format', '-f', nargs = 1,           dest='format', default=("gromacs",), metavar="gmeqdypoc",
                        help='Specify file format [g(romacs)|m(dview)|e(uler)|q(uaternion)|d(igraph)|y(aplot)|p(ython module)|o(penScad)|c(entersofmass)|r(elative com)]')
    parser.add_argument('--water', '-w', nargs = 1,           dest='water', default=("tip3p",), metavar="model",
                        help='Specify water model. (tip3p, tip4p, etc.)')
    parser.add_argument('--guest', '-g', nargs = 1,           dest='guests', metavar="D=empty", action="append", 
                        help='Specify guest in the cage. (D=empty, T=co2, etc.)')
    parser.add_argument('--debug', '-D', action='store_true', dest='debug',
                        help='Output debugging info.')
    parser.add_argument('--quiet', '-q', action='store_true', dest='quiet',
                        help='Do not output progress messages.')
    parser.add_argument('Type', nargs=1,
                       help='Crystal type (1c,1h,etc. See https://github.com/vitroid/GenIce for available ice structures.)')
    return parser.parse_args()



def main0():
    #prepare user's workarea
    home = os.path.expanduser("~")
    if os.path.exists(home+"/Library/Application Support"): #MacOS
        homegenice = home+"/Library/Application Support/GenIce"
    else:
        homegenice = os.path.expanduser(home + "/.genice") #Other unix
    sys.path.append(homegenice)
    try:
        os.makedirs(homegenice+"/lattices")
        os.makedirs(homegenice+"/molecules")
    except:
        pass #just ignore when failed.
    #Parse options
    options = getoptions()
    #Set verbosity level
    if options.debug:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s %(message)s")
    elif options.quiet:
        logging.basicConfig(level=logging.WARN,
                            format="%(asctime)s %(levelname)s %(message)s")
    else:
        #normal
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)s %(message)s")
    logger = logging.getLogger()
    logger.debug("Debug mode.")
    logger.debug(options.Type)
    
    #Water type: default is TIP3P, reluctantly.
    water_type    = options.water[0]

    #Output type: default is Gromacs, of course!
    output_format = options.format[0][0]
    if output_format in ["c", "r", ]:
        #com only ("c" absolute; "r" relative)
        stage = 0
    elif output_format in ["o", ]:
        #undir graph
        stage = 1
    elif output_format in ["d", ]:
        #directed graph
        stage = 2
    else:
        #everything
        stage = 3
        
    if output_format == "o":
        #OpenSCAD
        options.rep[0] += 2
        options.rep[1] += 2
        options.rep[2] += 2 #cut margin

    #Prepare everything here.
    result = generate_ice(options.Type[0],
                          seed=options.seed[0],
                          rep=options.rep,
                          density=options.dens[0],
                          stage=stage
                          )
    
    #Final output formats

    positions   = result["positions"]
    cell        = result["cell"]
    celltype    = result["celltype"]
    bondlen     = result["bondlen"]

    logger.info("Cell type: {0}".format(celltype))
    logger.info("Cell shape (nm): a {0} {1} {2}".format(*cell[0]))
    logger.info("Cell shape (nm): b {0} {1} {2}".format(*cell[1]))
    logger.info("Cell shape (nm): c {0} {1} {2}".format(*cell[2]))
    logger.info("Number of water molecules: {0}".format(len(positions)))
    logger.info("Water model: {0}".format(water_type))

    #These output types do not utilize the graph.
    if output_format == "p":        # python Lattice library
        s = format_python(positions, cell, celltype, bondlen)
        print(s,end="")
        sys.exit(0)
    elif output_format == "c":          # CoM only, AR3A
        s = format_com(positions, cell, celltype)
        print(s,end="")
        sys.exit(0)
    elif output_format == "r":          # Relative CoM only, AR3R
        s = format_rcom(positions, cell, celltype)
        print(s,end="")
        sys.exit(0)

    graph       = result["graph"]

    #In case the graph is wanted.
    if output_format == "d":
        s = format_digraph(graph, positions)
        print(s,end="")
        sys.exit(0)

    if output_format == "o":
        #OpenSCAD
        s = format_openscad2(graph, positions, cell, celltype, options.rep)
        print(s,end="")
        sys.exit(0)

    yaplot = ""
    if "yaplot" in result:
        yaplot += result["yaplot"]

    if "rotmatrices" in result:
        rotmatrices = result["rotmatrices"]
    else:
        #Random orientation
        if output_format == "y":
            s = format_yaplot0(graph, positions, cell, celltype)
            print(s,end="")
            sys.exit(0)
        logger.info("The network is not specified.  Water molecules will be orinented randomly.")
        rotmatrices = [rigid.rand_rotation_matrix() for pos in positions]

    #For rigid rotors; no atomic information is required.
    if output_format == "e":          # NX3A
        s = format_euler(positions, cell, rotmatrices, celltype)
        print(s,end="")
        sys.exit(0)
    elif output_format == "q":        # NX4A
        s = format_quaternion(positions, cell, rotmatrices, celltype)
        print(s,end="")
        sys.exit(0)

    #arrange water atoms
    assert audit_name(water_type), "Dubious water name: {0}".format(water_type)
    water = importlib.import_module("genice.molecules."+water_type)
    atoms = arrange_atoms(positions, cell, rotmatrices, water.sites, water.labels, water.name)

    #arrange guest atoms
    cagepos, cagetype = generate_cages(options.Type[0], options.rep)
    if cagepos is not None:
        cagetypes = set(cagetype)
        logger.info("Cage types: {0}".format(cagetypes))
    if options.guests is not None and cagepos is not None:
        #Make the cage type to guest type correspondence
        guest_in_cagetype = dict()
        for arg in options.guests:
            key, value = arg[0].split("=")
            guest_in_cagetype[key] = value
        #replicate the cagetype array
        cagetype = np.array([cagetype[i%len(cagetype)] for i in range(cagepos.shape[0])])
        for ctype in cagetypes:
            #filter the cagepos
            cpos = cagepos[cagetype == ctype]
            #guest molecules are not rotated.
            cmat = np.array([np.identity(3) for i in range(cpos.shape[0])])
            #If the guest molecule type is given,
            if ctype in guest_in_cagetype:
                gname = guest_in_cagetype[ctype]
                #Always check before dynamic import
                assert audit_name(gname), "Dubious guest name: {0}".format(gname)
                gmol = importlib.import_module("genice.molecules."+gname)
                logger.info("{0} is in the cage type '{1}'".format(guest_in_cagetype[ctype], ctype))
                atoms += arrange_atoms(cpos, cell, cmat, gmol.sites, gmol.labels, gmol.name)
    if output_format == "m":      # MDView
        s = format_mdv(atoms, cell, celltype)
    elif output_format == "g":    # GROMACS
        s = format_gro(atoms, cell, celltype)
    elif output_format == "y":    # yaplot
        #Depolarizing process is drawn in "yaplot" variable.
        s = yaplot
        s += format_yaplot(atoms, cell, celltype)
    print(s, end="")
    logger.info("Completed.")



        

def main():
    #prepare user's workarea
    home = os.path.expanduser("~")
    if os.path.exists(home+"/Library/Application Support"): #MacOS
        homegenice = home+"/Library/Application Support/GenIce"
    else:
        homegenice = os.path.expanduser(home + "/.genice") #Other unix
    sys.path.append(homegenice)
    try:
        os.makedirs(homegenice+"/lattices")
        os.makedirs(homegenice+"/molecules")
        os.makedirs(homegenice+"/formats")
    except:
        pass #just ignore when failed.
    #Parse options
    options = getoptions()
    #Set verbosity level
    if options.debug:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s %(message)s")
    elif options.quiet:
        logging.basicConfig(level=logging.WARN,
                            format="%(asctime)s %(levelname)s %(message)s")
    else:
        #normal
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)s %(message)s")
    logger = logging.getLogger()
    logger.debug("Debug mode.")
    logger.debug(options.Type)

    formatter = safe_import("format", options.format[0])
    writer = formatter.Formatter(options.Type[0],
                                seed=options.seed[0],
                                rep=options.rep,
                                density=options.dens[0])
    writer.run(options)
    
    
if __name__ == "__main__":
    main()
