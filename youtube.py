import subprocess
from os import remove as delete
import PySimpleGUI as sg
from PIL import Image

from urllib.parse import urlparse, parse_qs
import urllib.request as request

# really simple and also kinda broken gui for yt-dlp

sg.theme('DarkGrey4')

url_section = [
    [sg.Text('URL '), sg.In(size=(25, 1), key='-URL-'), sg.Button('Load', key='-LOAD-')], 
]

preview_section = [
    [sg.Text('Thumbnail Preview')],
    [sg.Image(key='-PREVIEW-', size=(50, 50))],
    [sg.Text('Save Location ', key='-SAVE_TEXT-', visible=False), sg.In(size=(25, 1), key='-LOCATION-', visible=False, enable_events=True), sg.FolderBrowse(visible=False, key='-BROWSE-', target='-LOCATION-', enable_events=True)],
    [sg.Button('Download', key='-DOWNLOAD-', visible=False)]
]

menu_def = [
    ['&Help', ['&How to Use', '&About']]
]

layout = [
    [sg.Menu(menu_def)],
    [
        sg.Column(url_section, element_justification='right'),
        sg.VSeparator(),
        sg.Column(preview_section, element_justification='right')
    ]
]

window = sg.Window('Youtube to MP3', layout, margins=(10, 10))

# important functions

def get_video_id(url):
    query = urlparse(url)
    return parse_qs(query.query)['v'][0]

def download_video(location, url):
    subprocess.run(f'yt-dlp --extract-audio --audio-format mp3 "{url}" --no-progress -o "{location}/%(title)s.%(ext)s"')

def get_thumbnail(url):
    request.urlretrieve(url, '.tempimg')
    img = Image.open('.tempimg').resize([300, 200])
    img.save('.tempimg', 'PNG')
    return '.tempimg'

browse_flag = False

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    
    if event == '-LOAD-':

        video_url = values['-URL-']

        window['-PREVIEW-'].Update(filename=get_thumbnail(f'https://img.youtube.com/vi/{get_video_id(video_url)}/0.jpg'), subsample=2)
        delete('.tempimg')

        window['-BROWSE-'].Update(visible=True)

    if event == '-LOCATION-':
        window['-DOWNLOAD-'].Update(visible=True)

    if event == '-DOWNLOAD-':
        download_video(values['-LOCATION-'], values['-URL-'])

        
