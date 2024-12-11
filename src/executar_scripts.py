import subprocess

# Lista dos scripts a serem executados
scripts = [
    "server.py",
    "user_interface.py",
    #"teste_api.py"
]

# Executando os scripts em novos terminais
for script in scripts:
    subprocess.Popen(["start", "cmd", "/K", "python", script], shell=True)
