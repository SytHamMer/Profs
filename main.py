from selenium import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import clean

DOWNLOAD_DELAY = 3
USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'


def connexion(login,password,name):
    DRIVER_PATH = 'C://Users//mathy//Desktop//Code//chromedriver.exe'
    driver = webdriver.Chrome(executable_path= DRIVER_PATH)
    driver.get(name)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="tarteaucitronAlertBig"]/button[2]').click()
    user = driver.find_element(By.XPATH, "//*[@id='user']")
    user.send_keys(login)
    passwordcase = driver.find_element(By.XPATH, "//*[@id='pass']")
    passwordcase.send_keys(password)
    driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div/div/div/form/fieldset/input[3]").click()
    driver.get(name)
    print("je me suis connecté")
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/div/form/div[2]/button[1]").click()
    time.sleep(3)
    liste =[]

    for i in range(1,963):
        if not(driver.find_element(By.XPATH,f"/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[{i}]/div[2]/ul/li[4]/a").text.strip() == ""):
                link = driver.find_element(By.XPATH,f"/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[{i}]/div[2]/ul/li[4]/a").get_attribute("href")
                liste.append(link)
    dict = {}
    for i in liste:
        driver.execute_script("window.open('');")
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])

        driver.get(i)
        name = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[3]/div[1]/div[2]").text
        mat = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[1]/div[2]").text
        names = clean.clean_name(name)
        if len(names)==1:
            if names[0] in dict:
                dict[names[0]].append(clean.clean_mat(mat))
            else:
                dict[names[0]] = [clean.clean_mat(mat)]
        else:
            for nom in names:
            
                print(nom)
                if nom in dict:
                    dict[nom].append(clean.clean_mat(mat))
                else:
                    dict[nom] = [clean.clean_mat(mat)]
    
        
    print(dict)
    with open("Ressources/clean_infos_V4.json","w") as f:
        json.dump(dict,f, indent = 3,ensure_ascii=False)



if __name__ == "__main__":
    login = 'lebonmat'
    mdp = '//Koala1792..'
    url = 'https://www.polytech.univ-smb.fr/intranet/scolarite/programmes-ingenieur.html'
    print(connexion(login,mdp,url))

    
    