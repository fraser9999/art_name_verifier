
import os 
os.system("cls")


import asyncio
import aiohttp
import json
import csv
import socket

from checkers import (
    check_wikipedia,
    check_duckduckgo,
    check_domain,
    check_discogs,
    check_bandcamp,
    check_domains,
    check_musicbrainz
)
from scoring import calculate_score, calculate_status
from checkers import check_social_media

from datetime import datetime
from random import randrange
import codecs

 
dir_path = os.path.dirname(os.path.realpath(__file__))



# --------------------------------
# Prüfen eines einzelnen Namens
# --------------------------------
async def check_name(session, name):
    

    wiki, ddg, domain_com, discogs, bandcamp, domains, musicbrainz, social_media = await asyncio.gather(
        check_wikipedia(session, name),
        check_duckduckgo(session, name),
        check_domain(name),
        check_discogs(session, name),
        check_bandcamp(session, name),
        check_domains(name),
        check_musicbrainz(session, name),
        check_social_media(session, name)
    )



    sources = {
        "discogs": discogs[0],
        "bandcamp": bandcamp[0],
        "musicbrainz": musicbrainz[0],
        "wikipedia": wiki[0],
        "duckduckgo": ddg[0],
        "domain_com_taken": domain_com[0],
        "domains": domains,
        "social_media": social_media
    }

   

    score = calculate_score(sources)
    status = calculate_status(score, sources)

    return {
        "name": name,
        "sources": sources,
        "score": score,
        "status": status
    }

# --------------------------------
# Hauptprogramm
# --------------------------------
async def main():

    os.system("cls")

    print("")
    print("Artist Names Checker v0.1a")
    print("")
    print("manche Seiten prüfen keine Leerzeichen!")
    print("\n\n")

    newpath = dir_path + "/" + "artists" 
    if not os.path.exists(newpath):
        os.makedirs(newpath)


    nam=input("Names List (.txt)> ")
    if nam=="" or nam==None:
        print("No name List found")
        a=input("wait key to exit")
        exit 

    nam=nam.replace('"',"")


    # Namen laden
    with open(nam) as f:
        names = [n.strip() for n in f if n.strip()]

    results = []

    print("Enter Async Proofing Routine...")  

    async with aiohttp.ClientSession(
        headers={"User-Agent": "ArtistNameChecker/1.0"}
    ) as session:
        tasks = [check_name(session, name) for name in names]
        results = await asyncio.gather(*tasks)


    #-------------------------------------------------------------
    # Results  sortieren auf 1.Sicher frei , 2. frei, 3. teilweise
    #-------------------------------------------------------------

    #-------------------------------------------------------------
    # Results sortieren:
    # 1. sicher frei
    # 2. frei
    # 3. teilweise
    # 4. rest (z.B. belegt)
    #-------------------------------------------------------------

    STATUS_ORDER = {
        "sicher frei": 0,
        "frei": 1,
        "teilweise": 2,
        "belegt": 3
    }

    #results = sorted(
    #    results,
    #    key=lambda r: STATUS_ORDER.get(r.get("status"), 99)
    #)

    print("Sorting Results...")

    results = sorted(
        results,
        key=lambda r: (
            STATUS_ORDER.get(r.get("status"), 99),
            r.get("score", 1.0)
        )
    )



    print("Saving Files...")


    # -------------------------------
    # JSON speichern
    # -------------------------------

    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    json_filename = newpath + "/" + "results_" + dt_string +".json"

    with open(json_filename, "w", encoding="utf-8") as f_json:
        json.dump(results, f_json, indent=2, ensure_ascii=False)

    # -------------------------------
    # CSV speichern
    # -------------------------------
    csv_headers = [
        "name", "score", "status",
        "discogs", "bandcamp", "musicbrainz",
        "wikipedia", "duckduckgo", "domain_com_taken",
        "domains_com", "domains_art", "domains_music",
        "domains_band", "domains_audio", "domains_de", "domains_at", "domains_fm", "domains_dj", "domains_rocks",
        "social_instagram", "social_tiktok", "social_youtube", "social_youtubemusic", "social_applemusic"
    ]

    csv_filename= newpath + "/" + "results_" + dt_string +".csv"


    with open(csv_filename, "w", newline="", encoding="utf-8") as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=csv_headers)
        writer.writeheader()

        for r in results:

            # Social-Media-Daten holen (oder Default)
            social = r["sources"].get("social_media", {})


            row = {
                "name": r["name"],
                "score": r["score"],
                "status": r["status"],
                "discogs": r["sources"]["discogs"],
                "bandcamp": r["sources"]["bandcamp"],
                "musicbrainz": r["sources"]["musicbrainz"],
                "wikipedia": r["sources"]["wikipedia"],
                "duckduckgo": r["sources"]["duckduckgo"],
                "domain_com_taken": r["sources"]["domain_com_taken"],
                "domains_com": r["sources"]["domains"].get("com"),
                "domains_art": r["sources"]["domains"].get("art"),
                "domains_music": r["sources"]["domains"].get("music"),
                "domains_band": r["sources"]["domains"].get("band"),
                "domains_audio": r["sources"]["domains"].get("audio"),
                "domains_de": r["sources"]["domains"].get("de"),
                "domains_at": r["sources"]["domains"].get("at"),
                "domains_fm": r["sources"]["domains"].get("fm"),
                "domains_dj": r["sources"]["domains"].get("dj"),
                "domains_rocks": r["sources"]["domains"].get("rocks"), 
                "social_instagram": social.get("instagram", (False, None))[0],
                "social_tiktok": social.get("tiktok", (False, None))[0],
                "social_youtube": social.get("youtube", (False, None))[0],
                "social_youtubemusic": social.get("youtubemusic", (False, None))[0],
                "social_applemusic": social.get("applemusic", (False, None))[0],
            }
            writer.writerow(row)

    #------------------------------------
    # Write sicher_frei into text file
    #------------------------------------

    txt_filename = newpath + "/" + "results_" + dt_string +".txt"
    file = codecs.open(txt_filename, "w", "utf-8")

    file.write("Künstlernamen - sicher frei")
    file.write("\n\n")
    file.write(dt_string)
    file.write("\n\n")

    # Ausgabe in Terminal and Txt File
    for r in results:
         
        if 'sicher frei' in str(r) or 'frei' in str(r):

            string= "Name: " + str(r["name"]) + "   Score: " +str(r["score"]) + " Status: " + str(r["status"])

            file.write(string)
            file.write("\n\n")

            # Debug print
            print(r)
    
    file.close()


    print("\n\n")
    a=input("wait key to end")


# --------------------------------
# Start
# --------------------------------
if __name__ == "__main__":
    asyncio.run(main())
