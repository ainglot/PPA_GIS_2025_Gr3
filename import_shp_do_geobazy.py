import arcpy
import os
import shutil

# ===================================================================
# KONFIGURACJA ŚCIEŻEK
# ===================================================================
# Ścieżka do folderu ze źródłowymi plikami SHP (BDOT10k, 2014)
folder_shp = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\2261_SHP_2014"

# Ścieżka do folderu roboczego – tu będą kopie z poprawionymi nazwami
folder_shp_new = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\new_2261_SHP_2014"

# Geobaza docelowa – tu będą eksportowane warstwy
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr3.gdb"

# Ustawienie nadpisywania (ważne przy wielokrotnym uruchamianiu)
arcpy.env.overwriteOutput = True

# ===================================================================
# ETAP 1: KOPIOWANIE I POPRAWIANIE NAZW PLIKÓW SHP
# ===================================================================
print("ETAP 1: Kopiowanie plików SHP i zmiana kropek na podkreślenia...")

# Sprawdzenie, czy folder docelowy istnieje – jeśli nie, utwórz
if not os.path.exists(folder_shp_new):
    os.makedirs(folder_shp_new)
    print(f"  → Utworzono folder: {folder_shp_new}")

# Przetwarzanie wszystkich plików w folderze źródłowym
for file in os.listdir(folder_shp):
    # Pełna ścieżka pliku źródłowego
    src_path = os.path.join(folder_shp, file)
    
    # Pomijamy foldery – tylko pliki
    if not os.path.isfile(src_path):
        continue

    # Rozdzielenie nazwy i rozszerzenia
    name, ext = os.path.splitext(file)
    
    # Zamiana kropek w nazwie na podkreślenia (np. "OT.PT.A" → "OT_PT_A")
    new_name = name.replace(".", "_") + ext.lower()  # .SHP → .shp (standaryzacja)
    
    # Pełna ścieżka docelowa
    dst_path = os.path.join(folder_shp_new, new_name)
    
    # Kopiowanie pliku (z nadpisywaniem)
    shutil.copy(src_path, dst_path)
    print(f"  → Skopiowano: {file} → {new_name}")

# ===================================================================
# ETAP 2: EKSPORT TYLKO PLIKÓW .SHP DO GEOBAZY (z nową nazwą)
# ===================================================================
print("\nETAP 2: Eksport plików .shp do geobazy...")

# Przetwarzanie tylko plików .shp w folderze roboczym
for file in os.listdir(folder_shp_new):
    src_path = os.path.join(folder_shp_new, file)
    
    # Sprawdzenie, czy to plik .shp
    name, ext = os.path.splitext(file)
    if ext.lower() != ".shp":
        continue  # Pomijamy .shx, .dbf, .prj itp.

    print(f"  Przetwarzanie: {file}")

    # PRZYKŁAD NAZWY: GDA2014_OT_PTTR_A_gr3__2261.shp
    # Chcemy wydobyć część po "__" → "2261"
    if "__" in name:
        # Podział na część przed i po "__"
        czesc_po = name.split("__", 1)[1]  # [1] = wszystko po pierwszym "__"
        print(f"     → Wydobyto kod: {czesc_po}")
    else:
        # Jeśli nie ma "__", użyj całej nazwy (lub pomiń)
        czesc_po = name
        print(f"     → Brak '__' – używam pełnej nazwy: {czesc_po}")

    # Nowa nazwa warstwy w geobazie: GDA2014_2261
    nowa_nazwa_w_geobazie = f"GDA2014_{czesc_po}"
    
    # Sprawdzenie, czy nazwa jest poprawna dla ArcGIS (bez spacji, znaków specjalnych)
    nowa_nazwa_w_geobazie = arcpy.ValidateTableName(nowa_nazwa_w_geobazie)

    # Eksport do geobazy
    try:
        arcpy.conversion.ExportFeatures(src_path, nowa_nazwa_w_geobazie)
        print(f"     → Eksportowano do geobazy: {nowa_nazwa_w_geobazie}")
    except arcpy.ExecuteError:
        print(f"     → BŁĄD eksportu: {arcpy.GetMessages()}")
    except Exception as e:
        print(f"     → Nieoczekiwany błąd: {e}")

# ===================================================================
# ZAKOŃCZENIE
# ===================================================================
print("\nKONIEC – przetwarzanie zakończone pomyślnie!")