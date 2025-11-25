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
            for parth in row[0]:
                for pnt in parth:
                    ListaWsp.append([pnt.X, pnt.Y])
            ListaOb.append(ListaWsp)
    return ListaOb

def nowa_warstwa_punktowa(nazwa_warstwy, uklad_wsp, list_coor):
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, nazwa_warstwy, "POLYLINE", "", "DISABLED", "DISABLED", uklad_wsp)
    array = arcpy.Array()
    pnt = arcpy.Point()
    with arcpy.da.InsertCursor(nazwa_warstwy, ["SHAPE@"]) as cursor:
        for ob in list_coor:
            for coor in ob:
                pnt.X = coor[0]
                pnt.Y = coor[1]
                array.add(pnt)
            poly = arcpy.Polyline(array)
            array.removeAll()
            cursor.insertRow([poly])

ListaLinii = odczytywanie_wspolrzednych(warstwa_poly_in)
lines_reduced = [line[::2] for line in ListaLinii]


nowa_warstwa_punktowa("LinieRWSR_02", warstwa_poly_in, lines_reduced)
print("KONIEC")