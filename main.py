import requests
from bs4 import BeautifulSoup
import tkinter as tk

# URL der Website
url = "https://quota.wohnheim.uni-kl.de/"

# HTML-Text der Website abrufen
response = requests.get(url)
html = response.text

# BeautifulSoup-Objekt erstellen
soup = BeautifulSoup(html, "html.parser")

# Tabelle mit der Klasse "greyBox" finden
table = soup.find("table", {"class": "greyBox"})

# Tabellenzeilen und Spalten extrahieren
rows = table.find_all("tr")
data = []
for row in rows:
    cols = row.find_all("td")
    row_data = []
    for col in cols:
        row_data.append(col.text.strip())
    data.append(row_data)


# Tkinter-Fenster erstellen
root = tk.Tk()
root.title("Tabelle extrahieren")

# Textfeld erstellen
text = tk.Text(root)
text.pack()

# Daten in Textfeld einfügen
for row in data:
    text.insert(tk.END, "\t".join(row) + "\n")

# Fenster öffnen
root.mainloop()
