'''
Este seria um caso caso as contas estejam corretas do desafio 4
onde e feito a leitura de todos os arquivos da pasta IMAGENS_PLANET
feito o SPLIT com o geojson e calculado o NDVI
'''
import rasterio
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import json
from matplotlib import pyplot
import glob
from rasterio.mask import mask
import csv

with open('gleba01.geojson') as f:
    data = json.load(f)
geoms = [data['features'][0]['geometry']]


listfiles = (glob.glob("IMAGENS_PLANET/*.tif"))

def CLIPNVDI(file):

    with rasterio.open(file) as src:
         out_image, out_transform = mask(src, geoms, crop=True)

    out_meta = src.meta.copy()

    # save the resulting raster
    out_meta.update({"driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
    "transform": out_transform})

    with rasterio.open("maskedonebuone.tif", "w", **out_meta) as dest:
        dest.write(out_image)

    filemask='maskedonebuone.tif'
    dataset = rasterio.open(filemask)

    b3 = dataset.read(3)
    b4 = dataset.read(4)
    ndvi = np.zeros(b3.shape, dtype=rasterio.uint16)
    ndvi = (b4.astype(float)-b3.astype(float))/(b4+b3)
    ndvi = np.nan_to_num(ndvi)

    return ndvi

def calcmedium(file):
    media = np.median(CLIPNVDI(file))

    data = file.split('/')[-1].split('_')
    data = data[0]+data[1]
    return data, media

header = ['data','media']
with open('dataall.csv', 'wt', newline ='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(i for i in header)
    for file in listfiles:
        data, media = calcmedium(file)
        writer.writerow([data,media])
