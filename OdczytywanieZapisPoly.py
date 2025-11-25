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
    ListaOb = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@"]) as cursor:
        for row in cursor:
            i += 1
            ListaWsp = []
            print(i, row)
            for parth in row[0]:
                print(parth)
                for pnt in parth:
                    print("  ", pnt.X, pnt.Y)
                    ListaWsp.append([pnt.X, pnt.Y])
            ListaOb.append(ListaWsp)
    return ListaOb

# def nowa_warstwa_punktowa(nazwa_warstwy, uklad_wsp, list_coor):
#     # list_coor = odczytywanie_pliku_txt("data.txt")
#     arcpy.management.CreateFeatureclass(arcpy.env.workspace, nazwa_warstwy, "POINT", "", "DISABLED", "DISABLED", uklad_wsp)
#     with arcpy.da.InsertCursor(nazwa_warstwy, ["SHAPE@X", "SHAPE@Y"]) as cursor:
#         for coor in list_coor:
#             X = coor[0]
#             Y = coor[1]
#             cursor.insertRow([X, Y])

ListaLinii = odczytywanie_wspolrzednych(warstwa_poly_in)
print(ListaLinii[-1])
# nowa_warstwa_punktowa("CentroidyRWSR", warstwa_poly_in, ListaWSP)
print("KONIEC")