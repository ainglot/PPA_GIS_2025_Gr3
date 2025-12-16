import arcpy

# ===================================================================
# KONFIGURACJA ŚRODOWISKA DLA WEKTORÓW
# ===================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\Geobaza ZTM\ZTM197.gdb"
warstwa_linii = "ZTM_195_PL92"

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

WspLini = odczytywanie_wspolrzednych(warstwa_linii)
print(WspLini)

# ===================================================================
# KONFIGURACJA ŚRODOWISKA DLA RASTRÓW
# ===================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\NMT pod ZTM\ZTM197_NMT_TIF"

ListaExtentR = []
rasters = arcpy.ListRasters("*", "TIF")
for raster in rasters:
    print(raster)
    R = arcpy.Raster(raster)
    print("Extent:", R.extent)
    ListaExtentR.append([raster, [R.extent.XMin, R.extent.YMin, R.extent.XMax, R.extent.YMax]])



print(ListaExtentR)