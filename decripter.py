#                                                                    ---------------------------------
#
#                                                                       Script  creado por  Hoshiku
#                                                                       https://github.com/Hoshikuu
#
#                                                                    ---------------------------------

from time import time
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, BarColumn, TextColumn, open as ropen
from os import mkdir, rename
from os.path import isdir, getmtime, isfile
from hashlib import sha3_256
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
        with open((Path(__file__).parent / "Logs" / "decripter" / "LogsLast.log").as_posix(), "a", encoding="UTF-8") as file:
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

        parentLogDir = (Path(__file__).parent / "Logs").as_posix()
        logsDir = (Path(__file__).parent / "Logs" / "decripter").as_posix()
        logsLast = (Path(__file__).parent / "Logs" / "decripter" / "LogsLast.log").as_posix()

        # Crea el directorio de logs si no exite y guarda el ultimo archivo de logs
        if not isdir(parentLogDir):
            mkdir(parentLogDir)
            UpdateProgress(progress, actualTask, 1, "[yellow][INIT] [green]Creando Directorio de logs", False)
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

# Lee el archivo de origen
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

# Comprueba la integridad del archivo encriptado si se ha modificado
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
            UpdateProgress(progress, actualTask, 0, "[yellow][CHECKSUM] [red]Error con la integridad del archivo, este archivo fue modificado!!", True)
            print("           Error con la integridad del archivo, este archivo fue modificado!!")
            print("           Revisa el numero de Bytes si esta correcto!!")
            # Termina el programa si no falla en la integridad del archivo
            exit()

# Calcula la semilla del srchivo
def CalculateSeed(hashedSeed, masterKey, chunkLevel):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        actualTask = progress.add_task("[red]Calculando Seed...", total=64)

        seed = ""
        for i in range(64):
            UpdateProgress(progress, actualTask, 1, f"[yellow][SEED] [green]Calculando Seed [purple]{i}", True)
            if sha256(i) == hashedSeed:
                seed = i
                UpdateProgress(progress, actualTask, 64 - i, f"[yellow][SEED] [green]Seed Calculado [purple]{seed}", True)
                break

        hashedMasterkey = sha256(masterKey)

        seededHashedMasterKey = hashedMasterkey[seed:seed+chunkLevel]
        return seed, seededHashedMasterKey

# Desencripta el archivo
def DecriptFile(content, seed, chunkLevel, seededHashedMasterKey):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        actualTask = progress.add_task("[red]Desencriptando Archivo...", total=(len(content)*2))

        actualKey = seededHashedMasterKey

        result = ""

        for chunk in content:
            binChunk = []
            for char in chunk:
                binChunk.append(format(ord(char), "08b"))
            binKey = []
            for char in actualKey:
                binKey.append(format(ord(char), "08b"))

            seg = ""
            for binC, binK in zip(binChunk, binKey):
                char = chr(abs(int(binC, 2) - int(binK, 2)))
                seg = seg + char
            result = result + seg
            UpdateProgress(progress, actualTask, 1, f"[yellow][CRYPT] [green]Desencriptando segment [purple]{repr(seg)[1:-1]}", False)
            actualKey = sha256(seg)[seed:seed+chunkLevel]
            UpdateProgress(progress, actualTask, 1, f"[yellow][CRYPT] [green]Calculando nueva llave [purple]{actualKey}", True)
        return result

# Crea el archivo de destino donde se guardara el resultado
def MakeFile(content, dstPath):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        actualTask = progress.add_task("[red]Guardando Archivo...", total=1)

        with open(dstPath, "w+", encoding="UTF-8") as file:
            file.write(content)
        
        UpdateProgress(progress, actualTask, 1, f"[yellow][MAKE] [green]Guardando archivo Desencriptado [purple]{dstPath}", True)
    return None

# MAIN
if __name__ == "__main__":
    
    # Inicial Variables to Set
    console = Console()
    actualTask = None
    start = time()

    # Configuration Variables
    verbose = True if Prompt.ask("Quieres activar verbose?", choices=["s", "n"]) == "s" else False

    # Settings Variables

    # fileName = "test.wei"
    fileName = Prompt.ask("Introduce la ruta del archivo que quieres Desencriptar")

    # dstPath = Prompt.ask("Introduce el archivo de destino")
    # dstPath = "Cifradowei.wei"
    dstPath = fileName.split(".")[0] + "Decripted.txt"

    # chunkLevel = 16
    while True:
        chunkLevel = IntPrompt.ask("Introduce la cantitdad de bytes que se usara por chunk [1 - 64]",default=16)
        if chunkLevel >= 1 and chunkLevel <= 64:
            break
        print("Cantidad introducida no entra al rango de seguridad permitida de momento")

    # masterKey = "secret"
    masterKey = getpass("Introduce la clave de cifrado: ")
   

    # Start

    Introduction()

    processedContent, hashedSeed, checksum = ReadFile(fileName, chunkLevel)

    CheckChecksum(processedContent, checksum)

    seed, seededHashedMasterKey = CalculateSeed(hashedSeed, masterKey, chunkLevel)

    result = DecriptFile(processedContent, seed, chunkLevel, seededHashedMasterKey)

    MakeFile(result, dstPath)