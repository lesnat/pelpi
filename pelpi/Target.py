#coding:utf8
import numpy as _np
from __init__ import unit
from __init__ import prefered_unit as _pu


class Material(object):
    """
    """
    def __init__(self,name="",density=0.,atomic_mass=0.,Z=0.,A=0.):
        if name=="":
            print("Define")
        elif name=="Al":
            self.name       = name
            self.density    = 2.69890e3 * unit.kg/unit.m**3
            self.atomic_mass = 26.98154 * unit.u
            self.Z          = 13
            self.A          = 27
        elif name=="W":
            self.name       = name
            self.density    = 1.93000e4 * unit.kg/unit.m**3
            self.atomic_mass = 183.85 * unit.u
            self.Z          = 74
            self.A          = 184
        else:
            self.name       = name
            self.density    = density * unit.kg/unit.m**3
            self.atomic_mass = atomic_mass * unit.u
            self.Z          = Z
            self.A          = A

        self.N              = self.A - self.Z
        self.ni             = self.density/self.atomic_mass
        self.ne             = self.Z*self.density/self.atomic_mass

class Geometry(object): # Ajouter pp
    """
    """
    # def __init__(self,name="",param=[]):
    #     if name=="":
    #         print("Define")
    #     elif name=="cuboid":
    #         self.name           = name
    #         if len(param)!=3:
    #             print("Wrong number of parameters")
    #         else:
    #             self.param      = param
    #     elif name=="cuboid with preplasma":
    #         self.name           = name
    #         if len(param)!=4:
    #             print("Wrong number of parameters")
    #         else:
    #             self.param      = param
    def __init__(self,width=0,Lpp=0):
        self.width      = width
        self.Lpp        = Lpp

class Target(object):
    """



    """
    def __init__(self,Material,Geometry):
        self.mat=Material
        self.geom=Geometry

    def getInfo(self):
        txt  = " \n"
        txt += " Target parameters :\n"
        txt += " ########################################## \n"
        txt += " Material \n"
        txt += " ------------------------------------------ \n"
        txt += " name               :      "+self.mat.name+"\n"
        txt += " density            :      "+str(self.mat.density.to(_pu['mass']*_pu['density']))+" \n"
        txt += " atomic mass        :      "+str(self.mat.atomic_mass.to(_pu['mass']))+" \n"
        txt += " Z                  :      "+str(self.mat.Z)+" \n"
        txt += " A                  :      "+str(self.mat.A)+" \n"
        txt += " N                  :      "+str(self.mat.N)+" \n"
        txt += " ni                 :      "+str(self.mat.ni.to(_pu['density']))+" \n"
        txt += " ne                 :      "+str(self.mat.ne.to(_pu['density']))+" \n"
        txt += " \n"
        txt += " Geometry \n"
        txt += " ------------------------------------------ \n"
        # txt += " name               :      "+self.geom.name+"\n"
        # if self.geom.name=='cuboid':
        #     txt += " param (Lx,Ly,Lz)   :      "+str(self.geom.param)+"\n"
        # if self.geom.name=='cuboid with preplasma':
        #     txt += " param (Lpp,Lx,Ly,Lz) :      "+str(self.geom.param)+"\n"

        txt += " width              :      "+str(self.geom.width.to(_pu['length']))+"\n"
        txt += " Lpp                :      "+str(self.geom.Lpp.to(_pu['length']))+" \n"
        txt += " ########################################## \n"

        return txt


    def plot(self):
        import matplotlib.pyplot as plt
        plt.figure()
