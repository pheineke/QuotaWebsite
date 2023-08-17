import tkinter as tk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
from functools import reduce

def remove_duplicates(input_str):
    words = input_str.split()
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
        table_content = table_content.replace("zugewiesene", "\nzugewiesene")
        table_content = table_content.replace("VerbrauchLimit", "\nVerbrauchLimit")
        
        table_content = table_content.replace("Download:", "\nDownload:\n")
        table_content = table_content.replace("Upload:", "\nUpload:\n")
        table_content = table_content.replace("Stand der Datenbank:\n", "\nStand der Datenbank:\n")
    else:
        table_content = "Keine Tabelle gefunden."
    return table_content
 


# Tkinter GUI
root = tk.Tk()
root.title("Inhalt der gescrapten Tabelle von Website")

text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_widget.pack(fill=tk.BOTH, expand=True)

url = "https://quota.wohnheim.uni-kl.de/"
table_content = get_table_content(url)
#table_content = remove_duplicates(table_content)
text_widget.insert(tk.END, table_content)



root.mainloop()