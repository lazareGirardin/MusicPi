from flask import Flask, render_template, request, redirect, url_for, jsonify
#from flask_socketio import SocketIO, emit
import time
from playerClass import PiPlayer, PlaylistLooper
import os


app = Flask(__name__)
#socketio = SocketIO(app)


pi_player = PiPlayer('history.txt', 'playlist.txt')
looper = PlaylistLooper(pi_player)
looper.start()

@app.route('/')
def main_page():
    #songs = pi_player.get_next_song_list(5)
    songs = pi_player.get_all_songs()
    return render_template('test.html', mainPage=True, songs=songs,
                            current=pi_player.get_current_song())

@app.route('/handle_url_entry', methods=['POST'])
def handle_url_entry():
    ytb_url = request.form['link_entry']
    add_entry(ytb_url)
    return redirect(url_for('main_page'))

@app.route('/display_next')
def display_nexts():
    songs = pi_player.get_next_song_list(5)
    return jsonify(songs)


@app.route('/pause_pressed')
def pause_pressed():
    pi_player.set_pause()
    return "nothing"

# @app.route('/next_pressed')
# def next_pressed():
#     pi_player.set_next()
#     songs = pi_player.get_next_song_list(5)
#     value = {}
#     value['now'] = pi_player.now_playing[1]
#     for i in range(5):
#         value[str(i)] = songs[i]
#     return jsonify(value)

@app.route('/next_pressed')
def next_pressed():
    pi_player.set_next()
    songs = pi_player.get_all_songs()
    return render_template('next_songs.html', current=pi_player.now_playing[1], songs=songs)

@app.route('/power_off_pi')
def power_off():
    # add some clean stuff here...
    os.system('shutdown -t now')
    return "Bye Bye"

def add_entry(entry):
    pi_player.add_entry(entry)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    #socketio.run(app, host='0.0.0.0')
