from constants import *

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

def rotula (img):
    list_componentes = []
    label = 2
    for linha, value in enumerate(img):
        for coluna, pix in enumerate (value):
            if pix == ARROZ:
                n_pixels, coordenadas = inunda(label, img, linha, coluna, n_pixels=0, coordenadas={'T': linha, 'L': coluna, 'B': linha, 'R':coluna})
                componente = {'label': label, 'n_pixels': n_pixels, 'coordenadas': coordenadas} # salva o arroz
                list_componentes.append(componente)
                label = label + 1

    return (list_componentes)

def estimate_blob_size(components):
    sizes = sorted(componente['n_pixels'] for componente in components)  
  
    list_diff = []
    for i in range(len(sizes)-1):
        list_diff.append(round(sizes[i+1] - sizes[i]))
    
    print(sizes)

    for i in range(len(sizes)-1):
        diff = sizes[i+1] - sizes[i]
        single_list = sizes
        if diff > 200:
            single_list = sizes[:i]
            print(i)
            break
        
            # o menor valor tem que ser mais ou menos a metade do tamanho do arroz mediano
            # o valor mediano tem que ser no máximo 2,5 vezes maior que o menor valor
            # desconsiderar os outros menores valores

    for i in range(len(single_list)-1):
        if np.median(single_list)/single_list[i] < 2: #esse é o local de corte
            print(np.median(single_list[i:]))
            return np.median(single_list[i:])
    
    return np.median(sizes)
    lower_third = sizes[:len(sizes) // 3]
    return sum(lower_third) / len(lower_third)

def estimate_quantity(components, avg_blob_size):
    estimated_quantity = 0
    for component in components:
        if component['n_pixels'] > avg_blob_size:
            estimated_quantity += math.floor(component['n_pixels'] / avg_blob_size)
            if round(component['n_pixels'] / avg_blob_size) != 1.0:
                #print((component['n_pixels'] / avg_blob_size))
                pass
        else:
            estimated_quantity += 1
    return estimated_quantity

def countRice(img, filename): 
    img = cv2.medianBlur(img, 11)
    # cv2.imshow("median/"+filename, img) 
    img = cv2.GaussianBlur(img, (7, 7), 0)
    # cv2.imshow("gaussian/"+filename, img)
    img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    # cv2.imshow("normalize/"+filename, img)
    img = cv2.Canny(img, 50, 150)
    # cv2.imshow("canny/"+filename, img)
    
    kernel = np.array([[0, 1, 0], 
                       [1, 1, 1], 
                       [0, 1, 0]], dtype=np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    # cv2.imshow("dilated/"+filename, img)
    
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.drawContours(img, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
    cv2.imshow("flooded/"+filename, img)

    img = img.astype (np.float32)/ 255.0
    components = rotula(img)
    quantity = estimate_quantity(components, estimate_blob_size(components))
    
    return {'quantity': quantity, 'components': components}