from bs4 import BeautifulSoup as BS
import requests
import shutil
import os



def get_img_url_from_page(url):
    page = requests.get(url)
    soup = BS(page.content,'html.parser')

    image= soup.find('img',attrs={'class':'img-responsive scan-page'})
    img=""
    if image!=None:
        img=image['src'].split(" ")[1]

    #print(img)
    return img

def dl_image_from_src(url,path):
    ## Set up the image URL and filename
    image_url = get_img_url_from_page(url)
    if image_url!="":
        filename = image_url.split("/")[-1]

        path+="/"+filename
        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Image sucessfully Downloaded: ', filename)
        else:
            print('Image Couldn\'t be retreived')

def dl_chapter(chapter_to_dl):
    if chapter_to_dl[-1]!="/":
        chapter_to_dl+="/"
    ## Set up the image URL and filename
    image_url = get_img_url_from_page(chapter_to_dl)
    chapter=image_url.split("/")[-2]
    serie=image_url.split("/")[-4]

    #create_serie_rep(os.getcwd()+"/"+serie)

    toCreate = os.getcwd()+"/"+serie+"/"+chapter
    #print(toCreate)
    try:
        os.mkdir(toCreate)
    except OSError:
        print("Impossible de créer le dossier")
    else:
        print("Création dossier : %s"%toCreate)

    for i in range(1,30):
        url=chapter_to_dl+str(i)
        r = requests.get(url)
        if r.status_code==200:
            dl_image_from_src(url,toCreate)
        else:
            break
def dl_chapterr(chapter_to_dl):
    if chapter_to_dl[-1]!="/":
        chapter_to_dl+="/"
    ## Set up the image URL and filename
    image_url = get_img_url_from_page(chapter_to_dl)
    chapter=image_url.split("/")[-2]
    serie=image_url.split("/")[-4]

    #create_serie_rep(os.getcwd()+"/"+serie)

    toCreate = os.getcwd()+"/"+chapter
    print(toCreate)
    try:
        os.mkdir(toCreate)
    except OSError:
        print("Impossible de créer le dossier")
    else:
        print("Création dossier : %s"%toCreate)

    for i in range(1,30):
        url=chapter_to_dl+str(i)
        r = requests.get(url)
        if r.status_code==200:
            dl_image_from_src(url,toCreate)
        else:
            break

def create_serie_rep(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Impossible de créer le dossier %s" %path)
    else:
        print("Création dossier : %s"%path)

def dl_all_chapters():

    series=str(input("Entrez l'url du manga lelscan a dl :\n"))
    if series[-1]!="/":
        series+="/" # on ajoute s'il n'y est pas
    #print(os.getcwd()+"/"+series.split("/")[-2])
    create_serie_rep(os.getcwd()+"/"+series.split("/")[-2])

    #print(series+"1")
    for i in range (1,300):
        r = requests.get(series+str(i)+"/")
        if r.status_code==200:
            dl_chapter(series+str(i)+"/")
        else:
            continue

choix=str(input("Que voulez vous faire?:\n 1. Télécharger un chapitre précis \n 2. Télécharqer une série entière\n"))
if choix=="1":
    dl_chapterr(str(input("Entrez l'url du chapitre lel-scan-vf à dl\n")))
if choix=="2":
    dl_all_chapters()