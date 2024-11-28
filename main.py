#===============================================================================
# Exemplo: Trabalho 4.
#-------------------------------------------------------------------------------
# Alunos: Guilherme Corrêa Koller e Mayara Dal Vesco Hoger
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import os
import sys
from countRice import *

INPUT_FOLDER =  'images'

def open_all_images(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".bmp"):
            img_path = os.path.join(folder, filename)
            img = open_image(img_path)
            if img is not None:
                images.append((img, filename))
    return images

def open_image(img_name):
    img = cv2.imread (img_name, cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()
    return img

def draw_components(img, components):
    img_out = img.copy()
    for c in components:
        cv2.rectangle (img_out, (c['coordenadas']['L'], c['coordenadas'] ['T']), (c['coordenadas'] ['R'], c['coordenadas'] ['B']), (1,0.8,0.9))
    return img_out

def main():
    images = open_all_images(INPUT_FOLDER)
    for img, filename in images:
        expected = filename.split('.')[0]
        img_out = img.copy()
        img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2GRAY)
        result = countRice(img_out, filename)      
        cv2.imwrite('output/' + filename, draw_components(img, result['components']))
        print("Expected: %s, Result: %s\n" % (expected, result['quantity']))
    
    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == "__main__":
    main()
