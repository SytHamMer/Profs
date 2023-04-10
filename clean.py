def clean_name(name):
    """function which transmorm a string with one or two people in a tuple of x people

    Args:
        name (String): The string with all the infos

    Returns:
        tuple: a tuple with one x people
    """
    #Lorsque que les enseignants rentrent ces informations dans le site il n'y a pas de nomenclature précise
    #Il faut donc effectuer tous les cas possibles afin d'obtenir les données les plus propres possibles
    #remove space before and after
    res = []
    name = name.lower()
    if '/' in name:
        r = name.split('/')
        res =[r[0],r[1]]
    elif ';' in name:
        r = name.split(';')
        res =[r[0],r[1]]
    elif ',' in name:
        r = name.split(',')
        res =[r[0],r[1]]
    elif ' et ' in name:
        r = name.split(' et ')
        res =[r[0],r[1]]
    elif ' - ' in name:
        r = name.split(' - ')
        res =[r[0],r[1]]
    else:
        res = [name]
     
    
    for i in range(0,len(res)):   
        if "." in res[i]:
            j = res[i].replace('.','')
            res[i] = j
        if "é" in res[i]:
            j = res[i].replace('é','e')
            res[i]=j
        if "è" in res[i]:
            j = res[i].replace('è','e')
            res[i]=j
        if "ê" in res[i]:
            j = res[i].replace('ê','e')
            res[i]=j
        res[i] = res[i].strip()
    return res


def clean_mat(mat):
    """clean mat 

    Args:
        mat (String): matière

    Returns:
        String: matière sans les accents
    """
    if "é" in mat:
        mat = mat.replace('é','e')
    if "è" in mat:
        mat = mat.replace('è','e')
    if "ê" in mat:
        mat = mat.replace('ê','e')
    return mat
    
#Néttoyage important, espace, et etc mais 
# corriger les fautes de frappes 'philipe' et 'philippe' par exemple trop précis 
# et "e" pour "emmanuel" mais aussi ernard et non bernard
#Ces erreurs sont donc laissées telle qu'elle.
#tout accents remplacé par e 


if __name__ == "__main__":
    #Voici simplement des exemple de teste de la fonction afin de déterminer son bon fonctionnement.
    print(clean_name(" Bonjour.  et èèeèrè "))    
    print(clean_name("Hervé et Josêph.")) 
    print(clean_name("Bonjour./Aurevoir")) 
    print(clean_mat("Ceci est une matière qui comporte des accents comme é et ê"))
