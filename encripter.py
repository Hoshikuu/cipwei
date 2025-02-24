#                                                                    ---------------------------------
#
#                                                                       Script  creado por  Hoshiku
#                                                                       https://github.com/Hoshikuu
#
#                                                                    ---------------------------------

from time import sleep, time
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, BarColumn, TextColumn, open as ropen
from os import mkdir, rename
from os.path import isdir, getmtime, isfile
from hashlib import sha3_256
from random import randint
from datetime import datetime
from re import sub
from getpass import getpass
from pathlib import Path

# Funcion para actualizar la barra uso Global
def UpdateProgress(progress, task, step, log, logIt):
    if task != None:
        progress.update(task, advance=step)
    if logIt == True:
        with open((Path(__file__).parent / "Logs" / "encripter" / "LogsLast.log").as_posix(), "a", encoding="UTF-8") as file:
            file.write(f"[{round((time() - start), 3):07.3f}] {sub(r'\[([a-z]+)\]', '', log)}\n")
    if verbose == True:
        progress.console.log(log)

# Devuelve la cadena de texto en sha3-256 Doble
def sha256(text):
    string = str(text)
    stringsha256 = sha3_256(string.encode("UTF-8")).hexdigest()
    return sha3_256(stringsha256.encode("UTF-8")).hexdigest()

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
        logsDir = (Path(__file__).parent / "Logs" / "encripter").as_posix()
        logsLast = (Path(__file__).parent / "Logs" / "encripter" / "LogsLast.log").as_posix()

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

# Funcion para leer los datos del archivo de origen
def ProcessInputFile(filePath, chunkLevel):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        fileContent = None

        # Lee el archivo con una barra de carga
        with ropen(filePath, "r", encoding="UTF-8", transient=False) as file:
            UpdateProgress(progress, None, 1, f"[yellow][READING] [green]Leyendo archivo [purple]{filePath}", True)
            fileContent = file.read()

        actualTask = progress.add_task("[red]Procesando Contenido...", total=(len(fileContent)//chunkLevel))

        processedContent = [] # Contenido separado por chunks

        # Carga los Chunks a la lista
        for i in range(0, len(fileContent), chunkLevel):
            processedContent.append(fileContent[i:i+chunkLevel])
            UpdateProgress(progress, actualTask, 1, f"[yellow][CHUNKS] [green]Procesando chunk [bold][purple]{i//chunkLevel+1}", False)

        UpdateProgress(progress, None, 1, f"[yellow][CHUNKS] [green]Cantidad chunks procesados [white]{len(processedContent)}", True)
        return processedContent

# Funcion para procesar la semilla del archivo que se usara
def ProcessFileSeed(masterKey, chunkLevel):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        actualTask = progress.add_task("[red]Generando Seed...", total=3)

        seed = randint(0, 64-chunkLevel) # La semilla del archivo
        UpdateProgress(progress, actualTask, 1, f"[yellow][SEED] [green]Seed del archivo calculado [purple]{seed}", False)

        hashedSeed = sha256(str(seed)) # El hash identificador de la semilla, para guardarlo al principio del archivo
        UpdateProgress(progress, actualTask, 1, f"[yellow][SEED] [green]Hash del Seed calculado [purple]{hashedSeed}", True)

        hashedMasterkey = sha256(masterKey) 
        UpdateProgress(progress, actualTask, 1, f"[yellow][SEED] [green]Hash de llave calculado [purple]{hashedMasterkey}", False)

        seededHashedMasterKey = hashedMasterkey[seed:seed+chunkLevel] # Hash que se usara para los calculos
        UpdateProgress(progress, actualTask, 1, f"[yellow][SEED] [green]Hash con Seed de llave calculado [purple]{seededHashedMasterKey}", True)

        return seed, hashedSeed, seededHashedMasterKey

# Encripta el archivo
def CiperFile(content, seed, seededHashedMasterKey, chunkLevel):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        actualTask = progress.add_task("[red]Cifrando Archivo...", total=(len(content)*2))

        actualKey = seededHashedMasterKey

        result = ""
        segments = []

        for chunk in content:
            binChunk = []
            for char in chunk:
                binChunk.append(format(ord(char), "08b"))
            binKey = []
            for char in actualKey:
                binKey.append(format(ord(char), "08b"))

            seg = ""
            for binC, binK in zip(binChunk, binKey):
                char = chr(abs(int(binC, 2) + int(binK, 2)))
                seg = seg + char
            result = result + seg
            segments.append(seg)
            UpdateProgress(progress, actualTask, 1, f"[yellow][CRYPT] [green]Calculando combinación [purple]{repr(seg)[1:-1]}", True)

            actualKey = sha256(chunk)[seed:seed+chunkLevel]
            UpdateProgress(progress, actualTask, 1, f"[yellow][CRYPT] [green]Calculando nueva llave [purple]{actualKey}", False)

    return result, segments

# Crea el checksum para la integridad del archivo
def GenerateChecksum(segments):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        actualTask = progress.add_task("[red]Calculando Checksum...", total=(len(segments)+1))
        
        shaSeg = ""

        for seg in segments:
            hash = sha256(seg)
            shaSeg = shaSeg + hash
            UpdateProgress(progress, actualTask, 1, f"[yellow][CHECKSUM] [green]Calculando checksum [purple]{hash}", True)

        checksum = sha256(shaSeg)
        UpdateProgress(progress, actualTask, 1, f"[yellow][CHECKSUM] [green]Checksum final [purple]{checksum}", True)
        return checksum

# Crea el archivo de destino donde se guarda el texto cifrado
def MakeFile(seed, content, checksum, dstPath):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        actualTask = progress.add_task("[red]Guardando Archivo...", total=1)

        with open(dstPath, "w+", encoding="UTF-8") as file:
            file.write(seed + content + checksum)
        
        UpdateProgress(progress, actualTask, 1, f"[yellow][MAKE] [green]Guardando archivo encriptado [purple]{dstPath}", True)
    return None

# MAIN
if __name__ == "__main__":
    # Inicial Variables to Set
    console = Console()
    actualTask = None
    start = time()

    # Configuration Variables
    verbose = True if Prompt.ask("Quieres activar verbose?", choices=["s", "n"]) == "s" else False

    Introduction()

    # Settings Variables
    fileName = Prompt.ask("Introduce la ruta del archivo que quieres encriptar")
    # fileName = "dfc.txt"

    while True:
        chunkLevel = IntPrompt.ask("Introduce la cantitdad de bytes que se usara por chunk [1 - 64]",default=16)
        if chunkLevel >= 1 and chunkLevel <= 64:
            break
        print("Cantidad introducida no entra al rango de seguridad permitida de momento")

    masterKey = getpass("Introduce la clave de cifrado: ")
    # masterKey = "secret"
    
    # dstPath = Prompt.ask("Introduce el archivo de destino")
    # dstPath = "Cifradowei.wei"
    dstPath = fileName.split(".")[0] + ".wei"

    # Start
    content = ProcessInputFile(fileName, chunkLevel)

    seed, hashedseed, seededHashedMasterKey = ProcessFileSeed(masterKey, chunkLevel)

    result, segments = CiperFile(content, seed, seededHashedMasterKey, chunkLevel)

    checksum = GenerateChecksum(segments)

    MakeFile(hashedseed, result, checksum, dstPath)