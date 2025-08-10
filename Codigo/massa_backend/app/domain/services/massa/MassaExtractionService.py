
import logging
import os
from fastapi import UploadFile
import pandas as pd

from app.domain.services.massa import MassaReaderService
from app.helpers import FileUtils


def name_extraction(file):
    names = []
    dict_names = {}
    for i in file:
        try:
            names.append(i.GetProp('_Name'))  # Get name of molecules to a list
            dict_names[i.GetProp('_Name')] = i  # Get name of molecules to a dict
        except:
            names.append(None)

    if None in names:  # If any molecule is unnamed it returns an error.
        raise ValueError("ERROR: Couldn't get any name from a molecule. Adding names before running the script is essential.")
    else:
        dataframe = pd.DataFrame({'molecules': pd.Series(dict_names)})
    return names, dataframe

def the_biological_handler(sdf_property_names, biological_activities):
    if biological_activities is None:  # If no biological activity name is passed as a command line argument.
        name_biological_list = sdf_property_names.copy()
        return name_biological_list
    else:  # If biological activity names are passed as a command-line argument.
        name_biological_list = biological_activities.copy()
        for i in name_biological_list:
            if i not in sdf_property_names:  # If the properties entered by the command line are typed incorrectly, raise an error.
                raise ValueError("ERROR: The name of the biological activity was not typed correctly.")
        return name_biological_list

def list_activities(file, name_biological_activity):
    for bioACname in name_biological_activity:  # For each biological activity:
        bio_dict = {}
        for i in file['molecules']:  # For each molecule in the dataframe:
            try:
                bio_name = i.GetProp('_Name')  # Capture the name of the molecule.
                bio_value = float(i.GetProp(bioACname))  # Capture the value of the biological activity.
                bio_dict[bio_name] = bio_value  # Add the "molecule name":"value" pair to the dictionary.
            except:  # If any molecule does not have the biological activity in question it will add NoneType in place of the value.
                bio_name = i.GetProp('_Name')
                bio_value = None
                bio_dict[bio_name] = bio_value

        if set(list(bio_dict.values())) == {None}:  # If no molecule has the biological property in question, raise an error.
            raise ValueError("ERROR: The chosen property does not contain data or the name of the biological activity was not typed correctly.")
        elif None in bio_dict.values():  # If any molecule has no biological activity value, raise an error.
            raise ValueError(f"ERROR: Some molecule has no biological activity value. Biological activity: {bioACname}, Molecules: {bio_dict}")

        file[bioACname] = pd.Series(bio_dict)
    return file

from rdkit import Chem

async def get_molecules_count(file: UploadFile) -> int:
    file_path = None

    # Configuração do logger para exibir mensagens no console
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Criação do arquivo temporário
        logger.info("Iniciando a criação do arquivo temporário.")
        file_path = await FileUtils.create_temp_file(file)
        logger.info(f"Arquivo temporário criado em: {file_path}")

        # Verifica se o arquivo foi criado corretamente
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado após criação: {file_path}")
        
        # Verifica o conteúdo do arquivo criado
        with open(file_path, "r") as f:
            content = f.read()
            if not content.strip():
                raise ValueError("O arquivo temporário foi criado, mas está vazio ou inválido.")
            logger.info(f"Conteúdo do arquivo SDF (amostra): {content[:500]}")  # Mostra uma amostra do conteúdo

    except Exception as e:
        logger.error(f"Erro ao criar o arquivo temporário: {e}")
        raise RuntimeError(f"Erro ao criar o arquivo temporário: {e}")

    try:
        # Passo 1: Ler as moléculas do arquivo
        logger.info(f"Tentando ler moléculas do arquivo: {file_path}")
        molecules = MassaReaderService.read_molecules(file_path)
        logger.info(f"Moléculas lidas: {len(molecules)}")

        if not molecules:
            raise ValueError("Nenhuma molécula foi encontrada no arquivo.")

        # Passo 2: Adicionar hidrogênios às moléculas
        logger.info("Adicionando hidrogênios às moléculas.")
        added_hydrogen_molecules = MassaReaderService.hydrogen_add(molecules)
        logger.info(f"Quantidade de moléculas após adição de hidrogênios: {len(added_hydrogen_molecules)}")

        # Retornar a quantidade de moléculas após adicionar hidrogênios
        return len(added_hydrogen_molecules)

    except Exception as e:
        logger.error(f"Erro ao contar as moléculas do arquivo: {e}")
        raise RuntimeError(f"Erro ao contar as moléculas do arquivo: {str(e)}")

    finally:
        # Remover o arquivo temporário para liberar espaço
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Arquivo temporário removido: {file_path}")
            except Exception as e:
                logger.warning(f"Erro ao remover o arquivo temporário: {file_path}. Detalhes: {e}")



