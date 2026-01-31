WEIGHTS = {
    "discogs": 0.25,
    "bandcamp": 0.20,
    "musicbrainz": 0.20,
    "wikipedia": 0.15,
    "duckduckgo": 0.10,
    "domain_com_taken": 0.05,
    "social_media": 0.10,   # max. 0.10
    "domains": 0.05
}

def calculate_social_score(social_dict: dict) -> float:
    if not social_dict:
        return 0.0
    taken = sum(1 for v in social_dict.values() if v[0])
    return round((taken / len(social_dict)) * WEIGHTS["social_media"], 2)

def calculate_score(sources: dict) -> float:
    score = 0.0
    for source, weight in WEIGHTS.items():
        if source == "social_media":
            score += calculate_social_score(sources.get("social_media"))
        elif source != "social_media" and sources.get(source):
            score += weight

    # Multi-Domain Score
    score += calculate_domain_score(sources.get("domains"))

    return round(min(score, 1.0), 2)



def calculate_domain_score(domains: dict) -> float:
    if not domains:
        return 0.0

    taken = sum(1 for v in domains.values() if v)
    total = len(domains)

    # max 0.30 Score für Domains
    return round((taken / total) * 0.30, 2)


def old_calculate_status(score: float, sources: dict) -> str:
    """
    Ermittelt den Status eines Namens basierend auf Score und Domainbelegung.
    Rückgabe: 'frei', 'teilweise', 'belegt'
    """

    # Wenn alle Domains frei und Score niedrig
    domains = sources.get("domains", {})
    any_domain_taken = any(domains.values()) if domains else False

    # Heuristik
    if score <= 0.2 and not any_domain_taken:
        return "frei"
    elif 0.2 < score <= 0.6 or any_domain_taken:
        return "teilweise"
    else:
        return "belegt"



def calculate_status(score: float, sources: dict) -> str:
    """
    Status des Namens ermitteln:
    - 'sicher frei' : alle Quellen + Domains + Social Media = False
    - 'frei'        : Score <= 0.2, Domains frei
    - 'teilweise'   : Score 0.2-0.6 oder Domains belegt
    - 'belegt'      : Score > 0.6
    """
    domains = sources.get("domains", {})
    social = sources.get("social_media", {})

    # Prüfen, ob wirklich alles False ist
    all_false = True

    main_sources = ["discogs", "bandcamp", "musicbrainz", "wikipedia", "duckduckgo", "domain_com_taken"]
    for src in main_sources:
        if sources.get(src):
            all_false = False
            break

    # Social-Media prüfen
    if all_false:
        for v in social.values():
            if v[0]:  # True/False im Tupel
                all_false = False
                break

    # Domains prüfen
    if all_false and any(domains.values()):
        all_false = False

    if all_false:
        return "sicher frei"
    elif score <= 0.2 and not any(domains.values()):
        return "frei"
    elif 0.2 < score <= 0.6 or any(domains.values()):
        return "teilweise"
    else:
        return "belegt"



