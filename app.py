from flask import Flask, request, jsonify
from pytube import YouTube
import threading
from flask_cors import CORS 
import os

app = Flask(__name__)
CORS(app)

def download_audio(current_url):
    with app.app_context():
        try:
            print("Started")
            video = YouTube(current_url)
            os_path = video.streams.filter(only_audio=True).first().download(output_path="C:\\Users\\chris\\Music\\Music Downloaded\\")
            new_name = os.path.splitext(os_path)
            os.rename(os_path, new_name[0] + '.mp3')
            print(new_name)
            print("Download Complete")
            return jsonify("Download Complete"), 200
        
        except Exception as error:
            if 'regex_search' in str(error):
                return jsonify("Invalid URL"), 400
            elif 'getaddrinfo failed' in str(error):
                return jsonify("Connect to Internet"), 500
            else:
                print(error)
                return jsonify(f"An error occurred: {error}"), 500

def download_video(current_url):
    with app.app_context():
        try:
            print("Started video download")
            video = YouTube(current_url)
            video_stream = video.streams.filter(file_extension='mp4').first()
            os_path = video_stream.download(output_path="C:\\Users\\Christin\\Videos\\Videos Downloaded\\")
            print("Video Download Complete")
            return jsonify("Video Download Complete"), 200
        
        except Exception as error:
            if 'regex_search' in str(error):
                return jsonify("Invalid URL"), 400
            elif 'getaddrinfo failed' in str(error):
                return jsonify("Connect to Internet"), 500
            else:
                return jsonify(f"An error occurred: {error}"), 500
            
@app.route("/")
def home_page():
    return "Server Started"

@app.route("/api/music", methods=['POST'])
def download_music():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify("Invalid JSON data"), 400

        current_url = data['url']
        thread = threading.Thread(target=download_audio, args=(current_url,))
        thread.start()

        return jsonify("Download started"), 200
    except Exception as error:
        return jsonify(error), 500

@app.route("/api/video", methods=['POST'])
def download_video_route():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify("Invalid JSON data"), 400

        current_url = data['url']
        thread = threading.Thread(target=download_video, args=(current_url,))
        thread.start()

        return jsonify("Video Download started"), 200
    except Exception as error:
        return jsonify(error), 500
    
        
if __name__ == "__main__":
    app.run(debug=True, port=9000)
