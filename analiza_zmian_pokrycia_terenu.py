import arcpy
from collections import defaultdict
import matplotlib.pyplot as plt
 
# ===================================================================
# KONFIGURACJA ŚRODOWISKA
# ===================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr3.gdb"
# arcpy.env.overwriteOutput = True  # Zezwala na nadpisywanie istniejących plików wyjściowych
 
# ===================================================================
# ETAP 1: AUTOMATYCZNE TWORZENIE WARSTW PT_2014 i PT_2020 (jeśli nie istnieją)
# ===================================================================

# Nazwy warstw wynikowych
out2014 = "PT_2014"
out2020 = "PT_2020"

# Listy warstw źródłowych do scalenia
input_2014 = []
input_2020 = []

# Pobranie wszystkich klas obiektów w geobazie
featureclasses = arcpy.ListFeatureClasses()

print("Sprawdzanie warstw pokrycia terenu...")

# Przeszukiwanie warstw pod kątem kryteriów
for fc in featureclasses:
    if "GDA2014" in fc and "OT_PT" in fc:
        # Próba wykrycia roku w nazwie (np. PT_2014, 2014_GDA, itp.)
        if "2014" in fc or fc.endswith("2014"):
            input_2014.append(fc)
        elif "2020" in fc or fc.endswith("2020"):
            input_2020.append(fc)
        else:
            # Jeśli rok nie jest w nazwie – przypisz do 2014 (domyślnie)
            # Możesz to zmienić lub dodać logikę na podstawie atrybutów
            input_2014.append(fc)

# === SPRAWDZENIE I TWORZENIE PT_2014 ===
if arcpy.Exists(out2014):
    print(f"Warstwa '{out2014}' już istnieje – pomijam scalanie.")
else:
    if input_2014:
        print(f"Tworzenie warstwy '{out2014}' z {len(input_2014)} warstw źródłowych...")
        arcpy.management.Merge(input_2014, out2014)
        print(f"   → Utworzono: {out2014}")
    else:
        raise ValueError(f"Nie znaleziono warstw źródłowych dla roku 2014 (kryteria: GDA2014 + OT_PT + 2014)")

# === SPRAWDZENIE I TWORZENIE PT_2020 ===
if arcpy.Exists(out2020):
    print(f"Warstwa '{out2020}' już istnieje – pomijam scalanie.")
else:
    if input_2020:
        print(f"Tworzenie warstwy '{out2020}' z {len(input_2020)} warstw źródłowych...")
        arcpy.management.Merge(input_2020, out2020)
        print(f"   → Utworzono: {out2020}")
    else:
        print("   → Brak warstw dla 2020 – warstwa nie zostanie utworzona.")
        # Opcjonalnie: raise ValueError(...) jeśli 2020 jest wymagane

# Debug: wypisz, co zostało znalezione
print(f"\nPodsumowanie warstw źródłowych:")
print(f"   2014: {len(input_2014)} warstw → {input_2014}")
print(f"   2020: {len(input_2020)} warstw → {input_2020}")
 
# ===================================================================
# ETAP 2: PRZECIĘCIE WARSTW 2014 i 2020
# ===================================================================
inter = "PT_2014_2020"

# Sprawdzenie, czy warstwa przecięcia już istnieje – jeśli nie, utwórz
if not arcpy.Exists(inter):
    print(f"Tworzenie warstwy przecięcia: {inter}")
    arcpy.analysis.Intersect(
        in_features=[f"{out2014} #", f"{out2020} #"],
        out_feature_class=inter,
        join_attributes="ALL",
        output_type="INPUT"
    )
else:
    print(f"Warstwa {inter} już istnieje – pomijam tworzenie.")

# ===================================================================
# ETAP 4: ANALIZA ZMIAN POKRYCIA TERENU
# ===================================================================
# Słownik: klucz = para (kod_2014, kod_2020), wartość = suma powierzchni zmiany
area_by_pair = defaultdict(float)

# Kursory do odczytu danych z warstwy przecięcia
fields = ["OID@", "X_KOD", "X_KOD_1", "SHAPE@AREA"]  # SHAPE@AREA zamiast Shape_Area (lepsza praktyka)
total_area = 0.0        # Całkowita powierzchnia przecięcia
change_area = 0.0       # Powierzchnia gdzie nastąpiła zmiana (X_KOD != X_KOD_1)

print("Przetwarzanie zmian pokrycia terenu...")
with arcpy.da.SearchCursor(inter, fields) as cursor:
    for row in cursor:
        oid, kod1, kod2, area = row
        total_area += area
        if kod1 != kod2:  # Zmiana klasy pokrycia
            pair = (kod1, kod2)
            area_by_pair[pair] += area
            change_area += area

# Obliczenie procentu zmian
change_percent = (change_area / total_area) * 100 if total_area > 0 else 0
print(f"\nCałkowita powierzchnia przecięcia: {total_area:.2f} m²")
print(f"Powierzchnia zmian: {change_area:.2f} m² ({change_percent:.2f}%)")

# ===================================================================
# ETAP 5: SORTOWANIE ZMIAN WG POWIERZCHNI
# ===================================================================
# Sortowanie malejąco po powierzchni zmiany
area_by_pair_sort = dict(sorted(area_by_pair.items(), key=lambda x: x[1], reverse=True))

# Lista zmian w formacie: [etykieta, procent_zmian]
ListaZmian = []
for (kod1, kod2), area in area_by_pair_sort.items():
    proc_zmian = (area / change_area) * 100 if change_area > 0 else 0
    ListaZmian.append([f"{kod1}-{kod2}", proc_zmian])

# ===================================================================
# ETAP 6: PRZYGOTOWANIE DANYCH DO WYKRESU (top X + "inne")
# ===================================================================
x = 20  # Liczba najczęstszych zmian do pokazania osobno
NewList = ListaZmian[:x]

# Sumowanie reszty jako "inne"
reszta_lista = ListaZmian[x:]
reszta_suma = sum(proc for _, proc in reszta_lista)
if reszta_suma > 0:
    NewList.append(["inne", reszta_suma])

print(f"\nPrzygotowano {len(NewList)} kategorii do wykresu (w tym 'inne' jeśli >0).")

# ===================================================================
# ETAP 7: WYKRES KOŁOWY – UDZIAŁ ZMIAN
# ===================================================================
wartosci = [proc for _, proc in NewList]
etykiety = [label for label, _ in NewList]

# Tworzenie wykresu
plt.figure(figsize=(10, 8))
plt.pie(
    wartosci,
    labels=etykiety,
    autopct='%1.1f%%',
    startangle=0,
    textprops={'fontsize': 9}
)
plt.axis('equal')  # Równe proporcje koła
plt.title(f"Największe powierzchniowo zmiany pokrycia terenu (top {x} + inne)\n"
          f"Łączny udział zmian: {change_percent:.2f}% powierzchni powiatu", 
          fontsize=12, pad=20)

# Zapis i wyświetlenie
output_chart = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\wykres_zmian_pokrycia.png"
plt.savefig(output_chart, dpi=300, bbox_inches='tight')
print(f"Wykres zapisany jako: {output_chart}")
plt.show()

# ===================================================================
# KONIEC
# ===================================================================
print("\nKONIEC ANALIZY – SKRYPT ZAKOŃCZONY POMYŚLNIE.")