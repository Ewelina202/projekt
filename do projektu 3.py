from tkinter import *
from tkinter import messagebox
import tkintermapview
import requests
from bs4 import BeautifulSoup


# System do zarządzania stacjami radiowymi
# Login: admin
# Hasło: admin

placowki = []
nadajniki = []
pracownicy = []
klienci = []

aktualna_lista = placowki
aktualny_typ = "Placówka"
edytowany_indeks = None


class Obiekt:
    def __init__(self, nazwa, firma, opis, lokalizacja, typ):
        self.nazwa = nazwa
        self.firma = firma
        self.opis = opis
        self.lokalizacja = lokalizacja
        self.typ = typ

        self.coordinates = self.get_coordinates()

        self.marker = map_widget.set_marker(
            self.coordinates[0],
            self.coordinates[1],
            text=self.nazwa
        )

    def get_coordinates(self):
        lokalizacja_url = self.lokalizacja.strip().replace(" ", "_")
        url = f"https://pl.wikipedia.org/wiki/{lokalizacja_url}"

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response_html = BeautifulSoup(response.text, "html.parser")

        latitudes = response_html.select(".latitude")
        longitudes = response_html.select(".longitude")

        if len(latitudes) == 0 or len(longitudes) == 0:
            raise ValueError("Nie znaleziono współrzędnych")

        index = 1 if len(latitudes) > 1 and len(longitudes) > 1 else 0

        latitude = float(latitudes[index].text.replace(",", "."))
        longitude = float(longitudes[index].text.replace(",", "."))

        return [latitude, longitude]


class Klient:
    def __init__(self, nazwa, rozglosnia):
        self.nazwa = nazwa
        self.rozglosnia = rozglosnia


# -------------------- LOGOWANIE --------------------

def zaloguj():
    if entry_login.get() == "admin" and entry_haslo.get() == "admin":
        okno_logowania.destroy()
        pokaz_program()
    else:
        messagebox.showerror("Błąd", "Niepoprawny login lub hasło")


# -------------------- WYBÓR MODUŁU --------------------

def wybierz_placowki():
    global aktualna_lista, aktualny_typ, edytowany_indeks

    aktualna_lista = placowki
    aktualny_typ = "Placówka"
    edytowany_indeks = None

    label_lista.config(text="Lista placówek rozgłośni")
    label_opis.config(text="Adres placówki:")
    button_dodaj.config(text="Dodaj", command=dodaj_obiekt)

    pokaz_liste()
    wyczysc_formularz()


def wybierz_nadajniki():
    global aktualna_lista, aktualny_typ, edytowany_indeks

    aktualna_lista = nadajniki
    aktualny_typ = "Nadajnik"
    edytowany_indeks = None

    label_lista.config(text="Lista nadajników")
    label_opis.config(text="Częstotliwość / opis:")
    button_dodaj.config(text="Dodaj", command=dodaj_obiekt)

    pokaz_liste()
    wyczysc_formularz()


def wybierz_pracownikow():
    global aktualna_lista, aktualny_typ, edytowany_indeks

    aktualna_lista = pracownicy
    aktualny_typ = "Pracownik"
    edytowany_indeks = None

    label_lista.config(text="Lista pracowników")
    label_opis.config(text="Stanowisko:")
    button_dodaj.config(text="Dodaj", command=dodaj_obiekt)

    pokaz_liste()
    wyczysc_formularz()


# -------------------- DODAWANIE, USUWANIE, EDYCJA --------------------

def pokaz_liste():
    listbox_obiekty.delete(0, END)

    for i, obiekt in enumerate(aktualna_lista):
        listbox_obiekty.insert(i, f"{obiekt.nazwa} - {obiekt.firma}")


def dodaj_obiekt():
    nazwa = entry_nazwa.get()
    firma = entry_firma.get()
    opis = entry_opis.get()
    lokalizacja = entry_lokalizacja.get()

    if nazwa == "" or firma == "" or lokalizacja == "":
        messagebox.showwarning(
            "Brak danych",
            "Uzupełnij nazwę, firmę/rozgłośnię i miejscowość"
        )
        return

    try:
        nowy_obiekt = Obiekt(nazwa, firma, opis, lokalizacja, aktualny_typ)
        aktualna_lista.append(nowy_obiekt)

        pokaz_liste()
        wyczysc_formularz()

    except:
        messagebox.showerror(
            "Błąd",
            "Nie udało się pobrać współrzędnych. Sprawdź nazwę miejscowości."
        )


def usun_obiekt():
    zaznaczenie = listbox_obiekty.curselection()

    if not zaznaczenie:
        messagebox.showwarning("Brak wyboru", "Zaznacz obiekt na liście")
        return

    indeks = zaznaczenie[0]

    aktualna_lista[indeks].marker.delete()
    aktualna_lista.pop(indeks)

    pokaz_liste()


def edytuj_obiekt():
    global edytowany_indeks

    zaznaczenie = listbox_obiekty.curselection()

    if not zaznaczenie:
        messagebox.showwarning("Brak wyboru", "Zaznacz obiekt na liście")
        return

    edytowany_indeks = zaznaczenie[0]
    obiekt = aktualna_lista[edytowany_indeks]

    wyczysc_formularz()

    entry_nazwa.insert(0, obiekt.nazwa)
    entry_firma.insert(0, obiekt.firma)
    entry_opis.insert(0, obiekt.opis)
    entry_lokalizacja.insert(0, obiekt.lokalizacja)

    button_dodaj.config(text="Zapisz zmiany", command=zapisz_zmiany)


def zapisz_zmiany():
    global edytowany_indeks

    if edytowany_indeks is None:
        return

    try:
        obiekt = aktualna_lista[edytowany_indeks]

        obiekt.nazwa = entry_nazwa.get()
        obiekt.firma = entry_firma.get()
        obiekt.opis = entry_opis.get()
        obiekt.lokalizacja = entry_lokalizacja.get()

        obiekt.coordinates = obiekt.get_coordinates()

        obiekt.marker.delete()
        obiekt.marker = map_widget.set_marker(
            obiekt.coordinates[0],
            obiekt.coordinates[1],
            text=obiekt.nazwa
        )

        edytowany_indeks = None
        button_dodaj.config(text="Dodaj", command=dodaj_obiekt)

        pokaz_liste()
        wyczysc_formularz()

    except:
        messagebox.showerror(
            "Błąd",
            "Nie udało się zapisać zmian. Sprawdź nazwę miejscowości."
        )


def pokaz_szczegoly():
    zaznaczenie = listbox_obiekty.curselection()

    if not zaznaczenie:
        messagebox.showwarning("Brak wyboru", "Zaznacz obiekt na liście")
        return

    indeks = zaznaczenie[0]
    obiekt = aktualna_lista[indeks]

    label_szczegoly.config(
        text=f"Typ: {obiekt.typ}\n"
             f"Nazwa: {obiekt.nazwa}\n"
             f"Firma / rozgłośnia: {obiekt.firma}\n"
             f"Opis: {obiekt.opis}\n"
             f"Miejscowość: {obiekt.lokalizacja}\n"
             f"Współrzędne: {obiekt.coordinates[0]}, {obiekt.coordinates[1]}"
    )

    map_widget.set_position(obiekt.coordinates[0], obiekt.coordinates[1])
    map_widget.set_zoom(13)


def wyczysc_formularz():
    entry_nazwa.delete(0, END)
    entry_firma.delete(0, END)
    entry_opis.delete(0, END)
    entry_lokalizacja.delete(0, END)


# -------------------- KLIENCI ROZGŁOŚNI --------------------

def dodaj_klienta():
    nazwa = entry_klient.get()
    rozglosnia = entry_klient_rozglosnia.get()

    if nazwa == "" or rozglosnia == "":
        messagebox.showwarning("Brak danych", "Podaj nazwę klienta i rozgłośnię")
        return

    klienci.append(Klient(nazwa, rozglosnia))

    entry_klient.delete(0, END)
    entry_klient_rozglosnia.delete(0, END)

    pokaz_klientow()


def pokaz_klientow():
    listbox_klienci.delete(0, END)

    szukana_rozglosnia = entry_szukaj_klientow.get()

    for klient in klienci:
        if szukana_rozglosnia == "" or klient.rozglosnia == szukana_rozglosnia:
            listbox_klienci.insert(END, f"{klient.nazwa} - {klient.rozglosnia}")


# -------------------- PRACOWNICY WYBRANEJ FIRMY --------------------

def pokaz_pracownikow_firmy():
    listbox_pracownicy_firmy.delete(0, END)

    szukana_firma = entry_szukaj_pracownikow.get()

    for pracownik in pracownicy:
        if szukana_firma == "" or pracownik.firma == szukana_firma:
            listbox_pracownicy_firmy.insert(
                END,
                f"{pracownik.nazwa} - {pracownik.firma} - {pracownik.opis}"
            )


# -------------------- GŁÓWNE OKNO PROGRAMU --------------------

def pokaz_program():
    global root, map_widget
    global label_lista, label_opis, label_szczegoly
    global listbox_obiekty, listbox_klienci, listbox_pracownicy_firmy
    global entry_nazwa, entry_firma, entry_opis, entry_lokalizacja
    global entry_klient, entry_klient_rozglosnia, entry_szukaj_klientow
    global entry_szukaj_pracownikow
    global button_dodaj

    root = Tk()
    root.title("System zarządzania stacjami radiowymi")
    root.geometry("1100x760")

    ramka_menu = Frame(root)
    ramka_lista = Frame(root)
    ramka_formularz = Frame(root)
    ramka_szczegoly = Frame(root)
    ramka_mapa = Frame(root)
    ramka_klienci = Frame(root)
    ramka_pracownicy = Frame(root)

    ramka_menu.grid(row=0, column=0, sticky=N)
    ramka_lista.grid(row=1, column=0, sticky=N)
    ramka_formularz.grid(row=2, column=0, sticky=N)
    ramka_mapa.grid(row=0, column=1, rowspan=3)
    ramka_szczegoly.grid(row=3, column=0, columnspan=2, sticky=W)
    ramka_klienci.grid(row=4, column=0, sticky=N)
    ramka_pracownicy.grid(row=4, column=1, sticky=N)

    # MENU
    Label(ramka_menu, text="Wybierz moduł").grid(row=0, column=0)

    Button(
        ramka_menu,
        text="Placówki rozgłośni",
        width=25,
        command=wybierz_placowki
    ).grid(row=1, column=0)

    Button(
        ramka_menu,
        text="Nadajniki",
        width=25,
        command=wybierz_nadajniki
    ).grid(row=2, column=0)

    Button(
        ramka_menu,
        text="Pracownicy",
        width=25,
        command=wybierz_pracownikow
    ).grid(row=3, column=0)

    # LISTA OBIEKTÓW
    label_lista = Label(ramka_lista, text="Lista placówek rozgłośni")
    label_lista.grid(row=0, column=0, columnspan=3)

    listbox_obiekty = Listbox(ramka_lista, width=40, height=8)
    listbox_obiekty.grid(row=1, column=0, columnspan=3)

    Button(ramka_lista, text="Pokaż", command=pokaz_szczegoly).grid(row=2, column=0)
    Button(ramka_lista, text="Usuń", command=usun_obiekt).grid(row=2, column=1)
    Button(ramka_lista, text="Edytuj", command=edytuj_obiekt).grid(row=2, column=2)

    # FORMULARZ
    Label(ramka_formularz, text="Formularz").grid(row=0, column=0, columnspan=2)

    Label(ramka_formularz, text="Nazwa:").grid(row=1, column=0, sticky=E)
    Label(ramka_formularz, text="Rozgłośnia / firma:").grid(row=2, column=0, sticky=E)

    label_opis = Label(ramka_formularz, text="Adres placówki:")
    label_opis.grid(row=3, column=0, sticky=E)

    Label(ramka_formularz, text="Miejscowość:").grid(row=4, column=0, sticky=E)

    entry_nazwa = Entry(ramka_formularz)
    entry_firma = Entry(ramka_formularz)
    entry_opis = Entry(ramka_formularz)
    entry_lokalizacja = Entry(ramka_formularz)

    entry_nazwa.grid(row=1, column=1)
    entry_firma.grid(row=2, column=1)
    entry_opis.grid(row=3, column=1)
    entry_lokalizacja.grid(row=4, column=1)

    button_dodaj = Button(
        ramka_formularz,
        text="Dodaj",
        width=20,
        command=dodaj_obiekt
    )
    button_dodaj.grid(row=5, column=0, columnspan=2)

    # MAPA
    map_widget = tkintermapview.TkinterMapView(
        ramka_mapa,
        width=700,
        height=480,
        corner_radius=4
    )
    map_widget.set_position(52.2, 21.0)
    map_widget.set_zoom(6)
    map_widget.grid(row=0, column=0)

    # SZCZEGÓŁY
    Label(
        ramka_szczegoly,
        text="Szczegóły zaznaczonego obiektu:"
    ).grid(row=0, column=0, sticky=W)

    label_szczegoly = Label(ramka_szczegoly, text="...", justify=LEFT)
    label_szczegoly.grid(row=1, column=0, sticky=W)

    # KLIENCI
    Label(
        ramka_klienci,
        text="Klienci wybranej rozgłośni"
    ).grid(row=0, column=0, columnspan=2)

    listbox_klienci = Listbox(ramka_klienci, width=45, height=7)
    listbox_klienci.grid(row=1, column=0, columnspan=2)

    Label(ramka_klienci, text="Klient:").grid(row=2, column=0)
    entry_klient = Entry(ramka_klienci)
    entry_klient.grid(row=2, column=1)

    Label(ramka_klienci, text="Rozgłośnia:").grid(row=3, column=0)
    entry_klient_rozglosnia = Entry(ramka_klienci)
    entry_klient_rozglosnia.grid(row=3, column=1)

    Button(
        ramka_klienci,
        text="Dodaj klienta",
        command=dodaj_klienta
    ).grid(row=4, column=0, columnspan=2)

    Label(
        ramka_klienci,
        text="Pokaż klientów rozgłośni:"
    ).grid(row=5, column=0)

    entry_szukaj_klientow = Entry(ramka_klienci)
    entry_szukaj_klientow.grid(row=5, column=1)

    Button(
        ramka_klienci,
        text="Pokaż",
        command=pokaz_klientow
    ).grid(row=6, column=0, columnspan=2)

    # PRACOWNICY FIRMY
    Label(
        ramka_pracownicy,
        text="Pracownicy wybranej firmy"
    ).grid(row=0, column=0, columnspan=2)

    listbox_pracownicy_firmy = Listbox(ramka_pracownicy, width=45, height=7)
    listbox_pracownicy_firmy.grid(row=1, column=0, columnspan=2)

    Label(ramka_pracownicy, text="Firma / rozgłośnia:").grid(row=2, column=0)

    entry_szukaj_pracownikow = Entry(ramka_pracownicy)
    entry_szukaj_pracownikow.grid(row=2, column=1)

    Button(
        ramka_pracownicy,
        text="Pokaż pracowników",
        command=pokaz_pracownikow_firmy
    ).grid(row=3, column=0, columnspan=2)

    # DANE STARTOWE
    placowki.append(
        Obiekt(
            "Centrala Warszawa",
            "Radio Warszawa",
            "ul. Radiowa 1",
            "Warszawa",
            "Placówka"
        )
    )

    nadajniki.append(
        Obiekt(
            "Nadajnik Kraków",
            "Radio Kraków",
            "101.5 FM",
            "Kraków",
            "Nadajnik"
        )
    )

    pracownicy.append(
        Obiekt(
            "Jan Kowalski",
            "Radio Warszawa",
            "Prezenter",
            "Warszawa",
            "Pracownik"
        )
    )

    klienci.append(Klient("Firma Alfa", "Radio Warszawa"))
    klienci.append(Klient("Sklep Beta", "Radio Kraków"))

    pokaz_liste()
    pokaz_klientow()
    pokaz_pracownikow_firmy()

    root.mainloop()


# -------------------- OKNO LOGOWANIA --------------------

okno_logowania = Tk()
okno_logowania.title("Logowanie")
okno_logowania.geometry("300x160")

Label(
    okno_logowania,
    text="Logowanie do systemu"
).grid(row=0, column=0, columnspan=2, pady=10)

Label(okno_logowania, text="Login:").grid(row=1, column=0)
entry_login = Entry(okno_logowania)
entry_login.grid(row=1, column=1)

Label(okno_logowania, text="Hasło:").grid(row=2, column=0)
entry_haslo = Entry(okno_logowania, show="*")
entry_haslo.grid(row=2, column=1)

Button(
    okno_logowania,
    text="Zaloguj",
    command=zaloguj
).grid(row=3, column=0, columnspan=2, pady=10)

entry_login.insert(0, "admin")
entry_haslo.insert(0, "admin")

okno_logowania.mainloop()