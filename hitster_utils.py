# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 22:15:29 2026

@author: tom
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import qrcode
from PIL import Image, ImageDraw, ImageFont
import math
import re
import numpy as np
import os
import json

script_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_folder)


with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

cid = config['cid']
secret = config['secret']
redirect_uri = config['redirect_uri']
cm_size = config['cm_size']
qr_color = config['qr_color']
color = config['color']
Schriftgröße = config['Font_size']
Abstand = config['Spacing']
Schriftart = config['Font']
Liederlimit = config['songlimit']
dpi = config['dpi']


pixel_size = int(cm_size * dpi / 2.54)



def create_document(images, reverse=False):   

    per_row = math.floor(21/cm_size)
    per_col = math.floor(29.7/cm_size)
    
    images_per_page = per_row * per_col
    img_width, img_height = images[0].size  # Annahme: alle Bilder gleich groß

    page_count = math.ceil(len(images) / images_per_page)

    files = []
    
    
    for p in range(page_count):
        page_images = images[p*images_per_page : (p+1)*images_per_page]

        # Neues Rasterbild für die Seite
        page_img = Image.new("RGB", (per_row*img_width, per_col*img_height), "white")

        for idx, img in enumerate(page_images):
            row = idx // per_row
            col = idx % per_row
            if reverse == False:
                x = col * img_width
            if reverse == True:
                x = (per_row - 1 - col) * img_width
            y = row * img_height
            page_img.paste(img, (x, y))
        
        files.append(page_img)
    return files
    
    
    
def merge_documents_to_pdf(text_files, qr_files, output_pdf):
    if len(text_files) != len(qr_files):
        raise ValueError("Text- und QR-Ordner müssen die gleiche Anzahl Dateien enthalten!")

    # Sicherstellen, dass der Ordner existiert
    output_dir = os.path.dirname(output_pdf)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Seiten abwechselnd kombinieren
    pages = [elem for pair in zip(text_files, qr_files) for elem in pair]

    # Erste Seite als Basis, die restlichen anhängen
    first_page = pages[0]
    rest_pages = pages[1:]

    # PDF speichern
    first_page.save(output_pdf, save_all=True, append_images=rest_pages)
    print(f"PDF erstellt: {output_pdf}")
    
    
    
    


def QR_code(Link, fill_color=qr_color, back_color="white", Länge_Breite = pixel_size):
    qr = qrcode.QRCode(
    version=1,  # Größe des QR-Codes (1 = klein)
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    
    qr.add_data(Link)
    qr.make(fit=True)
    
    # Bild generieren
    img_qr = qr.make_image(fill_color=fill_color, back_color=back_color)
    img_qr = img_qr.resize((Länge_Breite, Länge_Breite), Image.NEAREST)
    return img_qr


def Klammer_Zeilenumbruch(Input):
    parts = re.findall(r'\([^)]*\)|[^()]+', Input)
    return [p.strip() for p in parts if p.strip()]

def Text_Bild_inputs(Interpret, Jahr, Titel):
    lines = []
    colors = []
    font_sizes = []
    line_spacings = []

    # Künstler
    k = -1
    for i, name in enumerate(Interpret):
        parts = Klammer_Zeilenumbruch(name)
        for j, part in enumerate(parts):
            lines.append(part)
            colors.append(color[0])
            font_sizes.append(Schriftgröße[0])
            k=k+1
    if k>0:
        line_spacings.extend(np.full(k, 10))
    line_spacings.append(Abstand[0])

    # Jahr
    lines.append(Jahr)
    colors.append(color[1])
    font_sizes.append(Schriftgröße[1])
    line_spacings.append(Abstand[1])

    # Titel
    titel_parts = Klammer_Zeilenumbruch(Titel)
    for i, part in enumerate(titel_parts):
        lines.append(part)
        colors.append(color[2])
        font_sizes.append(Schriftgröße[2])
        k=i
    if k>0:
        line_spacings.extend(np.full(k, 10))
    line_spacings.append(0)


    return lines, colors, font_sizes, line_spacings


def Text_Bild_erstellen(lines, colors, font_sizes, line_spacings, color=color, Schriftart=Schriftart):
    # Bild erstellen
    img = Image.new("RGB", (pixel_size, pixel_size), color="white")
    draw = ImageDraw.Draw(img)

    # Fonts erstellen + automatisch anpassen
    fonts = []
    for i, size in enumerate(font_sizes):
        try:
            font = ImageFont.truetype(Schriftart, size)
        except:
            font = ImageFont.load_default()

        #  Schriftgröße anpassen, falls zu breit
        while True:
            bbox = draw.textbbox((0, 0), lines[i], font=font)
            text_width = bbox[2] - bbox[0]

            if text_width <= 0.95 * pixel_size:
                break

            new_size = max(1, int(font.size * 0.95))

            if new_size == font.size:
                break  # verhindert Endlosschleife

            try:
                font = ImageFont.truetype(Schriftart, new_size)
            except:
                font = ImageFont.load_default()
                break

        fonts.append(font)

    #  Gesamthöhe berechnen (nach Skalierung!)
    total_height = 0
    text_heights = []

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=fonts[i])
        text_height = bbox[3] - bbox[1]
        text_heights.append(text_height)
        total_height += text_height + line_spacings[i]

    total_height -= line_spacings[-1]

    # Vertikal zentrieren
    y_text = (pixel_size - total_height) // 2

    #  Text zeichnen
    for i, line in enumerate(lines):
        font = fonts[i]
        bbox = draw.textbbox((0, 0), line, font=font)

        text_width = bbox[2] - bbox[0]
        text_height = text_heights[i]

        x_text = (pixel_size - text_width) // 2

        draw.text((x_text, y_text), line, font=font, fill=colors[i])

        y_text += text_height + line_spacings[i]

    return img



def create_print_pdf(playlist_link, Liederlimit = Liederlimit):
    all_tracks = []
    limit = 100
    offset = 0
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=cid,
        client_secret=secret,
        redirect_uri=redirect_uri,
        #cope="playlist-read-private",
        #scope = "playlist-read-collaborative",
        scope="playlist-read-private playlist-read-collaborative",
        cache_path='hitster_cache.txt'
    ))

    
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    

    
    while True:
        results = sp.playlist_tracks(playlist_URI, limit=limit, offset=offset)
        songs = results['items']
        all_tracks.extend(songs)
    
        if results['next'] is None or len(all_tracks) >= Liederlimit:
            break
    
        offset += limit
    
    print(f"Tracks geladen: {len(all_tracks)}")
    
    
    
    playlist = sp.playlist(playlist_URI)
    playlist_name = playlist['name']
    
    text_images = []
    qr_images = []
    
    for i in range(0, len(all_tracks)):
        Jahr = all_tracks[i]['item']['album']['release_date'][:4]
        
        #möglichkeit mehrerer Interpreten        
        Interpret = [artist['name'] for artist in all_tracks[i]['item']['album']['artists']]
        Titel = all_tracks[i]['item']['name']
        Link = all_tracks[i]['item']['external_urls']['spotify']
    
    
        img_qr = QR_code(Link, fill_color=qr_color)
        lines, colors, font_sizes, line_spacings = Text_Bild_inputs(Interpret, Jahr, Titel)
        img_text = Text_Bild_erstellen(lines, colors, font_sizes, line_spacings, color=color, Schriftart=Schriftart)
        
        
        text_images.append(img_text)
        qr_images.append(img_qr)
    
    
    text_files = create_document(text_images,  reverse=True)
    qr_files = create_document(qr_images, reverse=False)  
    
    merge_documents_to_pdf(text_files, qr_files, "print_pdf/" + playlist_name + ".pdf")
    
    return playlist_name, len(all_tracks)