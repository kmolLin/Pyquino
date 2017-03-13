# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_graphy import Ui_Dialog

import pyqtgraph as pg

import pyqtgraph.opengl as gl

import numpy as np


class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        
        self.openGLWidget = gl.GLViewWidget()
        self.verticalLayout.insertWidget(0, self.openGLWidget)
        self.openGLWidget.show()
        
        self.openGLWidget.setCameraPosition(distance=40)
        
        g = gl.GLGridItem()
        g.scale(2,2,1)
        self.openGLWidget.addItem(g)
        
        self.__3dtest__()
        #self.__test__()
        
    def __3dtest__(self):
        
        n = 6
        pos = np.empty((n, 3))
        size = np.empty((n))
        color = np.empty((n, 4))
        pos[0] = (0,0,0); size[0] = 0.2;   color[0] = (1.0, 0.0, 0.0, 0.5)
        pos[1] = (0,0,0.6); size[1] = 0.2;   color[1] = (0.0, 0.0, 1.0, 0.5)
        pos[2] = (0,0,0.6); size[2] = 0.2; color[2] = (0.0, 1.0, 0.0, 0.5)
        pos[3] = (10.0,0,0.6); size[2] = 0.2; color[3] = (0.0, 1.0, 0.0, 0.5)
        pos[4] = (0,0,0); size[2] = 0.2; color[4] = (0.0, 1.0, 0.0, 0.5)
        pos[5] = (-14.2,-13.2,0.6); size[5] = 0.2; color[5] = (0.0, 1.0, 0.0, 0.5)
        #pos[0] = (1, 0, 1);
        #for i in range()
        sp1 = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
        sp1.translate(5,5,0)
        #print(sp1)
        self.openGLWidget.addItem(sp1)
        
        '''
        #def fn(x, y):
         #   return np.cos((x**2 + y**2)**0.5)

        n = 51
        y = np.linspace(-10,10,n)
        x = np.linspace(-10,10,100)
        for i in range(n):
            yi = np.array([y[i]]*100)
            d = (x**2 + yi**2)**0.5
            z = 10 * np.cos(d) / (d+1)
            pts = np.vstack([x,yi,z]).transpose()
            print(pts)
            plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor((i,n*1.3)), width=(i+1)/10., antialias=True)
            self.openGLWidget.addItem(plt)
        '''
    def __test__(self):
        
        verts = np.array([
            [0, 0, 0],
            [2, 0, 0],
            [1, 2, 0],
            [1, 1, 1],
        ])
        faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [0, 2, 3],
            [1, 2, 3]
        ])
        colors = np.array([
            [1, 0, 0, 0.3],
            [0, 1, 0, 0.3],
            [0, 0, 1, 0.3],
            [1, 1, 0, 0.3]
        ])

        ## Mesh item will automatically compute face normals.
        m1 = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False)
        m1.translate(5, 5, 0)
        m1.setGLOptions('additive')
        self.openGLWidget.addItem(m1)
        
        
        ## Example 2:
        ## Array of vertex positions, three per face
        verts = np.empty((36, 3, 3), dtype=np.float32)
        theta = np.linspace(0, 2*np.pi, 37)[:-1]
        verts[:,0] = np.vstack([2*np.cos(theta), 2*np.sin(theta), [0]*36]).T
        verts[:,1] = np.vstack([4*np.cos(theta+0.2), 4*np.sin(theta+0.2), [-1]*36]).T
        verts[:,2] = np.vstack([4*np.cos(theta-0.2), 4*np.sin(theta-0.2), [1]*36]).T
            
        ## Colors are specified per-vertex
        colors = np.random.random(size=(verts.shape[0], 3, 4))
        m2 = gl.GLMeshItem(vertexes=verts, vertexColors=colors, smooth=False, shader='balloon', 
                           drawEdges=True, edgeColor=(1, 1, 0, 1))
        m2.translate(-5, 5, 0)
        self.openGLWidget.addItem(m2)



        ## Example 3:
        ## sphere

        md = gl.MeshData.sphere(rows=10, cols=20)
        #colors = np.random.random(size=(md.faceCount(), 4))
        #colors[:,3] = 0.3
        #colors[100:] = 0.0
        colors = np.ones((md.faceCount(), 4), dtype=float)
        colors[::2,0] = 0
        colors[:,1] = np.linspace(0, 1, colors.shape[0])
        md.setFaceColors(colors)
        m3 = gl.GLMeshItem(meshdata=md, smooth=False)#, shader='balloon')

        m3.translate(5, -5, 0)
        self.openGLWidget.addItem(m3)


        # Example 4:
        # wireframe

        md = gl.MeshData.sphere(rows=4, cols=8)
        m4 = gl.GLMeshItem(meshdata=md, smooth=False, drawFaces=False, drawEdges=True, edgeColor=(1,1,1,1))
        m4.translate(0,10,0)
        self.openGLWidget.addItem(m4)

        # Example 5:
        # cylinder
        md = gl.MeshData.cylinder(rows=10, cols=20, radius=[1., 2.0], length=5.)
        md2 = gl.MeshData.cylinder(rows=10, cols=20, radius=[2., 0.5], length=10.)
        colors = np.ones((md.faceCount(), 4), dtype=float)
        colors[::2,0] = 0
        colors[:,1] = np.linspace(0, 1, colors.shape[0])
        md.setFaceColors(colors)
        m5 = gl.GLMeshItem(meshdata=md, smooth=True, drawEdges=True, edgeColor=(1,0,0,1), shader='balloon')
        colors = np.ones((md.faceCount(), 4), dtype=float)
        colors[::2,0] = 0
        colors[:,1] = np.linspace(0, 1, colors.shape[0])
        md2.setFaceColors(colors)
        m6 = gl.GLMeshItem(meshdata=md2, smooth=True, drawEdges=False, shader='balloon')
        m6.translate(0,0,7.5)

        m6.rotate(0., 0, 1, 1)
        #m5.translate(-3,3,0)
        self.openGLWidget.addItem(m5)
        self.openGLWidget.addItem(m6)
