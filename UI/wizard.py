#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''Pychemqt, Chemical Engineering Process simulator
Copyright (C) 2016, Juan José Gómez Romera <jjgomera@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''


###############################################################################
# Module with wizard project configuration
# when it creates a new pychemqt project it execute this wizard to configure:
#   -Component list
#   -Thermodynamic properties methods
#   -Transport properties methods
#   -Units prefered
# The wizard can be launch whanever you want using its menu entry
#
# -auto: Function to calculate autovalues for thermo calculation
# -AutoDialog: Dialog to define values for auto function, this dialog can be
# launch in thermo page of wizard to autoselect a good stimation of values
###############################################################################


from configparser import ConfigParser
import os

from PyQt5 import QtGui, QtWidgets

from lib.config import conf_dir
from lib.unidades import Temperature, Pressure
from tools import (UI_confComponents, UI_confTransport, UI_confThermo,
                   UI_confUnits, UI_confResolution)
from lib import mEoS, gerg, refProp, coolProp
from UI.widgets import Entrada_con_unidades


def auto(tmin=None, tmax=None, pmin=None, pmax=None, components=[]):
    """Function to calculate autovalues for thermo calculation
        tmin: Stimated minimum temperature from project
        tmax: Stimated maximum temperature from project
        pmin: Stimated minimum pressure from project
        pmax: Stimated maximum pressure from project
        Components: array with ids numbers component from project"""
    config = ConfigParser()
    config = UI_confThermo.UI_confThermo_widget.default(config)

    # TODO: add EOS configuration

    GERG_available = True
    REFPROP_available = True
    for id in components:
        if id not in gerg.id_GERG:
            GERG_available = False
        if id not in refProp.__all__:
            REFPROP_available = False

    if len(components) == 1 and components[0] == 62:
        config.set("Thermo", "iapws", "True")
        if os.environ["freesteam"] == "True":
            config.set("Thermo", "freesteam", "True")

    if len(components) == 1 and components[0] in mEoS.id_mEoS:
        config.set("Thermo", "MEoS", "True")
    if os.environ["CoolProp"] == "True" and len(components) == 1 and \
            components[0] in coolProp.__all__:
            config.set("Thermo", "coolprop", "True")
    if os.environ["refprop"] == "True" and REFPROP_available:
        config.set("Thermo", "refprop", "True")
    if GERG_available:
        config.set("Thermo", "GERG", "True")

    return config


class AutoDialog(QtWidgets.QDialog):
    """Dialog to input value for auto thermal function"""
    def __init__(self, parent=None):
        super(AutoDialog, self).__init__(parent)
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(QtWidgets.QLabel(QtWidgets.QApplication.translate(
            "pychemqt", "T<sub>min</sub>")), 1, 1)
        self.Tmin = Entrada_con_unidades(Temperature)
        layout.addWidget(self.Tmin, 1, 2)
        layout.addWidget(QtWidgets.QLabel(QtWidgets.QApplication.translate(
            "pychemqt", "T<sub>max</sub>")), 2, 1)
        self.Tmax = Entrada_con_unidades(Temperature)
        layout.addWidget(self.Tmax, 2, 2)
        layout.addWidget(QtWidgets.QLabel(QtWidgets.QApplication.translate(
            "pychemqt", "P<sub>min</sub>")), 3, 1)
        self.Pmin = Entrada_con_unidades(Pressure)
        layout.addWidget(self.Pmin, 3, 2)
        layout.addWidget(QtWidgets.QLabel(QtWidgets.QApplication.translate(
            "pychemqt", "P<sub>max</sub>")), 4, 1)
        self.Pmax = Entrada_con_unidades(Pressure)
        layout.addWidget(self.Pmax, 4, 2)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox, 5, 1, 1, 2)


class Wizard(QtWidgets.QWizard):
    """Wizard dialog for project configuration"""
    def __init__(self, config=None, parent=None):
        super(Wizard, self).__init__(parent)
        self.config = config
        self.setWindowTitle(QtWidgets.QApplication.translate(
            "pychemqt", "Configuration wizard..."))
        self.setOptions(QtWidgets.QWizard.ExtendedWatermarkPixmap |
                        QtWidgets.QWizard.IndependentPages |
                        QtWidgets.QWizard.HaveCustomButton1)
        self.setWizardStyle(QtWidgets.QWizard.ModernStyle)

        botonAuto = QtWidgets.QPushButton(
            QtWidgets.QApplication.translate("pychemqt", "Auto"))
        botonAuto.setToolTip(QtWidgets.QApplication.translate(
            "pychemqt",
            "Choose good values from project components and conditions"))
        self.setButton(QtWidgets.QWizard.CustomButton1, botonAuto)
        self.customButtonClicked.connect(self.auto)

        page1_welcome = QtWidgets.QWizardPage()
        page1_welcome.setTitle(
            QtWidgets.QApplication.translate("pychemqt", "Welcome"))
        page1_welcome.setSubTitle(QtWidgets.QApplication.translate(
            "pychemqt",
            "That's the configuration wizard of a new project from pychemqt"))
        page1_welcome.setPixmap(QtWidgets.QWizard.LogoPixmap, QtGui.QPixmap(
            os.path.join(os.environ["pychemqt"], "images", "pychemqt_98.png")))
        page1_welcome.setPixmap(
            QtWidgets.QWizard.WatermarkPixmap, QtGui.QPixmap(
                os.path.join(os.environ["pychemqt"], "images", "logo_2.jpg")))
        lyt = QtWidgets.QVBoxLayout(page1_welcome)
        lyt.addWidget(QtWidgets.QLabel(QtWidgets.QApplication.translate(
            "pychemqt",
            """<html><body>
This wizard let's you configure all parameters necessary in a pychemqt's
project<br>
All options will can be changed later using the options in menu Edit, and this
wizard<br>
can be run at any time later.<br>
These are the options you must expecific next:<br>

<ul>
 <li>Component list</li>
 <li>Thermodinamic properties</li>
 <li>Transport properties</li>
 <li>Engineering units preferred</li>
</ul>
<body></html>""")))
        self.addPage(page1_welcome)

        page2_components = QtWidgets.QWizardPage()
        page2_components.setTitle(QtWidgets.QApplication.translate(
            "pychemqt", "Define components"))
        page2_components.setSubTitle(QtWidgets.QApplication.translate(
            "pychemqt", "Add componentes from database"))
        page2_components.setPixmap(QtWidgets.QWizard.LogoPixmap, QtGui.QPixmap(
            os.path.join(os.environ["pychemqt"], "images", "pychemqt_98.png")))
        lyt = QtWidgets.QVBoxLayout(page2_components)
        self.componentes = UI_confComponents.UI_confComponents_widget(config)
        self.componentes.componentChanged.connect(self.button(
            QtWidgets.QWizard.NextButton).setEnabled)

        lyt.addWidget(self.componentes)
        self.addPage(page2_components)

        page3_thermo = QtWidgets.QWizardPage()
        page3_thermo.setTitle(QtWidgets.QApplication.translate(
            "pychemqt", "Define thermodynamics procedures"))
        page3_thermo.setSubTitle(QtWidgets.QApplication.translate(
            "pychemqt", "The thermodynamics properties are the basic of \
pychemqt, a bad selection would be disastrous for the results"))
        page3_thermo.setPixmap(QtWidgets.QWizard.LogoPixmap, QtGui.QPixmap(
            os.path.join(os.environ["pychemqt"], "images", "pychemqt_98.png")))
        lyt = QtWidgets.QVBoxLayout(page3_thermo)
        self.thermo = UI_confThermo.UI_confThermo_widget(config)
        lyt.addWidget(self.thermo)
        self.addPage(page3_thermo)

        page4_transport = QtWidgets.QWizardPage()
        page4_transport.setTitle(QtWidgets.QApplication.translate(
            "pychemqt", "Define transport procedures"))
        page4_transport.setSubTitle(QtWidgets.QApplication.translate(
            "pychemqt", "The transport properties are important too for good \
simulation results"))
        page4_transport.setPixmap(QtWidgets.QWizard.LogoPixmap, QtGui.QPixmap(
            os.path.join(os.environ["pychemqt"], "images", "pychemqt_98.png")))
        lyt = QtWidgets.QVBoxLayout(page4_transport)
        self.transport = UI_confTransport.UI_confTransport_widget(config)
        lyt.addWidget(self.transport)
        self.addPage(page4_transport)

        page5_units = QtWidgets.QWizardPage()
        page5_units.setTitle(QtWidgets.QApplication.translate(
            "pychemqt", "Define preferred units"))
        page5_units.setSubTitle(QtWidgets.QApplication.translate(
            "pychemqt", "The preferred units are not necessary for the \
simulation, but a good election let you only focus in simulation"))
        page5_units.setPixmap(QtWidgets.QWizard.LogoPixmap, QtGui.QPixmap(
            os.path.join(os.environ["pychemqt"], "images", "pychemqt_98.png")))
        lyt = QtWidgets.QVBoxLayout(page5_units)
        self.units = UI_confUnits.UI_confUnits_widget(config)
        lyt.addWidget(self.units)
        self.addPage(page5_units)
        self.currentIdChanged.connect(self.checkComponents)

    def checkComponents(self, id):
        """Component window can be only passed with any added components"""
        if id == 1:
            self.button(QtWidgets.QWizard.NextButton).setEnabled(len(
                self.componentes.indices) != 0)
        self.button(QtWidgets.QWizard.CustomButton1).setVisible(id == 2)

    def auto(self):
        """Dialog to define project parameter to auto thermal configuration"""
        dialogo = AutoDialog()
        if dialogo.exec_():
            tmin = dialogo.Tmin.value
            tmax = dialogo.Tmax.value
            pmin = dialogo.Pmin.value
            pmax = dialogo.Pmax.value
            config = auto(tmin, tmax, pmin, pmax, self.componentes.indices)
            self.thermo.setConfig(config)

    @property
    def value(self):
        config = self.componentes.value(self.config)
        config = self.thermo.value(config)
        config = self.transport.value(config)
        config = self.units.value(config)
        if not config.has_section("PFD"):
            config.add_section("PFD")
            Preferences = ConfigParser()
            Preferences.read(conf_dir+"pychemqtrc")
            config.set("PFD", "x", Preferences.get("PFD", "x"))
            config.set("PFD", "y", Preferences.get("PFD", "y"))
        return config

    @classmethod
    def default(cls):
        config = ConfigParser()
        config = UI_confComponents.UI_confComponents_widget.default(config)
        config = UI_confThermo.UI_confThermo_widget.default(config)
        config = UI_confTransport.UI_confTransport_widget.default(config)
        config = UI_confUnits.UI_confUnits_widget.default(config)
        config = UI_confResolution.UI_confResolution_widget.default(config)
        return config

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Wizard()
    ui.show()
    sys.exit(app.exec_())
