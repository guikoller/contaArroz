from constants import *

def binariza (img, threshold):
    return np.where(img > threshold, ARROZ, NO_ARROZ)

def inunda(label, img, linha, coluna, n_pixels, coordenadas):
    stack = [(linha, coluna)]
    while stack:
        linha, coluna = stack.pop()
        if coluna < coordenadas['L']:
            coordenadas['L'] = coluna
        if coluna > coordenadas['R']:
            coordenadas['R'] = coluna
        if linha < coordenadas['B']:
            coordenadas['B'] = linha
        if linha > coordenadas['T']:
            coordenadas['T'] = linha

        img[linha][coluna] = label
        n_pixels += 1

        if linha-1 >= 0 and img[linha-1][coluna] == ARROZ:
            stack.append((linha-1, coluna))
        if coluna-1 >= 0 and img[linha][coluna-1] == ARROZ:
            stack.append((linha, coluna-1))
        if linha+1 < img.shape[0] and img[linha+1][coluna] == ARROZ:
            stack.append((linha+1, coluna))
        if coluna+1 < img.shape[1] and img[linha][coluna+1] == ARROZ:
            stack.append((linha, coluna+1))

    return n_pixels, coordenadas

def rotula (img, largura_min, altura_min, n_pixels_min):
    list_componentes = []
    label = 2
    for linha, value in enumerate(img):
        for coluna, pix in enumerate (value):
            if pix == ARROZ:
                n_pixels, coordenadas = inunda(label, img, linha, coluna, n_pixels=0, coordenadas={'T': linha, 'L': coluna, 'B': linha, 'R':coluna})
                # verificar ruídos
                if n_pixels < n_pixels_min and (coordenadas['T'] - coordenadas['B']) < altura_min and (coordenadas['R'] - coordenadas['L']) < largura_min: #ruído
                    np.where(img == label, NO_ARROZ, img) #coloca como fundo onde tem ruído
                else: # não ruído
                    componente = {'label': label, 'n_pixels': n_pixels, 'coordenadas': coordenadas} # salva o arroz
                    list_componentes.append(componente)
                    label = label + 1

    return (list_componentes)


def countRice(img):    
    img = binariza(img, THRESHOLD)    
    components = rotula(img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    return {'quantity': len(components), 'components': components}