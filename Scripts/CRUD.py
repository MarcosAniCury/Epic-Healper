#Meus arquivos .py
from Scripts import TOKENs

#Bibliotecas python
from pymongo import MongoClient

class Crud:

    #Construtor
    def __init__(self):
        DB = TOKEN.get_tokenCrud()
        banco = DB.Epic_Healper_Tester

    def teste():
        Servidores = banco.Servidores
        Server = {
            "Server_id": "711375776351649875",
            "Channel_Arena" : "819730770875645952",
            "Channel_Miniboss" : "819730770875645952",
            "Channel_not_allower" : "All_Another" 
        }
        server_id = Servidores.insert_one(Server).inserted_id
        print(server_id)