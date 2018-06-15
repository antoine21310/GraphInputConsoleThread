import numpy, PyDAQmx

class CAcquisition():
    
    def __init__(self):
        
        self.taskHandle=PyDAQmx.TaskHandle()
        self.read=PyDAQmx.int32()
        self.vMin=-10.;self.vMax=10.0;self.fe=1000;self.N=2;self.timeOut=100.

        self.Tableau = []   #Déclaration du tableau de valeurs
        
        for k in range (6):
            self.Tableau.append(numpy.zeros((self.N,), dtype=numpy.float64))   #Initialisation du tableau
        
    def startAcquisition(self, dev):

        for i in range (6):   #Boucle for qui fait varier l'entrée pour 4 capteurs 
            PyDAQmx.DAQmxCreateTask("",PyDAQmx.byref(self.taskHandle))
            
            #On spécifie les entrées
            PyDAQmx.DAQmxCreateAIVoltageChan(self.taskHandle,dev+"/ai"+str(i),"",PyDAQmx.DAQmx_Val_Cfg_Default,self.vMin,self.vMax,PyDAQmx.DAQmx_Val_Volts,None)

            PyDAQmx.DAQmxCfgSampClkTiming(self.taskHandle,"",self.fe,PyDAQmx.DAQmx_Val_Rising,PyDAQmx.DAQmx_Val_FiniteSamps,self.N)

            PyDAQmx.DAQmxStartTask(self.taskHandle)
            PyDAQmx.DAQmxReadAnalogF64(self.taskHandle,self.N,self.timeOut,PyDAQmx.DAQmx_Val_GroupByChannel, self.Tableau[i],self.N,PyDAQmx.byref(self.read),None)
            
            PyDAQmx.DAQmxStopTask(self.taskHandle)
            PyDAQmx.DAQmxClearTask(self.taskHandle)
        
        TableauValeurs = (float(round(self.Tableau[0][0], 3)), float(round(self.Tableau[1][0], 3)), float(round(self.Tableau[2][0], 3)), float(round(self.Tableau[3][0], 3)), float(round(self.Tableau[4][0], 3)), float(round(self.Tableau[5][0], 3))) 
        return TableauValeurs   #Retourne un tableau avec les valeurs de l'acquisition
