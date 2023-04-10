import json
import requests
#Ici nous allons effectuer toutes les requètes auprès de l'API
#L'objectif est en partant du fichier généré par le main.py récupérer les adresses des lieux de travail
#des enseignants.



# Cette fonction split simplement le nom et prénoms des enseignants afin de les renseigner dans les requêtes.
#Prise en compte des prénoms composés
def get_first_and_last_name(string):
    res = string.split(' ')
    if len(res)>2:
        name = res[0]+ res[1]
        lastname = res[2]
        return (name,lastname)
    elif len(res)==1:
        return ("","")
    return (res[0],res[1])

# Cette fonction permet de vérifier ou est stocker l'adresse, en effet l'api étant rempli par les enseignants eux 
#mêmes les données ne sont pas correctement rangées et l'adresse peut se trouver à deux endroits différents aux
#seins du json généré par la requête.
def check_addrLine(data):
    if "desc" in data:
        
        if "addrLine" in data["desc"]["address"]:
            return data["desc"]["address"]["addrLine"]
        else:
            print("Pas d'informations d'adresse")
    else:
        print("Pas d'informations d'adresse")
    
#Fonction principale générant un json avec la liste des lieux de travails des enseignants ainsi 
#qu'une liste de l'adresse de ces derniers quand elle est renseignée.
def get_workplaces(filename):
    dic ={}
    with open(filename,'r') as f:
        data = json.load(f)
    for prof in data.keys():
        firstname = get_first_and_last_name(prof)[0]
        lastname = get_first_and_last_name(prof)[1]
        url = f"https://api.archives-ouvertes.fr/search/authorstructure/?firstName_t={firstname}&lastName_t={lastname}&wt=json"
        res = requests.get(url)
        new_data = res.json()
        if new_data["response"]["result"] != "": #Ceci conserve uniquement les enseignants présent dans l'API
            
            list_org = new_data["response"]["result"]["org"]
            if type(list_org) == list:
                
                for i in list_org:
                    list_orgname = []
                    list_adresse = []
                    # print("dans la boucle des list_org : ")
                    # print(url)
                    # print(prof)
                    orgname = i["orgName"]
                    adresse = check_addrLine(i)
                    list_orgname.append(orgname)
                    list_adresse.append(adresse)
                dic[prof] = (list_orgname,list_adresse)
            else:
                orgname =  i["orgName"][0]
                adresse = check_addrLine(i)
                dic[prof]=(orgname,adresse)
        
        else: #Le cas ou le prof n'est pas prépsent dans l'API 
            dic[prof] = "Pas d'informations"
    
    
    with open("Ressources/address_V1.json","w") as f:
        json.dump(dic,f, indent = 3,ensure_ascii=False)
        
        
        
        
        

if __name__ == "__main__":
    get_workplaces("Ressources/clean_infos_V4.json")

