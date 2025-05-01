import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

# Caminho onde seus arquivos CSV estão armazenados
csv_path = r"C:\Users\USER\Desktop\CODE_IBM\Project_Complete_DE\csv_files"

# Função para converter um CSV em JSON
def csv_to_json(file_path: str) -> list:
    try:
        df = pd.read_csv(file_path)
        df = df.where(pd.notnull(df), None)
        return df.to_dict(orient="records")
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Arquivo CSV vazio")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo: {str(e)}")

# Função para criar as rotas automaticamente com base nos arquivos CSV
def create_csv_routes():
    for filename in os.listdir(csv_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(csv_path, filename)

            @app.get(f"/csv_to_json/{filename}") #selecione o csv que deve ser alterado para json (AUTOMATIZAR COM AIRFLOW)
            async def get_csv_data():
                if not os.path.exists(file_path):
                    raise HTTPException(status_code=404, detail="Arquivo não encontrado")
                
                dados = csv_to_json(file_path)
                return JSONResponse(content=dados)

create_csv_routes()
