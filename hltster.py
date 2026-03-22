# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:47:59 2026

@author: tom
"""
import json
import os
import importlib
import matplotlib.pyplot as plt

script_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_folder)

import hitster_utils as hu

# Access to Spotify API:
# https://developer.spotify.com --> log in with Spotify account --> "create app"
# --> enter name and description, recommended Redirect URI: http://127.0.0.1:8888 (for authentication)
# --> client id (cid) and Client secret (secret)

config = {
    'cid': <client_id_string>,
    'secret': <client_secret_string>,
    'redirect_uri': <Rederect_URL_string>,
    'cm_size': 5.25, # Length or width of the square cards. (A4: 21 cm x 29.7 cm)
    'qr_color': "black", # Color of the QR codes (background is always white)
    # The text on the cards has the following order from top to bottom: Artist, Year, Title.
    'color': ["black", "red", "black"],  # Text colors in order
    'Font_size': [70, 150, 55], # Font sizes in order
    'Spacing': [100,120], # Spacing between the texts in order
    'Font': "arial.ttf", # Font for all text
    'songlimit': 300, # Maximum number of songs the Spotify playlist can have
    'dpi': 300 # Image resolution
    }


with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=4, ensure_ascii=False)

importlib.reload(hu)
#%% Test if the Text settings work for you!

#Test Text
Test_artist = ["Artist"]
Test_year ="XXXX"
Test_title = "title"


#longer Titles and artist names as reference:
# =============================================================================
# Test_artist = ["why is this so fucking long", "a second artist"]
# Test_year ="XXXX"
# Test_title = "(hello) from the other side (of the side)"
# =============================================================================


color = config['color']
Schriftart = config['Font']
lines, colors, font_sizes, line_spacings = hu.Text_Bild_inputs(Test_artist, Test_year, Test_title)
img = hu.Text_Bild_erstellen(lines, colors, font_sizes, line_spacings)
plt.imshow(img)
plt.axis('off')
plt.show()

#%% create the print ready pdf!

# Insert Spotify link: Open playlist in Spotify --> click on three dots --> Share --> Copy playlist link
# Only your own playlists work!
# To make public playlists your own: open public playlist in Spotify
# --> click on three dots --> Add to a playlist --> new playlist

playlist_link = "https://open.spotify.com/playlist/..."


# Folder "print_pdf" will be created in the same folder as this Python file and
# the print-ready PDF will be saved there
hu.create_print_pdf(playlist_link)

# Double-sided printing with mirroring on the long side!
