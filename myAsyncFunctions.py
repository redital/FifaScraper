from requests_html import AsyncHTMLSession
import flatdict
import csv

def setUpAsyncSession():
    session = AsyncHTMLSession()
    session.headers["User-Agent"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
    return session


async def getAsyncTeamsUrls(session, teamsListUrl):
    r = await session.get(teamsListUrl)
    await r.html.arender()

    teams = r.html.absolute_links
    teams = [i for i in teams if i.split("/")[-2]=='team']
    teams = list(set(teams))    # Elimino eventuali duplicati 

    r.close()

    return teams


async def getAsyncPlayersUrls(session, teamUrl):

    t = await session.get(teamUrl)
    await t.html.arender(timeout=20)
    players = t.html.find('html body div.wrapper.both-skin-adx div.main main.content div.row.no-gutters div.col-12.col-md-7.col-lg-7.col-xl-8 div.card.pb-2 div.row.no-gutters div.col-12.align-self-center.text-left div.ml-1.ml-xl-3.mr-1.mr-xl-3.mb-xl-3 div.table-responsive.h-100.overflow-hidden table.table.table-striped.table-sm.table-hover.mb-0 tbody tr td div.entries')
    players = [[j for j in i.absolute_links if j.split("/")[-2] !='position'][0] for i in players]

    t.close()

    #print(" ".join(teamUrl.split("/")[-1].split("-")))
    return players

async def getAsyncStats(session, playerUrl):

    p = await session.get(playerUrl)
    await p.html.arender(timeout=20)

    #cards = r.html.find('html body div.wrapper.both-skin-adx div.main main.content div.container-fluid div#nav-tabContent.tab-content.mb-4.pb-2 div#nav-attributes.tab-pane.fade.show.active.mt-3 div.row div.col-12.col-md-6.ml-md-n1 div.card')
    cards = p.html.find('html body div.wrapper.both-skin-adx div.main main.content div.container-fluid div#nav-tabContent.tab-content.mb-4.pb-2 div#nav-attributes.tab-pane.fade.show.active.mt-3 div.row div.col-12.col-md-6 div.card')
    cards = cards[:-2]

    stats={}
    for card_html in cards:
        card_name = card_html.find('div.card-header h5.card-title.mb-0.ml-1',first=True).text
        stats[card_name.split(" ")[1]] = {}

        attributi = card_html.find('div.card-body.py-3.mb-1 div.row.no-gutters div.col-12.align-self-center.text-left ul.list-group.list-no-bullet li.mb-1')
        for j in attributi:
            val = j.text.split(" ")[0]
            name = j.text.replace(val + " ", "")
            if val.isdigit() : 
                stats[card_name.split(" ")[1]][name] = int(val)
            else:
                print("\nIl valore {} non è convertibile in stringa, setto il valore a None".format(val))
                stats[card_name.split(" ")[1]][name] = None
    
    p.close()
    
    return stats

async def getAsyncPlayerInfo(session, playerUrl):
    global id
    playerInfo = {}
    
    playerName = " ".join([word for word in playerUrl.split("/")[-1].split("-") if word.isalpha()])
    

    playerInfo["Name"] = playerName
    playerInfo["WebPage"] = playerUrl
    #playerInfo["Team"] = teamName
    playerInfo["Id"] = id

    stats = await getAsyncStats(session, playerUrl)
    
    stats = dict(flatdict.FlatDict(stats))


    
    #print(playerName)
    id+=1
    return (playerInfo | stats)


def progressBar(globalLength, iterazioneGlobale, lunghezzaBarraProgressoGlobale = 50):
    
    # Progresso globale
    perc = int(((iterazioneGlobale+1)/globalLength)*10000)/100
    progress = int(((iterazioneGlobale+1)/globalLength)*lunghezzaBarraProgressoGlobale)
    remaining = (lunghezzaBarraProgressoGlobale-progress)
    print('{2:=<{0}}{4:5}%{3: >{1}}'.format(progress+1,remaining+1,"[","]",perc),end="\r")
    

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def writeCSV(playersInfo, path, fileName):
    with open(path + "/" + fileName, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=playersInfo[0].keys())
        writer.writeheader()
        writer.writerows(playersInfo)


