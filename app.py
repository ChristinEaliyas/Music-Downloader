from flask import Flask, request, jsonify
from pytube import YouTube
from flask_cors import CORS
import os
import json
import threading

app = Flask(__name__)
CORS(app)

DIRECTORY = "C:\\Users\\chris\Music\\"
WORKING_DIRECTORY = "C:\\Users\\chris\Music\\Music"
FILE_PATH = "Playlist.json"


def get_title(url):
    try:
        title = YouTube(url).title
        return title, 200
    except Exception as error:
        if 'regex_search' in str(error):
            return "Invalid URL",
        elif 'getaddrinfo failed' in str(error):
            return "Connect to Internet", 602
        else:
            print(error)
            return "An error occurred", 603

# -----  Music Downloader -----
def download_audio(current_url):
    with app.app_context():
        try:
            filenames = [os.path.splitext(f)[0] for f in os.listdir(WORKING_DIRECTORY) if os.path.isfile(os.path.join(WORKING_DIRECTORY, f))]
            video = YouTube(current_url)
            if video.title not in filenames:
                audio_stream = video.streams.filter(only_audio=True).order_by('abr').desc().first()
                os_path = audio_stream.download(output_path=WORKING_DIRECTORY)
                new_name = os.path.splitext(os_path)
                os.rename(os_path, new_name[0] + '.mp3')
                print("Downloaded " + str(new_name))
            else:
                print(video.title + " is already downloaded")
            return jsonify("Download Complete"), 200
        
        except Exception as error:
            print(error)
            return jsonify(f"An error occurred: {error}"), 500

# ----- Video Downloader ----
def download_video(current_url):
    with app.app_context():
        try:
            filenames = [os.path.splitext(f)[0] for f in os.listdir(WORKING_DIRECTORY) if os.path.isfile(os.path.join(WORKING_DIRECTORY, f))]
            video = YouTube(current_url)
            if video.title not in filenames:
                video_stream = video.streams.filter(file_extension='mp4').order_by('abr').desc().first()
                video_stream.download(output_path="C:\\Users\\chris\\Videos\\Tutorials")
                print("Completed"+video.title)
                return jsonify("Video Download Complete"), 200
            else:
                return jsonify("Video Already Existin"), 200
        except Exception as error:
            print(error)
            return jsonify(f"An error occurred: {error}"), 500
            
@app.route("/")
def home_page():
    return "Server Running"


@app.route("/api/music", methods=['POST'])
def download_music_route():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify("Invalid JSON data"), 400

        current_url = data['url']
        video_title = get_title(current_url)
        if video_title[1] == 200:
            thread = threading.Thread(target=download_audio, args=(current_url,))
            thread.start()
            return jsonify("Downloding Song "+video_title[0]), 200
        else:
            return jsonify(video_title[0]), 400
        # return jsonify("Server Error"), 400
    except Exception as error:
        return jsonify(error), 500

@app.route("/api/video", methods=['POST'])
def download_video_route():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify("Invalid JSON data"), 400

        current_url = data['url']
        video_title = get_title(current_url)
        if video_title[1] == 200:
            thread = threading.Thread(target=download_video, args=(current_url,))
            thread.start()
            return jsonify("Downloading Video: "+video_title[0]), 200
        else:
            return jsonify(video_title[0]), 400
        # return jsonify("Server Error"), 400
    except Exception as error:
        return jsonify(error), 500

@app.route("/api/addToList", methods=['POST'])
def save_url_route():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify("Invalid JSON data"), 400
        video_title = get_title(data['url'])
        if video_title[1] == 200:

            with open(FILE_PATH, 'r') as file:
                playlist_links = json.load(file)

            if data['url'] not in playlist_links["urls"]:
                playlist_links["urls"].append(data['url'])
            else:
                return jsonify("Url is Already in Queue"), 301

            with open(FILE_PATH, 'w') as file:
                json.dump(playlist_links, file, indent=4)

            return jsonify(video_title[0]+" Added To Queue"), 200
        else:
            return jsonify(video_title[0]), 400
    except Exception as error:
        return jsonify(error), 500

            

@app.route("/api/downloadQueue", methods=['POST'])
def download_queue_route():
    try:
        queue = []
        with open(FILE_PATH, 'r') as file:
            playlist_links = json.load(file)
        
        for i in range(0, len(playlist_links["urls"])):
            status = download_video(playlist_links["urls"][i])

            if status[1] == 200 or status[1] == 400:
                queue.append(playlist_links["urls"][i])

        for url in queue:
            playlist_links["urls"].remove(url)

        with open(FILE_PATH, 'w') as file:
            json.dump(playlist_links, file, indent=4)
        return jsonify("Queue Download Complete"), 200
    except Exception as error:
        return jsonify(error), 500
    
@app.route("/api/changeDirecotory", methods=['POST'])
def change_directory_route():
    try:
        data = request.get_json()
        WORKING_DIRECTORY = DIRECTORY + data['Directory']
        print(WORKING_DIRECTORY)
        
        return jsonify("Directory Changed to " + data['Directory']), 200
    except Exception as error:
        print(error)
        return jsonify(error), 500
    
        
if __name__ == "__main__":
    app.run(debug=True, port=9000)