#!/usr/bin/env python3
"""Lock visible randomized-page readings before opening MAPPING_SEALED.json."""
from pathlib import Path
import datetime, hashlib, json

ROOT = Path(__file__).resolve().parent
TEXT = [
"However, Ein\nwas never seen\nagain...",
"Ein remained\nin Riviera to\nhelp maintain\nthe peace with\nFia, who\nbecame a\nvaliant\nwarrior.",
"Epilogue\n\n~At a Temple\nNear Elendia",
"Ein remained\nin Riviera,\nwhere he and\nLina became\ntreasure\nhunters,\nwandering from\nruin to ruin.",
"I saw, heard,\nand\nexperienced\nthe events\nfirst-hand...",
"Thanks to Ein\nand his\nfriends, the\nAccursed were\ndefeated and\nRiviera was\nsaved.",
"This is\ndedicated to a\ncertain angel,\nwho was my\ndearest\nfriend.",
"Epilogue\n\n~In a Forest",
"Ein remained\nin Riviera and\ntraveled\nacross the\nland with\nSerene to rid\nthe world of\ndemons.",
"in the\nPromised Land\nwith the\nSprites...",
"One day, the\npair's\nunrelenting\n10-year battle\nwill be passed\ndown from",
"Fate is\nsomething to\nbe carved with\none's own\nhands...",
"If you believe\nin yourself,\nyou will break\nfree from all\nthat binds\nyou...",
"In fact, all\nthe spells\nused today in\nmodern Riviera\nstem from\nmagic those\ntwo\ndiscovered...",
"generation to\ngeneration in\nthe Annals of\nRiviera.",
"Fate is not\nsomething\nforced onto\nyou, nor is it\nsomething one\nyields to.",
"Ein remained\nin Riviera\nand, along\nwith Cierra,\nsearched the\nNelde Ruins\nfor hidden\nknowledge.",
"The unlikely\npair would\nlater make a\ngrand\ndiscovery and\nbecome known",
"It is said\nthat Ein never\nreturned to\nAsgard, but\ninstead lived\nout his days",
"Thanks to Ein\nand his\nfriends, the\nAccursed were\ndefeated and\nRiviera was\nsaved.",
"Epilogue\n\n~At the Nelde\nRuins",
"Thus ends my\naccount of the\nintertwining\nhistories of\nAsgard and\nRiviera.",
"They kept busy\nby recording\nthe entire\naccount of the\ngreat war,\nfought by",
"Epilogue\n\n~At an Ancient\nCastle",
"Written by\nRose R.\nCrawford\nHistorian",
"as the\nLegendary\nTreasure\nHunters.",
"Ein was\nsurprised his\nFamiliar was\nfemale (and\nnow human),\nbut they\nremained an\ninseparable\nteam.",
"Thus began a\nnew adventure...",
"brave Sprites\nand Angels, in\nthe pages of\nRiviera's\nhistory...",
"Epilogue\n\n~At the Guild\nat Asgard",
"Due to their\nefforts, it is\nsaid, the\nSprites of\nElendia spent\nan eternity of\npeace without\nany suffering.",
"I hope to pass\nthis message\non to as many\npeople as I\ncan...",
]
assert len(TEXT) == 32
rows = [{"blind_id": f"R{i:02d}", "visible_transcription": text, "legibility": "PASS", "clipping": "PASS", "japanese_visible": False} for i, text in enumerate(TEXT, 1)]
transcript = ROOT / "BLIND_TRANSCRIPTION_LOCKED.json"
transcript.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
mapping = ROOT / "MAPPING_SEALED.json"
lock = {
    "method": "visual transcription of randomized screenshots before mapping reveal",
    "page_count": 32,
    "transcription_file": transcript.name,
    "transcription_sha256": hashlib.sha256(transcript.read_bytes()).hexdigest(),
    "mapping_file": mapping.name,
    "mapping_sha256_at_lock": hashlib.sha256(mapping.read_bytes()).hexdigest(),
    "locked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "mapping_not_read_by_this_locking_script": True,
}
(ROOT / "TRANSCRIPTION_LOCK.json").write_text(json.dumps(lock, indent=2) + "\n")
print(json.dumps(lock, indent=2))
