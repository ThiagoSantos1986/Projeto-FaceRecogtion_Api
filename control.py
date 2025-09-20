from ast import Return
import base64
import io
import pathlib
from PIL import Image
import face_recognition
import os
from flask import Flask
import numpy as np 
import cv2

pathlib.Path('static').mkdir(exist_ok=True)
UPLOAD_FOLDER = "static/uploads/"

# Diretório que contém as imagens de rostos para treinamento
database_path = UPLOAD_FOLDER

def facematch(file1, file2):
    
    query_image = face_recognition.load_image_file(file1, mode='RGB')# recebendo imagem 
    query_image1 = face_recognition.load_image_file(file2, mode='RGB')# recebendo imagem 
    
    try:
        query_encoding = face_recognition.face_encodings(query_image)[0] # criando encoding imagem
        query_encoding1 = face_recognition.face_encodings(query_image1)[0] # criando encoding imagem
        
        matches = face_recognition.compare_faces([query_encoding], query_encoding1)
        
        distances = face_recognition.face_distance([query_encoding], query_encoding1)
        
        for i, face_distance in enumerate(distances):
            print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i))
            print("Is the unknown face a new person that we've never seen before? {}".format(not True in distances))
            # print("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
            # print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(face_distance < 0.5))
            print()
        
        if True in matches :
        
            return "ROSTOS CORRESPONDEM!!" , "success"

        return "ROSTOS NÃO CORRESPONDEM!!" , "warning"
        
        # print(distances)
    
    except IndexError:
        print(IndexError)
        # print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        
    return ("Não consegui localizar nenhum rosto em pelo menos uma das imagens. Verifique os arquivos de imagem." ,  "danger")
    

#funcao que encotra o rosto e retorna o encoding e o rosto recortado.
def detect_faces_in_image(file_stream, name_arq):
    
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream, mode='RGB')
    face_locations = face_recognition.face_locations(img)  
    encoding = face_recognition.face_encodings(img)[0]    
    encoding = np.array(encoding, dtype=np.float64).tobytes()
    
    face_imgs_path = [] 
    
   #codico para salvar e nomear o rosto localizado
    for face_location in face_locations:
        
        top, right, bottom, left = face_location
        face_image = img[top:bottom, left:right]
        pil_image = Image.fromarray(face_image) 
        # pil_image_name = 'FACE'  + '_' + os.path.basename(file_stream)
        pil_image_name = 'NEW_FACE'  + '_' + name_arq
        
        pil_image.save(os.path.join(UPLOAD_FOLDER, pil_image_name)) #salvando rosto na pasta
        face_imgs_path.append(os.path.join(UPLOAD_FOLDER, pil_image_name)) # endereco do rosto salvo
        
        face = filetobyte(face_imgs_path[0]) # vai no rosto salvo e transforma em bytes
        
    return  encoding, face

# Função para consultar rostos na base de dados
def find_face(face_database, face_image):
    # Carrega a imagem de consulta e gera o encoding
    query_image = face_recognition.load_image_file(face_image, mode='RGB')
    query_encoding = face_recognition.face_encodings(query_image)

    if not query_encoding:
        return ['Rosto não localizado na foto enviada para consulta', 1]

    query_encoding = query_encoding[0]

    # Pré-processa os encodings da base de dados
    database_encodings = np.array([np.frombuffer(face.encoding, dtype=np.float64) for face in face_database])

    # Calcula as distâncias entre o encoding de consulta e os encodings da base
    distances = face_recognition.face_distance(database_encodings, query_encoding)

    # Encontra o índice do menor valor de distância
    min_distance_index = np.argmin(distances)

    # Verifica se a menor distância está dentro da tolerância
    if distances[min_distance_index] <= 0.60:
        return face_database[min_distance_index].id_pessoa

    return ["Rosto não encontrado na base de dados", "not found"]

def filetobyte(file_path: str) -> bytes:
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"O arquivo '{file_path}' não foi encontrado.")

    try:
        with open(file_path, 'rb') as arq:
            return arq.read()
    except IOError as e:
        raise IOError(f"Erro ao ler o arquivo '{file_path}': {e}")


