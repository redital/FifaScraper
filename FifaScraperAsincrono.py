from time import sleep, perf_counter
from myAsyncFunctions import *


print("inizio")

startTime = perf_counter()

url = 'https://www.fifaratings.com/teams'

# Inizializzo le variabili 
id = 1
session = setUpAsyncSession()
playersInfo =[] 
try:    
    # Colleziono la lista dei link alle pagine delle singole squadre
    print("\nColleziono la lista dei link alle pagine delle singole squadre")
    teams = list(session.run(getAsyncTeamsUrls(session, url)))[0]

    
    print("\nColleziono la lista dei link alle pagine dei giocatori")
    players=[]
    chunckSize=50
    chunksNumber=(len(teams)+chunckSize-1)//chunckSize
    currentChunk=0
    for teamsChunk in chunks(teams,chunckSize):
        players.extend(session.run(*[getAsyncPlayersUrls(session, teamUrl) for teamUrl in teamsChunk],progress=False))
        progressBar(chunksNumber,currentChunk)
        currentChunk+=1
        sleep(1)
    flattenPlayers = []
    for sublist in players: flattenPlayers.extend(sublist)
    players = flattenPlayers
    print("\nNumero di giocatori trovati:", len(flattenPlayers))

    print("Colleziono le statistiche dei giocatori")
    chunckSize=50
    chunksNumber=(len(players)+chunckSize-1)//chunckSize
    currentChunk=0
    for playersChunk in chunks(players,chunckSize):
        playersInfo.extend(session.run(*[getAsyncPlayerInfo(session, playerUrl) for playerUrl in playersChunk],progress=False))
        progressBar(chunksNumber,currentChunk)
        currentChunk+=1
        sleep(1)

finally:
    session.run(session.close())
    


print("\nFine scraping \nScrivo il file")
endScrapingTime = perf_counter()

writeCSV(playersInfo, "C:\\Users\\rippo\\Desktop\\FifaScraper", "PlayersStatsAsync.csv")

endTime=perf_counter()

print("Fine")

print("Tempo impiegato per lo scraping:              ", endScrapingTime-startTime)
print("Tempo impiegato per la scrittura del CSV:     ", endTime-endScrapingTime)
print("Tempo totale di esecuzuione:                  ", endTime-startTime)

