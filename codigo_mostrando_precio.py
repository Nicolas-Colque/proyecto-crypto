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
contador_Datos=0

x=0


print("#~~~====================================~~~#")
print("Versión del programa: 1.0")
print("Estrategia:Obteniendo y Mostrando los datos")
print("Temporalidad de operación: 3 minutos")
print("#~~~====================================~~~#")




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

            contador_Datos=contador_Datos+1  
            x=x+1
            print("####====================================####")
            print("Contador_datos:",contador_Datos)
            print("Fecha:",fecha)
            print("Apertura:",Apertura)
            print("Cierre:",Cierre)
            print("Pmax:",MaxPrice)
            print("Pmin:",MinPrice)

            print("####====================================####")
        except BinanceAPIException as e:
            print (e.message)
            print("entro a API")
            time.sleep(2)
        except:
            print("paso un error")
            time.sleep(2)

