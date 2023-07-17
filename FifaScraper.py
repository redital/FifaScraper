from requests_html import HTMLSession, HTML
import flatdict
from time import time
from myFunctions import *

startTime = time()

url = 'https://www.fifaratings.com/teams'

# Inizializzo le variabili 
playersInfo = []
id = 1

# Colleziono la lista dei link alle pagine delle singole squadre
teams = getTeamsUrls(url)[:2]

for teamNumber, team in enumerate(teams):
    teamName = " ".join(team.split("/")[-1].split("-"))

    print(teamName)

    players = getPlayersUrls(team)
    for playerNumber, player in enumerate(players) : 

        playerInfo = {}
        
        playerName = " ".join([word for word in player.split("/")[-1].split("-") if word.isalpha()])
        
        playerInfo["Name"] = playerName
        playerInfo["WebPage"] = player
        playerInfo["Team"] = teamName
        playerInfo["Id"] = id

        stats = getStats(player)
        
        stats = dict(flatdict.FlatDict(stats))
        playersInfo.append(playerInfo | stats)

        id+=1

        progressBar(len(teams), len(players), teamNumber, playerNumber)
    print()
print()

endScrapingTime = time()

writeCSV(playersInfo, "C:\\Users\\rippo\\Desktop\\FifaScraper", "PlayersStats.csv")

endTime=time()

print("Tempo impiegato per lo scraping:              ", endScrapingTime-startTime)
print("Tempo impiegato per la scrittura del CSV:     ", endTime-endScrapingTime)
print("Tempo totale di esecuzuione:                  ", endTime-startTime)


