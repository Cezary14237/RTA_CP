# apostrof i cudzysłów jako kwalifikator tekstu 1 wierszowego
osoba = 'Dariusz'
# print(osoba)
# osoba = "Dariusz"
# print(osoba)

# potrojona ilość pozwala tworzyć tekst wielowierszowy
# osoba = """
# Dariusz
# Nowak
# """
# print(osoba)
# osoba = '''
# Dariusz
# Nowak
# '''
# print(osoba)

# użycie w tekście
# tekst = "can't"
# zdanie = 'i napisano cytuję:”jestem kim jestem”'
# # znak ucieczki
# ucieczka = 'can\'t'
# print(tekst)
# print(zdanie)
# print(ucieczka)

# teksty pozwalają na stosowanie metod z użyciem notacji kropki
# pesel = '90030312345'
# print(pesel.isdigit())
# osoba = 'Dariusz Nowak'
# print("0123456789")
# print(osoba.capitalize())
# print(osoba.upper())
# print(osoba.lower())
# print(osoba.title())
# print(osoba.startswith('D'))
# print(osoba.find(' ')) # położenie spacji w tekście
# osoba = osoba.split() # zamiana na listę
# print(f"imię {osoba[0]}, nazwisko {osoba[1]}")

# wycinki z listy
# pobranie danych z numeru pesel
# rok = pesel[:2] # wycinek od znaku 0 do 2 (bez 2) -> 90
# miesiac = pesel[2:4] # wycinek od znaku 2 do 4 (bez 4) -> 03
# dzien = pesel[4:6] # jw.
# rok = int(rok) # zamiana na liczbę całkowitą
# miesiac = int(miesiac)
# dzien = int(dzien)
# if miesiac > 12:
#     miesiac -= 20 # osoby urodzone po roku 2000 mają do miesiąca + 20
#     rok += 2000
# else:
#     rok += 1900
# print(f"data urodzenia: {rok}/{miesiac:02}/{dzien}")
#  (opcjonalnie)
# import datetime
# print(datetime.date(rok, miesiac, dzien)) # data ur z pesel
# gender = pesel[9] # tylko 1 znak z tekstu z indeksu 9
# if int(gender) % 2 == 0:
#     print('kobieta')
# else:
#     print('mężczyzna')

# przykład użycia string.format()
# napis = "Promocja: {cena:.2f} zł!"
# print(napis.format(cena = 64.99))
# print(napis.format(cena = 64))
# print("Mam na imię {imie}, lat {wiek}".format(imie = "Jan", wiek = 31))
# print("Mam na imię {0}, lat {1}".format("Ewa",32))
# print("Mam na imię {}, lat {}".format("Jacek",34))
