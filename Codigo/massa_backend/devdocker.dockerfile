# Define a imagem base Python 3.10.15
FROM python:3.10.15-bullseye

# Define o diretório de trabalho dentro do container
WORKDIR /Codigo/massa_backend

# Copia os arquivos do projeto para o container (ajuste se necessário), SIM SABEMOS QUE NÃO FAZ SENTIDO, MAS FUNCIONA!
COPY requirements/ /Codigo/massa_backend/requirements/  

# Define a variável de ambiente para não criar arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Cria o ambiente virtual
RUN python -m venv .venv

# Ativa o ambiente virtual (no contexto do Docker)
SHELL ["/bin/bash", "-c"] 
RUN source .venv/bin/activate

# Atualiza o pip
SHELL ["/bin/sh", "-c"]
RUN python -m pip install --upgrade pip

# Instala as dependências do projeto
RUN pip install -r  /Codigo/massa_backend/requirements/requirements.txt

# Copia os arquivos do projeto para o container (ajuste se necessário)
COPY . /Codigo/massa_backend/

# Define a variável de ambiente para o Python encontrar os módulos
ENV PYTHONPATH="/Codigo/massa_backend"

# CMD para rodar o servidor
CMD ["python", "/Codigo/massa_backend/MASSA_Algorithm/MASSA_Algorithm/MASSA.py"]

