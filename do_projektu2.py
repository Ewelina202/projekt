# from tkinter import *
# from tkinter import messagebox
# import tkintermapview
# import requests
# from bs4 import BeautifulSoup
#
# placowki = []
# nadajniki = []
# pracownicy = []
# klienci = []
#
# aktualna_lista = placowki
# aktualny_typ = "Placówka"
# edytowany_indeks = None
#
#
# class Obiekt:
#     def __init__(self, nazwa, firma, opis, lokalizacja, typ):
#         self.nazwa = nazwa
#         self.firma = firma
#         self.opis = opis
#         self.lokalizacja = lokalizacja
#         self.typ = typ
#
#         self.coordinates = self.get_coordinates()
#
#         self.marker = map_widget.set_marker(
#             self.coordinates[0],
#             self.coordinates[1],
#             text=self.nazwa
#         )
#
#     def get_coordinates(self):
#         tekst = self.lokalizacja.strip()
#
#         if "," in tekst:
#             try:
#                 dane = tekst.split(",")
#                 latitude = float(dane[0].strip())
#                 longitude = float(dane[1].strip())
#                 return [latitude, longitude]
#             except:
#                 pass
#
#         lokalizacja_url = tekst.replace(" ", "_")
#         url = f"https://pl.wikipedia.org/wiki/{lokalizacja_url}"
#
#         response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#         response_html = BeautifulSoup(response.text, "html.parser")
#
#         latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
#         longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
#
#         return [latitude, longitude]
#
#
# class Klient:
#     def __init__(self, nazwa, rozglosnia, usluga):
#         self.nazwa = nazwa
#         self.rozglosnia = rozglosnia
#         self.usluga = usluga
#
#
# def zaloguj():
#     if entry_login.get() == "admin" and entry_haslo.get() == "admin":
#         okno_logowania.destroy()
#         pokaz_program()
#     else:
#         messagebox.showerror("Błąd", "Niepoprawny login lub hasło")
#
#
# def wybierz_placowki():
#     global aktualna_lista, aktualny_typ, edytowany_indeks
#     aktualna_lista = placowki
#     aktualny_typ = "Placówka"
#     edytowany_indeks = None
#     label_lista.config(text="Lista placówek rozgłośni")
#     label_opis.config(text="Adres placówki:")
#     button_dodaj.config(text="Dodaj", command=dodaj_obiekt)
#     pokaz_liste()
#     wyczysc_formularz()
#
#
# def wybierz_nadajniki():
#     global aktualna_lista, aktualny_typ, edytowany_indeks
#     aktualna_lista = nadajniki
#     aktualny_typ = "Nadajnik"
#     edytowany_indeks = None
#     label_lista.config(text="Lista nadajników")
#     label_opis.config(text="Częstotliwość / opis:")
#     button_dodaj.config(text="Dodaj", command=dodaj_obiekt)
#     pokaz_liste()
#     wyczysc_formularz()
#
#
# def wybierz_pracownikow():
#     global aktualna_lista, aktualny_typ, edytowany_indeks
#     aktualna_lista = pracownicy
#     aktualny_typ = "Pracownik"
#     edytowany_indeks = None
#     label_lista.config(text="Lista pracowników")
#     label_opis.config(text="Stanowisko:")
#     button_dodaj.config(text="Dodaj", command=dodaj_obiekt)
#     pokaz_liste()
#     wyczysc_formularz()
#
#
# def pokaz_liste():
#     listbox_obiekty.delete(0, END)
#     for i, obiekt in enumerate(aktualna_lista):
#         listbox_obiekty.insert(i, f"{obiekt.nazwa} - {obiekt.firma}")
#
#
# def dodaj_obiekt():
#     nazwa = entry_nazwa.get()
#     firma = entry_firma.get()
#     opis = entry_opis.get()
#     lokalizacja = entry_lokalizacja.get()
#
#     if nazwa == "" or firma == "" or lokalizacja == "":
#         messagebox.showwarning("Brak danych", "Uzupełnij nazwę, firmę/rozgłośnię i współrzędne lub nazwę miejscowości")
#         return
#
#     try:
#         nowy_obiekt = Obiekt(nazwa, firma, opis, lokalizacja, aktualny_typ)
#         aktualna_lista.append(nowy_obiekt)
#         pokaz_liste()
#         wyczysc_formularz()
#     except ValueError:
#         messagebox.showerror("Błąd", "Wpisz poprawną nazwę miejscowości albo współrzędne, np. 52.2297,21.0122")
#
#
# def usun_obiekt():
#     zaznaczenie = listbox_obiekty.curselection()
#     if not zaznaczenie:
#         messagebox.showwarning("Brak wyboru", "Zaznacz obiekt na liście")
#         return
#
#     indeks = zaznaczenie[0]
#     if aktualna_lista[indeks].marker is not None:
#         aktualna_lista[indeks].marker.delete()
#     aktualna_lista.pop(indeks)
#     pokaz_liste()
#
#
# def edytuj_obiekt():
#     global edytowany_indeks
#
#     zaznaczenie = listbox_obiekty.curselection()
#     if not zaznaczenie:
#         messagebox.showwarning("Brak wyboru", "Zaznacz obiekt na liście")
#         return
#
#     edytowany_indeks = zaznaczenie[0]
#     obiekt = aktualna_lista[edytowany_indeks]
#
#     wyczysc_formularz()
#     entry_nazwa.insert(0, obiekt.nazwa)
#     entry_firma.insert(0, obiekt.firma)
#     entry_opis.insert(0, obiekt.opis)
#     entry_lokalizacja.insert(0, obiekt.lokalizacja)
#
#     button_dodaj.config(text="Zapisz zmiany", command=zapisz_zmiany)
#
#
# def zapisz_zmiany():
#     global edytowany_indeks
#
#     if edytowany_indeks is None:
#         return
#
#     try:
#         obiekt = aktualna_lista[edytowany_indeks]
#         obiekt.nazwa = entry_nazwa.get()
#         obiekt.firma = entry_firma.get()
#         obiekt.opis = entry_opis.get()
#         obiekt.lokalizacja = entry_lokalizacja.get()
#         obiekt.coordinates = obiekt.get_coordinates()
#
#         if obiekt.marker is not None:
#             obiekt.marker.delete()
#         obiekt.marker = map_widget.set_marker(
#             obiekt.coordinates[0],
#             obiekt.coordinates[1],
#             text=obiekt.nazwa
#         )
#
#         edytowany_indeks = None
#         button_dodaj.config(text="Dodaj", command=dodaj_obiekt)
#         pokaz_liste()
#         wyczysc_formularz()
#     except ValueError:
#         messagebox.showerror("Błąd", "Wpisz poprawną nazwę miejscowości albo współrzędne, np. 52.2297,21.0122")
#
#
# def pokaz_szczegoly():
#     zaznaczenie = listbox_obiekty.curselection()
#     if not zaznaczenie:
#         messagebox.showwarning("Brak wyboru", "Zaznacz obiekt na liście")
#         return
#
#     indeks = zaznaczenie[0]
#     obiekt = aktualna_lista[indeks]
#
#     label_szczegoly.config(
#         text=f"Typ: {obiekt.typ}\n"
#              f"Nazwa: {obiekt.nazwa}\n"
#              f"Firma / rozgłośnia: {obiekt.firma}\n"
#              f"Opis: {obiekt.opis}\n"
#              f"Lokalizacja: {obiekt.lokalizacja}\n"
#              f"Współrzędne: {obiekt.coordinates[0]}, {obiekt.coordinates[1]}"
#     )
#
#     usun_wszystkie_markery()
#     pokaz_marker_obiektu(obiekt)
#     map_widget.set_position(obiekt.coordinates[0], obiekt.coordinates[1])
#     map_widget.set_zoom(13)
#
#
# def wyczysc_formularz():
#     entry_nazwa.delete(0, END)
#     entry_firma.delete(0, END)
#     entry_opis.delete(0, END)
#     entry_lokalizacja.delete(0, END)
#
#
# def dodaj_klienta():
#     nazwa = entry_klient.get()
#     rozglosnia = entry_klient_rozglosnia.get()
#     usluga = entry_klient_usluga.get()
#
#     if nazwa == "" or rozglosnia == "" or usluga == "":
#         messagebox.showwarning("Brak danych", "Podaj nazwę klienta, rozgłośnię i rodzaj reklamy/usługi")
#         return
#
#     klienci.append(Klient(nazwa, rozglosnia, usluga))
#     entry_klient.delete(0, END)
#     entry_klient_rozglosnia.delete(0, END)
#     entry_klient_usluga.delete(0, END)
#
#     pokaz_klientow()
#
#
# def usun_wszystkie_markery():
#     for lista in [placowki, nadajniki, pracownicy]:
#         for obiekt in lista:
#             if obiekt.marker is not None:
#                 obiekt.marker.delete()
#                 obiekt.marker = None
#
#
# def pokaz_marker_obiektu(obiekt):
#     obiekt.marker = map_widget.set_marker(
#         obiekt.coordinates[0],
#         obiekt.coordinates[1],
#         text=obiekt.nazwa
#     )
#
#
# def pokaz_wszystkie_markery():
#     usun_wszystkie_markery()
#
#     for lista in [placowki, nadajniki, pracownicy]:
#         for obiekt in lista:
#             pokaz_marker_obiektu(obiekt)
#
#
# def pokaz_klientow():
#     listbox_klienci.delete(0, END)
#     szukana_rozglosnia = entry_szukaj_klientow.get()
#
#     for klient in klienci:
#         if szukana_rozglosnia == "" or klient.rozglosnia == szukana_rozglosnia:
#             listbox_klienci.insert(END, f"{klient.nazwa} - {klient.rozglosnia} - {klient.usluga}")
#
#
# def pokaz_pracownikow_firmy():
#     listbox_pracownicy_firmy.delete(0, END)
#     szukany_tekst = entry_szukaj_pracownikow.get().strip().lower()
#
#     znalezieni_pracownicy = []
#
#     if szukany_tekst == "":
#         pokaz_wszystkie_markery()
#     else:
#         usun_wszystkie_markery()
#
#     for pracownik in pracownicy:
#         nazwa = pracownik.nazwa.strip().lower()
#         firma = pracownik.firma.strip().lower()
#         opis = pracownik.opis.strip().lower()
#
#         if szukany_tekst == "" or szukany_tekst in nazwa or szukany_tekst in firma or szukany_tekst in opis:
#             listbox_pracownicy_firmy.insert(END, f"{pracownik.nazwa} - {pracownik.firma} - {pracownik.opis}")
#
#             znalezieni_pracownicy.append(pracownik)
#
#             if szukany_tekst != "":
#                 pokaz_marker_obiektu(pracownik)
#
#     if len(znalezieni_pracownicy) == 1:
#         pracownik = znalezieni_pracownicy[0]
#         map_widget.set_position(pracownik.coordinates[0], pracownik.coordinates[1])
#         map_widget.set_zoom(13)
#
#     if len(znalezieni_pracownicy) == 0 and szukany_tekst != "":
#         messagebox.showinfo("Brak wyników", "Nie znaleziono pracownika pasującego do wpisanego tekstu")
#
#
# def dodaj_przykladowe_dane():
#     if placowki or nadajniki or pracownicy or klienci:
#         return
#
#     placowki.append(Obiekt("Siedziba Radio Fala Warszawa", "Radio Fala", "Główna siedziba rozgłośni", "52.2297,21.0122", "Placówka"))
#     placowki.append(Obiekt("Oddział Radio Echo Kraków", "Radio Echo", "Oddział regionalny rozgłośni", "50.0647,19.9450", "Placówka"))
#     placowki.append(Obiekt("Biuro Radio Puls Poznań", "Radio Puls", "Biuro reklamy i kontaktu z klientami", "52.4064,16.9252", "Placówka"))
#
#     nadajniki.append(Obiekt("Nadajnik Warszawa Centrum", "Radio Fala", "Częstotliwość 98.4 FM", "52.2390,21.3200", "Nadajnik"))
#     nadajniki.append(Obiekt("Nadajnik Kraków Północ", "Radio Echo", "Częstotliwość 101.2 FM", "50.9760,19.9565", "Nadajnik"))
#     nadajniki.append(Obiekt("Nadajnik Poznań Zachód", "Radio Puls", "Częstotliwość 94.7 FM", "52.0500,16.9100", "Nadajnik"))
#
#     pracownicy.append(Obiekt("Anna Kowalska", "Radio Fala", "Prezenterka poranna", "52.8097,21.0122", "Pracownik"))
#     pracownicy.append(Obiekt("Marek Nowak", "Radio Fala", "Realizator dźwięku", "52.5310,21.5150", "Pracownik"))
#     pracownicy.append(Obiekt("Julia Wiśniewska", "Radio Echo", "Specjalistka ds. reklamy", "50.8047,19.9450", "Pracownik"))
#
#     klienci.append(Klient("Kawiarnia Słodka Fala", "Radio Fala", "Reklama lokalu gastronomicznego"))
#     klienci.append(Klient("Salon AutoMax", "Radio Fala", "Spot reklamowy 30 sekund"))
#     klienci.append(Klient("Firma Bud-Mix", "Radio Echo", "Ogłoszenie sponsorowane"))
#
#
# def pokaz_program():
#     global root, map_widget
#     global label_lista, label_opis, label_szczegoly
#     global listbox_obiekty, listbox_klienci, listbox_pracownicy_firmy
#     global entry_nazwa, entry_firma, entry_opis, entry_lokalizacja
#     global entry_klient, entry_klient_rozglosnia, entry_klient_usluga, entry_szukaj_klientow
#     global entry_szukaj_pracownikow
#     global button_dodaj
#
#     root = Tk()
#     root.title("System zarządzania stacjami radiowymi")
#     root.geometry("1100x760")
#
#     ramka_menu = Frame(root)
#     ramka_lista = Frame(root)
#     ramka_formularz = Frame(root)
#     ramka_szczegoly = Frame(root)
#     ramka_mapa = Frame(root)
#     ramka_klienci = Frame(root)
#     ramka_pracownicy = Frame(root)
#
#     ramka_menu.grid(row=0, column=0, sticky=N)
#     ramka_lista.grid(row=1, column=0, sticky=N)
#     ramka_formularz.grid(row=2, column=0, sticky=N)
#     ramka_mapa.grid(row=0, column=1, rowspan=3)
#     ramka_szczegoly.grid(row=3, column=0, columnspan=2, sticky=W)
#     ramka_klienci.grid(row=4, column=0, sticky=N)
#     ramka_pracownicy.grid(row=4, column=1, sticky=N)
#
#     Label(ramka_menu, text="Wybierz moduł").grid(row=0, column=0)
#     Button(ramka_menu, text="Placówki rozgłośni", width=25, command=wybierz_placowki).grid(row=1, column=0)
#     Button(ramka_menu, text="Nadajniki radiowe", width=25, command=wybierz_nadajniki).grid(row=2, column=0)
#     Button(ramka_menu, text="Pracownicy", width=25, command=wybierz_pracownikow).grid(row=3, column=0)
#
#     label_lista = Label(ramka_lista, text="Lista placówek rozgłośni")
#     label_lista.grid(row=0, column=0, columnspan=3)
#
#     listbox_obiekty = Listbox(ramka_lista, width=40, height=8)
#     listbox_obiekty.grid(row=1, column=0, columnspan=3)
#
#     Button(ramka_lista, text="Pokaż", command=pokaz_szczegoly).grid(row=2, column=0)
#     Button(ramka_lista, text="Usuń", command=usun_obiekt).grid(row=2, column=1)
#     Button(ramka_lista, text="Edytuj", command=edytuj_obiekt).grid(row=2, column=2)
#
#     label_szczegoly = Label(ramka_szczegoly, text="Szczegóły obiektu", justify=LEFT)
#     label_szczegoly.grid(row=0, column=0, sticky=W)
#
#     Label(ramka_formularz, text="Formularz").grid(row=0, column=0, columnspan=2)
#     Label(ramka_formularz, text="Nazwa:").grid(row=1, column=0, sticky=E)
#     Label(ramka_formularz, text="Rozgłośnia / firma:").grid(row=2, column=0, sticky=E)
#     label_opis = Label(ramka_formularz, text="Adres placówki:")
#     label_opis.grid(row=3, column=0, sticky=E)
#     Label(ramka_formularz, text="Miejscowość lub współrzędne:").grid(row=4, column=0, sticky=E)
#
#     entry_nazwa = Entry(ramka_formularz)
#     entry_firma = Entry(ramka_formularz)
#     entry_opis = Entry(ramka_formularz)
#     entry_lokalizacja = Entry(ramka_formularz)
#
#     entry_nazwa.grid(row=1, column=1)
#     entry_firma.grid(row=2, column=1)
#     entry_opis.grid(row=3, column=1)
#     entry_lokalizacja.grid(row=4, column=1)
#
#     button_dodaj = Button(ramka_formularz, text="Dodaj", width=20, command=dodaj_obiekt)
#     button_dodaj.grid(row=6, column=0, columnspan=2)
#
#     map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=700, height=480, corner_radius=4)
#     map_widget.set_position(52.2, 21.0)
#     map_widget.set_zoom(6)
#     map_widget.grid(row=0, column=0)
#
#     dodaj_przykladowe_dane()
#
#     Label(ramka_klienci, text="Klienci wybranej rozgłośni").grid(row=0, column=0, columnspan=2)
#     listbox_klienci = Listbox(ramka_klienci, width=45, height=7)
#     listbox_klienci.grid(row=1, column=0, columnspan=2)
#
#     Label(ramka_klienci, text="Nazwa klienta/firmy:").grid(row=2, column=0)
#     entry_klient = Entry(ramka_klienci)
#     entry_klient.grid(row=2, column=1)
#
#     Label(ramka_klienci, text="Rozgłośnia:").grid(row=3, column=0)
#     entry_klient_rozglosnia = Entry(ramka_klienci)
#     entry_klient_rozglosnia.grid(row=3, column=1)
#
#     Label(ramka_klienci, text="Rodzaj reklamy/usługi:").grid(row=4, column=0)
#     entry_klient_usluga = Entry(ramka_klienci)
#     entry_klient_usluga.grid(row=4, column=1)
#
#     Button(ramka_klienci, text="Dodaj klienta", command=dodaj_klienta).grid(row=5, column=0, columnspan=2)
#
#     Label(ramka_klienci, text="Pokaż klientów rozgłośni:").grid(row=6, column=0)
#     entry_szukaj_klientow = Entry(ramka_klienci)
#     entry_szukaj_klientow.grid(row=6, column=1)
#
#     Button(ramka_klienci, text="Pokaż", command=pokaz_klientow).grid(row=7, column=0, columnspan=2)
#
#     Label(ramka_pracownicy, text="Pracownicy wybranej firmy").grid(row=0, column=0, columnspan=2)
#     listbox_pracownicy_firmy = Listbox(ramka_pracownicy, width=45, height=7)
#     listbox_pracownicy_firmy.grid(row=1, column=0, columnspan=2)
#
#     Label(ramka_pracownicy, text="Firma / rozgłośnia:").grid(row=2, column=0)
#     entry_szukaj_pracownikow = Entry(ramka_pracownicy)
#     entry_szukaj_pracownikow.grid(row=2, column=1)
#
#     Button(ramka_pracownicy, text="Pokaż pracowników", command=pokaz_pracownikow_firmy).grid(row=3, column=0, columnspan=2)
#
#     pokaz_liste()
#     pokaz_klientow()
#     pokaz_pracownikow_firmy()
#
#     root.mainloop()
#
#
# okno_logowania = Tk()
# okno_logowania.title("Logowanie")
# okno_logowania.geometry("300x160")
#
# Label(okno_logowania, text="Logowanie do systemu").grid(row=0, column=0, columnspan=2, pady=10)
#
#
# Label(okno_logowania, text="Login:").grid(row=1, column=0)
# entry_login = Entry(okno_logowania)
# entry_login.grid(row=1, column=1)
#
# Label(okno_logowania, text="Hasło:").grid(row=2, column=0)
# entry_haslo = Entry(okno_logowania, show="*")
# entry_haslo.grid(row=2, column=1)
#
# Button(okno_logowania, text="Zaloguj", command=zaloguj).grid(row=3, column=0, columnspan=2, pady=10)
#
# entry_login.insert(0, "admin")
# entry_haslo.insert(0, "")
#
# okno_logowania.mainloop()
