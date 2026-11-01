# Irish India Radio

A free web radio station for the Indian community in Ireland, running on GitHub Pages.

- It plays your playlist non-stop, in shuffled order.
- Between songs, and on the hour over the music, it plays a chime and announces:
  *"You are listening to Irish India Radio, in Dublin. It is Sunday, the 1st of November, 2026. The time is 5:28 PM."*
  It adds a Hindi line if the listener's device has a Hindi voice.
- It shows a live Dublin clock, an ON AIR light, the song playing now, what's coming up next, and the music credits.
- There's no server and no build step: the site is just `index.html`, `playlist.json` and the `music/` folder.

## Put it online (GitHub Pages)

```powershell
cd C:\Users\akhil\Projects\irishindiaradio
git init
git add .
git commit -m "Irish India Radio"
git branch -M main
git remote add origin https://github.com/akhilendraverma/irishindiaradio.git
git push -u origin main
```

Before you push, create the empty repository first: go to github.com/new, name it `irishindiaradio`, choose **Public**, and don't add a README.
Then, on GitHub, go to **Settings → Pages → Deploy from a branch → `main` / `/ (root)` → Save**.
The site goes live at `https://akhilendraverma.github.io/irishindiaradio/`.

## Add songs

```powershell
python add_song.py              # asks for the file, title, artist, licence and source
python add_song.py --list       # show the playlist
python add_song.py --remove 2   # remove song number 2
git add .
git commit -m "Add songs"
git push
```

The helper copies the MP3 into `music/` and writes the entry in `playlist.json` for you.

## Where to find Indian music you can legally stream for free

| Source | What to look for | Notes |
|---|---|---|
| **Free Music Archive** (freemusicarchive.org) | Search "India", "Bollywood", "sitar", "tabla", "raga", "bhangra" | The best fit for a radio station. Each track shows its Creative Commons licence. |
| **Jamendo** (jamendo.com) | Search "indian", "bollywood", "desi" | Tracks carry Creative Commons licences. Read each track's licence before downloading. |
| **Internet Archive** (archive.org/details/audio) | Indian classical and folk recordings | Check each item's licence. Many are public domain or Creative Commons; some are not. |
| **Wikimedia Commons** (commons.wikimedia.org) | Category "Audio files of music of India" | Free licences, though mostly short recordings. |
| **ccMixter** (ccmixter.org) | Search "indian", "sitar" | Creative Commons remixes and instrumentals. |
| **Indian artists in Ireland** | Local bands, singers and students | Ask for written permission (an email is enough). This is the best way to get real Hindi vocal songs, and it builds your community. |

**Which licences are OK for this radio**

- ✅ **CC0 or public domain:** fine; no credit needed, though credit is nice.
- ✅ **CC BY, CC BY-SA:** fine; credit the artist. The page's Music credits section does this automatically.
- ✅ **CC BY-ND:** fine; the radio plays songs unchanged.
- ⚠️ **Anything with NC (NonCommercial):** fine only while the radio has **no ads, sponsors or paid features**.
- ❌ **Pixabay Music:** **avoid it for radio.** Its licence forbids distributing tracks "on a standalone basis", that is, unchanged, and playing them on a stream counts as that.
- ❌ **"No copyright" YouTube uploads, YouTube Audio Library tracks, and Bollywood film songs:** not allowed without a licence. Film songs need licences from IMRO and PPI in Ireland, and often from the label as well (T-Series, Saregama, Sony Music India, Zee Music, Tips…).

Keep a note, or a screenshot of the licence page, for every song you add, in case anyone asks later. This is general information, not legal advice.
