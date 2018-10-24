'''
Desafio leitura arquivos tif
separar usando um arquivo geojson
calcular NDVI
criacao csv

Um dos problemas foi descobrir quais pacotes são utilizados
achei este rasterio que le os arquivos tif
Sobre as bandas de cores nao esta muito claro
e nao entendo muito bem deste assunto, mas fiz o calculo do nvdi
utilizando o numpy.

neste examplo main e lido um arquivo de teste
feito o split com o geojson e depois calculado o nvdi e criado um csv

este foi o modelo basico para teste


'''
import rasterio
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import json
from matplotlib import pyplot
import glob
from rasterio.mask import mask
import csv

geifile = 'gleba01.geojson'
listfiles = (glob.glob("IMAGENS_PLANET/*.tif"))

'''
Primeiro Desafio
leitura arquivo e calculo nvdi
'''

#Arquivo teste
file = '/home/andre/Documentos/zonasul/DESAFIO_PYTHON/IMAGENS_PLANET/20170916_125749_0f38.tif'


dataset = rasterio.open(file)
#red
b3 = dataset.read(3)
#infrared
b4 = dataset.read(4)

ndvi = np.zeros(b3.shape, dtype=rasterio.uint16)
ndvi = (b4.astype(float)-b3.astype(float))/(b4+b3)
ndvi = np.nan_to_num(ndvi)
#Imagem convertida
#pyplot.imshow(ndvi)#, cmap='pink')
#pyplot.show()
#Imagem convertida
'''
Segundo Desafio
'''

with open('gleba01.geojson') as f:
    data = json.load(f)
geoms = [data['features'][0]['geometry']]



#TODO nao consegui fazer aparecer o limit do geoms
with rasterio.open(file) as src:
     out_image, out_transform = mask(src, geoms, crop=True)

out_meta = src.meta.copy()

# save the resulting raster
out_meta.update({"driver": "GTiff",
    "height": out_image.shape[1],
    "width": out_image.shape[2],
"transform": out_transform})

with rasterio.open("masked.tif", "w", **out_meta) as dest:
    dest.write(out_image)

filemask='masked.tif'
dataset = rasterio.open(filemask)

b3 = dataset.read(3)
b4 = dataset.read(4)
ndvi = np.zeros(b3.shape, dtype=rasterio.uint16)
ndvi = (b4.astype(float)-b3.astype(float))/(b4+b3)
ndvi = np.nan_to_num(ndvi)


#pyplot.imshow(ndvi)#, cmap='pink')
#pyplot.show()


'''
Terceiro Desafio
'''
media = np.median(ndvi)
print('media ndvi: {}'.format(media))

'''
Quarto Desafio
'''

data = file.split('/')[-1].split('_')
data = data[0]+data[1]
header = ['data','media']
with open('data.csv', 'wt', newline ='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(i for i in header)
    writer.writerow([data,media])
