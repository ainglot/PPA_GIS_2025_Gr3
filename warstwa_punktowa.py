import arcpy

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

def nowa_warstwa_punktowa(nazwa_warstwy, uklad_wsp):
    list_coor = odczytywanie_pliku_txt("data.txt")
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, nazwa_warstwy, "POINT", "", "DISABLED", "DISABLED", uklad_wsp)
    with arcpy.da.InsertCursor(nazwa_warstwy, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for coor in list_coor:
            X = coor[0] + 469839
            Y = coor[1] + 741088
            cursor.insertRow([X, Y])

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


# odczytywanie_wspolrzednych(warstwa_drzew)
# aktualizacja_wspolrzednych(warstwa_drzew)

print(odczytywanie_pliku_txt("data.txt")[:50])
nowa_warstwa_punktowa("silos_02", 2180)

print("KONIEC")