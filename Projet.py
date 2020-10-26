import mysql.connector as mc
import pandas as pd
#instantier une connexion
mydb = mc.connect(
host="localhost",
user="hamza",
password="formation",
database='banque'
)

mycursor=mydb.cursor()
mycursor.execute("SELECT * FROM  banque.clients")
clients = mycursor.fetchall()
mycursor.execute("SELECT * FROM  banque.comptes")
comptes = mycursor.fetchall()
mycursor.execute("SELECT * FROM  banque.operations")
operations = mycursor.fetchall()
#liste_solde=clients.values.tolist()
#print(clients)      

class Table(object):	
 	# def __init__(self,fileName):	
 	
    def lecture(self, fileName):
        self.fileName=fileName
        if self.fileName == clients :
            print("ma table clients \n = ",  self.fileName)
            print("----------------------------------------")
        elif self.fileName == comptes:
            print("ma table comptes \n = ",  self.fileName)
            print("----------------------------------------")
        elif self.fileName == operations:
            print("ma table operation \n = ",  self.fileName) 
            print("----------------------------------------")
        elif self.fileName == credits:
            print("ma table credits \n = ",  self.fileName) 
            print("----------------------------------------")


#Clients: [identifiant,numero_de_compte,nom,prenom,adresse]
#comptes : [id_compte,identifiant,solde]
#operation = [id_operation,id_compte,nb_operation,nb_decouverts]

class TableClient(Table):
    def __init__(self):
        Table.__init__(self)
        self.s=0
    def score (self):

        # mycursor=mydb.cursor()
        # mycursor.execute("ALTER TABLE clients ADD COLUMN score int") # bloque le programme
        sc=mydb.cursor()
        sc.execute("select solde from comptes")
        solde = sc.fetchall()
        sc.execute("select nb_operations from operations")
        nb_operations=sc.fetchall()
        sc.execute("select nb_decouverts from operations")
        nb_decouverts=sc.fetchall()
        

        #creation des liste operations, decouvert et solde
        
        op=[] #liste operation
        dec=[] #liste decouvert
        sold=[] # liste solde
        self.s=[] #liste score
        for i in range(0,len(nb_operations)):
            op.append(nb_operations[i][0])
        for i in range(0,len(nb_decouverts)):
            dec.append(nb_decouverts[i][0])
        for i in range(0,len(solde)):
            sold.append(solde[i][0])
        #print(op)
        # print(self.dec)
        # print(self.sold)

        
        #alimenter ma liste score
        
        for i in range(0,len(solde)):        
            if sold[i]>=0:
                score1 = 0+ (op[i]/100) - (dec[i]/12)
                self.s.append(round(score1,2))
            else:
                score1 = (op[i]/100)-(dec[i]/12)-0.5
                self.s.append(round(score1,2))
        #return self.s


        #print(s) #liste score calculé
        
        # inserer les elemnts de la liste score à ma colonne clients1.score 
        
        for i in range(0,len(solde)):
            sql= "update clients set score=%s where identifiant=%s" 
            val = (self.s[i],i+1) 
            sc.execute(sql, val)
        sc.execute("select score from clients")
        score=sc.fetchall()
        #print(score)
        mydb.commit()
   # def ajout_client
  
class Tablecredits(TableClient):
    def __init__(self):
        TableClient.__init__(self)
    
    def credit(self):
        sc=mydb.cursor()
        #(id,nom,prenom,num_comptes, credit_accorde
        sc.execute("create table credits (identifiant int, nom varchar(60),prenom varchar(60),numero_de_compte int,credit_accorde float)")
    
    def calcul_credit(self):

        sc=mydb.cursor()
        sc.execute("select score from clients")
        score=sc.fetchall()
        sc.execute("select identifiant from clients")
        identifiant=sc.fetchall()
        sc.execute("select nom from clients")
        nom=sc.fetchall()
        sc.execute("select prenom from clients")
        prenom=sc.fetchall()
        sc.execute("select numero_de_compte from clients")
        numero_de_compte=sc.fetchall()
        benefice=0
        for i in range(0,len(score)):       
            if score[i][0]>0.4:
                credit_client=score[i][0]*10000
                benefice+=credit_client*0.05
             
                sc=mydb.cursor()
                sql = "INSERT INTO credits (identifiant,nom,prenom,numero_de_compte,credit_accorde) VALUES (%s,%s,%s,%s,%s)"
                val=(identifiant[i][0],nom[i][0],prenom[i][0],numero_de_compte[i][0],credit_client)
                sc.execute(sql,val)
                
           
        print("benefice de la banque (€) =",benefice)
        

class TableCompte(Table):
    def __init__(self):
        Table.__init__(self)
        
class TableOperation(Table):
    def __init__(self):
        Table.__init__(self)



objetTable = Table()
#objetTable.lecture(clients)
# objetTable.lecture(comptes)
# objetTable.lecture(operations)
#objetTable.lecture(credits)

# nouvelle colonne score
client=TableClient()
client.score()
#ma table credit
credit=Tablecredits()
#credit.credit()
credit.calcul_credit()