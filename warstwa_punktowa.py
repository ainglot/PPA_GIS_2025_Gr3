import arcpy

# ===================================================================
# KONFIGURACJA ŚRODOWISKA
# ===================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr3.gdb"
warstwa_drzew = "GDA2020_OT_OIPR_P"

cursor = arcpy.da.SearchCursor(warstwa_drzew, ["SHAPE@X", "SHAPE@Y"])
for row in cursor:
    print(row)


print("KONIEC")