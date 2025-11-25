import arcpy

# ===================================================================
# KONFIGURACJA ŚRODOWISKA
# ===================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr3.gdb"
warstwa_poly_in_2014 = "GDA2014_OT_SWRS_L"
warstwa_poly_in_2020 = "GDA2020_OT_SWRS_L"

# ===================================================================
# ZDEFINIOWANE FUNKCJE DLA WARSTWY LINIOWEJ LUB POLIGONOWEJ
# ===================================================================

def odczytywanie_wspolrzednych(warstwa):
    i = 0
    ListaOb = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@"]) as cursor:
        for row in cursor:
            i += 1
            ListaWsp = []
            for parth in row[0]:
                for pnt in parth:
                    if pnt:
                        ListaWsp.append([pnt.X, pnt.Y])
            ListaOb.append(ListaWsp)
    return ListaOb

def nowa_warstwa_poly(nazwa_warstwy, uklad_wsp, list_coor):
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, nazwa_warstwy, "POLYGON", "", "DISABLED", "DISABLED", uklad_wsp)
    array = arcpy.Array()
    pnt = arcpy.Point()
    with arcpy.da.InsertCursor(nazwa_warstwy, ["SHAPE@"]) as cursor:
        for ob in list_coor:
            for coor in ob:
                pnt.X = coor[0]
                pnt.Y = coor[1]
                array.add(pnt)
            poly = arcpy.Polygon(array)
            array.removeAll()
            cursor.insertRow([poly])

def nowa_warstwa_punktowa(nazwa_warstwy, uklad_wsp, list_coor):
    # list_coor = odczytywanie_pliku_txt("data.txt")
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, nazwa_warstwy, "POINT", "", "DISABLED", "DISABLED", uklad_wsp)
    with arcpy.da.InsertCursor(nazwa_warstwy, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for coor in list_coor:
            X = coor[0]
            Y = coor[1]
            cursor.insertRow([X, Y])

# ===================================================================
# WYWOŁYWANIE FUNKCJI ODCZYTU WSPÓŁRZĘDNYCH LINII
# ===================================================================
Lista2014 = odczytywanie_wspolrzednych(warstwa_poly_in_2014)
Lista2020 = odczytywanie_wspolrzednych(warstwa_poly_in_2020)
# lines_reduced = [line[::2] for line in ListaLinii]

from collections import namedtuple

# Tolerancja w metrach – dostosuj do jakości danych (0.1–0.5 m zazwyczaj wystarczy)
TOLERANCJA = 0.3

Point = namedtuple('Point', ['x', 'y'])

def punkt_juz_istnieje(p, zbior_punktow2014):
    """Sprawdza czy punkt p jest już w zbiorze z 2014 (z tolerancją)"""
    for istniejacy in zbior_punktow2014:
        if ((p.x - istniejacy.x)**2 + (p.y - istniejacy.y)**2) < TOLERANCJA**2:
            return True
    return False

# 1. Tworzymy zbiór wszystkich punktów z 2014 (unikalne z tolerancją)
zbior2014 = set()

for linia in Lista2014:
    for x, y in linia:
        p = Point(round(x / TOLERANCJA), round(y / TOLERANCJA))  # siatka zaokrąglona do tolerancji
        zbior2014.add(p)

# 2. Sprawdzamy każdy punkt z 2020
nowe_punkty = []
istniejace_punkty = []

for linia2020 in Lista2020:
    for x, y in linia2020:
        p = Point(round(x / TOLERANCJA), round(y / TOLERANCJA))
        if p not in zbior2014:
            nowe_punkty.append([x, y])
        else:
            istniejace_punkty.append([x, y])

print(f"Liczba WSZYSTKICH punktów w 2020: {len(nowe_punkty) + len(istniejace_punkty)}")
print(f"Liczba punktów ISTNIEJĄCYCH już w 2014: {len(istniejace_punkty)}")
print(f"Liczba NOWYCH punktów w 2020:       {len(nowe_punkty)}")
print(nowe_punkty[:20])
nowa_warstwa_punktowa("Punkty_2020", warstwa_poly_in_2020, nowe_punkty)

print("KONIEC")