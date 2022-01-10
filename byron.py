from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import pandas as pd
import time
import calendar
import os
import time
from pymongo import MongoClient
from pprint import pprint
client = Client("W5p8RIjZlWWWkTF3XTpAw4xxWcc1nbCZdrl1Kcwjt7WGIId5hvpuVHpq7YF4WcDO","0i5QafRamaUrptE0TqaddIvYgTOVumDRD3yCBsUJo2OFtcbQRsdlDgralR67n2w4")
prices = client.get_all_tickers()
#Estas son variables de prueba
Contador_Cruces=0
Valor=1
EstadoRapida_Anterior=0
EstadoLenta_Anterior=0

#Fin||

clientx = MongoClient('localhost')
##Nombre de la base de datos
db = clientx['AnalisisBTC']
## Colección de personas
col = db['Precio']
col2 = db['Operaciones']
col3 = db['Balance']
col4 = db['Indicadores']
contador_Datos=0
x=0
#Inicio de la función
#DEFINIENDO VARIABLES ASOCIADAS CON EL CAPITAL
Capital_inicial=10000
Balance_Parcial=10000
key_controladora=0
cantidad_compras=0
cantidad_ventas=0
QBTC=0
print("#~~~====================================~~~#")
print("Versión del programa: 7.0")
print("Cantidad de capital inicial:",Capital_inicial)
print("Comision:N/A")
print("Estrategia: Cruces de media bajista y alcista")
print("Modalidad: Total")
print("Temporalidad de operación: 3 minutos")
print("#~~~====================================~~~#")


def EMAX(y,CantDatos,Pcierre):
    valoresx=[]
    K=(2/(y+1))
    if (CantDatos>=y):
        if (CantDatos==y):
            i=0
            for documentoX2 in col.find({},{"Cierre":1}).sort("ts",-1).limit(y):
                train = pd.DataFrame.from_dict(documentoX2, orient='index')
                train.reset_index(level=0, inplace=True)
                valoresx.append(int(train[0][1]))
            acumulado=0
            j=0
            for j in range(len(valoresx)):
                valor = valoresx[j]
                acumulado = valor + acumulado   
            SMATotal=int(acumulado/len(valoresx))
            Retorno=SMATotal
            print(SMATotal)
        else:
            cont="EMA"+str(y)
            for documentoX3 in col.find({},{cont:1}).sort("ts",-1).limit(1):
                train2 = pd.DataFrame.from_dict(documentoX3, orient='index')
                train2.reset_index(level=0, inplace=True)
                Auxiliar=(int(train2[0][1]))
            EMA_anterior=Auxiliar
            EMA_Calculada=int(K*Pcierre+(1-K)*EMA_anterior)
            Retorno=EMA_Calculada
    else:
        Retorno=0
    return Retorno
#Fin de la función

#Inicio Función Cruces
def Cruces(Cant_datos,EMAXIMO,MediaR,MediaL):
    global EstadoLenta_Anterior
    global EstadoRapida_Anterior
    EstadoLenta=0
    EstadoRapida=0
    retornable=2
    if Cant_datos>EMAXIMO+1 and MediaR!=MediaL:
        if MediaR>MediaL:
            EstadoRapida=1
            EstadoLenta=0
        if MediaR<MediaL:
      
            EstadoRapida=0
            EstadoLenta=1
        if Cant_datos>EMAXIMO+2:
           
            if EstadoRapida!=EstadoRapida_Anterior and EstadoLenta!=EstadoLenta_Anterior and EstadoRapida==0 and EstadoLenta==1:
                retornable=0
                print("cruce bajista")
                print("Imprimiendo retornable:",retornable)
            if EstadoRapida!=EstadoRapida_Anterior and EstadoLenta!=EstadoLenta_Anterior and EstadoRapida==1 and EstadoLenta==0:
                retornable=1
                print("Cruce alcista")
        if MediaR!=MediaL:
            EstadoLenta_Anterior=EstadoLenta
            EstadoRapida_Anterior=EstadoRapida
    return retornable
def Ejecuta_compra_venta(Parametro_cruce,Precio_Operativo):
    print("Entro al ejecutador")
    global Balance_Parcial
    global Capital_inicial
    global key_controladora
    global QBTC
    global cantidad_compras
    global cantidad_ventas
    operacion=0
    #Operacion=0 nada, Operacion=1 compra, Operacion=2 venta
    print("IMPRIMIENDO PARAMETRO_CRUCE:",Parametro_cruce)
    print("IMPRIMIENDO Key_controladora:",key_controladora)
    if Parametro_cruce==0 and key_controladora!=0:

        print("se produjo un cruce bajista")
        key_controladora=0
        Balance_Parcial=QBTC*Precio_Operativo
        print("Se VENDIO")
        cantidad_ventas=cantidad_ventas+1
        
        operacion=2

    if Parametro_cruce==1 and key_controladora==0:
        QBTC=Balance_Parcial/Precio_Operativo
        key_controladora=1
        
        cantidad_compras=cantidad_compras+1
        operacion=1


    else:
        print("No Ejecuta nada")
        operacion=0
    return operacion
      
#El ciclo infinito
while(Valor==1):
        tiempo_partida=int(time.time())
        tiempo_actual=tiempo_partida
        key=0
        operador=0
        #ACA SE PONE EL TIEMPO

        try: 
            while(tiempo_partida+2-tiempo_actual>0):
                #Obtiene Los datos
                prices = client.get_all_tickers()
                data=pd.DataFrame(prices)
                x1=int(float(data.loc[11,'price']))
                x2=data.loc[11,'symbol']
                #Es el primero
                if(key==0):
                    Apertura=x1
                    MaxPrice=x1
                    MinPrice=x1
                    key=1        
                else:
                    if(x1>MaxPrice):
                        MaxPrice=x1
                    if(x1<MinPrice):
                        MinPrice=x1
                tiempo_actual=int(time.time())
            
            Cierre=x1
            fecha=str(pd.to_datetime(tiempo_actual, unit='s'))
            
            EMA10=EMAX(10,contador_Datos,Cierre)
            EMA55=EMAX(55,contador_Datos,Cierre)

            parametro_Cruces=Cruces(contador_Datos,55,EMA10,EMA55)
             #Ejecutamos una compra o venta
            if parametro_Cruces==0 or parametro_Cruces==1:
                Contador_Cruces=Contador_Cruces+1
                operador=Ejecuta_compra_venta(parametro_Cruces,Cierre)
              
            
           
            
            #Precios

            #Indicadores

            #Balance


            contador_Datos=contador_Datos+1  
            x=x+1
            print("####====================================####")
            print("contador_datos:",contador_Datos)
            print("Fecha:",fecha)
            print("Apertura:",Apertura)
            print("Cierre:",Cierre)
            print("Pmax:",MaxPrice)
            print("Pmin:",MinPrice)
            print("ts:",tiempo_actual)
            print("EMA10:",EMA10)
            print("EMA55:",EMA55)
            print("Cantidad de cruces:",Contador_Cruces)
            print("Balance_Parcial en USD:",Balance_Parcial)
            print("Cantidad_Compras",cantidad_compras)
            print("Cantidad_Ventas:",cantidad_ventas)
            print("####====================================####")
        except BinanceAPIException as e:
            print (e.message)
            print("entro a API")
            time.sleep(2)
        except:
            print("paso un error")
            time.sleep(2)
## Insertar un documento
#Hay que agregar el ID al precio Para que no haya GAP al graficar, pARA ESO Hay que tomar una consulta de mongodb
#y obtener el maximo valor de la consulta, y en caso de que no haya hay que hacer que el ID sea = 1

