import os
import sys
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

INPUT_FOLDER =  'images'
NEGATIVO = True
THRESHOLD = 0.8  # 0.8 arroz e 0.3 texto
ALTURA_MIN = 0
LARGURA_MIN = 0
N_PIXELS_MIN = 0  # 100 arroz e 20 texto
N_PIXELS_MAX = 100000
ARROZ = 1.0
NO_ARROZ = 0.0

# JANELA = 33
# MARGEM = math.floor(JANELA/2)