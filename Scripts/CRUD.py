#Meus arquivos .py
from Scripts import TOKENs

#Bibliotecas python
from pymongo import MongoClient

class Crud:

    #Construtor
    def __init__(self):
        DB = MongoClient(TOKENs.get_tokenCrud())
        self.banco = DB.Epic_Healper_Tester
        self.Servidores = self.banco.Servidores
        print("Conexão com o MongoDB realizada")

    #--------Colection Servidores Inicio--------

    #--------------Crud Inicio--------------

    def create_Servidores(self,Server): #Criar um documento
        self.Servidores.insert_one(Server)
        return True

    def read_ServidoresById(self,Server_id): #Criar um documento
        return self.Servidores.find_one({"Server_id":Server_id})

    def update_Servidores(self,Server):
        Obj = self.read_ServidoresById(Server["Server_id"])
        conseguiu = False
        if Obj != None:
            self.Servidores.update_one({"Server_id" : Server["Server_id"]}, {"$set":Server})
            conseguiu = True
        return conseguiu

    def delete_Servidores(self,Server_id):
        conseguiu = False
        if (self.read_ServidoresById(Server_id) != None):
            self.Servidores.delete_one({"Server_id": Server_id})
            conseguiu = True
        return conseguiu

    #---------------Crud Fim------------------

    def ServidoresCheck(self,Arr,op): #Checar para alterar um dos valores presentes na Coleção
        Server = dict(Arr)
        Obj = self.read_ServidoresById(Server["Server_id"]) 
        conseguiu = False
        if (Obj != None): #Existe logo irei fazer um update
            if op == 0: #Alterar o Valor 0 após a Server_id
                Obj["Channel_Arena"] = Server["Channel_Arena"]
            elif op == 1: #Alterar o Valor 1 após a Server_id   
                Obj["Channel_Miniboss"] = Server["Channel_Miniboss"]
            elif op == 2: #Alterar o Valor 2 após a Server_id
                Obj["Channel_Not_Allower"] = Server["Channel_Not_Allower"]
            else: #Alterar tudo
                Obj = Server
            self.update_Servidores(Obj)
            conseguiu = True
        else:
            self.create_Servidores(Server)

    #----------Colection Servidores Fim----------

    def teste(self):
        Servidores = self.banco.Servidores
        Server = {
            "Server_id": "711375776351649875",
            "Channel_Arena" : "819730770875645952",
            "Channel_Miniboss" : "819730770875645952",
            "Channel_Not_Allower" : "All_Another" 
        }
        server_id = Servidores.insert_one(Server).inserted_id
        print(server_id)
    