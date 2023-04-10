from selenium import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import clean

DOWNLOAD_DELAY = 3
USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'

#Cette première fonction permet de récupérer l'ensemble des professeurs de l'USMB ainsi que tous les UEs dans lesquelles
#ils travaillent. 
def connexion(login,password,name):
    DRIVER_PATH = 'C://Users//mathy//Desktop//Code//chromedriver.exe'
    driver = webdriver.Chrome(executable_path= DRIVER_PATH)
    #récupération de la page internet 
    driver.get(name)
    time.sleep(1)
    #click du boutons cookies
    driver.find_element(By.XPATH, '//*[@id="tarteaucitronAlertBig"]/button[2]').click()
    #Les informations login et password sont renseignées et validé avec le click.
    user = driver.find_element(By.XPATH, "//*[@id='user']")
    user.send_keys(login)
    passwordcase = driver.find_element(By.XPATH, "//*[@id='pass']")
    passwordcase.send_keys(password)
    driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div/div/div/form/fieldset/input[3]").click()
    #Après la connexion il faut renseigner à nouveau la bonne adresse ou faire le scrapping
    driver.get(name)
    print("je me suis connecté")
    time.sleep(2)
    #Ce bouton permet d'afficher l'ensemble des formations données dans l'université.
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/div/form/div[2]/button[1]").click()
    time.sleep(3)
    liste =[]
    #On parcourt l'ensemble des lignes du tableau 
    for i in range(1,963):
        #Cependant une grande partie des premières lignes ne contiennent aucune informations on vérifie donc ce cas
        if not(driver.find_element(By.XPATH,f"/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[{i}]/div[2]/ul/li[4]/a").text.strip() == ""):
            link = driver.find_element(By.XPATH,f"/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[{i}]/div[2]/ul/li[4]/a").get_attribute("href")
            liste.append(link)
            #On obtient une liste des liens, avec tous les liens des UEs données dans cette université    
    dict = {}
    #On parcourt cette liste et ouvre tous les liens dans des nouvelles fenètres
    for i in liste:
        driver.execute_script("window.open('');")
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])

        driver.get(i)
        #Puis on récupère la donnée "name" qui est le/les professeurs enseignant dans cet UE
        #Ainsi que la matière donnée. 
        name = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[3]/div[1]/div[2]").text
        mat = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[1]/div[2]").text
        #La fonction clean_name() est expliquée dans le fichier clean
        names = clean.clean_name(name)
        #Pour chacun des enseignants correspondant à l'UE du lien en cours on vérifie si il existe dans le dictionnaire
        #de réponse et on lui rajoute la matière correspondante
        if len(names)==1:
            if names[0] in dict:
                dict[names[0]].append(clean.clean_mat(mat))
            else:
                dict[names[0]] = [clean.clean_mat(mat)]
        else:
            for nom in names:
            
                if nom in dict:
                    dict[nom].append(clean.clean_mat(mat))
                else:
                    dict[nom] = [clean.clean_mat(mat)]
    
    #Le fichier final est clean_info_V4.json, les autres versions permettent de voir l'évolution sur le néttoyage
    #des données notamment
    with open("Ressources/clean_infos_V4.json","w") as f:
        json.dump(dict,f, indent = 3,ensure_ascii=False)



if __name__ == "__main__":
    login = 'YOUR_LOGIN'
    mdp = 'YOUR_PASSWORD'
    url = 'https://www.polytech.univ-smb.fr/intranet/scolarite/programmes-ingenieur.html'
    connexion(login,mdp,url)

    
    