import arcpy
import numpy as np

# ===================================================================
# KONFIGURACJA ŚRODOWISKA
# ===================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\NMT"
RasterIn = "81008_1561328_N-34-50-C-d-3-3.asc"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(2180)  # układ 2180

# ===================================================================
# WCZYTYWANIE RASTRA JAKO OBIEKT RASTER
# ===================================================================
R = arcpy.Raster(RasterIn)
print("Extent:", R.extent)
print("Rozdzielczość komórki:", R.meanCellWidth)

# ===================================================================
# PARAMETRY RASTRA
# ===================================================================
# Uwaga: RasterToNumPyArray domyślnie liczy wiersze od GÓRNEJ krawędzi rastra,
# więc do przeliczenia współrzędnych potrzebujemy:
# XMin i YMax z extenta
XMin = R.extent.XMin
YMax = R.extent.YMax

RozdzielczoscPrzestrzenna = R.meanCellWidth  # zakładamy kwadratowe piksele
# ===================================================================
# CONVERT TO NUMPY ARRAY (NODATA → np.nan)
# ===================================================================
nodata_value = R.noDataValue  # pobieramy wartość NoData z rastra
if nodata_value is None:
    nodata_value = -9999  # jeśli raster nie ma NoData, ustaw tymczasowe

# ===================================================================
# PRZEJŚCIE DO TABLICY NUMPY
# ===================================================================
R_array = arcpy.RasterToNumPyArray(R, nodata_to_value=np.nan)

# ===================================================================
# MIN i MAX – WARTOŚCI ORAZ WSPÓŁRZĘDNE
# ===================================================================

# 1. Obliczamy wartości min i max np.nanmin()
min_val = np.nanmin(R_array)
max_val = np.nanmax(R_array)

print(f"MIN wartość: {min_val}, MIN z rastra: {R.minimum}")
print(f"MAX wartość: {max_val}, MAX z rastra: {R.maximum}")

# ==========================
# 4. SZUKANIE MINIMUM I MAKSIMUM W TABLICY
# ==========================
# nanargmin / nanargmax ignorują wartości np.nan
min_flat = np.nanargmin(R_array)
max_flat = np.nanargmax(R_array)
print(min_flat, max_flat)

# # 2. Szukamy indeksów (wiersz, kolumna) dla min i max
# min_rows, min_cols = np.where(R_array == min_val)
# max_rows, max_cols = np.where(R_array == max_val)

# # Jeżeli jest wiele pikseli z tą samą wartością, bierzemy pierwszy
# min_row, min_col = int(min_rows[0]), int(min_cols[0])
# max_row, max_col = int(max_rows[0]), int(max_cols[0])

# print(f"MIN indeks tablicy (wiersz, kolumna): ({min_row}, {min_col})")
# print(f"MAX indeks tablicy (wiersz, kolumna): ({max_row}, {max_col})")

# # 3. Przeliczamy indeksy na współrzędne X, Y
# # Kolumna -> X rośnie w prawo od XMin
# # Wiersz -> Y maleje w dół od YMax (bo w tablicy [0,0] to górny-lewy róg)
# cell = RozdzielczoscPrzestrzenna

# min_x = XMin + min_col * cell
# min_y = YMax - min_row * cell

# max_x = XMin + max_col * cell
# max_y = YMax - max_row * cell

# print(f"MIN współrzędne XY: ({min_x}, {min_y})")
# print(f"MAX współrzędne XY: ({max_x}, {max_y})")

# # Możesz też stworzyć obiekty Point, jeśli chcesz:
# pt_min = arcpy.Point(min_x, min_y)
# pt_max = arcpy.Point(max_x, max_y)

# print("Punkt MIN:", pt_min)
# print("Punkt MAX:", pt_max)

# # ===================================================================
# # DALSZE OBLICZENIA NA TABLICY (JEŚLI CHCESZ JE ZOSTAWIĆ)
# # ===================================================================
# # Przykład z Twojego skryptu – modyfikacja fragmentu rastra
# # R_array[200:400, 200:400] = -2  # przykładowa operacja

# # ===================================================================
# # PRZEJŚCIE Z TABLICY NUMPY DO RASTRA
# # ===================================================================
# # Tu lewy dolny punkt do zapisu nowego rastra:
# # LewyDolnyPunkt = arcpy.Point(R.extent.XMin, R.extent.YMin)

# # outR = arcpy.NumPyArrayToRaster(
# #     R_array,
# #     LewyDolnyPunkt,
# #     RozdzielczoscPrzestrzenna,
# #     value_to_nodata=NoData
# # )

# # outR.save("NowyRaster02")

print("KONIEC")
