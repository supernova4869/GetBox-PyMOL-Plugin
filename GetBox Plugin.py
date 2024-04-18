# -*- coding: utf-8 -*-   
from __future__ import print_function
from pymol import cgo
from pymol import cmd
from random import randint
from pymol.vfont import plain
 
##############################################################################
# GetBox Plugin.py --  Draws a box surrounding a selection and gets box information
# This script is used to get box information for LeDock, Autodock Vina and AutoDock Vina. 
# Copyright (C) 2014 by Mengwu Xiao (Hunan University)
#                                                         
# USAGES:  See function GetBoxHelp()
# REFERENCE:  drawBoundingBox.py  written by  Jason Vertrees 
# EMAIL: mwxiao AT hnu DOT edu DOT cn
# Changes:  
# 2014-07-30 first version was uploaded to BioMS http://bioms.org/forum.php?mod=viewthread&tid=1234
# 2018-02-04 uploaded to GitHub https://github.com/MengwuXiao/Getbox-PyMOL-Plugin 
#            fixed some bugs: python 2/3 and PyMOL 1.x are supported;
#            added support to AutoDock;
#            added tutorials in English;
# NOTES: 
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
# the GNU General Public License for more details.                                        
##############################################################################


def __init__(self):
	self.menuBar.addcascademenu('Plugin', 'GetBox Plugin', 'GetBox PyMOL Plugin', label='GetBox Plugin')
	self.menuBar.addmenuitem('GetBox Plugin', 'command', 'GetBoxHelp', label='Advanced usage', command=lambda _ : GetBoxHelp())
	self.menuBar.addmenuitem('GetBox Plugin', 'command', 'AutoBox', label='Autodetect box', command=lambda _ : autobox())
	self.menuBar.addmenuitem('GetBox Plugin', 'command', 'GetBox', label='Get box from selection (sele)', command=lambda _ : getbox())
	# self.menuBar.addmenuitem('GetBox Plugin', 'command', 'WriteBox', label='Write box file', command=lambda _ : writebox())
	self.menuBar.addmenuitem('GetBox Plugin', 'command', 'Remove HETATM', label='Remove HETATM', command=lambda _ : rmhet())


def GetBoxHelp():
    print('''
get latest plugin and tutorials at https://github.com/MengwuXiao/Getbox-PyMOL-Plugin

Usages:
this plugin is a simple tool to get box information for LeDock, Autodock (Vina) and DSDP. Using the following functions to get box is recommended.

* autobox [extending] (NOTES: solvent & some anions will be removed)
    this function autodetects box in chain A with one click of mouse, but sometimes it fails for too many ligands or no ligand
    e.g. autobox
    
* getbox [selection = (sele), [extending = 5.0]]
    this function creates a box that around the selected objects (residues or ligands or HOH or others). Selecting ligands or residues in the active cavity reported in papers is recommended
    e.g. getbox
    e.g. getbox (sele), 6.0
    
* resibox [Residues String, [extending = 5.0]]
    this function creates a box that arroud the input residues in chain A. Selecting residues in the active cavity reported in papers is recommended\n\
    e.g. resibox resi 214+226+245, 8.0
    e.g. resibox resi 234 + resn HEM, 6.0
    
* showbox [minX, maxX, minY, maxY, minZ, maxZ]
    this function creates a box based on the input axis, used to visualize box or amend box coordinate
    e.g. showbox 2,3,4,5,6,7
 
 * rmhet
 	remove HETATM, remove all HETATM in the screen
 	   
Notes:
* If you have any questions or advice, please do not hesitate to contact me (mwxiao AT hnu DOT edu DOT cn), thank you!
''')

    return

# def showaxes(minX, minY, minZ):
	# cmd.delete('axes')
	# w = 0.3 # cylinder width 
	# l = 5.0 # cylinder length
	# obj = [
    #     CYLINDER, minX, minY, minZ, minX + l, minY, minZ, w, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
    #     CYLINDER, minX, minY, minZ, minX, minY + l, minZ, w, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
    #     CYLINDER, minX, minY, minZ, minX, minY, minZ + l, w, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
	# ]
	# cyl_text(obj,plain,[minX + l, minY, minZ - w],'X',0.20,axes=[[3,0,0],[0,3,0],[0,0,3]])
	# cyl_text(obj,plain,[minX - w, minY + l , minZ],'Y',0.20,axes=[[3,0,0],[0,3,0],[0,0,3]])
	# cyl_text(obj,plain,[minX-w, minY, minZ + l],'Z',0.20,axes=[[3,0,0],[0,3,0],[0,0,3]])
	# cmd.load_cgo(obj,'axes')
	# return
   
def showbox(minX, maxX, minY, maxY, minZ, maxZ):
    linewidth = 5.0
    minX = float(minX)
    minY = float(minY)
    minZ = float(minZ)
    maxX = float(maxX)
    maxY = float(maxY)
    maxZ = float(maxZ)
    # showaxes(minX, minY, minZ)
    boundingBox = [
        cgo.LINEWIDTH, float(linewidth),
        cgo.BEGIN, cgo.LINES,
        # x lines	 
        cgo.COLOR, 1.0, 0.0, 0.0, 	#red
        cgo.VERTEX, minX, minY, minZ,       #1
        cgo.VERTEX, maxX, minY, minZ,       #5
        cgo.VERTEX, minX, maxY, minZ,       #3
        cgo.VERTEX, maxX, maxY, minZ,       #7
        cgo.VERTEX, minX, maxY, maxZ,       #4
        cgo.VERTEX, maxX, maxY, maxZ,       #8
        cgo.VERTEX, minX, minY, maxZ,       #2
        cgo.VERTEX, maxX, minY, maxZ,       #6
        # y lines
		cgo.COLOR, 0.0, 1.0, 0.0, 	#green
		cgo.VERTEX, minX, minY, minZ,       #1
		cgo.VERTEX, minX, maxY, minZ,       #3
		cgo.VERTEX, maxX, minY, minZ,       #5
		cgo.VERTEX, maxX, maxY, minZ,       #7
		cgo.VERTEX, minX, minY, maxZ,       #2
		cgo.VERTEX, minX, maxY, maxZ,       #4
		cgo.VERTEX, maxX, minY, maxZ,       #6
		cgo.VERTEX, maxX, maxY, maxZ,       #8		
		# z lines
		cgo.COLOR, 0.0, 0.0, 1.0,		#blue
		cgo.VERTEX, minX, minY, minZ,       #1
		cgo.VERTEX, minX, minY, maxZ,       #2
		cgo.VERTEX, minX, maxY, minZ,       #3
		cgo.VERTEX, minX, maxY, maxZ,       #4
		cgo.VERTEX, maxX, minY, minZ,       #5
		cgo.VERTEX, maxX, minY, maxZ,       #6
		cgo.VERTEX, maxX, maxY, minZ,       #7
		cgo.VERTEX, maxX, maxY, maxZ,       #8

        cgo.END
    ]
    i = 0
    boxName = "box_" + str(i)
    while boxName in cmd.get_names():
        i += 1
        boxName = "box_" + str(i)
    cmd.load_cgo(boundingBox, boxName)
    sizeX = maxX - minX
    sizeY = maxY - minY
    sizeZ = maxZ - minZ
    centerX = (maxX + minX) / 2
    centerY = (maxY + minY) / 2
    centerZ = (maxZ + minZ) / 2
    BoxCode = "BoxCode(" + boxName + ") = showbox %0.1f, %0.1f, %0.1f, %0.1f, %0.1f, %0.1f" % (minX, maxX, minY, maxY, minZ, maxZ)
    # output LeDock input file
    LeDockBox = "*********LeDock Binding Pocket*********\n" + \
    "Binding pocket\n%.1f %.1f\n%.1f %.1f\n%.1f %.1f\n" % (minX, maxX, minY, maxY, minZ, maxZ)
    # output AutoDock box information
    AutoDockBox ="*********AutoDock Grid Option*********\n" + \
    "npts %d %d %d # num. grid points in xyz\n" % (sizeX/0.375, sizeY/0.375, sizeZ/0.375) + \
    "spacing 0.375 # spacing (A)\n" + \
    "gridcenter %.3f %.3f %.3f # xyz-coordinates or auto\n" % (centerX, centerY, centerZ)
    # output AutoDock Vina input file
    VinaBox = "*********AutoDock Vina Binding Pocket*********\n" + \
    "--center_x %.3f --center_y %.3f --center_z %.3f --size_x %.3f --size_y %.3f --size_z %.3f\n" % (centerX, centerY, centerZ, sizeX, sizeY, sizeZ)
    # output DSDP args
    DSDPBox = "*********DSDP Binding Pocket*********\n" + \
    "--box_min %.3f %.3f %.3f --box_max %.3f %.3f %.3f\n" % (minX, minY, minZ, maxX, maxY, maxZ)

    print(LeDockBox)
    print(AutoDockBox)
    print(VinaBox)
    print(DSDPBox)
    print(BoxCode)
    cmd.zoom(boxName)
    #cmd.show('surface')
    return boxName
        
def getbox(selection="(sele)", extending=5.0):
	cmd.hide("spheres")
	cmd.show("spheres", selection)
	([minX, minY, minZ], [maxX, maxY, maxZ]) = cmd.get_extent(selection)
	minX = minX - float(extending)
	minY = minY - float(extending)
	minZ = minZ - float(extending)
	maxX = maxX + float(extending)
	maxY = maxY + float(extending)
	maxZ = maxZ + float(extending)
	cmd.zoom(showbox(minX, maxX, minY, maxY, minZ, maxZ))
	return


# remove ions
def removeions():
	cmd.select("Ions", "((resn PO4) | (resn SO4) | (resn ZN) | (resn CA) | (resn MG) | (resn CL)) & hetatm")
	cmd.remove("Ions")
	cmd.delete("Ions")
	return


# autodedect box
def autobox(extending = 5.0):
	cmd.remove('solvent')
	removeions()
	cmd.select("Chain_A_Het","hetatm & chain A") #found error in pymol 1.8 change "chain a" to "chain A"
	getbox("Chain_A_Het", extending)
	return


# remove hetatm
def rmhet(extending = 5.0):
	cmd.select("rmhet", "hetatm")
	cmd.remove("rmhet")
	return


# getbox from cavity residues that reported in papers 
def resibox(ResiduesStr="", extending = 5.0):
	cmd.select("Residues", ResiduesStr + " & chain A")
	getbox("Residues", extending)
	return


cmd.extend("GetBoxHelp", GetBoxHelp)
cmd.extend("autobox", autobox)
cmd.extend("getbox", getbox)
cmd.extend("rmhet", rmhet)
cmd.extend("showbox", showbox)
cmd.extend("resibox", resibox)
