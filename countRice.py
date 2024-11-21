from constants import *

def binariza (img, threshold):
    return np.where(img > threshold, ARROZ, NO_ARROZ)

def binariza_limiar_adaptativo(img, janela):
    normalizada = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    bilateral = cv2.bilateralFilter(normalizada, 21, 55, 55) 
    limiar = cv2.adaptiveThreshold(bilateral, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, janela, 2)
    return limiar

def erosao(img, components):
    # fazer erosão apenas nos blobs grandes
    kernel = np.ones((9, 9), np.uint8) 

    #itera pelos compments
    # os que tiverem numero de pixel maior, faz a erosao daquela parte da imagem
    media_pixels = 80
    for componente in components:
        if componente["n_pixels"] > media_pixels:
            img_aux = img[componente["coordenadas"]["B"]:componente["coordenadas"]["T"], componente["coordenadas"]["L"]:componente["coordenadas"]["R"]]
            if len(img_aux) != 0:
                img_aux = cv2.erode(img_aux, kernel) 
            img[componente["coordenadas"]["B"]:componente["coordenadas"]["T"], componente["coordenadas"]["L"]:componente["coordenadas"]["R"]] = img_aux
    
    return img


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

def rotula (img, largura_min, altura_min, n_pixels_min, n_pixels_max):
    list_componentes = []
    label = 2
    for linha, value in enumerate(img):
        for coluna, pix in enumerate (value):
            if pix == ARROZ:
                n_pixels, coordenadas = inunda(label, img, linha, coluna, n_pixels=0, coordenadas={'T': linha, 'L': coluna, 'B': linha, 'R':coluna})
                # verificar ruídos
                if (n_pixels < n_pixels_min or n_pixels > n_pixels_max)  and (coordenadas['T'] - coordenadas['B']) < altura_min and (coordenadas['R'] - coordenadas['L']) < largura_min: #ruído
                    np.where(img == label, NO_ARROZ, img) #coloca como fundo onde tem ruído
                else: # não ruído
                    componente = {'label': label, 'n_pixels': n_pixels, 'coordenadas': coordenadas} # salva o arroz
                    list_componentes.append(componente)
                    label = label + 1

    return (list_componentes)

def pinta_fundo(img, n_pixels_max):
    label = 2
    for linha, value in enumerate(img):
        for coluna, pix in enumerate (value):
            if pix == ARROZ:
                n_pixels, _ = inunda(label, img, linha, coluna, n_pixels=0, coordenadas={'T': linha, 'L': coluna, 'B': linha, 'R':coluna})
                # verificar ruídos
                if n_pixels > n_pixels_max:
                    img = np.where(img == label, NO_ARROZ, img) #coloca como fundo onde tem ruído
                else: # não ruído
                    label = label + 1

    img = np.where(img == NO_ARROZ, NO_ARROZ, ARROZ)
    return img

def countRice(img, filename):    
    #img = binariza(img, THRESHOLD)    
    img = binariza_limiar_adaptativo(img, 31) #.astype (np.uint8)*255
    cv2.imwrite("binarizada_limiar/"+filename, img)
    img = np.where(img == 255, ARROZ, NO_ARROZ)

    # pinta o fundo de preto, inundando
    img = pinta_fundo(img, N_PIXELS_MAX)

    cv2.imwrite("fundo/"+filename, img*255)
    img = img.astype (np.float32)
    components = rotula(img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN, N_PIXELS_MAX)
    return {'quantity': len(components), 'components': components}