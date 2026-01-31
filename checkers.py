import asyncio
import socket
import aiohttp
from bs4 import BeautifulSoup


# -------------------------------
# Wikipedia Checker (REST API)
# -------------------------------
async def check_wikipedia(session: aiohttp.ClientSession, name: str):
    safe_name = name.replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{safe_name}"

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as r:
            if r.status == 200:
                data = await r.json()
                if "extract" in data:
                    page = data.get("content_urls", {}).get("desktop", {}).get("page")
                    return True, page
    except Exception:
        pass

    return False, None


# -------------------------------
# DuckDuckGo Checker (HTML)
# -------------------------------
async def check_duckduckgo(session: aiohttp.ClientSession, name: str):
    query = name.replace(" ", "+")
    url = f"https://duckduckgo.com/html/?q={query}+artist"

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as r:
            html = await r.text()
            soup = BeautifulSoup(html, "html.parser")
            results = soup.select(".result__title")
            return len(results) > 0, None
    except Exception:
        pass

    return False, None


# -------------------------------
# Domain Checker (.com via DNS)
# (OHNE aiodns)
# -------------------------------
async def check_domain(name: str):
    domain = f"{name.lower().replace(' ', '')}.com"
    loop = asyncio.get_running_loop()

    try:
        await loop.getaddrinfo(domain, None)
        return True, domain   # Domain existiert
    except socket.gaierror:
        return False, domain  # Domain frei



# -------------------------------
# Discogs Checker (API)
# -------------------------------
async def check_discogs(session, name):
    from config import DISCOGS_TOKEN

    url = "https://api.discogs.com/database/search"
    params = {
        "q": name,
        "type": "artist",
        "per_page": 5,
        "token": DISCOGS_TOKEN
    }

    try:
        async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=8)) as r:
            if r.status == 200:
                data = await r.json()
                results = data.get("results", [])

                # Exakte oder sehr nahe Treffer?
                for artist in results:
                    title = artist.get("title", "").lower()
                    if name.lower() == title:
                        return True, artist.get("resource_url")

                # Fallback: irgend ein Artist vorhanden
                return len(results) > 0, None
    except Exception:
        pass

    return False, None


# -------------------------------
# Bandcamp Checker (HTML Search)
# -------------------------------
async def check_bandcamp(session, name):
    query = name.replace(" ", "+")
    url = f"https://bandcamp.com/search?q={query}&item_type=b"

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as r:
            html = await r.text()

        soup = BeautifulSoup(html, "html.parser")
        results = soup.select("li.searchresult")

        if not results:
            return False, None

        name_lower = name.lower()

        for result in results:
            heading = result.select_one(".heading")
            if not heading:
                continue

            title = heading.get_text(strip=True).lower()
            link = heading.find("a")["href"]

            # Exakter oder sehr enger Match
            if title == name_lower or name_lower in title:
                return True, link

        # Treffer vorhanden, aber kein exakter Match
        return True, None

    except Exception:
        pass

    return False, None

# -------------------------------
# Multi-Domain Checker (DNS)
# -------------------------------
async def check_domains(name: str, tlds=None):
    if tlds is None:
        tlds = ["com", "art", "music", "band", "audio", "de", "at", "fm", "dj", "rocks",]

    base = name.lower().replace(" ", "").replace("-", "")
    loop = asyncio.get_running_loop()

    results = {}

    for tld in tlds:
        domain = f"{base}.{tld}"
        try:
            await loop.getaddrinfo(domain, None)
            results[tld] = True   # Domain existiert
        except socket.gaierror:
            results[tld] = False  # Domain frei

    return results

# -------------------------------
# MusicBrainz Checker (API)
# -------------------------------
async def check_musicbrainz(session, name: str):
    """
    Prüft, ob ein Künstler mit dem Namen bei MusicBrainz existiert.
    Rückgabe: (True/False, URL oder None)
    """
    import urllib.parse

    query = urllib.parse.quote(name)
    url = f"https://musicbrainz.org/ws/2/artist/?query={query}&fmt=json&limit=5"

    headers = {
        "User-Agent": "ArtistNameChecker/1.0 (your_email@example.com)"
    }

    try:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=8)) as r:
            if r.status == 200:
                data = await r.json()
                artists = data.get("artists", [])

                name_lower = name.lower()
                for artist in artists:
                    title = artist.get("name", "").lower()
                    if name_lower == title or name_lower in title:
                        url_mb = f"https://musicbrainz.org/artist/{artist.get('id')}"
                        return True, url_mb

                # Treffer vorhanden, aber kein exakter Match
                return len(artists) > 0, None
    except Exception:
        pass

    return False, None



# -------------------------------
# Social Media Checker (Instagram, TikTok, YouTube)
# -------------------------------
async def check_social_media(session, name):
    """
    Prüft, ob ein Künstlername auf Social Media existiert.
    Rückgabe: dict mit True/False + optionaler URL
    """
    import urllib.parse

    results = {}

    # Konfigurierte Plattformen
    platforms = {
        "instagram": f"https://www.instagram.com/{name}/",
        "tiktok": f"https://www.tiktok.com/@{name}",
        "youtube": f"https://www.youtube.com/results?search_query={urllib.parse.quote(name)}",
        "youtubemusic": f"https://music.youtube.com/search?q={urllib.parse.quote(name)}",
        "applemusic": f"https://music.apple.com/us/search?term={urllib.parse.quote(name)}"
    }

    headers = {"User-Agent": "ArtistNameChecker/1.0"}

    async def check_platform(platform, url):
        try:
            async with session.get(url, headers=headers, timeout=8) as r:
                if r.status == 200:
                    return True, url
        except Exception:
            pass
        return False, url

    tasks = [check_platform(p, url) for p, url in platforms.items()]
    responses = await asyncio.gather(*tasks)

    for (platform, _), (exists, url) in zip(platforms.items(), responses):
        results[platform] = (exists, url if exists else None)

    return results




