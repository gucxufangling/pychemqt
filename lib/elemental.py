#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# Library to implement a library for chemical component from mendeleev table
###############################################################################

import sqlite3


connection = sqlite3.connect('dat/elemental.db')
databank = connection.cursor()


class float(float):
    code = ""
    
color_serie = {
    "Actinide": "#795681", 
    "Alkali metal": "#B92D2D", 
    "Alkaline earth metal": "#B8873A", 
    "Halogen": "#D7C848", 
    "Lanthanide": "#94738F", 
    "Noble gas": "#6186AC", 
    "Nonmetal": "#88AE62", 
    "Post transition metal": "#949692", 
    "Semimetal": "#BF924E", 
    "Transition metal": "#C44343"}

color_block = {
    "D": "#B83A3A", 
    "F": "#725279", 
    "P": "#CEBE3B", 
    "S": "#BC8A3D"}

color_phase = {
    "Solid": "#BB8F4A", 
    "Liquid": "#7BB245", 
    "Gas": "#5D82A8"}

class Elemental(object):
    """Element class with data"""
    
    def __init__(self, id):
        """@param id atomic number of element
        
        The class implement this properties
           id: atomic number
           name
           altname
           symbol
           serie
           group
           period
           block
           density_Solid
           density_Liq
           density_Gas
           appearance
           date
           country
           discover
           etymology
           atomic_mass
           atomic_volume
           atomic_radius
           covalent_radius
           vanderWaals_radius
           ionic_radii
           lattice_type
           space_group
           lattice_edges
           lattice_angles
           electron_configuration
           oxidation
           electronegativity
           electron_affinity
           first_ionization
           Tf
           Tb
           Heat_f
           Heat_b
           Cp
           k
           T_debye
           color
           notes
        """
        if id > 118:
            id = 118
        databank.execute("SELECT * FROM ELEMENTS WHERE id=='%i'" % id)
        data = databank.fetchone()
        
        self.id = int(data[0])
        self.name = data[1]
        self.altname = data[2]
        self.symbol = data[3]
        self.serie = data[4]
        self.group = int(data[5])
        self.period = int(data[6])
        self.block = data[7]
        self.density_Solid = self._unit(data[8])
        self.density_Liq = self._unit(data[9])
        self.density_Gas = self._unit(data[10])
        self.appearance = data[11]
        self.date = data[12]
        self.country = data[13]
        self.discover = data[14]
        self.etymology = data[15]
        self.atomic_mass = self._unit(data[16])
        self.atomic_volume = self._unit(data[17])
        self.atomic_radius = self._unit(data[18])
        self.covalent_radius = self._unit(data[19])
        self.vanderWaals_radius = self._unit(data[20])
        self.ionic_radii = data[21]
        self.lattice_type = data[22]
        self.space_group = data[23]
        self.lattice_edges = eval(data[24])
        self.lattice_angles = eval(data[25])
        self.electron_configuration = data[26]
        self.oxidation = data[27]
        self.electronegativity = self._unit(data[28])
        self.electron_affinity = self._unit(data[29])
        self.first_ionization = self._unit(data[30])
        self.Tf = self._unit(data[31])
        self.Tb = self._unit(data[32])
        if not self.Tf or not self.Tb:
            self.phase = ""
        elif self.Tf > 273.15:
            self.phase = "Solid"
        elif self.Tb < 273.15:
            self.phase = "Gas"
        else:
            self.phase = "Liquid"
        self.Heat_f = self._unit(data[33])
        self.Heat_b = self._unit(data[34])
        self.Cp = self._unit(data[35])
        self.k = self._unit(data[36])
        self.T_debye = self._unit(data[37])
        self.color = data[38]
        self.notes = data[39]

    def _unit(self, str):
        aproximate = False
        try:
            value = float(str)
        except:
            if not str:
                value = None
            elif str[-1] == ")":
                value = float(str.split("(")[1].split(",")[0])
                aproximate = True
#        var = func(value, unit)
        if aproximate:
            value.code = "stimated"
        return value
        
if __name__ == '__main__':
    for i in range(1, 119):
        elemento = Elemental(i)
        print(elemento.symbol, elemento.lattice_edges)