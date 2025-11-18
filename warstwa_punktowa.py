import arcpy

# ===================================================================
# KONFIGURACJA ŚRODOWISKA
# ===================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr3.gdb"
warstwa_drzew = "GDA2020_OT_OIPR_P_copy"

def odczytywanie_wspolrzednych(warstwa):
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:
            print(row)


def aktualizacja_wspolrzednych(warstwa):
    with arcpy.da.UpdateCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:
            row[0] += 100
            row[1] += 100
            print(row)
            cursor.updateRow(row) 

# odczytywanie_wspolrzednych(warstwa_drzew)
aktualizacja_wspolrzednych(warstwa_drzew)

print("KONIEC")