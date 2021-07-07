from PIL import Image
import rasterio
import pickle
#image = Image.open('Data/DSM/GeoTIFF/DHMVIIDSMRAS1m_k43.tif')
#for x in range
dictionnaire = dict()
pas = 1000
for i in range(1,44,1):
    if i < 10:
        num = "0"+str(i)
    else:
        num = str(i)
    with rasterio.open("Data/tiff/DHMVIIDSMRAS1m_k"+num+".tif") as src:
        l, b, r, t = src.bounds
        l = int(l)
        b = int(b)
        r = int(r)
        t = int(t)

        for y in range(t, b, -pas):
            for x in range(l, r, pas):
                name = "k"+num+"-DSM-"+str(x)+"-"+str(y)
                #lt, lb, rb, rt
                dictionnaire[name] = [(x, y), (x,y-pas), (x+pas, y-pas), (x+pas, y)]
print(dictionnaire)
with open('index.pickle', 'wb') as handle:
    pickle.dump(dictionnaire, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(len(dictionnaire))