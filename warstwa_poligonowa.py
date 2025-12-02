import arcpy

# ===================================================================
# KONFIGURACJA ŚRODOWISKA
# ===================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr3.gdb"
warstwa_poligonowa = "Budynek"

# ===================================================================
# ZDEFINIOWANE FUNKCJE DLA WARSTWY LINIOWEJ LUB POLIGONOWEJ
# ===================================================================

#### [ob1[granica[[x1, y1], [x2, y2]], dziura[[x1, y1], [x2, y2]], ...], ob2[]...]

def odczytywanie_wspolrzednych_poligonu(warstwa):
    i = 0
    ListaOb = []
    Centr = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@", "SHAPE@XY"]) as cursor:
        for row in cursor:
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

def nowa_warstwa_poligonowa(nazwa_warstwy, uklad_wsp, list_coor):
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, nazwa_warstwy, "POLYGON", "", "DISABLED", "DISABLED", uklad_wsp)
    array = arcpy.Array()
    part = arcpy.Array()
    pnt = arcpy.Point()
    with arcpy.da.InsertCursor(nazwa_warstwy, ["SHAPE@"]) as cursor:
        for ob in list_coor:
            for cze in ob:
                for coor in cze:
                    pnt.X = coor[0]
                    pnt.Y = coor[1]
                    part.add(pnt)
                array.add(part)
                part.removeAll()
            poly = arcpy.Polygon(array)
            array.removeAll()
            cursor.insertRow([poly])

listaPOLY, listaCENTR = odczytywanie_wspolrzednych_poligonu(warstwa_poligonowa)
print(listaPOLY[0][0])

i=0
for ob in listaPOLY:
    for part in ob:
        for pkt in part:
            pkt[0] = (pkt[0]-listaCENTR[i][0])*0.5+listaCENTR[i][0]
            pkt[1] = (pkt[1]-listaCENTR[i][1])*0.5+listaCENTR[i][1]
    i += 1
print(listaPOLY[0][0])

Nowy_Budynek = "Budynek02"
nowa_warstwa_poligonowa(Nowy_Budynek, warstwa_poligonowa, listaPOLY)



print("KONIEC")