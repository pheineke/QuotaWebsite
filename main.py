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

        table_content = table_content.replace("\n", "")

        replacements = [("Quotierungszeitraum:", "\nQuotierungszeitraum:\n"),
                ("zugewiesene IP:", "\nzugewiesene IP:\n"),
                ("(", "\n("),
                ("VerbrauchLimit", "\nVerbrauch Limit\n"),
                ("Download:", "|  Download:    "),
                ("Upload:", "|    Upload:    "),
                ("30 GiB", " von 30 GiB\n"),
                ("B0%", "B\n"),
                ("100%", "\n"),
                ("Stand der Datenbank:\n", "\nStand der Datenbank:\n"),
                ("Quotierungszeit:", "\nQuotierungszeit:\n"),
                ("Stand der Datenbank:", "Stand der Datenbank:\n"),
                ("Status wird nicht in Echtzeit aktualisiert!", "\n\nStatus wird nicht in Echtzeit aktualisiert!\n")]

        for old, new in replacements:
            table_content = table_content.replace(old, new)
        

        tbl = table_content.split("0%")
        tbl[1].replace("|  Download:    ", "")
        tbl[1].replace("|  Upload:    ", "")
        tbl[1] = "\n" + tbl[1]
        table_content = tbl[0] + tbl[1][32:]

        tabless = table_content.split("!")
        table_content = tabless[0] + tabless[1]

    else:
        table_content = "Keine Tabelle gefunden."
    return table_content
 


root = tk.Tk()
root.title("Wohnheim - Quota")

text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="black", fg="white")
text_widget.pack(fill=tk.BOTH, expand=True)

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
