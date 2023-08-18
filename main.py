import tkinter as tk
from tkinter import scrolledtext, colorchooser, ttk
import requests
from bs4 import BeautifulSoup

def remove_duplicates(input_str):
    words = input_str.split(" ")
    unique_words = list(set(words))
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

        size_parts = [part for part in table_content.split() if "MiB" in part or "GiB" in part]

        download_size_parts = [part for part in size_parts if "Download:" in part]
        upload_size_parts = [part for part in size_parts if "Upload:" in part]


        download_size_total = 0
        download_size_current = 0
        for part in download_size_parts:
            if "GiB" in part:
                download_size_total += float(part.replace("GiB", "").replace(",", ".")) * 1024
            elif "MiB" in part:
                download_size_current += float(part.replace("MiB", "").replace(",", "."))

        upload_size_total = 0
        upload_size_current = 0
        for part in upload_size_parts:
            if "GiB/s" in part:
                upload_size_total += float(part.replace("GiB/s", "").replace(",", ".")) * 1024
            elif "MiB/s" in part:
                upload_size_current += float(part.replace("MiB/s", "").replace(",", "."))

        if download_size_total == 0:
            download_percentage = 0
        else:
            download_percentage = (download_size_current / download_size_total) * 100

        if upload_size_total == 0:
            upload_percentage = 0
        else:
            upload_percentage = (upload_size_current / upload_size_total) * 100

        return [download_percentage, upload_percentage]

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Internet Usage")

        self.download_label = tk.Label(self.window, text="Download")
        self.download_label.grid(column=0, row=0)

        self.download_progressbar = ttk.Progressbar(self.window, orient="horizontal", length=200, mode="determinate")
        self.download_progressbar.grid(column=1, row=0)

        self.upload_label = tk.Label(self.window, text="Upload")
        self.upload_label.grid(column=0, row=1)

        self.upload_progressbar = ttk.Progressbar(self.window, orient="horizontal", length=200, mode="determinate")
        self.upload_progressbar.grid(column=1, row=1)

        self.update_progressbars()

        self.window.mainloop()

    def update_progressbars(self):
        progress_values = get_table_content("https://quota.wohnheim.uni-kl.de/")
        if progress_values:
            download_percentage, upload_percentage = progress_values
            self.download_progressbar["value"] = download_percentage
            self.upload_progressbar["value"] = upload_percentage
        self.window.after(10000, self.update_progressbars)

app = App()
