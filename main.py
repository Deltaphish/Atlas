import sqlite3
import os
import atlas.scanner as scanner
import atlas.scrapper as scrapper

def first_run():
    return (not os.path.isdir("/var/lib/atlas"))

def init_atlas():
    os.mkdir("/var/lib/atlas")
    conn = sqlite3.connect("/var/lib/atlas/atlas.db")
    c = conn.cursor()
    c.executescript(INIT_SQL)
    conn.commit()
    conn.close()

def handle(command):
    if command[:5] == "scan ":
        tokens = command.strip().split(" ")
        if len(tokens) != 3:
            print("Invalid amount of args for scan\nExample: scan tag dir")
            return False
        else:
            (_,tag,target) = tokens
            hits = scanner.run_scanner(target,tag,"/var/lib/atlas/atlas.db")
            print(f"found {hits} media files, adding to db under {tag}")
            return True
    elif command[:7] == "scrape ":
        tokens = command.split(" ")
        if len(tokens) != 2:
            print("Invalid amount of args for scrape\nExample: scrape tag")
            return False
        else:
            (_,tag) = tokens
            conn = sqlite3.connect("/var/lib/atlas/atlas.db")
            c = conn.cursor()
            tags = []
            for id,path in c.execute("SELECT media_id,file_path FROM res_index WHERE media_type = ?",[tag]):
                tags += [(id,plugin,key,value) for (plugin,key,value) in scrapper.scrape(path)]

            print(tags)
            
            c.executemany("INSERT INTO tags VALUES (?,?,?,?)",tags)
            conn.commit()
            conn.close()
            print(f"Scrape complete: {len(tags)} new tags in db")
            return True
    else:
        print("Invalid command")
        return False



INIT_SQL = '''  
CREATE TABLE IF NOT EXISTS res_index (
    media_id INTEGER PRIMARY KEY,
    media_type TEXT NOT NULL,
    file_path TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS stream_ready_index(
    media_id INTEGER PRIMARY KEY,
    media_type TEXT NOT NULL,
    file_path TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS tags (
    media_id INTEGER NOT NULL,
    plugin   TEXT NOT NULL,
    tag      TEXT NOT NULL,
    tag_value TEXT,
    FOREIGN KEY(media_id) REFERENCES stream_ready_index(media_id)
);'''

if first_run():
    init_atlas()
while handle(input("atlas:>")):
    pass
print("Goodbye")

