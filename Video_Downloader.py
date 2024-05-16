from pytube import YouTube

def download_video(current_url):
    print("Started video download")
    video = YouTube(current_url)
    video_stream = video.streams.filter(file_extension='mp4').order_by('abr').desc().first()
    os_path = video_stream.download(output_path="C:\\Users\\chris\\Videos\\Tutorials")
    print(os_path)

