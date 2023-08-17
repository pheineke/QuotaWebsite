import tkinter as tk
from tkinter import scrolledtext, colorchooser
import requests
from bs4 import BeautifulSoup
from functools import reduce

def remove_duplicates(input_str):
    words = input_str.split(" ")
    unique_words = reduce(lambda x, y: x if y in x else x + [y], [[], ] + words)
    return ' '.join(unique_words)

def get_table_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if table:
        rows = table.find_all('tr')
        table_content = "\n".join([row.get_text(strip=True) for row in rows])
        table_content = remove_duplicates(table_content)
        table_content = table_content.replace("Quotierungszeitraum:", "\nQuotierungszeitraum:\n")
        table_content = table_content.replace("zugewiesene IP:", "\nzugewiesene IP:\n")
        table_content = table_content.replace("(", "\n(")
        table_content = table_content.replace("VerbrauchLimit", "\nVerbrauch Limit")
        
        table_content = table_content.replace("Download:", "\nDownload:   ")
        
        table_content = table_content.replace("Upload:", "\nUpload:   ")

        table_content = table_content.replace("MiB", "MiB\n")
        table_content = table_content.replace("GiB", "GiB\n")
        table_content = table_content.replace("Stand der Datenbank:\n", "\nStand der Datenbank:\n")
        table_content = table_content.replace("Quotierungszeit:", "\nQuotierungszeit:\n")
        table_content = table_content.replace("Stand der Datenbank:", "Stand der Datenbank:\n")
        table_content = table_content.replace("Status wird nicht in Echtzeit aktualisiert!", "\nStatus wird nicht in Echtzeit aktualisiert!\n")


        #index = table_content.index("sein!") + (len("sein!")+1)
        #table_content = table_content[index:].strip()
        
        #table_content = remove_duplicates(table_content)
    else:
        table_content = "Keine Tabelle gefunden."
    return table_content
 


# Tkinter GUI
def change_colors():
    bg_color = colorchooser.askcolor()[1]
    text_widget.config(bg=bg_color)
    
    fg_color = get_complementary_color(bg_color)
    text_widget.config(fg=fg_color)

def get_complementary_color(hex_color):
    hex_color = hex_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    inverted_rgb = tuple(255 - value for value in rgb_color)
    complementary_color = '#%02x%02x%02x' % inverted_rgb
    return complementary_color

root = tk.Tk()
root.title("Wohnheim - Quota")

text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_widget.pack(fill=tk.BOTH, expand=True)

change_color_button = tk.Button(root, text="Farben ändern", command=change_colors)
change_color_button.pack()

url = "https://quota.wohnheim.uni-kl.de/"
table_content = get_table_content(url)
text_widget.insert(tk.END, table_content)

# Zentrieren des Texts
text_widget.tag_configure("center", justify="center")
text_widget.tag_add("center", 1.0, "end")

# Anpassen des Fensters an die Inhaltsgröße
content_width = max([len(line) for line in table_content.split("\n")])
content_height = len(table_content.split("\n"))
root.geometry(f"{content_width * 10}x{content_height * 20}")

root.mainloop()