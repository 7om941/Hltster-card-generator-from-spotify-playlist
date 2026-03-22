This program generates a print-ready PDF file containing cards similar to the game HITSTER (text and QR codes). It uses a Spotify playlist as input.

To use the code, you need access to the Spotify API:
Go to https://developer.spotify.com --> log in with your Spotify account --> “Create App”
--> Enter a name and description; recommended redirect URI: http://127.0.0.1:8888 (for authentication)
--> You will now see your Client ID and Client Secret, which you must enter in hitster.py


Hltster.py consists of three cells:
1. Select the card parameters, such as size, text color, and font size. You can also simply use the default settings
2. Displays a preview of what a card will look like with the current settings
3. Creates the print-ready PDF file in a new subfolder named “print_pdf”. The input is a link to a Spotify playlist that YOU OWN.
This API access does not have permission for playlists that you do not own. However, you can easily copy any public playlist as your own:
Open a public playlist in Spotify --> click the three dots --> Add to a playlist --> New playlist
Here’s how to get the link for a Spotify playlist: Open the playlist in Spotify --> click the three dots --> Share --> Copy playlist link



The PDF is formatted so that when printed double-sided with mirroring along the long edge, the QR codes appear below the corresponding text.

Scan the QR codes using a standard QR code scanner app, not the Hitster app.

Enjoy!
