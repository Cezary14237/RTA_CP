import math
from typing import List, Dict, Callable, Generator  # WYMÓG 8: Typowanie (type hinting)

# WYMÓG 4: Instrukcja pass (użyta do zdefiniowania pustego wyjątku biznesowego)
class DaneFinansoweError(Exception):
    pass

# WYMÓG 10: Zmienna liczba argumentów (*args do przyjmowania opcjonalnych odliczeń od dochodu)
def oblicz_skale(przychod: float, koszty: float, *odliczenia: float) -> float:
    dochod = max(0.0, przychod - koszty - sum(odliczenia))
    
    # WYMÓG 3: Operator warunkowy potrójny (wyznaczenie podatku wg progów 12% i 32% dla 120 tys. zł)
    podatek_wstepny = dochod * 0.12 if dochod <= 120000 else (120000 * 0.12) + ((dochod - 120000) * 0.32)
    podatek = max(0.0, podatek_wstepny - 3600)  # Kwota zmniejszająca podatek 3600 zł
    
    # Składka zdrowotna 2026 dla skali: 9% dochodu, nie mniej niż 432.54 zł (100% minimalnej)
    skladka_zdrowotna = max(432.54 * 12, dochod * 0.09)
    return podatek + skladka_zdrowotna

def oblicz_liniowy(przychod: float, koszty: float) -> float:
    dochod = max(0.0, przychod - koszty)
    # W 2026 r. składka zdrowotna liniowca to 4.9% dochodu (minimum 432.54 zł/mc). Max odliczenie od dochodu to 14100 zł.
    skladka_miesieczna = max(432.54, (dochod / 12) * 0.049)
    skladka_zdrowotna_roczna = skladka_miesieczna * 12
    
    dochod_opodatkowany = max(0.0, dochod - min(skladka_zdrowotna_roczna, 14100))
    podatek = dochod_opodatkowany * 0.19
    return podatek + skladka_zdrowotna_roczna

# WYMÓG 9: Argumenty domyślne i nazwane (stawka_ryczaltu ma wartość domyślną 12% - np. dla IT)
def oblicz_ryczalt(przychod: float, stawka_ryczaltu: float = 0.12) -> float:
    podatek = przychod * stawka_ryczaltu
    
    # Składka zdrowotna ryczałtu 2026 zależy od rocznego przychodu
    if przychod <= 60000:
        skladka_zdrowotna = 498.35 * 12
    elif przychod <= 300000:
        skladka_zdrowotna = 830.58 * 12
    else:
        skladka_zdrowotna = 1495.04 * 12
        
    return podatek + skladka_zdrowotna

# WYMÓG 7: Generator generujący symulowane scenariusze wzrostu przychodów firmy
def generator_scenariuszy(base_przychod: float) -> Generator[float, None, None]:
    for mnoznik in [1.0, 1.25, 1.5]:
        yield base_przychod * mnoznik

# GŁÓWNA FUNKCJA ANALITYCZNA
def uruchom_symulator():
    # Dane wejściowe firmy
    firma_info = "  PROFIL_FIRMY: Usługi Programistyczne B2B   "
    roczny_przychod = 160000.0
    roczne_koszty = 20000.0
    
    # WYMÓG 1: Funkcje przetwarzające łańcuch znaków (.strip() oraz .replace() - niewykluczone z oceny)
    profil_czysty = firma_info.strip().replace(" ", "_")
    
    # WYMÓG 6: Operator przynależności (in) do sprawdzenia słów kluczowych w profilu działalności
    if "Programistyczne" in profil_czysty:
        stawka_rycz = 0.12
    else:
        stawka_rycz = 0.15

    # WYMÓG 11: Funkcja anonimowa (lambda) do szybkiego liczenia czystego zysku brutto przed podatkami
    oblicz_wynik_brutto = lambda p, k: p - k
    wynik_brutto = oblicz_wynik_brutto(roczny_przychod, roczne_koszty)

    # WYMÓG 5: Instrukcja match do wyboru optymalnych kalkulacji
    formy_opodatkowania = ["Skala", "Liniowy", "Ryczałt"]
    wyniki = {}

    for forma in formy_opodatkowania:
        match forma:
            case "Skala":
                # Wywołanie z dodatkowym argumentem *args (np. ulga na Internet 760 zł)
                wyniki[forma] = oblicz_skale(roczny_przychod, roczne_koszty, 760.0)
            case "Liniowy":
                wyniki[forma] = oblicz_liniowy(roczny_przychod, roczne_koszty)
            case "Ryczałt":
                # WYMÓG 9: Wywołanie funkcji z użyciem argumentu nazwanego
                wyniki[forma] = oblicz_ryczalt(roczny_przychod, stawka_ryczaltu=stawka_rycz)

    print(f"--- Raport podatkowy 2026 dla: {profil_czysty} ---")
    print(f"Wynik finansowy brutto: {wynik_brutto:.2f} zł\n")

    for f, obciazenie in wyniki.items():
        czysty_zysk = wynik_brutto - obciazenie
        # WYMÓG 2: Formatowanie łańcucha znaków (f-string z zaokrągleniem do 2 miejsc po przecinku)
        print(f"Forma: {f:<8} | Suma (Podatek+ZUS): {obciazenie:>10.2f} zł | Zysk netto: {czysty_zysk:>10.2f} zł")

    # WYMÓG 3: Operator Walrus (assignment expression) użyty w warunku sprawdzającym najlepszą formę
    najlepsza_forma = min(wyniki, key=wyniki.get)
    if (roznica := max(wyniki.values()) - min(wyniki.values())) > 0:
        print(f"\n[Rekomendacja]: Wybierz {najlepsza_forma}. Różnica między skrajnymi opcjami to {roznica:.2f} zł.")

# Uruchomienie programu
if __name__ == "__main__":
    uruchom_symulator()