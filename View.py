import random
import sys
import threading
import time
from tkinter import filedialog, messagebox
from cx_Oracle import  DatabaseError
from  pygame import mixer
import Player
from MyException import *
import tkinter as tk
import tkinter.ttk as ttk
import musicplayer_support
import traceback

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global root
    root = tk.Tk()
    top = View(root)
    musicplayer_support.init(root, top)
    root.resizable(False, False)
    root.mainloop()

class View:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#ececec' # Closest X11 color: 'gray92' 
        font11 = "-family {Avenir Next Cyr Medium} -size 23 -weight "  \
            "normal -slant roman -underline 0 -overstrike 0"
        font12 = "-family {Avenir Next Cyr} -size 9 -weight bold "  \
            "-slant roman -underline 0 -overstrike 0"
        font13 = "-family {Vivaldi} -size 22 -weight " \
                 "bold -slant roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("687x526+558+155")
        top.title("New Toplevel")
        top.configure(background="#fff")
        self.top=top
        self.songName = tk.Label(top)
        self.songName.place(relx=0.437, rely=0.038, height=44, width=281)
        self.songName.configure(background="#fff")
        self.songName.configure(disabledforeground="#a3a3a3")
        self.songName.configure(font=("Segoe Script", 16, "bold"))
        #self.songName.configure(font=font13)
        self.songName.configure(foreground="#000000")
        self.songName.configure(text='''Ladki Aankh Maare''')

        self.songProgress = ttk.Progressbar(top)
        self.songProgress.place(relx=0.393, rely=0.209, relwidth=0.495
                , relheight=0.0, height=7)

        self.progress_scale = ttk.Scale(top)
        self.progress_scale.place(relx=0.393, rely=0.209, relwidth=0.495
                              , relheight=0.0, height=7)
        self.progress_scale.configure(takefocus="")

        self.songTotalDuration = ttk.Label(top)
        self.songTotalDuration.place(relx=0.844, rely=0.171, height=19, width=29)

        self.songTotalDuration.configure(background="#fff")
        self.songTotalDuration.configure(foreground="#3399ff")
        self.songTotalDuration.configure(font=font12)
        self.songTotalDuration.configure(relief='flat')


        self.songTimePassed = ttk.Label(top)
        self.songTimePassed.place(relx=0.393, rely=0.171, height=19, width=29)
        self.songTimePassed.configure(background="#ffffff")
        self.songTimePassed.configure(foreground="#000000")
        self.songTimePassed.configure(font=font12)
        self.songTimePassed.configure(relief='flat')


        self.pauseButton = tk.Button(top)
        self.pauseButton.place(relx=0.568, rely=0.266, height=34, width=34)
        self.pauseButton.configure(activebackground="#ececec")
        self.pauseButton.configure(activeforeground="#000000")
        self.pauseButton.configure(background="#fff")
        self.pauseButton.configure(borderwidth="0")
        self.pauseButton.configure(disabledforeground="#a3a3a3")
        self.pauseButton.configure(foreground="#000000")
        self.pauseButton.configure(highlightbackground="#d9d9d9")
        self.pauseButton.configure(highlightcolor="black")
        self._img1 = tk.PhotoImage(file="./icons/pause.png")
        self.pauseButton.configure(image=self._img1)
        self.pauseButton.configure(pady="0")
        self.pauseButton.configure(text='''Button''')

        self.playButton = tk.Button(top)
        self.playButton.place(relx=0.64, rely=0.266, height=34, width=34)
        self.playButton.configure(activebackground="#ececec")
        self.playButton.configure(activeforeground="#000000")
        self.playButton.configure(background="#fff")
        self.playButton.configure(borderwidth="0")
        self.playButton.configure(disabledforeground="#a3a3a3")
        self.playButton.configure(foreground="#000000")
        self.playButton.configure(highlightbackground="#d9d9d9")
        self.playButton.configure(highlightcolor="black")
        self._img2 = tk.PhotoImage(file="./icons/play.png")
        self.playButton.configure(image=self._img2)
        self.playButton.configure(pady="0")
        self.playButton.configure(text='''Button''')

        self.stopButton = tk.Button(top)
        self.stopButton.place(relx=0.713, rely=0.266, height=34, width=34)
        self.stopButton.configure(activebackground="#ececec")
        self.stopButton.configure(activeforeground="#000000")
        self.stopButton.configure(background="#fff")
        self.stopButton.configure(borderwidth="0")
        self.stopButton.configure(disabledforeground="#a3a3a3")
        self.stopButton.configure(foreground="#000000")
        self.stopButton.configure(highlightbackground="#d9d9d9")
        self.stopButton.configure(highlightcolor="black")
        self._img3 = tk.PhotoImage(file="./icons/stop.png")
        self.stopButton.configure(image=self._img3)
        self.stopButton.configure(pady="0")
        self.stopButton.configure(text='''Button''')

        self.vinylRecordImage = tk.Label(top)
        self.vinylRecordImage.place(relx=0.0, rely=0.0, height=204, width=204)
        self.vinylRecordImage.configure(background="#d9d9d9")
        self.vinylRecordImage.configure(disabledforeground="#a3a3a3")
        self.vinylRecordImage.configure(foreground="#000000")
        self._img4 = tk.PhotoImage(file="./icons/vinylrecord.png")
        self.vinylRecordImage.configure(image=self._img4)
        self.vinylRecordImage.configure(text='''Label''')

        self.playList = ScrolledListBox(top)
        self.playList.place(relx=0.0, rely=0.38, relheight=0.532, relwidth=0.999)

        self.playList.configure(background="white")
        self.playList.configure(disabledforeground="#a3a3a3")
        self.playList.configure(font="TkFixedFont")
        self.playList.configure(foreground="black")
        self.playList.configure(highlightbackground="#d9d9d9")
        self.playList.configure(highlightcolor="#d9d9d9")
        self.playList.configure(selectbackground="#c4c4c4")
        self.playList.configure(selectforeground="black")
        self.playList.configure(width=10)

        self.previousButton = tk.Button(top)
        self.previousButton.place(relx=0.509, rely=0.285, height=16, width=16)
        self.previousButton.configure(background="#fff")
        self.previousButton.configure(borderwidth="0")
        self.previousButton.configure(disabledforeground="#a3a3a3")
        self.previousButton.configure(foreground="#000000")
        self._img5 = tk.PhotoImage(file="./icons/previous.png")
        self.previousButton.configure(image=self._img5)
        self.previousButton.configure(text='''Label''')

        self.bottomBar = ttk.Label(top)
        self.bottomBar.place(relx=0.0, rely=0.913, height=49, width=686)
        self.bottomBar.configure(background="#d9d9d9")
        self.bottomBar.configure(foreground="#000000")
        self.bottomBar.configure(font="TkDefaultFont")
        self.bottomBar.configure(relief='flat')
        self.bottomBar.configure(width=686)
        self.bottomBar.configure(state='disabled')


        self.vol_scale = ttk.Scale(top)
        self.vol_scale.place(relx=0.015, rely=0.932, relwidth=0.146, relheight=0.0
                , height=26, bordermode='ignore')
        self.vol_scale.configure(takefocus="")

        self.addSongsToPlayListButton = tk.Button(top)
        self.addSongsToPlayListButton.place(relx=0.961, rely=0.323, height=17
                , width=17)
        self.addSongsToPlayListButton.configure(activebackground="#ececec")
        self.addSongsToPlayListButton.configure(activeforeground="#d9d9d9")
        self.addSongsToPlayListButton.configure(background="#fff")
        self.addSongsToPlayListButton.configure(borderwidth="0")
        self.addSongsToPlayListButton.configure(disabledforeground="#a3a3a3")
        self.addSongsToPlayListButton.configure(foreground="#000000")
        self.addSongsToPlayListButton.configure(highlightbackground="#d9d9d9")
        self.addSongsToPlayListButton.configure(highlightcolor="black")
        self._img6 = tk.PhotoImage(file="./icons/add.png")
        self.addSongsToPlayListButton.configure(image=self._img6)
        self.addSongsToPlayListButton.configure(pady="0")
        self.addSongsToPlayListButton.configure(text='''Button''')

        self.deleteSongsFromPlaylistButton = tk.Button(top)
        self.deleteSongsFromPlaylistButton.place(relx=0.917, rely=0.323
                , height=18, width=18)
        self.deleteSongsFromPlaylistButton.configure(activebackground="#ececec")
        self.deleteSongsFromPlaylistButton.configure(activeforeground="#000000")
        self.deleteSongsFromPlaylistButton.configure(background="#fff")
        self.deleteSongsFromPlaylistButton.configure(borderwidth="0")
        self.deleteSongsFromPlaylistButton.configure(disabledforeground="#a3a3a3")
        self.deleteSongsFromPlaylistButton.configure(foreground="#000000")
        self.deleteSongsFromPlaylistButton.configure(highlightbackground="#d9d9d9")
        self.deleteSongsFromPlaylistButton.configure(highlightcolor="black")
        self._img7 = tk.PhotoImage(file="./icons/delete.png")
        self.deleteSongsFromPlaylistButton.configure(image=self._img7)
        self.deleteSongsFromPlaylistButton.configure(pady="0")
        self.deleteSongsFromPlaylistButton.configure(text='''Button''')

        self.addFavourite = tk.Button(top)
        self.addFavourite.place(relx=0.932, rely=0.913, height=42, width=42)
        self.addFavourite.configure(activebackground="#ececec")
        self.addFavourite.configure(activeforeground="#000000")
        self.addFavourite.configure(background="#d9d9d9")
        self.addFavourite.configure(borderwidth="0")
        self.addFavourite.configure(disabledforeground="#a3a3a3")
        self.addFavourite.configure(foreground="#000000")
        self.addFavourite.configure(highlightbackground="#d9d9d9")
        self.addFavourite.configure(highlightcolor="black")
        self._img8 = tk.PhotoImage(file="./icons/like.png")
        self.addFavourite.configure(image=self._img8)
        self.addFavourite.configure(pady="0")
        self.addFavourite.configure(text='''Button''')
        self.addFavourite.configure(width=42)

        self.removeFavourite = tk.Button(top)
        self.removeFavourite.place(relx=0.873, rely=0.913, height=42, width=42)
        self.removeFavourite.configure(activebackground="#ececec")
        self.removeFavourite.configure(activeforeground="#000000")
        self.removeFavourite.configure(background="#d9d9d9")
        self.removeFavourite.configure(borderwidth="0")
        self.removeFavourite.configure(disabledforeground="#a3a3a3")
        self.removeFavourite.configure(foreground="#000000")
        self.removeFavourite.configure(highlightbackground="#d9d9d9")
        self.removeFavourite.configure(highlightcolor="black")
        self._img9 = tk.PhotoImage(file="./icons/broken-heart.png")
        self.removeFavourite.configure(image=self._img9)
        self.removeFavourite.configure(pady="0")
        self.removeFavourite.configure(text='''Button''')
        self.removeFavourite.configure(width=48)

        self.loadFavourite = tk.Button(top)
        self.loadFavourite.place(relx=0.83, rely=0.932, height=26, width=26)
        self.loadFavourite.configure(activebackground="#ececec")
        self.loadFavourite.configure(activeforeground="#000000")
        self.loadFavourite.configure(background="#d9d9d9")
        self.loadFavourite.configure(borderwidth="0")
        self.loadFavourite.configure(disabledforeground="#a3a3a3")
        self.loadFavourite.configure(foreground="#000000")
        self.loadFavourite.configure(highlightbackground="#d9d9d9")
        self.loadFavourite.configure(highlightcolor="black")
        self._img10 = tk.PhotoImage(file="./icons/refresh.png")
        self.loadFavourite.configure(image=self._img10)
        self.loadFavourite.configure(pady="0")
        self.loadFavourite.configure(text='''Button''')
        self.setup_player()

    def setup_player(self):
        try:
            self.my_player = Player.Player()
            if self.my_player.get_db_status():
                #messagebox.showinfo("Success!", "Connected successfully to the DataBase")
                pass
            else:
                raise Exception("Sorry! you cannot save or load favourites")
            self.addFavourite.config(command = self.add_song_to_favourites)
            self.loadFavourite.config(command=self.load_songs_from_favourites)
            self.removeFavourite.config(command=self.remove_song_from_favourites)
        except Exception as ex:
            messagebox.showerror("Error", ex)
            self.addFavourite.config(state="disabled")
            self.removeFavourite.config(state="disabled")
            self.loadFavourite.config(state="disabled")


        self.vol_scale.config(from_=0, to=100, command=self.change_volume)
        self.vol_scale.set(50)
        self.addSongsToPlayListButton.config(command=self.add_song)
        self.deleteSongsFromPlaylistButton.config(command=self.remove_song)
        self.playButton.config(command=self.play_song_from_button)
        self.previousButton.config(command=self.play_previous_song)
        self.pauseButton.config(command=self.pause_song)
        self.stopButton.config(command=self.stop_song)
        # self.playList.config(font="Vivaldi 12")
        self.playList.config(font=("Segoe Script", 12, "bold"))
        self.playList.bind("<Double-1>", self.list_double_click)
        self.top.title("MOUZIKKA-Dance To The Rhythm Of Your Heart!")
        img = tk.PhotoImage(file="./icons/musicicon.png")
        self.top.iconphoto(self.top, img)
        self.top.protocol("WM_DELETE_WINDOW", self.close_window)
        self.isPlaying = False
        self.isPaused = False
        self.my_thread = None
        self.isThreadRunning = False
        self.stopThread = False

    def change_volume(self, volume_level):
        volume_level = float(volume_level)/100
        print("volume level", volume_level)
        self.my_player.set_volume(volume_level)

    def add_song(self):
        song_name = self.my_player.add_song()
        if song_name is None:
            return
        else:
            count = 0
            for song in song_name:
                if song.find("already") != -1:
                    count+=1
                    if count ==1:
                        messagebox.showinfo("song present", "song is already present")
                else:
                    self.playList.insert(tk.END, song)
        color = lambda : random.randint(0, 255)
        red = hex(color())[2:]
        green = hex(color())[2:]
        blue = hex(color())[2:]
        if len(red) == 1:
            red = '0'+red
        if len(green) == 1:
            green = '0'+green
        if len(blue) == 1:
            blue = '0'+blue
        self.playList.config(fg='#'+red+green+blue)

    def remove_song(self):
        song_tuple = self.playList.curselection()
        try:
            if len(song_tuple) == 0:
                raise NoSongSelectedError("Song has not been selected!!")
            song_name = self.playList.get(song_tuple[0])
            # print(self.song_name)
            self.playList.delete(song_tuple[0])
            self.my_player.remove_song(song_name)
            if hasattr(self, 'song_name') == True:
                if song_name == self.song_name:
                    mixer.music.stop()
                    self.stopThread = True
                    self.isThreadRunning = False
                    self.isPaused = False
        except NoSongSelectedError as ex:
            messagebox.showerror("Error!", ex)

    def show_song_details(self):
        self.song_length = int(self.my_player.get_song_length(self.song_name))
        min, sec = divmod(self.song_length, 60)
        #min = round(min)
        #sec = round(sec)

        self.songTotalDuration.config(text=str(min)+":"+str(sec))
        self.songTimePassed.config(text="0:0")
        ext_index = self.song_name.rfind(".")
        ext_str = self.song_name[0:ext_index]
        if len(ext_str) > 14:
            ext_str = ext_str[0:14]+". . ."
        self.songName.config(text=ext_str)

    def play_song_from_button(self):
        if self.isThreadRunning == True:
            self.stopThread = True
        self.play_song()

    def play_song(self):
        if self.isThreadRunning == True:
            mixer.music.stop()
            self.isPaused = False
            self.isThreadRunning = False
            self.isPlaying = False
            #time.sleep(1)
        self.song_tuple = self.playList.curselection()
        try:
            if len(self.song_tuple) == 0:
                raise NoSongSelectedError("Song has not been selected!!")
            self.song_name = self.playList.get(self.song_tuple[0])
            #print(self.song_name)
            self.show_song_details()
            self.my_player.play_song()
            self.vol_scale.set(self.vol_scale.get())
            self.songProgress.config(length=self.song_length)
            self.songProgress.config(maximum=self.song_length)
            self.setup_thread()
            print(self.song_name)
            print(type(self.song_name))
            #self.isPaused  = False
        except NoSongSelectedError as ex:
            messagebox.showerror("Error!", ex)
        #print(self.playList.size())
        #print(type(self.playList.size()))

    def setup_thread(self):
        self.my_thread = threading.Thread(target=self.show_timer, args=(self.song_length,)) # args can be drop
        print(self.song_length)
        self.isPlaying = True
        self.isThreadRunning = True
        self.progress_scale.config(from_=0, to=self.song_length, command=self.drag_song)
        self.progress_scale.set(0)
        self.my_thread.start()

    def drag_song(self, song_level):
        # print("song level", float(song_level))
        # min,sec = divmod(float(song_level),60)
        # total_seconds = (min*60)+sec
        # print("seconds",total_seconds)
        total_seconds = int(float(song_level)) # song_level is str so we have converted into int
        print("seconds", total_seconds)
        self.curr_sec = total_seconds
        # print(total_seconds1)
        self.my_player.set_song_pos(total_seconds)


    def show_timer(self, total_length):
        self.curr_sec = 0
        self.songProgress.stop()
        while self.curr_sec <= total_length:
            min,sec = divmod(self.curr_sec,60)
            self.songTimePassed.config(text=str(min)+":"+str(sec))
            self.progress_scale.set(self.curr_sec) # we have written here so that play_next_song() should play smoothly
            time.sleep(1)
            if self.isPaused == True:
                continue
            self.curr_sec+=1
            if self.stopThread == True:
                break
            self.songProgress.step()

        print("thread terminated")
        if self.stopThread == False:
            self.play_next_song()
        else:
            self.stopThread = False

    def play_next_song(self):
            data = (self.song_tuple[0])+1
            #print(data)
            if data == self.my_player.get_song_count():
                data = 0
            # print(self.playList.size())
            # print(type(self.playList.size()))
            #self.song_tuple = (data,)
            self.playList.select_clear(0, tk.END)        #  we can also use selection_clear(), it takes the current index which has to be cleared
            self.playList.selection_set(data)
            self.play_song()


    def play_previous_song(self):
        try:
            if not hasattr(self, 'song_tuple'):
                raise NoSongSelectedError("Song has not been selected!!")
            data = (self.song_tuple[0])-1
            #print(data)
            if data < 0:
                data = self.my_player.get_song_count()-1
            # print(self.playList.size())
            # print(type(self.playList.size()))
            #self.song_tuple = (data,)
            self.playList.select_clear(0, tk.END)        #  we can also use selection_clear(), it takes the current index which has to be cleared
            self.playList.selection_set(data)
            if self.isThreadRunning == True:
                self.stopThread = True
            self.play_song()
        except NoSongSelectedError as ex:
            messagebox.showerror("Error!", ex)

    def pause_song(self):
        if self.isPlaying:
            if self.isPaused:
                self.my_player.unpause_song()
                self.isPaused = False
            else:
                self.my_player.pause_song()
                self.isPaused = True

    def stop_song(self):
        if self.isThreadRunning == True:
            self.stopThread = True
            self.isPaused = False
            self.isThreadRunning = False
        self.my_player.stop_song()
        self.isPlaying = False

    def list_double_click(self, e):
        if self.isThreadRunning == True:
            self.stopThread = True
        self.play_song()

    def close_window(self):
        ans = messagebox.askyesno("App Closing!!", "Do you want to Quit?")
        if (ans):
            self.isPaused = False
            self.stopThread = True
            self.my_player.close_player()
            messagebox.showinfo("Have a good day!!", "Thankyou for using \"MOUZIKKA\" ")
            self.top.destroy()

    def add_song_to_favourites(self):
        song_tuple = self.playList.curselection()
        try:
            if len(song_tuple) == 0:
                raise NoSongSelectedError("Song has not been selected!!")
            song_name = self.playList.get(song_tuple[0])
            result = self.my_player.add_song_to_favourites(song_name)
            messagebox.showinfo("Success!", result)
        except NoSongSelectedError as ex1:
            messagebox.showerror("Error!", ex1)
        except DatabaseError as ex2:
            messagebox.showerror("DB Error!", "Song cannot be added")
            print(traceback.format_exc())

    def load_songs_from_favourites(self):
        try:
            load_result = self.my_player.load_songs_from_favourites()
            result = load_result[0]
            if result.find("No songs present") != -1:
                messagebox.showinfo("Favourites empty!", "No songs present in your favourites")
                return
            self.playList.delete(0, tk.END)
            song_dict = load_result[1]
            for song_name in song_dict:
                self.playList.insert(tk.END, song_name)
            color = lambda: random.randint(0, 255)
            red = hex(color())[2:]
            green = hex(color())[2:]
            blue = hex(color())[2:]
            if len(red) == 1:
                red = '0' + red
            if len(green) == 1:
                green = '0' + green
            if len(blue) == 1:
                blue = '0' + blue
            self.playList.config(fg='#' + red + green + blue)
            messagebox.showinfo("Favourites loaded!", "List populated from the favourites")
        except DatabaseError as ex2:
            messagebox.showerror("DB Error!", "Songs cannot be loaded")
            print(traceback.format_exc())

    def remove_song_from_favourites(self):
        song_tuple = self.playList.curselection()
        try:
            if len(song_tuple) == 0:
                raise NoSongSelectedError("Song has not been selected!!")
            song_name = self.playList.get(song_tuple[0])
            result = self.my_player.remove_song_from_favourites(song_name)
            if result.find("not present") != -1:
                messagebox.showinfo("Song not present!", "Song not present in your favourites")
                return
            self.playList.delete(song_tuple[0])
            print(song_name)
            if hasattr(self, 'song_name') == True:
                if song_name == self.song_name:
                    mixer.music.stop()
                    self.stopThread = True
                    self.isThreadRunning = False
            messagebox.showinfo("Success!", "Song deleted from your favourites")
        except NoSongSelectedError as ex1:
            messagebox.showerror("Error!", ex1)
        except DatabaseError as ex2:
            messagebox.showerror("DB Error!", "Song cannot be deleted")
            print(traceback.format_exc())

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, tk.Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')

if __name__ == '__main__':
    vp_start_gui()





