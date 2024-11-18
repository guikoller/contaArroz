import os
import sys
import cv2
import numpy as np

INPUT_FOLDER =  'images'
NEGATIVO = False
THRESHOLD = 0.8  # 0.8 arroz e 0.3 texto
ALTURA_MIN = 1000
LARGURA_MIN = 1000
N_PIXELS_MIN = 100  # 100 arroz e 20 texto
ARROZ = 1.0
NO_ARROZ = 0.0

# JANELA = 33
# MARGEM = math.floor(JANELA/2)