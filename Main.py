#Importation des modules nécessaires
import os
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import collections
import random
import time
import numpy as np
import threading

#Importation des classes
import CAcquisition
import CBDD
#######################################
# ATTENTION AUX INDEX DU TABLEAU DATA #
#######################################
class Graph():

    def __init__(self, sampleinterval=0.1, timewindow=20., size=(1100,650), dev ='dev1'):
        # Data stuff

        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)

		#Création des buffers
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer1 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer2 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer3 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer4 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer5 = collections.deque([0.0]*self._bufsize, self._bufsize)

        #Variables globales
        self.intervalle = sampleinterval
        self.device = dev
        self.i = 0

        #Instanciation d'objets
        self.bdd = CBDD.CBDD()
        self.Acquisition=CAcquisition.CAcquisition()

        #Création des tableaux Numpy
        self.x = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=np.float)

        self.x1 = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y1 = np.zeros(self._bufsize, dtype=np.float)

        self.x2 = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y2 = np.zeros(self._bufsize, dtype=np.float)

        self.x3 = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y3 = np.zeros(self._bufsize, dtype=np.float)

        self.x4 = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y4 = np.zeros(self._bufsize, dtype=np.float)

        self.x5 = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y5 = np.zeros(self._bufsize, dtype=np.float)

        self.app = QtGui.QApplication([])
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.app.setWindowIcon(icon)

        #Configuration PyQtGraph
        self.plt = pg.plot(title='Simulateur 2018')
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', 'Amplitude', 'V')
        self.plt.setLabel('bottom', 'Temps', 's')

        #Couleurs des courbes
        self.curve = self.plt.plot(self.x, self.y, pen=(255,0,0))
        self.curve1 = self.plt.plot(self.x1, self.y1, pen=(0,255,0))
        self.curve2 = self.plt.plot(self.x2, self.y2, pen=(0,0,255))
        self.curve3 = self.plt.plot(self.x3, self.y3, pen=(0,255,255))
        self.curve4 = self.plt.plot(self.x4, self.y4, pen=(255,0,255))
        self.curve5 = self.plt.plot(self.x5, self.y5, pen=(255,255,0))

        #Lancement de la fonction principale en parralèlle
        threading.Timer(0, self.main).start()
        threading.Timer(0, self.getdata).start()



    def main(self):
        try:
            threading.Timer(0.1, self.main).start()

            #Récupération des données


            #Affichage des données dans la console
            threading.Timer(self.intervalle, self.printconsole, [self.data]).start()

            #Actualisation du graphique
            threading.Timer(0.1, self.updateplot, [self.data]).start()
            #self.updateplot(self.data)
            #Ecriture des données dans la BDD
            threading.Timer(self.intervalle, self.writeBDD, [self.data]).start()


        except:
            print("Erreur main")

    def printconsole(self, data):
        try:
            os.system("cls")

            print("Device : "+str(self.device)+" | Intervalle : "+str(self.intervalle)+"s")
            print(round(self.i*self.intervalle, 2))
            print("Bleu clair - Roulis Consigne : " + str(data[3]))
            print("Bleu - Roulis Mesure : " + str(data[2]))
            print("Violet - Tangage Consigne : " + str(data[4]))
            print("Vert - Tangage Mesure : " + str(data[1]))
            print("Rouge - Roulis Nouveau : " + str(data[0]))
            print("Jaune - Tangage Nouveau : " + str(data[5]))
        except:
            print("Erreur affichage console")

    def writeBDD(self, data):
        try:

            for k in range(6):
                donnees = (float(round(self.i*self.intervalle,3)), data[k], k+1)
                self.bdd.WriteBDD(donnees)
        except:
            print("Erreur écriture dans la base de données")



    def getdata(self):
        try:
            threading.Timer(self.intervalle, self.getdata).start()
            self.data = self.Acquisition.startAcquisition(self.device)
            self.i +=1
        except:
            print("Erreur acquisition")


    def updateplot(self, data):

        self.databuffer.append( data[0] )
        self.y[:] = self.databuffer
        self.curve.setData(self.x, self.y)

        self.databuffer1.append( data[1] )
        self.y1[:] = self.databuffer1
        self.curve1.setData(self.x1, self.y1)

        self.databuffer2.append( data[2] )
        self.y2[:] = self.databuffer2
        self.curve2.setData(self.x2, self.y2)

        self.databuffer3.append( data[3] )
        self.y3[:] = self.databuffer3
        self.curve3.setData(self.x3, self.y3)

        self.databuffer4.append( data[4] )
        self.y4[:] = self.databuffer4
        self.curve4.setData(self.x4, self.y4)

        self.databuffer5.append( data[5] )
        self.y5[:] = self.databuffer5
        self.curve5.setData(self.x5, self.y5)

        self.app.processEvents()


    def run(self):
        self.app.exec_()

if __name__ == '__main__':
    os.system("cls")
    print("Saisir Device :")
    device = ("dev") + input()
    print("Saisir intervalle :")
    intervalle = input()
    os.system("cls")


    m = Graph(sampleinterval=float(intervalle), timewindow=20.0, dev=device)

m.run()
