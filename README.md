# Analiza Zmian Pokrycia Terenu w ArcGIS (BDOT10k)

Witaj! To repozytorium zawiera dwa skrypty Pythona z użyciem biblioteki `arcpy` do automatyzacji zadań GIS w ArcGIS Pro. Skrypty są zaprojektowane do pracy z danymi BDOT10k (pokrycie terenu) i importem plików SHP. Są uniwersalne i gotowe do użycia w geobazach File Geodatabase (.gdb).

## Wymagania
- **ArcGIS Pro 3.5.2** (z zainstalowaną licencją ArcPy).
- **Python 3.11.11** (wbudowany w ArcGIS).
- Dane źródłowe: Pliki SHP z BDOT10k lub warstwy w geobazie.
- Uruchomienie: Wpisz `python nazwa_skryptu.py` w terminalu ArcGIS Pro lub VS Code (z rozszerzeniem Python).

## Skrypty

### 1. `analiza_zmian_pokrycia_terenu.py`
**Opis:** Skrypt do analizy zmian pokrycia terenu między rocznikami BDOT10k (2014–2024). Automatycznie:
- Wykrywa i scala warstwy dla wybranych lat (np. 2014 vs 2020).
- Tworzy przecięcie (Intersect) i oblicza powierzchnie zmian klas (np. las → zabudowa).
- Generuje wykres kołowy z top 20 zmianami (z Matplotlib) i zapisuje jako PNG.

**Jak użyć:**
1. Zmień ścieżkę geobazy w linii `arcpy.env.workspace = ...`.
2. Ustaw `rok1 = 2014` i `rok2 = 2020` (lub inne lata).
3. Uruchom skrypt – wygeneruje warstwy jak `PT_2014_2020` i wykres.

**Przykładowe wyjście:**
- Powierzchnia zmian: 15.2% obszaru.
- Wykres: `wykres_zmian_2014_2020.png`.

**Uwagi:** Obsługuje tylko warstwy z "GDA2014" i "OT_PT". Dodaj mapowanie kodów (np. "BU" → "Zabudowa") dla czytelniejszych etykiet.

### 2. `import_shp_do_geobazy.py`
**Opis:** Skrypt do importu plików SHP z folderu do geobazy. Automatycznie:
- Kopiuje i czyści nazwy plików (kropki → podkreślenia).
- Wydobywa kody (np. z `__2261` → `GDA2014_2261`).
- Eksportuje tylko .shp do geobazy z walidacją nazw.

**Jak użyć:**
1. Zmień ścieżki: `folder_shp` (źródło) i `arcpy.env.workspace` (geobaza).
2. Uruchom – skrypt utworzy folder `new_...` i zaimportuje warstwy.

**Przykładowe wejście/wyjście:**
- Wejście: `OT.PTTR.A_gr3__2261.shp` → Wyjście: Warstwa `GDA2014_2261` w GDB.

**Uwagi:** Obsługuje błędy (try/except). Dodaj `.gitignore` dla plików tymczasowych.

### 3. `warstwa puktowa.py`
**Opis:** Skrypt do odczywywania i aktualizowania współrzędnych w istniejącej warstiwe wektorowej oraz budowania nowej warstwy punktowej:
- Funkcja do odczytywania współrzędnych z warstwy punktowej.
- Funkcja do modyfikacji współrzędnych warstwy punktowej.
- Budowanie nowej warstwy punktowej wraz z wstawianiem punktów z pliku txt.
- Przykład generowania warstwy punktowej 3D dla danych X, Y i Z.

**Jak użyć:**
1. Wykorzystaj odpowiednie funkcje - `odczytywanie_wspolrzednych`, `aktualizacja_wspolrzednych`, `wstawianie_wspolrzednych`.
2. Uruchom – skrypt trzeba dostosować do swoich potrzeb.

**Przykładowe wejście/wyjście:**
- Wejście: dane pozyskane z BDOT10k `GDA2020_OT_OIPR_P` w GDB.

## Instalacja i Uruchomienie
1. Sklonuj repo: `git clone https://github.com/TwojeKonto/PPA_ArcGIS_Skrypty.git`.
2. Otwórz w VS Code.
3. Uruchom w terminalu: `python analiza_zmian_pokrycia_terenu.py`.

## Licencja
MIT License – używaj swobodnie, ale podaj źródło.

## Kontakt
Pytania? Otwórz issue na GitHub lub napisz: twoj.email@example.com.

Dzięki za użycie! 🌍