from time import sleep, time
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, BarColumn, TextColumn, open as ropen
from os import mkdir, rename, name
from os.path import isdir, getmtime, isfile
from hashlib import sha3_256
from random import randint
from datetime import datetime
from re import sub
from getpass import getpass
from pathlib import Path

# Devuelve la cadena de texto en sha3-256 Doble
def sha256(text):
    string = str(text)
    stringsha256 = sha3_256(string.encode("UTF-8")).hexdigest()
    return sha3_256(stringsha256.encode("UTF-8")).hexdigest()

# Funcion para actualizar la barra uso Global
def UpdateProgress(progress, task, step, log, logIt):
    if task != None:
        progress.update(task, advance=step)
    if logIt == True:
        with open((Path(__file__).parent / "Logs" / "LogsLast.log").as_posix(), "a", encoding="UTF-8") as file:
            file.write(f"[{round((time() - start), 3):07.3f}] {sub(r'\[([a-z]+)\]', '', log)}\n")
    if verbose == True:
        progress.console.log(log)

# Introduccion al programa no hace nada solo es estetico
def Introduction():
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        actualTask = progress.add_task("[red]Iniciando...", total=6)

        logo = """
██╗░░██╗░█████╗░░██████╗██╗░░██╗██╗██╗░░██╗██╗░░░██╗
██║░░██║██╔══██╗██╔════╝██║░░██║██║██║░██╔╝██║░░░██║
███████║██║░░██║╚█████╗░███████║██║█████═╝░██║░░░██║
██╔══██║██║░░██║░╚═══██╗██╔══██║██║██╔═██╗░██║░░░██║
██║░░██║╚█████╔╝██████╔╝██║░░██║██║██║░╚██╗╚██████╔╝
╚═╝░░╚═╝░╚════╝░╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░╚═╝░╚═════╝░"""

        UpdateProgress(progress, actualTask, 1, logo, False)
        if verbose == False:
            print(logo)

        UpdateProgress(progress, actualTask, 1, "[yellow][INIT] [green]Estableciendo variables", False)

        logsDir = (Path(__file__).parent / "Logs").as_posix()
        logsLast = (Path(__file__).parent / "Logs" / "LogsLast.log").as_posix()

        # Crea el directorio de logs si no exite y guarda el ultimo archivo de logs
        if not isdir(logsDir):
            mkdir(logsDir)
            UpdateProgress(progress, actualTask, 1, "[yellow][INIT] [green]Creando Directorio de logs", False)
        else:
            UpdateProgress(progress, actualTask, 1, "", False)
        if isfile(logsLast):
            dateTime = datetime.fromtimestamp(getmtime(logsLast)).strftime("%Y-%m-%d-%H-%M-%S")
            rename(logsLast, (Path(logsDir) / f"Logs{dateTime}.log").as_posix())
            UpdateProgress(progress, actualTask, 1, "[yellow][INIT] [green]Guardando el archivo de logs", False)
        else:
            UpdateProgress(progress, actualTask, 1, "", False)

        #Limpia el archivo de logs
        with open(logsLast, "w+", encoding="UTF-8") as file:
            file.write(f"{logo}\n{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}\n\n")
        UpdateProgress(progress, actualTask, 1, "[yellow][INIT] [green]Creando Fichero de logs", True)
        
        UpdateProgress(progress, actualTask, 1, "[yellow][INIT] [green]Terminando", True)

def ReadFile(filePath, chunkLevel):
        with ropen(filePath, "r", encoding="UTF-8") as file:
            fileContent = file.read()

            hashedSeed = fileContent[:64]
            checksum = fileContent[-64:]

            content = fileContent[64:-64]

            processedContent = []

            for i in range(0, len(content), chunkLevel):
                processedContent.append(content[i:i+chunkLevel])

        return processedContent, hashedSeed, checksum

def CheckChecksum(content, checksum):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        actualTask = progress.add_task("[red]Comprobando Checksum...", total=len(content) + 1)

        hashedContent = ""
        for chunk in content:
            hashedContent = hashedContent + sha256(chunk)
            UpdateProgress(progress, actualTask, 1, f"[yellow][CHECKSUM] [green]Hashing [purple]{repr(chunk)[1:-1]}", True)

        contentChecksum = sha256(hashedContent)

        if contentChecksum == checksum:
            UpdateProgress(progress, actualTask, 1, f"[yellow][CHECKSUM] [green]Checksum comprobado [purple]NO ERROR", True)
        else:
            UpdateProgress(progress, actualTask, 1, f"[yellow][CHECKSUM] [green]Checksum comprobado [purple]ERROR Checksum invalido", True)


        

if __name__ == "__main__":
    
        # Inicial Variables to Set
    console = Console()
    actualTask = None
    start = time()

    # Configuration Variables
    pauseTime = 0.5
    verbose = True

     # Settings Variables
    # fileName = Prompt.ask("Introduce la ruta del archivo que quieres encriptar")
    fileName = "test.wei"

    # while True:
    #     chunkLevel = IntPrompt.ask("Introduce la cantitdad de bytes que se usara por chunk [1 - 64]",default=16)
    #     if chunkLevel >= 1 and chunkLevel <= 64:
    #         break
    #     print("Cantidad introducida no entra al rango de seguridad permitida de momento")

    chunkLevel = 16

    # masterKey = getpass("Introduce la clave de cifrado: ")
    masterKey = "secret"

    Introduction()

    processedContent, hashedSeed, checksum = ReadFile(fileName, chunkLevel)

    print(processedContent, hashedSeed, checksum)

    CheckChecksum(processedContent, checksum)




# with ropen("test.wei", "r", encoding="UTF-8") as file:
#     fileContent = file.read()
#     content = fileContent[64:-64]
#     print(content)
#     for i in range(0, len(content), chunkLevel):
#         processedContent.append(content[i:i+chunkLevel])
#     print(processedContent)

#     sha256Content = ""

#     for seg in processedContent:
#         sha256Content = sha256Content + sha256(seg)

#     checksum = sha256(sha256Content)
#     print(checksum)

#     print(fileContent[-64:])
    
#     for i in range(64):
#         seed = sha256(i)
#         print(seed)
#         if seed == fileContent[:64]:
#             print(i)
#             break
