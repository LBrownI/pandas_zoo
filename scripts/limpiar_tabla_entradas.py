import os
import pandas as pd

ruta = os.path.join('zoo_dataset', 'entradas_zoo_sucio_generado.csv')

loaded = pd.read_csv(ruta)
display(loaded)