import os
import tempfile
from io import BytesIO, FileIO

from fastapi import UploadFile

@staticmethod
async def create_temp_file(file: UploadFile) -> str:
    # Obtém a extensão do arquivo
    extension = __get_file_extension(file.filename)

    # Cria um arquivo temporário no disco com a extensão correta
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
        tmp_file.write(await file.read())
        file_path = tmp_file.name

    return file_path

@staticmethod
async def buffer_to_blob(file) -> bytes:
    """Converte um arquivo recebido no buffer para um blob (bytes)."""
    if isinstance(file, UploadFile):
        # Caso seja UploadFile do FastAPI, lê o conteúdo
        return await file.read()
    elif isinstance(file, BytesIO):
        # Caso seja um BytesIO, pega os dados do buffer
        return file.getvalue()
    else:
        raise TypeError("O tipo de arquivo não é suportado.")

@staticmethod
def __get_file_extension(filename: str) -> str:
    __, ext = os.path.splitext(filename)

    return ext