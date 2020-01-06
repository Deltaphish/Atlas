# Dummy transcoder
#TODO: make an actual transcoder

import sqlite3

def transcode(start_dir,db_loc):
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    c.execute('SELECT * FROM res_index')
    for id, media_type, path in c.fetchall():
        c.execute("INSERT INTO stream_ready_index VALUES (?,?,?);",[id, media_type, path])
    conn.commit()
    conn.close()