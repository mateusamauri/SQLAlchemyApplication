import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select

Base = declarative_base()

class Usuario(Base):
    __tablename__  = "usuario"

    id = Column(Integer, primary_key = True)
    nome = Column(String)
    nome_completo = Column(String)

    endereco = relationship("Endereco", back_populates="usuario", cascade= "all, delete-orphan")
    dadospessoais = relationship("DadosPessoais", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Usuario(id={self.id}, nome ={self.nome}, nomecompleto ={self.nome_completo})"

class Endereco(Base):
    __tablename__ = "endereco"

    id = Column(Integer, primary_key = True)
    logradouro = Column(String(60), nullable = False )
    email = Column(String(30))
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)

    usuario = relationship("Usuario", back_populates= "endereco")

    def __repr__(self):
        return f"Endereco(id={self.id}, logradouro ={self.logradouro}, email ={self.email})"
    
class DadosPessoais(Base):
    __tablename__ = "dadospessoais"

    id = Column(Integer, primary_key=True)
    cpf = Column(String(20), nullable=False)
    rg = Column(String (20))
    data_nascimento = Column(String(20), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="dadospessoais")

    def __repr__(self):
        return f"DadosPessoais(id={self.id}, cpf ={self.cpf}, rg ={self.rg}, datanascimento = {self.data_nascimento})"



#Conectando com o banco de dados
engine = create_engine("sqlite://")

#Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

inspetor = inspect(engine)

print(inspetor.get_table_names())

with Session(engine) as session:
    rodrigo = Usuario(
        nome = "rodrigo",
        nome_completo = "Rodrigo Fernandes",
        endereco = [Endereco(logradouro ="Rua Zeca de Julho" , email = "rodrigofernandes@email.com")],
        dadospessoais = [DadosPessoais(cpf = "03265412389", rg = "457082351", data_nascimento = "13/06/1988")]
    )

    fernando = Usuario(
        nome = "fernando",
        nome_completo = "Fernando Luiz Alves",
        endereco = [Endereco(logradouro ="Rua Thomas de Alvarenga", email = "fernandoalves@email.com")],
        dadospessoais = [DadosPessoais(cpf = "12345678902", data_nascimento = "28/12/1991")]
    )

    sandra = Usuario(
        nome = "sandra",
        nome_completo = "Sandra Lima Duarte",
        endereco = [Endereco(logradouro ="Rua Wanderley Osmar", email = "sandralima@email.com")],
        dadospessoais = [DadosPessoais(cpf = "05673155812", data_nascimento = "06/03/1978")]
    )

    marcela = Usuario(
        nome = "marcela",
        nome_completo = "Marcela Ramos Siqueira",
        endereco = [Endereco(logradouro ="Rua Victor Arantes", email = "marcelasiqueira@email.com")],
        dadospessoais = [DadosPessoais(cpf = "01234567809", rg = "123456789", data_nascimento = "09/11/1995")]
    )

    

#Enviar os dados para o BD (Persistência de dados)
session.add_all([rodrigo, fernando, sandra, marcela])

session.commit()


#Realizando consultas
consulta = select(Usuario).where(Usuario.nome.in_(["rodrigo", "fernando", "sandra", "marcela"]))
print("\nRealizando consulta....")
for usuario in session.scalars(consulta):
   print(usuario)


consulta_2 = select(Endereco).where(Endereco.id_usuario.in_(select(Usuario.id).where(Usuario.nome.in_(["rodrigo", "fernando", "sandra", "marcela"]))))
for endereco in session.scalars(consulta_2):
   print(endereco)


consulta_3 = select(DadosPessoais).where(DadosPessoais.id_usuario.in_(select(Usuario.id).where(Usuario.nome.in_(["rodrigo", "fernando", "sandra", "marcela"]))))
for dados_pessoais in session.scalars(consulta_3):
    print(dados_pessoais)