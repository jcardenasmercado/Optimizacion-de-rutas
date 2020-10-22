import json
import requests
import pprint as pp
import time
import math
import matplotlib.pyplot as plt
import numpy as np
import webbrowser

#Loc contiene la lista de las direcciones a rutear, cada parametro debe contener 
#la direccion, la comuna/provincia y el país.
loc = ["Hospital el pino, san bernardo, chile", "Hospital del salvador, providencia, chile", "Hospital Dr. Luis Tisné Brousse, peñalolen, Chile", "Clinica las condes, las condes, Chile"]

API1 = "https://us1.locationiq.com/v1/search.php?key=pk.0bcfdf18973ec7dc66d274a58578acb7"
API2 = "http://www.mapquestapi.com/directions/v2/routematrix?key=K4YQLdWn9G3LkCzYAt0LDixd9T1J0MLL"

req1 = [] #Request 1 hecho a la API LocationIQ, es una lista que contiene los response para debug. 
req1_dict = [] #Es una lista que contiene el Json de cada response.
cords = [] #Es una lista que contiene las coordenadas extraidas de cada response.

for x in range(len(loc)):
	req1.append(requests.get(url=API1, params = {'q':loc[x], 'accept-language':'es', 'format':'json'}))
	if x % 2 == 0:
		time.sleep(1) #La API no puede procesar mas de 2 valores por segundo
	req1_dict.append(req1[x].json())
	cords.append(req1_dict[x][0]['lat'] + ", " + req1_dict[x][0]['lon'])

#Json estructurado que nutre a la API2 (MapQuest)
data = {
	"locations": cords,
	"options":{
		"allToAll": True
	}

}

req2 = requests.post(API2, json = data) #Request 2 Hecha a la API MapQuest, contiene los response.
req2_dict = json.loads(req2.text) #Contiene el Json del request 2

matriz_d = req2_dict['distance'] #Matriz distancia
matriz_t = req2_dict['time'] #Matriz tiempo


nodos = len(loc) #Nodos por rutear

ruta = [0]
distancia = 0

visitados = [] #Lista del estado de los nodos; 0: No visitado , 1: Visitado
for l in range(0, nodos):
	visitados.append(0)

i = 0
for z in range(nodos):	#Algoritmo que ordena la ruta a seguir según distancia.
	temp_val = 0
	temp_j = 0
	ol = 0
	for j in range(nodos):
		if visitados[j] == 0:
			if matriz_d[i][j] != 0:
				if j != 0:
					if ol == 0:
						temp_val = matriz_d[i][j]
						temp_j = j
						ol = 1
			if matriz_d[i][j] != 0:
				if matriz_d[i][j] < temp_val:
					temp_val = matriz_d[i][j]
					temp_j = j			
		if j+1 == nodos:
			ruta.append(temp_j)
			if temp_j == 0:
				distancia += matriz_d[i][0]
			i = temp_j
			visitados[temp_j] = 1
			distancia += temp_val
			print(ruta)
			print(visitados)
	print("_________________________________________________")		


distancia = f"{distancia:.2f}"
distancia_f = float(distancia)

print("MEJOR RUTA:",end="")
for u in range(len(ruta)):
	print(" ->", ruta[u], end="")
print("\nDISTANCIA TOTAL:",distancia_f,"KM")

for z in range(nodos):
	webbrowser.open("https://www.google.com/maps/dir/?api=1&origin="+loc[ruta[z]]+"&destination="+loc[ruta[z+1]])
	print("ORIGEN: " + loc[ruta[z]] + "  DESTINO: " + loc[ruta[z+1]])
	print("_____________________________________________________________________________")
	input("PRESIONE UNA TECLA PARA CONTINUAR")


"""
DEBUG -- MATRIZ DISTANCIA Y TIEMPO --
print(matriz_d)
print("______________________________________")
print(matriz_t)

fig, pd = plt.subplots()
fig, pt = plt.subplots()
d = len(matriz_d)
pd.matshow(matriz_d, cmap=plt.cm.Blues)
pt.matshow(matriz_t, cmap=plt.cm.Oranges)
for i in range(d):
    for j in range(d):
        c = matriz_d[j][i]
        t = matriz_t[j][i]
        pd.text(i, j, str(c), va='center', ha='center')
        pt.text(i, j, str(t), va='center', ha='center')


pp.pprint(x_dict)
plt.show()

"""