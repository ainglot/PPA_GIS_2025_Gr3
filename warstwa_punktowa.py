import arcpy
from collections import defaultdict
import numpy as np  # opcjonalnie, ale wygodnie

# ===================================================================
# KONFIGURACJA ŚRODOWISKA
# ===================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr3.gdb"
warstwa_drzew = "GDA2020_OT_OIPR_P_copy"
# https://mostwiedzy.pl/pl/open-research-data/3d-point-cloud-as-a-representation-of-silo-tank,615070441641526-0

# ===================================================================
# ZDEFINIOWANE FUNKCJE DLA WARSTWY PUNKTOWEJ
# ===================================================================
def odczytywanie_wspolrzednych(warstwa):
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:
            print(row)


def aktualizacja_wspolrzednych(warstwa):
    with arcpy.da.UpdateCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:
            row[0] += 100
            row[1] += 100
            print(row)
            cursor.updateRow(row) 


def wstawianie_wspolrzednych(warstwa):
    with arcpy.da.UpdateCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:
            row[0] += 100
            row[1] += 100
            print(row)
            cursor.updateRow(row) 

def nowa_warstwa_punktowa(nazwa_warstwy, uklad_wsp, list_coor):
    # list_coor = odczytywanie_pliku_txt("data.txt")
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, nazwa_warstwy, "POINT", "", "DISABLED", "ENABLED", uklad_wsp)
    with arcpy.da.InsertCursor(nazwa_warstwy, ["SHAPE@X", "SHAPE@Y", "SHAPE@Z"]) as cursor:
        for coor in list_coor:
            X = coor[0]
            Y = coor[1]
            Z = coor[2]
            cursor.insertRow([X, Y, Z])

def odczytywanie_pliku_txt(plik_txt):
    # Sposób 1 - najprostszy i najczęściej używany
    with open(plik_txt, 'r') as f:
        coordinates = []
        for line in f:
            line = line.strip()          # usuwa \n i ewentualne spacje na końcu
            if line:                     # pomija puste linie
                x, y, z = map(float, line.split())
                coordinates.append([x, y, z])
    return coordinates


odczytywanie_wspolrzednych(warstwa_drzew)
aktualizacja_wspolrzednych(warstwa_drzew)

print(odczytywanie_pliku_txt("data.txt")[:50])

nowa_warstwa_punktowa("silos_03", 2180)

# coor_silos = odczytywanie_pliku_txt("data.txt")

# # 2. Znajdź minimalną i maksymalną wartość Z
# z_values = [p[2] for p in coor_silos]
# z_min = min(z_values)
# z_max = max(z_values)

# print(f"Z zakres: {z_min:.3f} → {z_max:.3f}")

# # 3. Grupowanie co 2 metry (przedziały: [z_min, z_min+2), [z_min+2, z_min+4), ...)
# step = 2.0
# layers = defaultdict(list)   # klucz = początek przedziału, wartość = lista punktów

# for x, y, z in coor_silos:
#     # który przedział?
#     layer_start = (z - z_min) // step * step + z_min   # zaokrągla w dół do najbliższego wielokrotności 2 m
#     layers[layer_start].append([x, y, z])

# # 4. Obliczenie średnich X i Y dla każdej warstwy
# print("\nWarstwa (Z)      |  Liczba punktów  |  Średnie X   |  Średnie Y")
# print("-" * 65)

# coor_prze = []
# for layer_z in sorted(layers.keys()):
#     points = layers[layer_z]
#     xs = [p[0] for p in points]
#     ys = [p[1] for p in points]
    
#     avg_x = np.mean(xs)
#     avg_y = np.mean(ys)
#     count = len(points)
    
#     z_end = layer_z + step
#     print(f"{layer_z:6.3f} – {z_end:6.3f} m  |  {count:12}    |  {avg_x:8.3f}   |  {avg_y:8.3f}")
#     coor_prze.append([avg_x + 469839, avg_y + 741088, layer_z+1])
# print(coor_prze)
# nowa_warstwa_punktowa("silos_04", 2180, coor_prze)
print("KONIEC")