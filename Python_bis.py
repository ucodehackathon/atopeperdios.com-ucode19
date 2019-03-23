#
# Codigo python para calibracion del sensor
#
import csv
import numpy as np

nombre=input('Nombre archivo: ')
frec=float(input('Frecuencia del sensor: '))


archivo = open(nombre, mode='r', encoding='utf-8-sig', newline='\n')  
lector = csv.reader(archivo, delimiter=',',quotechar="'")
r=0
for row in lector:
    c=0
    for col in row:
        c=c+1
    r=r+1
archivo.close()

y=np.zeros([r-1,c])

archivo = open(nombre, mode='r', encoding='utf-8-sig', newline='\n')
lector = csv.reader(archivo, delimiter=',',quotechar=" ")
r=0
wy=0.0
for row in lector:
    c=0
    if r>0:
        for yn in row:        
            y[r-1,c]=float(yn)
            c=c+1
        wy=wy+np.abs(y[r-1,7])
#    else:
#        cabecera=row

#        print(row)
    r=r+1
archivo.close()
wy=wy/r
# print(wy)
#
# buscamos aceleraciones maximas
# and np.abs(y[j,3]) > 9.0 and np.abs(y[j,3]) < 12.0
vz=0.0
j=0
cnt=0
vmax=0.0
maxcnt=0
while j<r-1:
    if int(vz) == int(y[j,7]) and int(vz) != 0 : 
#    if vz < np.abs(y[j,7]*1.05) and vz > np.abs(y[j,7]*0.95):
#        if np.abs(y[j,7]) > np.abs(y[j,5]*2.0) + np.abs(y[j,6]*2.0) and np.abs(y[j,7]) > wy:
        cnt = cnt + 1
#            print('segro que si Pau',j)
#            print(cnt)
        if maxcnt < cnt:
            maxcnt=cnt
            vmax=vz
    else:
        cnt=0  
#                                   
# el maximo llano es el de calibracion
#        print('contador maximo: ',maxcnt)
    vz = y[j,7]
    j=j+1
#
# buscamos puntos de corte
# and np.abs(y[j,3]) > 9.0 and np.abs(y[j,3]) < 12.0
print('max_cnt',maxcnt)
flg=0
cnt=0
corte=np.zeros(4,dtype='int')
corte[1:3]=y.shape[0]
j=0
vz=0.0
while j<r-1:
    if int(vz) == int(y[j,7]) and int(vz) != 0 :
#        if np.abs(y[j,7]) > np.abs(y[j,5]*2.0) + np.abs(y[j,6]*2.0) and np.abs(y[j,7]) > wy*1.5:
        cnt = cnt + 1
#            print('segro que si Pau',j)
    else:
#        if cnt == maxcnt:
        if cnt>0 and (vz>vmax*0.95 and vz<vmax*1.05):
            corte[flg]=j
            print('punto de corte de ensayo', corte[flg])
            flg = 1
        cnt=0  
    vz = y[j,7]  
    j=j+1
#
# generamos vector tiempo
#tiempo=np.zeros(r-1)
#while j<r-1:
#    tiempo[j]=(y[j,0]-float(corte[0]))/frec
#    j=j+1
#
# iniciamos cabeceras
cabecera=[]
cabecera.append('time_ref')
cabecera.append('fotograma')
cabecera.append('Acc. X [m/s2]')
cabecera.append('Acc. Y [m/s2]')
cabecera.append('Acc. Z [m/s2]')
cabecera.append('Gir. X [º/s]')
cabecera.append('Gir. Y [º/s]')
cabecera.append('Gir. Z [º/s]')
#
# escritura de datos
archivo = open('output_data_one.csv', mode='w') 
#lector = csv.writer(archivo, delimiter=',',quotechar="'")
i=0
# escribo cabecera
while i<len(cabecera):
    archivo.write(cabecera[i])
    archivo.write(', ')
    if i==len(cabecera)-1:
            archivo.write('\n')
    i=i+1
# ecribo datos
#r=corte[0]-maxcnt
r=0
#while r<corte[1]:
while r<y.shape[0]:
#    archivo.write(repr((tiempo[r])).rjust(8))
    archivo.write(repr((float(r)-corte[0])/frec).rjust(8))         
    archivo.write(', ')
    archivo.write(repr((r-corte[0])).rjust(8))
    archivo.write(', ')
    archivo.write(repr((y[r,1])).rjust(8))
    archivo.write(', ') 
    archivo.write(repr((y[r,2])).rjust(8))
    archivo.write(', ')
    archivo.write(repr((y[r,3])).rjust(8))
    archivo.write(', ')
    archivo.write(repr((y[r,5])).rjust(8))
    archivo.write(', ')
    archivo.write(repr((y[r,6])).rjust(8))
    archivo.write(', ')
    archivo.write(repr((y[r,7])).rjust(8))
    archivo.write(',') 
    if r<corte[0] or r>(corte[1]-maxcnt):  
        archivo.write(repr(vmax*1.1).rjust(8))
#        archivo.write(repr((y[r,7])+250).rjust(8))
    else:
        archivo.write(repr(0).rjust(8))
    archivo.write('\n')  

#    while c<y.shape[1]:
#        archivo.write(repr((y[r,c])).rjust(8))
#        archivo.write(', ')
#        if c==y.shape[1]-1:
#            archivo.write('\n')
#        c=c+1
    r=r+1
archivo.close()


#
# escritura de datos
archivo = open('output_data_bis.csv', mode='w') 
#lector = csv.writer(archivo, delimiter=',',quotechar="'")
i=0
# escribo cabecera
while i<len(cabecera):
    archivo.write(cabecera[i])
    archivo.write(', ')
    if i==len(cabecera)-1:
            archivo.write('\n')
    i=i+1
# ecribo datos
r=corte[0]
#r=0
while r<corte[1]-maxcnt:
#while r<y.shape[0]
#    archivo.write(repr((tiempo[r])).rjust(8))
    archivo.write(repr((float(r)-corte[0])/frec).rjust(8))         
    archivo.write(', ')
    archivo.write(repr((r-corte[0])).rjust(8))
    archivo.write(', ')
    archivo.write(repr((y[r,1])).rjust(8))
    archivo.write(', ') 
    archivo.write(repr((y[r,2])).rjust(8))
    archivo.write(', ')
    archivo.write(repr((y[r,3])).rjust(8))
    archivo.write(', ')
    archivo.write(repr((y[r,5])).rjust(8))
    archivo.write(', ')
    archivo.write(repr((y[r,6])).rjust(8))
    archivo.write(', ')
    archivo.write(repr((y[r,7])).rjust(8))
    archivo.write(',') 
    if r<corte[0] or r>(corte[1]-maxcnt):  
        archivo.write(repr(vmax*1.1).rjust(8))
#        archivo.write(repr((y[r,7])+250).rjust(8))
    else:
        archivo.write(repr(0).rjust(8))
    archivo.write('\n')  

#    while c<y.shape[1]:
#        archivo.write(repr((y[r,c])).rjust(8))
#        archivo.write(', ')
#        if c==y.shape[1]-1:
#            archivo.write('\n')
#        c=c+1
    r=r+1
archivo.close()
