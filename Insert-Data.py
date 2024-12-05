import os
import re
from datetime import datetime
from pathlib import Path
import platform
import subprocess

def obter_data_criacao(arquivo):
    """
    Obtém a data de criação do arquivo.
    Em sistemas Unix, usa a data de modificação como fallback,
    já que nem todos os sistemas suportam data de criação.
    """
    if platform.system() == "Windows":
        return datetime.fromtimestamp(os.path.getctime(arquivo))
    else:
        # Usar 'stat' para data de criação no Linux/Unix
        try:
            data_criacao = subprocess.check_output(['stat', '-c', '%W', str(arquivo)])
            timestamp = int(data_criacao.strip())
            if timestamp > 0:
                return datetime.fromtimestamp(timestamp)
        except Exception:
            pass
        # Fallback para data de modificação
        return datetime.fromtimestamp(os.path.getmtime(arquivo))

def renomear_arquivos_na_pasta(pasta):
    regex = re.compile(r"^[0-9]{4}\.[0-9]{2}\.[0-9]{2} - ")
    pasta_path = Path(pasta)
    
    for arquivo in pasta_path.iterdir():
        if arquivo.is_file():
            nome_arquivo = arquivo.name
            if not regex.match(nome_arquivo):
                data_criacao = obter_data_criacao(arquivo)
                data_formatada = data_criacao.strftime("%Y.%m.%d")
                novo_nome = f"{data_formatada} - {nome_arquivo}"
                novo_path = arquivo.with_name(novo_nome)
                
                print(f"Renomeando: {arquivo} -> {novo_path}")
                arquivo.rename(novo_path)
    
    print("Renomeação completa!")

if __name__ == "__main__":
    # Obtém o diretório atual
    pasta_atual = os.getcwd()
    renomear_arquivos_na_pasta(pasta_atual)
