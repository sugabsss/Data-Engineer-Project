import requests 
import pandas as pd
import logging
import os
import pyodbc
from pythonjsonlogger import jsonlogger
import yaml

log_file_path = r'C:\Users\USER\Desktop\CODE_IBM\Project_Complete_DE\LogsFile\extract_json.log'

os.makedirs(os.path.dirname(log_file_path),exist_ok=True)


logger = logging.getLogger("Extract_logs")
logger.setLevel(logging.DEBUG)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)    

def log_process(level, message):
    levels = {
        'Info': logging.INFO,
        'Warning': logging.WARNING,
        'Error': logging.ERROR,
        'Debug': logging.DEBUG
    }
    logger.log(levels.get(level, logging.INFO), message)

try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-J90B10V;"
        "DATABASE=TESTEUNI1;"
        "Trusted_Connection=yes;"
    )
    log_process("Info", f" Conexão com banco de dados estabelecida! ")
except FileNotFoundError:
    log_process("Error",f"Banco não encontrado não foi possivel estabelecer conexão!")

url_base = "http://127.0.0.1:8000/csv_to_json"

dataframes = {}
dataframes_path = r"C:\Users\USER\Desktop\CODE_IBM\Project_Complete_DE\Insert-API-connect\dataframe.txt"

def extract_json():
    with open(dataframes_path, "r+", enconde= "utf-8") as f:
        conteudo = f.read()
    
    if '###df_usuario.csv###' not in conteudo: 
        try : 
            with open(r'C:\Users\USER\Desktop\CODE_IBM\Project_Complete_DE\Insert-API-connect\Endpoints.yaml') as f:
                endpoints = yaml.safe_load(f)['Endpoints']

            for endpoint in endpoints:
                path = endpoint['path']
                response = requests.get(f'{url_base}{path}')

                if response.status_code == 200:
                    data = response.json()
                    df = pd.DataFrame(data)
                    df_name = f"df_{path.strip('/').replace('/', '_')}"
                    dataframes[df_name] = df

                    log_process('Info' , f" Sem erros na requisição : {response.status_code}")
                else:
                    log_process('Error', f"Erro na requisição HTTP: {response.status_code}")
                    return None
                
            with open(dataframes_path, 'w+',encoding='utf-8') as f:
                for df_name,df in dataframes.items():
                    f.read()
                    f.write(f'###{df_name}###\n')
                    f.write(df.to_string(index=False))
                    f.write("\n\n")

        except Exception as e:
                log_process('Warning', f"Exceção na extração: {str(e)}")
                return None
    else:
        log_process('Info'f' Todos os dataframes já foram inseridos no {dataframes_path}')

def transform_df():
    with open(dataframes_path, "r+", enconde="utf-8") as f:
    dados = f.read()
    

if __name__ == "__main__":
    extract_json()