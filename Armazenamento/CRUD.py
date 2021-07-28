#Meus arquivos .py
from Armazenamento import TOKENs

#Bibliotecas python
from pymongo import MongoClient

class Crud:

    #Construtor
    def __init__(self):
        DB = MongoClient(TOKENs.get_tokenCrud())
        self.banco = DB.3cm
        print("Conexão com o MongoDB realizada")
        print("------------------------------")

    #--------Colection Servidores Inicio--------

    #--------------Crud Inicio--------------

    def create(self,Colecao,item): #Criar um documento
        colecao = self.banco.Colecao
        colecao.insert_one(item)
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

    def ServidoresCheck(self,Arr,key): #Checar para alterar um dos valores presentes na Coleção
        Server = dict(Arr)
        Obj = self.read_ServidoresById(Server["Server_id"]) 
        conseguiu = False
        if (Obj != None): #Existe logo irei fazer um update
            if key != "None": #Verifica se altera um key expecifica
                Obj[key] = Server[key]
            else:    
                Obj = Server
            self.update_Servidores(Obj)
            conseguiu = True
        else:
            self.create_Servidores(Server)

    def checkPlayer(self,id):
        Players = self.banco.Players
        retorno = False
        if(Players.find_one({"PlayerId":id}) != None):
            retorno = True
        return retorno

    #----------Colection Servidores Fim----------
    