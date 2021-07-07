import rasterio.mask
import pickle
import os

# importing sys
infile = open("index.pickle", 'rb')
dic = pickle.load(infile)
keys = dic.keys()
fichier_prec = 0

for i, k in enumerate(keys):
    try:
        infos = k.split("-")
        fichier = infos[0]
        dossier = infos[1]
        abs = infos[2]
        ord = infos[3]


        if os.path.exists("tiff_decoupe_DTM/" + abs + "-" + ord + ".tif"):
            continue

        lt, lb, rb, rt = dic[k]

        masker_shp = [{'type': 'Polygon', 'coordinates': [[lt, lb, rb, rt]]}]
        if fichier != fichier_prec:
            fichier_prec = fichier
            tiff = "Data/tiff/DHMVIIDTMRAS1m_" + fichier + ".tif"
            try:
                src.close()
            except:
                pass
            src = rasterio.open(tiff)

        out_image, out_transform = rasterio.mask.mask(src, shapes=masker_shp, crop=True)
        out_meta = src.meta

        # print(f'out meta :{out_meta}')

        out_meta.update({"driver": "GTiff",
                        "height": out_image.shape[1],
                        "width": out_image.shape[2],
                        "transform": out_transform})

        with rasterio.open("tiff_decoupe_DTM/" + abs + "-" + ord + ".tif", "w", **out_meta) as dest:
            dest.write(out_image)

        if i % 1000 == 1:
            print(i)
    except:
        print('Error on:',  "tiff_decoupe_DTM/" + abs + "-" + ord + ".tif")
src.close()