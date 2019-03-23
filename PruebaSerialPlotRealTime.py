# Prueba de Graficas en tiempo rela usando Python 
## Librerias
import serial
from matplotlib import pyplot as plt
from matplotlib import animation as animation
import matplotlib.pyplot as plt
from serial import *
from math import *
import numpy as np     # installed with matplotlib
import array as arr
from serial import SerialException


#Se define el puerto del cual se tomaran los datos y los baudios 
arduino = serial.Serial('COM3', 9600)

#Figura sobre la cual se tendrán 2 subgráficas
fig = plt.figure()


#Se definen los limites de los ejes pata cada subgráfica
ax1 = fig.add_subplot(2,1,2)
ax1.set_xlim([0,15])
ax1.set_ylim([-10,10])
line1, = ax1.plot([], [], lw=2)  #Linea de la gráfica 1
ax1.grid()
xdata1, ydata1 =[], [] # Areglos vacios donde se agregaran los datos recibidos

ax2 =  fig.add_subplot(2,1,1)
ax2.set_xlim([0,15])
ax2.set_ylim([0,10])
line2, = ax2.plot([], [], lw=2) #Linea de la gráfica 2
ax2.grid()
xdata2, ydata2 =[], []  # Areglos vacios donde se agregaran los datos recibidos



#Limites iniciales de la subgrafica 1
xmi=0
xma=10
ymi=-5
yma=5

#Limites iniciales de la subgrafica 1
xmi2=0
xma2=10
ymi2=0
yma2=30

#Función que inicia un subgráfica 1 con sus características
def init1():
    ax1.set_ylim(ymi, yma)
    ax1.set_xlim(xmi, xma)
    line1.set_data(xdata1, ydata1)
    ax1.set_xlabel('TIME (s)')
    ax1.set_ylabel('ACELERATION X  (m/s)')
    return line1,

#Función que inicia un subgráfica 2 con sus características
def init2():
    ax2.set_ylim(ymi2, yma2)
    ax2.set_xlim(xmi2, xma2)
    line2.set_data(xdata2, ydata2)
    line2.set_color('red')
    #ax2.set_xlabel('TIME (s)')
    ax2.set_ylabel('TEMPERATURE (°C)')
    ax2.set_title('REAL TIME GRAPHICS')
    return line2,

#Función que lleva a cabo la grafica 1 en tiempo real 
def animate1(i):
    
 
    try:

        data = arduino.readline().decode('utf-8') #Obtiene los datos del puerto serial y los codifica
        DATA = np.fromstring(data, dtype=float, sep=',') #Convierte el String en un areglo
        while len(DATA) != 3: #filtro de datos no validos conforme a la longitud
            
            data = arduino.readline().decode('utf-8')
            DATA = np.fromstring(data, dtype=float, sep=',')
            #Agrega los datos erroneos en un archivo .CVS sin borrar los anteriores
            f= open('Datosmalos.cvs', 'a')   
            f.write(data) 
            f.close()
            
        #Agrega los datos buenos a los arregos vacios para graficar        
        xdata1.append(DATA[0]/1000)
        ydata1.append(DATA[2])
        ydata2.append(DATA[1])

        f= open('Datos.cvs', 'a')
        f.write(data) 
        f.close()
        x = xdata1
        y = ydata1

        #Obtención de los limites minimo y maximo de las gráficas

        xmin, xmax = ax1.get_xlim()
        ymin, ymax = ax1.get_ylim()
        
        #Obtiene los valores máximos de los arreglos
        w=np.amax(y)
        v=np.amin(y)

        #Configuración de limites dinamicos de la gráfica 1

        if x[-1] >= xmax:
            ax1.set_xlim(xmax-5, xmax+5)
            ax1.figure.canvas.draw()
            xma=xmax+5
            xmi=xmax-5

        if w >= ymax :
            ax1.set_ylim(ymin, 1.5*ymax)
            ax1.figure.canvas.draw()
            yma=2*ymax
            ymi=ymin
    
        if v <= ymin and v <= 0 :
            ax1.set_ylim(v-abs(ymin), ymax)
            ax1.figure.canvas.draw()
            yma=ymax
            ymi=v-abs(ymin)

    
        if v <= ymin and v >= 0 :
            ax.set_ylim(v-abs(ymin), ymax)
            ax.figure.canvas.draw()
            yma=ymax
            ymi=v-abs(ymin)

    

       #Grafíca la linea
        line1.set_data(x,y)
        return line1, 
    
    except UnicodeEncodeError:
        pass


anim1 = animation.FuncAnimation(fig, animate1, interval=30, init_func=init1 , blit=True)

#Se hace lo mismo que en las funciones anteriores pero ahora para la subgráfica 2

def animate2(i):

    x = xdata1
    y = ydata2

    xmin, xmax = ax2.get_xlim()
    ymin, ymax = ax2.get_ylim()

    w=np.amax(y)
    v=np.amin(y)

    if x[-1] >= xmax:
        ax2.set_xlim(xmax-5, xmax+5)
        ax2.figure.canvas.draw()
        xma2=xmax+5
        xmi2=xmax-5

    if w >= ymax :
        ax2.set_ylim(ymin, 1.5*ymax)
        ax2.figure.canvas.draw()
        yma2=1.5*ymax
        ymi2=ymin
    
    if v <= ymin and v <= 0 :
        ax2.set_ylim(v-abs(ymin), ymax)
        ax2.figure.canvas.draw()
        yma2=ymax
        ymi2=v-abs(ymin)

    
    if v <= ymin and v >= 0 :
        ax2.set_ylim(v-abs(ymin), ymax)
        ax2.figure.canvas.draw()
        yma2=ymax
        ymi2=v-abs(ymin)
   
    line2.set_data(x,y)
    return line2, 



    

anim2 = animation.FuncAnimation(fig, animate2, interval=90, init_func=init2 , blit=True)


plt.show()
