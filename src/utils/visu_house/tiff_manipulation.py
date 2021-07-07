import rioxarray as rxr
import rasterio
import rasterio.mask
import rasterio.merge

def substract_dtm_dsm(dtm, dsm):
    # open the digital terrain model     
    with rasterio.open(dtm) as src:
        lidar_dem_im = src.read(1, masked=True)
        # sjer_ext = rasterio.plot.plotting_extent(src)

    # open the surface terrain model 
    with rasterio.open(dsm) as src:
        lidar_dsm_im = src.read(1, masked=True)
        dsm_meta = src.profile

    lidar_chm = lidar_dsm_im - lidar_dem_im
    # export chm as a new geotiff to use or share with colleagues
    with rasterio.open("dataset/chm.tif", 'w', **dsm_meta) as ff:
        ff.write(lidar_chm,1)

def merge_tif(list_tif):
    liste_dtm = []
    for tif in list_tif:
        locals()[tif] = rasterio.open(f"dataset/DTM/{tif}")
        liste_dtm.append(locals()[tif])

    rasterio.merge.merge(liste_dtm, dst_path= "dataset/DTM/merged.tif")

    liste_dsm = []
    for tif in list_tif:
        locals()[tif] = rasterio.open(f"dataset/DSM/{tif}")
        liste_dsm.append(locals()[tif])
    rasterio.merge.merge(liste_dsm, dst_path= "dataset/DSM/merged.tif")
    
    return "merged.tif"

def mask_chm(bounding_box):
    shapes = [feature for feature in bounding_box]
    with rasterio.open("dataset/chm.tif") as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta
        out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    with rasterio.open("dataset/masked_chm.tif", "w", **out_meta) as dest:
        dest.write(out_image)
