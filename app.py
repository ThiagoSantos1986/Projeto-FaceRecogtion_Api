import base64
import os
import os.path as op
from waitress import serve
# from pkg_resources import resource_filename

from flask import Flask, request, jsonify

from control import UPLOAD_FOLDER, detect_faces_in_image, filetobyte, find_face


from model import Imagens, Pessoa, Encoding, configure

DATA_URL = (f"mysql://root:xNUorSENSVWtMkQJcmHRSvXxTGNPkQKv@autorack.proxy.rlwy.net:17633/railway")

app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_DATABASE_URI'] = DATA_URL
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# configure(app)

# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# path = op.join(op.dirname(__file__), 'static/uploads/')

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS    


# @app.route('/consulta_api', methods=['POST'])
# def consultaApi():
    
#     if request.method == 'POST':
        
#         face_data_base = Encoding.query.order_by(Encoding.encoding.desc()).all()

        
#         if 'file' not in request.files:
            
#             return jsonify({'status': 'error'}), 500
            
#         file = request.files['file']
        
#         if file and allowed_file(file.filename):
            
#             filename = "desconhecido.jpg"
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)
            
            
#         id = find_face(face_data_base, file_path)
        
#         if isinstance(id, int):    
            
#             query_pessoa = Pessoa.query.filter_by(id_pessoa=id).first() #pega a pessoa
#             foto_perfil =  query_pessoa.foto_perfil
#             img_b64 = base64.b64encode(foto_perfil).decode()
#             # endereco  = str('https://localhost:3000/perfil')


#             dict_result = {
#                 'nome': query_pessoa.nome,
#                 'cpf': query_pessoa.cpf_pessoa, 
#                 'teste': img_b64
#                 # 'url': f"{endereco}/{query_pessoa.id_pessoa}"
#             }
           
            
#             return jsonify(dados=dict_result ), 200
        
#         return jsonify(dados={'status': 'Rosto nao Localizado'}), 404
    
# @app.route('/cadastro', methods=['POST'])
# def cadastro():
    
#     data = request.get_json()# verificar regex cpf

#     # Verifica se os campos obrigatórios estão presentes
#     if not data or 'nome' not in data or 'cpf' not in data:
#         return jsonify({'status': 'error', 'message': 'Campos obrigatórios não fornecidos'}), 400

#     nome = data['nome'].upper()
#     cpf = formatar_cpf(data['cpf'])  # Aplica a máscara ao CPF

#     # Verifica se o CPF já está cadastrado
#     if Pessoa.query.filter_by(cpf_pessoa=cpf).first():
#         return jsonify({'status': 'error', 'message': 'CPF já cadastrado'}), 409
    
    
#     file_path = os.path.join(UPLOAD_FOLDER, f"desconhecido.jpg")
    
#     encoding, face_profile = detect_faces_in_image(file_path, f"desconhecido.jpg")  
#     image_original = filetobyte(file_path) 
    
#     # Cria um novo registro de pessoa
#     new_pessoa = Pessoa(nome=nome, cpf_pessoa=cpf, foto_perfil=face_profile)
   
#     try:
#         # Adiciona ao banco de dados
       
#         app.db.session.add(new_pessoa)
#         app.db.session.commit()
        
#         id_pessoa = new_pessoa.id_pessoa
#         new_encoding = Encoding(id_pessoa=id_pessoa, encoding=encoding)
#         app.db.session.add(new_encoding)
#         app.db.session.commit()
        
#         new_imagem = Imagens(id_pessoa=id_pessoa, nome_imagem=f"{nome}.jpg", imagens=image_original)
#         app.db.session.add(new_imagem)
#         app.db.session.commit()

#         return jsonify({'status': 'success', 'message': 'Usuário cadastrado com sucesso'}), 201
    
#     except Exception as e:
#         app.db.session.rollback()
#         return jsonify({'status': 'error', 'message': 'Erro ao cadastrar usuário', 'error': str(e)}), 500
        
# def formatar_cpf(cpf):
  
#     cpf = ''.join(filter(str.isdigit, cpf))  # Remove qualquer caractere não numérico
#     return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else cpf 

           
if __name__ == "__main__":
   
    app.run(debug=True, host='localhost', port=3000)
    # serve(app, host='0.0.0.0', port=3000)
    
