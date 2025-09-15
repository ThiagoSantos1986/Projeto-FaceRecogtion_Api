from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin, LoginManager
# from flask_admin.contrib.sqla import ModelView


db = SQLAlchemy()
# login_manager = LoginManager()

def configure(app):
    
    db.init_app(app)
    # login_manager.init_app(app)
    app.db = db

# @login_manager.user_loader
# def load_user(id_user):                          
#     return User.query.get(int(id_user))


class User(db.Model):
    __tablename__ = 'user'
    
    id_user = db.Column(db.Integer, autoincrement=True,  primary_key=True)
    nome  =  db.Column(db.String(86), nullable=False)
    cpf_user = db.Column(db.String(30), nullable=False, unique=True)
    email =  db.Column(db.String(84), nullable=False, unique=True) 
    senha = db.Column(db.String(256), nullable=False) 
    
    def __init__(self, nome, cpf_user, email, senha):
        self.nome = nome
        self.cpf_user = cpf_user
        self.email = email
        self.senha = generate_password_hash(senha) #salvar senha encript
    
    def get_id(self):
           return (self.id_user)
       
    def verify_password(self, pwd):
        return check_password_hash(self.senha, pwd)
    
            
class Pessoa(db.Model):
    
    id_pessoa = db.Column(db.Integer, autoincrement=True,  primary_key=True)
    nome = db.Column(db.String(50))
    cpf_pessoa = db.Column(db.String(20))
    foto_perfil = db.Column(db.LargeBinary)
    encoding =  db.relationship("Encoding", backref='pessoa')        
    imagens =  db.relationship("Imagens", backref='pessoa')        
    observacoes =  db.relationship('Observacoes', back_populates="pessoa")        

    def __init__(self, nome, cpf_pessoa, foto_perfil):
        
        self.nome = nome
        self.cpf_pessoa = cpf_pessoa
        self.foto_perfil = foto_perfil

    def __str__(self):
        return self.nome
          
class Encoding(db.Model):
    
    id_encoding = db.Column(db.Integer, autoincrement=True,  primary_key=True)
    id_pessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id_pessoa'), nullable=False)
    encoding = db.Column(db.LargeBinary)         

    def __init__(self, id_pessoa, encoding):
    
        self.id_pessoa = id_pessoa
        self.encoding = encoding       

class Imagens(db.Model):
    
    id_imagens = db.Column(db.Integer, autoincrement=True,  primary_key=True)
    id_pessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id_pessoa'), nullable=False)
    nome_imagem = db.Column(db.String(100))
    imagens = db.Column(db.LargeBinary)         

    def __init__(self, id_pessoa, nome_imagem, imagens):
    
        self.id_pessoa = id_pessoa
        self.nome_imagem = nome_imagem
        self.imagens = imagens  
        

class Observacoes(db.Model):
    
    id_observacoes = db.Column(db.Integer, autoincrement=True,  primary_key=True)
    relato = db.Column(db.Text)      
    criado_em = db.Column(db.DateTime)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id_pessoa'), nullable=False)
    pessoa = db.relationship("Pessoa", back_populates="observacoes")
    
    def __init__(self, pessoa_id, relato, criado_em):
    
        self.id_pessoa = pessoa_id
        self.relato = relato
        self.criado_em = criado_em 
   
        
# class ObsevacoesView(ModelView):
    
#     can_delete = False
#     form_columns = ['pessoa', 'criado_em', 'relato']
#     column_list =  ['pessoa', 'criado_em', 'relato']

