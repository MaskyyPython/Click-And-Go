from tkinter import *
from meteo import *
import wikipedia
from PIL import Image, ImageTk
import urllib.request
import io
from serpapi import GoogleSearch

# Fênetre et sa création

api_key = (None, None)
def get_api_key():
    global api_key
    api_key = (api_entry.get(), api_entry2.get())
def show_weather_data():
    city = city_entry.get()
    data = get_weather_data(city, api_key[1])
    if 'weather' in data:
        weather_label.config(text=data['weather'][0]['description'])
        temp_celsius = data['main']['temp'] - 273.15 # conversion en Celsius
        temp_label.config(text=str(round(temp_celsius, 1)) + "°C") # arrondi à 1 décimale
    else:
        weather_label.config(text="Error : city not found")
        temp_label.config(text="")

def show_city_data():
    city = city_entry.get()
    try:
        city_description = wikipedia.summary(city)
        city_text.delete('1.0', END)  # Effacer le contenu précédent
        city_text.insert(END, city_description)
    except:
        city_description = "Error : City not found"
        city_text.delete('1.0', END)  # Effacer le contenu précédent
        city_text.insert(END, city_description)

def show_city_img():
    global image_tk
    city = city_entry.get()
    params = {
      "engine": "yandex_images",
      "text": city,
      "api_key": api_key[0]
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    images_results = results["images_results"]
    image_link = images_results[1]["thumbnail"]
    with urllib.request.urlopen(image_link) as u:
        raw_data = u.read()
        #self.image = tk.PhotoImage(data=base64.encodebytes(raw_data))
    image = Image.open(io.BytesIO(raw_data))
    image = image.resize((500, 500), Image.ANTIALIAS)
    image_tk = ImageTk.PhotoImage(image)
    image_label.config(image=image_tk)


root = Tk()
root.title("Click and Go - W.I.P.")
root.resizable(height=True, width=True)
screen_x = int(root.winfo_screenwidth())
screen_y = int(root.winfo_screenheight())
window_x = screen_x - (screen_x // 4)
window_y = screen_y - (screen_y // 4)

posX = (screen_x // 2) - (window_x // 2)
posY = (screen_y // 2) - (window_y // 2)

geo = "{}x{}+{}+{}".format(window_x, window_y, posX, posY)
root.geometry(geo)

# Définir des couleurs personnalisées pour les éléments de votre interface
primary_color = "#244416"
secondary_color = "#FFFDD0"
accent_color = "#765219"

# Ajouter un Canvas pour gérer le défilement
main_canvas = Canvas(root, bg=primary_color)
main_canvas.pack(side=LEFT, fill=BOTH, expand=True)

# Ajouter une barre de défilement pour le Canvas
main_scrollbar = Scrollbar(root, orient=VERTICAL, command=main_canvas.yview)
main_scrollbar.pack(side=RIGHT, fill=Y)
main_canvas.config(yscrollcommand=main_scrollbar.set)

# Créer un Frame à l'intérieur du Canvas pour contenir tous les widgets
main_frame = Frame(main_canvas, bg=primary_color)
main_canvas.create_window((0, 0), window=main_frame, anchor="nw")

# Fonction pour ajuster la taille du Canvas après ajout des widgets
def update_scroll_region(event):
    main_canvas.config(scrollregion=main_canvas.bbox("all"))

main_frame.bind("<Configure>", update_scroll_region)

# Ajouter les widgets dans le Frame
image_tk = None
welcome_label = Label(main_frame, text="Welcome to Click and Go, the app of the future", font=("Arial", 20), bg=primary_color, fg=secondary_color)
welcome_label.pack(padx=5, pady=5)

# Ajouter une image en haut à gauche
try:
    logo = Image.open("images/henri4.jpg")
    logo = logo.resize((166, 124), Image.ANTIALIAS)

    logo = ImageTk.PhotoImage(logo)
    logo_label = Label(main_frame, image=logo, bg=primary_color)
    logo_label.pack(side=TOP, padx=2, pady=2)
except:
    logo = Label(main_frame, text="Image not found", bg=primary_color, fg=secondary_color)
    logo.pack(padx=10, pady=10)

image_button = Button(main_frame, text="Show the city image", command=show_city_img, font=("Courier", 15), bg=accent_color, fg="white")
image_button.pack()

# Entrée de la ville
city_entry = Entry(main_frame, font=("Courier", 15))
city_entry.pack()

# Bouton pour afficher les données météo
weather_button = Button(main_frame, text="Show the weather", command=show_weather_data, font=("Courier", 15), bg=accent_color, fg="white")
weather_button.pack()

# Labels pour afficher les données météo
weather_label = Label(main_frame, text="", font=("Arial", 18), bg=primary_color, fg=secondary_color)
weather_label.pack()
temp_label = Label(main_frame, text="", font=("Arial", 18), bg=primary_color, fg=secondary_color)
temp_label.pack()

# La présentation de la ville
city_data_button = Button(main_frame, text="Show city's information", command=show_city_data, font=("Courier", 15), bg=accent_color, fg="white")
city_data_button.pack()

# Créer un cadre pour afficher le texte de la ville avec une hauteur réduite
city_frame = Frame(main_frame, bg=primary_color, bd=2, relief="solid", height=200)
city_frame.pack(side=TOP, expand=False, fill=X)

# Ajouter une barre de défilement verticale pour le texte de la ville
scrollbar_city = Scrollbar(city_frame)
scrollbar_city.pack(side=RIGHT, fill=Y)

# Ajouter un widget image pour afficher une image de la ville
blank_image = Image.open("images/blank.png")
blank_image = blank_image.resize((250, 250), Image.ANTIALIAS)
blank_image = ImageTk.PhotoImage(blank_image)
image_label = Label(city_frame, image=blank_image, bg=primary_color)
image_label.pack(side=LEFT)

# Ajouter un widget Text pour afficher le texte de la ville
city_text = Text(city_frame, font=("Arial", 15), wrap=WORD, yscrollcommand=scrollbar_city.set, height=10, bg=primary_color, fg=secondary_color)
city_text.pack(side=LEFT, fill=BOTH, expand=True)

# Lier la barre de défilement au widget Text
scrollbar_city.config(command=city_text.yview)

# API Entry
api_entry = Entry(main_frame, font=("Courier", 15))
api_entry.pack()
api_entry2 = Entry(main_frame, font=("Courier", 15))
api_entry2.pack()
api_key_button = Button(main_frame, text="Get Api", command=get_api_key, font=("Courier", 15), bg=accent_color, fg="white")
api_key_button.pack()


# Lier la barre de défilement à l'ensemble du frame principal
main_canvas.bind_all("<MouseWheel>", lambda event: main_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

# Configurer les couleurs de l'interface
root.configure(bg=primary_color)

root.mainloop()
