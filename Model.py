from cx_Oracle import *
from traceback import format_exc
class Model:
    def __init__(self):
        self.song_dict = {}
        self.db_status = True
        self.conn = None
        self.cur = None
        try:
            self.conn = connect("mouzikka/music@DESKTOP-OSNSRAS/xe")
            print("successfully connected to the database!!")
            self.cur =self.conn.cursor()
        except DatabaseError:
            print("DB error")
            print(format_exc())
            self.db_status = False

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            print("cursor closed")
        if self.conn is not None:
            self.conn.close()
            print("connection closed")

    def add_song(self, sname, spath):
        self.song_dict[sname] = spath
        print("song added : ", self.song_dict[sname])

    def get_song_path(self, sname):
        return self.song_dict[sname]

    def get_song_count(self):
        return len(self.song_dict)

    def remove_song(self, sname):
        self.song_dict.pop(sname)
        print("after deletion ", self.song_dict)

    def search_song_in_favourites(self, sname):
        self.cur.execute("select song_name from Myfavourites where song_name=:1", (sname,))
        song_tuple = self.cur.fetchone()
        if song_tuple is None:
            return False
        return True

    def add_song_to_favourites(self, sname, spath):
        if self.search_song_in_favourites(sname):
            return "Song already present in your favourites"
        self.cur.execute("select max(song_id) from Myfavourites")   # if there is no record then it will return None otherwise return max(song_id)
        last_song_id = self.cur.fetchone()[0]
        if last_song_id is None:
            last_song_id = 0
        last_song_id+=1
        self.cur.execute("insert into Myfavourites values (:1, :2, :3)", (last_song_id, sname, spath))
        self.conn.commit()
        return "Song successfully added to your favourites"

    def load_songs_from_favourites(self):
        self.cur.execute("select song_name, song_path from Myfavourites")
        song_present = False
        for sname, spath in self.cur:
            self.song_dict[sname] = spath
            song_present = True
        if song_present:
            return "List populated from the favourites"
        return "No songs present in your favourites"

    def remove_song_from_favourites(self, sname):
        self.cur.execute("delete from Myfavourites where song_name=:1", (sname,))
        self.conn.commit()
        x = self.cur.rowcount
        if x == 0:
            return "Song not present in your favourites"
        self.remove_song(sname)
        return "Song deleted from your favourites"