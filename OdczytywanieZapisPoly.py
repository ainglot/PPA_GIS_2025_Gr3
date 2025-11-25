import arcpy

# ===================================================================
# KONFIGURACJA ŚRODOWISKA
# ===================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr3.gdb"
warstwa_poly_in = "GDA2014_OT_SWRS_L"

# ===================================================================
# ZDEFINIOWANE FUNKCJE DLA WARSTWY LINIOWEJ LUB POLIGONOWEJ
# ===================================================================

def odczytywanie_wspolrzednych(warstwa):
    i = 0
    ListaWsp = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:
            i += 1
            print(i, row)
            ListaWsp.append(row)

def nowa_warstwa_punktowa(nazwa_warstwy, uklad_wsp, list_coor):
    # list_coor = odczytywanie_pliku_txt("data.txt")
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, nazwa_warstwy, "POINT", "", "DISABLED", "ENABLED", uklad_wsp)
    with arcpy.da.InsertCursor(nazwa_warstwy, ["SHAPE@X", "SHAPE@Y", "SHAPE@Z"]) as cursor:
        for coor in list_coor:
            X = coor[0]
            Y = coor[1]
            Z = coor[2]
            cursor.insertRow([X, Y, Z])

ListaWSP = odczytywanie_wspolrzednych(warstwa_poly_in)
print(ListaWSP)
print("KONIEC")