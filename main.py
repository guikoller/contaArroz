#===============================================================================
# Exemplo: Trabalho 4.
#-------------------------------------------------------------------------------
# Alunos: Guilherme Corrêa Koller e Mayara Dal Vesco Hoger
# Universidade Tecnológica Federal do Paraná
#===============================================================================

from constants import *
from countRice import *

sys.setrecursionlimit(1000000000)
def open_all_images(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".bmp"):
            img_path = os.path.join(folder, filename)
            img = open_image(img_path)
            if img is not None:
                images.append((img, filename))
    return images

def open_image(img_name, grayscale=True):
    img = cv2.imread (img_name, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()
    return img.astype (np.float32) / 255.0

def draw_components(img, components):
    img_out = img.copy()
    for c in components:
        cv2.rectangle (img_out, (c['coordenadas']['L'], c['coordenadas'] ['T']), (c['coordenadas'] ['R'], c['coordenadas'] ['B']), (0,1,1))
    return img_out

def verify_image_components(images):
    for img, filename in images:
        expected = filename.split('.')[0]
        result = countRice(img)
        
        cv2.imwrite('output/' + filename, draw_components(img, result['components'])*255)
        print("Expected: %s, Result: %s" % (expected, result['quantity']))

def main():
    images = open_all_images(INPUT_FOLDER)
    verify_image_components(images)

if __name__ == "__main__":
    main()