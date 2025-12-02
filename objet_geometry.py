import arcpy

# ===================================================================
# KONFIGURACJA ŚRODOWISKA
# ===================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr3.gdb"
warstwa_poligonowa = "Budynki"

geometry = arcpy.management.CopyFeatures(warstwa_poligonowa, arcpy.Geometry())

def odczytywanie_wspolrzednych_poligonu(warstwa):
    i = 0
    ListaOb = []
    Centr = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@", "SHAPE@XY"]) as cursor:
        for row in cursor:
            print(row)
            i += 1
            ListaPart = []
            Centr.append(row[1])
            for parth in row[0]:
                ListaWsp = []
                for pnt in parth:
                    # print(pnt)
                    if pnt:
                        ListaWsp.append([pnt.X, pnt.Y])
                    else:
                        ListaPart.append(ListaWsp)
                        ListaWsp = []
                ListaPart.append(ListaWsp)
            ListaOb.append(ListaPart)
    return ListaOb, Centr

Otoczki = []
i = 0

for geo1 in geometry:
    # j = 0
    # for geo2 in geometry:
    #     if i < j:
    #         if geo1.touches(geo2):
    #             print(i, j, geo1.touches(geo2))
    #         print(i, j, geo1.distanceTo(geo2))
    #     j += 1
    # i += 1
    print(geo1.getArea("GEODESIC", "SquareMeters"), geo1.area)# XMin, YMin, XMax, YMax
    # Otoczki.append(geo.convexHull().buffer(10).boundary())


# arcpy.management.CopyFeatures(Otoczki, "Budynki_11")
# odczytywanie_wspolrzednych_poligonu(warstwa_poligonowa)

print("KONIEC")