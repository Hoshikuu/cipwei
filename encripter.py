from time import sleep
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, BarColumn, TextColumn, track, open as ropen
from os import system, name, mkdir
from os.path import isdir, dirname
from hashlib import sha3_256
from random import randint

# Introduccion al programa no hace nada solo es estetico
def Introduction():
    if name == "nt":
        system("cls")
    else:
        system("clear")

    print("""██╗░░██╗░█████╗░░██████╗██╗░░██╗██╗██╗░░██╗██╗░░░██╗
██║░░██║██╔══██╗██╔════╝██║░░██║██║██║░██╔╝██║░░░██║
███████║██║░░██║╚█████╗░███████║██║█████═╝░██║░░░██║
██╔══██║██║░░██║░╚═══██╗██╔══██║██║██╔═██╗░██║░░░██║
██║░░██║╚█████╔╝██████╔╝██║░░██║██║██║░╚██╗╚██████╔╝
╚═╝░░╚═╝░╚════╝░╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░╚═╝░╚═════╝░""")
    for i in track(range(10), description="Iniciando programa..."):
        sleep(0.05)
    #Limpia el archivo de logs
    #Hacer algo para cambiar el nombre del ultimo lastlog para guardarlo
    if not isdir(f"{dirname(__file__)}/Logs"):
        mkdir(f"{dirname(__file__)}/Logs")
    with open("Logs/LogsLast.log", "w+", encoding="UTF-8") as file:
        file.write("Comienzo Archivo Log\n\n")
    
    if name == "nt":
        system("cls")
    else:
        system("clear")

# --------------------------------------------------------------------------------------------------------------

# Devuelve la cadena de texto en sha3-256 Doble
def sha256(text):
    string = str(text)
    stringsha256 = sha3_256(string.encode("UTF-8")).hexdigest()
    return sha3_256(stringsha256.encode("UTF-8")).hexdigest()

# Funcion para actualizar la barra uso Global
def UpdateProgress(progress, task, step, log):
    if task != None:
        progress.update(task, advance=step)
    with open("Logs/LogsLast.log", "a", encoding="UTF-8") as file:
        file.write(log + "\n")
    if verbose == True:
        progress.console.log(log)

# Funcion para leer los datos del archivo de origen
def ProcessInputFile(filePath, chunkLevel):
    fileContent = None
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        sleep(pauseTime)

        # Lee el archivo con una barra de carga
        with ropen(filePath, "r", encoding="UTF-8", transient=False) as file:
            UpdateProgress(progress, None, 1, f"[yellow][READING] [green]Leyendo archivo [purple]{filePath}")
            sleep(pauseTime)
            fileContent = file.read()

        actualTask = progress.add_task("[red]Procesando Contenido...", total=(len(fileContent)//chunkLevel))

        processedContent = [] # Contenido separado por chunks

        # Carga los Chunks a la lista
        for i in range(0, len(fileContent), chunkLevel):
            processedContent.append(fileContent[i:i+chunkLevel])
            UpdateProgress(progress, actualTask, 1, f"[yellow][CHUNKS] [green]Procesando chunk [bold][purple]{i//chunkLevel+1}")

        UpdateProgress(progress, None, 1, f"[yellow][CHUNKS] [green]Cantidad chunks procesados [white]{len(processedContent)+1}")
        return processedContent

# Funcion para procesar la semilla del archivo que se usara
def ProcessFileSeed(masterKey, chunkLevel):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        sleep(pauseTime)
        
        actualTask = progress.add_task("[red]Generando Seed...", total=3)

        seed = randint(0, 64-chunkLevel) # La semilla del archivo
        UpdateProgress(progress, actualTask, 1, f"[yellow][SEED] [green]Seed del archivo calculado [purple]{seed}")

        hashedSeed = sha256(str(seed)) # El hash identificador de la semilla, para guardarlo al principio del archivo
        UpdateProgress(progress, actualTask, 1, f"[yellow][SEED] [green]Hash del Seed calculado [purple]{hashedSeed}")

        hashedMasterkey = sha256(masterKey) 
        UpdateProgress(progress, actualTask, 1, f"[yellow][SEED] [green]Hash de llave calculado [purple]{hashedMasterkey}")

        seededHashedMasterKey = hashedMasterkey[seed:seed+chunkLevel] # Hash que se usara para los calculos
        UpdateProgress(progress, actualTask, 1, f"[yellow][SEED] [green]Hash con Seed de llave calculado [purple]{seededHashedMasterKey}")

        return seed, hashedSeed, seededHashedMasterKey

def CiperFile(content, seed, seededHashedMasterKey, chunkLevel):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        sleep(pauseTime)

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
                char = chr((int(binC, 2) + int(binK, 2)))
                seg = seg + char
            result = result + seg
            segments.append(seg)
            UpdateProgress(progress, actualTask, 1, f"[yellow][CRYPT] [green]Calculando combinación [purple]{seg}")

            actualKey = sha256(seg)[seed:seed+chunkLevel]
            UpdateProgress(progress, actualTask, 1, f"[yellow][CRYPT] [green]Calculando nueva llave [purple]{actualKey}")

    return result, segments

def GenerateChecksum(segments):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        sleep(pauseTime)
        
        actualTask = progress.add_task("[red]Calculando checksum...", total=(len(segments)+1))
        
        shaSeg = ""

        for seg in segments:
            hash = sha256(seg)
            shaSeg = shaSeg + hash
            UpdateProgress(progress, actualTask, 1, f"[yellow][CHECKSUM] [green]Calculando chekcsum [purple]{hash}")

        checksum = sha256(shaSeg)
        UpdateProgress(progress, actualTask, 1, f"[yellow][CHECKSUM] [green]Checksum final [purple]{checksum}")
        return checksum

def MakeFile(seed, content, checksum, dstPath):
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console, transient=False) as progress:
        sleep(pauseTime)

        actualTask = progress.add_task("[red]Guardando Archivo...", total=1)

        with open(dstPath, "w+", encoding="UTF-8") as file:
            file.write(seed + content + checksum)
        
        UpdateProgress(progress, actualTask, 1, f"[yellow][MAKE] [green]Guardando archivo encriptado [purple]{dstPath}")
    return None

if __name__ == "__main__":
    Introduction()

    # Inicial Variables to Set
    console = Console()
    actualTask = None

    # Configuration Variables
    pauseTime = 0.5
    verbose = False

    # Settings Variables
    fileName = Prompt.ask("Introduce la ruta del archivo que quieres encriptar")
    # fileName = "dfc.txt"

    chunkLevel = IntPrompt.ask("Introduce la cantitdad de bytes",default=16)
    # chunkLevel = 16

    masterKey = Prompt.ask("Introduce la clave de cifrado")
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