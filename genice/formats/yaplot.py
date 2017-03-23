import numpy     as np
from genice.formats.baseclass import GenIce
from genice import yaplotlib as yp
class Formatter(GenIce):
    """
    Gro file format
    defined in http://manual.gromacs.org/current/online/gro.html
    """
    def run(self, options):
        water_type    = options.water[0]
        guests        = options.guests
        self.stage1()   #replicate the unit cell
        self.stage2()   #prepare random graph

        #Failed to build the undirected graph obeying the ice rule.
        self.logger.info("Output HBN in Yaplot format.")

        undir = self.graph.to_undirected()
        
        s = ""
        s += yp.Size(0.06)
        for i in self.graph.nodes_iter():
            pos = np.dot( self.reppositions[i], self.cell )
            if 4 == len(undir.neighbors(i)):
                s += yp.Color(3)
            else:
                logger.debug("Z({1})={0}".format(undir.neighbors(i),i))
                s += yp.Color(5)
            s += yp.Circle(pos)
        s += yp.Color(2)
        for i,j in self.graph.edges_iter(data=False):
            s1 =self.reppositions[i]
            s2 =self.reppositions[j]
            d = s2-s1
            d -= np.floor( d + 0.5 )
            s2 = s1 + d
            s += yp.Line(np.dot(s1,self.cell),np.dot(s2,self.cell))

        if not self.test2:
            print(s)
            return

        self.stage3()   #Make an ice graph
        self.stage4()   #Depolarize
        self.stage5()   #Orientation
        self.stage6(water_type)  #Water atoms
        self.stage7(guests)      #Guest atoms
        self.logger.info("Total number of atoms: {0}".format(len(self.atoms)))
        network = s
        s = self.yapresult
        H = []
        O  = ""
        for atom in self.atoms:
            resno, resname, atomname, position = atom
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
        s += network
        print(s)
