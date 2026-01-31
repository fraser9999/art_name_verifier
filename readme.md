---

## 📄 `README.md`

````markdown
# Artist Name Availability Checker

An asynchronous Python tool to check the availability of artist / band names across multiple public data sources, domains, and social media platforms.

The tool supports:
- name variants (e.g. `NeonFox`, `Neon Fox`, `NeonFoxMusic`)
- score-based evaluation
- status classification (`sicher frei`, `frei`, `teilweise`, `belegt`)
- JSON, CSV and TXT export

---

## ✨ Features

- 🔎 Checks multiple public data sources:
  - Discogs
  - MusicBrainz
  - Bandcamp
  - Wikipedia
  - DuckDuckGo
- 🌐 Domain availability check:
  - `.com`, `.art`, `.music`, `.band`, `.audio`, `.de`, `.at`, `.fm`, `.dj`, `.rocks`
- 📱 Social media checks:
  - Instagram
  - TikTok
  - YouTube (search-based)
- 🔁 Automatic name variant generation
- ⚖️ Weighted scoring system
- 🟢 Status classification:
  - **sicher frei** (all checks negative)
  - **frei**
  - **teilweise**
  - **belegt**
- ⚡ Fully asynchronous using `asyncio` and `aiohttp`
- 📁 Exports results to:
  - JSON
  - CSV
  - TXT (list of "sicher frei" names)

---

## 🧠 How It Works

1. Load a list of artist names from a `.txt` file
2. Generate name variants automatically
3. Check each variant across all sources
4. Aggregate results:
   - worst status wins
   - highest score wins
   - sources are merged
5. Sort results by status priority
6. Export results

---

## 📂 Project Structure

```text
.
├── main.py          # Main application
├── checkers.py      # All external checks (APIs, domains, social media)
├── scoring.py       # Scoring & status logic
├── variants.py      # Artist name variant generation
├── artists/         # Output directory (auto-created)
├── requirements.txt
└── README.md
````

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/artist-name-checker.git
cd artist-name-checker
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\\Scripts\\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

1. Prepare a text file with artist names (one per line):

```text
NeonFox
QuantumNovaX
Zypheralon
```

2. Run the program:


```bash

use pushd to change to local directory in .bat file

python main.py
```

3. Enter the path to your `.txt` file when prompted.

4. Results will be saved to the `artists/` folder:

   * `results_YYYYMMDD_HHMMSS.json`
   * `results_YYYYMMDD_HHMMSS.csv`
   * `results_YYYYMMDD_HHMMSS.txt`

---

## 📊 Output Example

```json
{
  "name": "NeonFox",
  "status": "teilweise",
  "score": 0.34,
  "variants_checked": [
    "NeonFox",
    "Neon Fox",
    "NeonFoxMusic"
  ]
}
```

---

## ⚠️ Notes & Limitations

* This tool uses **publicly accessible endpoints only**
* No aggressive scraping
* No login-protected APIs (unless you add API keys)
* Results are **heuristic**, not legally binding
* Some platforms may block requests if rate limits are exceeded

---

## 🛣️ Roadmap (Ideas)

* SQLite result cache
* CLI arguments (`--only-free`, `--no-variants`)
* Additional social platforms (X/Twitter, SoundCloud)
* Name similarity scoring
* Web UI

---

## 📜 License

MIT License – free to use, modify and distribute.

---

## 🙌 Disclaimer

This project is intended for **research and creative name discovery only**.
Always verify trademark and legal availability independently.

````

---

## 📄 `requirements.txt`

```text
aiohttp>=3.8.5
asyncio
````

👉 **Hinweis:**

* `asyncio` ist in Python ≥3.8 **bereits enthalten**, kann aber für Klarheit drin bleiben
* Keine unnötigen Abhängigkeiten – bewusst minimal gehalten

