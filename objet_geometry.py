import arcpy

# ===================================================================
# KONFIGURACJA ŚRODOWISKA
# ===================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr3.gdb"
warstwa_poligonowa = "Budynki"

geometry = arcpy.management.CopyFeatures(warstwa_poligonowa, arcpy.Geometry())

for geo in geometry:
    print(geo)

print("KONIEC")