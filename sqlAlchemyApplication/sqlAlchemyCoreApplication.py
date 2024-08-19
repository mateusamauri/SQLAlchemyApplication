#Outra maneira de criação de tabelas, sem utilizar ORM, utilizando apenas Metadata Object.

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import MetaData
from sqlalchemy import Table


engine = create_engine("sqlite:///:memory:")

objeto_metadata = MetaData()

usuario = Table(
    "usuario",
    objeto_metadata,
    Column("id_usuario", Integer, primary_key=True),
    Column("nome", String(50), nullable=False),
    Column("email", String(50)),
    Column("apelido", String(30)),
    
)

objeto_metadata.create_all(engine)
inspetor = inspect(engine)
print(inspetor.get_table_names())

