import os

def create_temp_file(content, name):
    """Cria um arquivo temporário com o conteúdo especificado."""
    with open(name, "w", encoding="utf-8") as file:
        file.write(content)

def remove_temp_file(name):
    """Remove o arquivo temporário criado para os testes."""
    if os.path.exists(name):
        os.remove(name)