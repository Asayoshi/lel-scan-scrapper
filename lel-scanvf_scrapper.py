from bs4 import BeautifulSoup as BS
import requests
import shutil
import os

def get_img_url_from_page(url):
    page = requests.get(url)
    soup = BS(page.content,'html.parser')

    image= soup.find('img',attrs={'class':'img-responsive scan-page'})
    image=image['src'].split(" ")[1]

    print(image)
    return image



def dl_image_from_src(url):
    ## Set up the image URL and filename
    image_url = get_img_url_from_page(url)
    filename = image_url.split("/")[-1]
    chapter=image_url.split("/")[-2]

    path=chapter+"/"+filename
    # toCreate = os.getcwd()+"/"+chapter
    # print(toCreate)
    # try:
    #     os.mkdir(toCreate)
    # except OSError:
    #     print("Impossible de créer le dossier")
    # else:
    #     print("Création dossier : %s"%toCreate)

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

def dl_chapter():


    chapter_to_dl=str(input("Entrez l'url du chapitre lelscan a dl :\n"))
    if chapter_to_dl[-1]!="/":
        chapter_to_dl+="/"
    ## Set up the image URL and filename
    image_url = get_img_url_from_page(chapter_to_dl)
    chapter=image_url.split("/")[-2]
    toCreate = os.getcwd()+"/"+chapter
    print(toCreate)
    try:
        os.mkdir(toCreate)
    except OSError:
        print("Impossible de créer le dossier")
    else:
        print("Création dossier : %s"%toCreate)

    for i in range(1,100):
        url=chapter_to_dl+str(i)
        dl_image_from_src(url)

dl_chapter()