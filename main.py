import sqlite3
import os
import cmd
import atlas.scanner as scanner
import atlas.scrapper as scrapper

INSTALL_PATH = "/usr/local/lib/atlas"
DB_PATH = INSTALL_PATH + "/atlas.db"

def first_run():
    return (not os.path.isdir(INSTALL_PATH))

def init_atlas():
    os.mkdir(INSTALL_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript(INIT_SQL)
    conn.commit()
    conn.close()


class AtlasShell(cmd.Cmd):
    intro   = "Welcome to Atlas.\nType help or ? to list commands.\n"
    prompt = "Atlas:>"
    file = None

    def do_scan(self,arg):
        tokens = arg.split(" ")
        if len(tokens) < 2:
            print("Error: not enough arguments\nSyntax: Atlas:>scan tag path\nExample: Atlas:> scan tv /home/john/media/tv")
            return
        else:
            tag = tokens[0]
            path = " ".join(tokens[1:])
            (hits,dupplicates) = scanner.run_scanner(path,tag,DB_PATH)
            print(f"Added {hits} media files, found {dupplicates} dupplicates")
    
    def do_scrape(self,arg):
        tokens = arg.split(" ")
        if len(tokens) != 1:
            print("Invalid amount of args for scrape\nSyntax: Atlas:>scrape tag\nExample: Atlas:>scrape tv")
            return
        else:
            tag = tokens[0]
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            tags = []
            for id,path in c.execute("SELECT media_id,file_path FROM res_index WHERE media_type = ?",[tag]):
                tags += [(id,plugin,key,value) for (plugin,key,value) in scrapper.scrape(path)]

            inserted_tags = 0
            tag_collisions = 0
            for new_tag in tags:
                try:
                    with conn:
                        conn.execute("INSERT INTO tags VALUES (?,?,?,?)",new_tag)
                        inserted_tags += 1
                except sqlite3.IntegrityError:
                        tag_collisions += 1
            conn.commit()
            conn.close()
            print(f"Scrape complete: {inserted_tags} new tags in db, {tag_collisions} dupplicates skipped")
    
    def do_EOF(self,arg):
        return True


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
    FOREIGN KEY(media_id) REFERENCES stream_ready_index(media_id),
    UNIQUE (media_id,plugin,tag)
);'''


if __name__ == '__main__':
    if first_run():
        init_atlas()
    AtlasShell().cmdloop()
    print("Goodbye")

