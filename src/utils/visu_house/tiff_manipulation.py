import rioxarray as rxr
import rasterio
import rasterio.mask
import rasterio.merge

def substract_dtm_dsm(dtm, dsm):
    '''
    Take a dsm and a dtm, do a substraction and create a chm
    '''
    # with rasterio.open(dtm) as src:
    #     lidar_dem_im = src.read(1, masked=True)
    #     sjer_ext = rasterio.plot.plotting_extent(src)

    # with rasterio.open(dsm) as src:
    #     lidar_dsm_im = src.read(1, masked=True)
    #     dsm_meta = src.profile

    lidar_dem_xr = rxr.open_rasterio(dtm, masked=True).squeeze()
    lidar_dsm_xr = rxr.open_rasterio(dsm, masked=True).squeeze()
    lidar_chm_xr = lidar_dsm_xr - lidar_dem_xr
    lidar_chm_xr.rio.to_raster("chm.tif")

def merge_tif(list_tif):
    liste = []
    for tif in list_tif:
        locals()[tif] = rasterio.open(f"/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/{tif}")
        liste.append(locals()[tif])
        rasterio.merge.merge(liste, dst_path= "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/merged.tif")

    for tif in list_tif:
        locals()[tif] = rasterio.open(f"/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/{tif}")
        liste.append(locals()[tif])
        rasterio.merge.merge(liste, dst_path= "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/merged.tif")
    
    return "merged.tif"

def mask_chm(bounding_box):
    shapes = [feature for feature in bounding_box]
    print(shapes)
    with rasterio.open("chm.tif") as src:
        print(src.bounds)
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta
        out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    with rasterio.open("masked_chm.tif", "w", **out_meta) as dest:
        dest.write(out_image)
