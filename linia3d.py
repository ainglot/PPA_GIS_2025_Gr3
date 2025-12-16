import arcpy
import numpy as np

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

def punkt_na_rastrze(punkt, zakres_rastra):
    x, y = punkt
    xmin, ymin, xmax, ymax = zakres_rastra

    return xmin <= x <= xmax and ymin <= y <= ymax




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

PKT = [474467.48060000036, 720576.0291000009]
for rast_ext in ListaExtentR:
    # print(punkt_na_rastrze(PKT, rast_ext[1]))
    if punkt_na_rastrze(PKT, rast_ext[1]):
        cellSIZE = R.meanCellWidth
        XMIN = rast_ext[1][0] + (cellSIZE*0.5)
        YMAX = rast_ext[1][3] - (cellSIZE*0.5)
        dx = (PKT[0] - XMIN)/cellSIZE
        dy = (YMAX - PKT[1])/cellSIZE
        col = int(dx)
        row = int(dy)
        R_array = arcpy.RasterToNumPyArray(R, nodata_to_value=np.nan)
        print(dx, dy, R_array[col, row])

print(ListaExtentR)