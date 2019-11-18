import cfscrape
from bs4 import BeautifulSoup
import sys


def soupify(url):
    scraper = cfscrape.create_scraper()
    cfurl = scraper.get(url).content
    soup = BeautifulSoup(cfurl, 'html.parser')
    return soup

def downloadFile(filename,url):
    scraper = cfscrape.create_scraper()
    cfurl = scraper.get(url).content
    f = open(filename, 'wb')
    print(filename)
    with open(filename, 'wb') as f:
        f.write(cfurl)
    f.close()
    return

def modlisterMod(modid):
    dependecyurl ="https://www.curseforge.com/minecraft/mc-mods/"+modid+"/relations/dependencies?filter-related-dependencies=3"
    soup1 = soupify(dependecyurl)
    modcontents = soup1.find_all(class_ = "flex items-end lg:hidden")
    modlist = []
    modlist2 = []
    for modcontent in modcontents:
            modlist.append((((modcontent.find('a'))['href']).split('/'))[-1])
    while True:
        modlist2 = modlist
        for modlistitem in modlist:
            modlisttemp = modlisterMod(modlistitem)
            for modlisttemp in modlisttemp:
                modlist.append(modlisttemp)
        if modlist2 == modlist:
            break
    return modlist

def moddependecylister(modid):
    modlist = modlisterMod(modid)
    modlist.append(modid)
    modlist = list(dict.fromkeys(modlist))
    return modlist

def downloadMod(modid):
    url = "https://www.curseforge.com/minecraft/mc-mods/" +modid+"/files/all?filter-game-version=1738749986%3A628"
    soup = soupify(url)
    filedetails = soup.find(attrs={"data-action": "file-link"})
    filename = (filedetails.get_text()).strip()
    if filename[-4:] == ".jar":
        pass
    else:
        filename = filename + ".jar"
    fileid = ((filedetails['href']).split('/'))[-1]
    downloadurl = "https://www.curseforge.com/minecraft/mc-mods/"+modid+"/download/"+fileid+"/file"
    downloadFile(filename,downloadurl)

urlprimer = 'https://www.curseforge.com/minecraft/mc-mods'

##modid = "thermal-expansion"
modidlist = sys.argv[1:]
##print(modidlist)
##modid = sys.argv[1]
for modid in modidlist:
    modlist = moddependecylister(modid)

    for mod in modlist:
        downloadMod(mod)



