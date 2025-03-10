#                                                                    ---------------------------------
#
#                                                                       Script  creado por  Hoshiku
#                                                                       https://github.com/Hoshikuu
#
#                                                                    ---------------------------------

import tkinter
import tkinter.filedialog
from random import randint
from os.path import isfile
from os import chdir
import sys
from hashlib import sha3_256
from weicore.coder import encodeb64, decodeb64
import cipweiCore
import cipweiEncripter
import cipweiDecripter

# Interfaz principal
class Aplication:
    def __init__(self, root):
        self.root = root
        self.root.title("cipweiTool")
        if hasattr(sys, '_MEIPASS'):
            chdir(sys._MEIPASS)
        root.iconbitmap("resources/cipwei.ico")
        self.root.geometry("800x600") # Tamaño de la pantalla
        self.allLogs = [] # Donde se guardan todos los logs que genera el programa para posteriormente guardarlos en un archivo todo

        self.BarraHerramientas() # Generar la barra de herramientas 

        self.pestanaCifrado() # Mostrar la interfaz de cifrado

    # Barra de herramientas
    def BarraHerramientas(self):
        barraHerramientas = tkinter.Menu(self.root)

        menuHerramientas = tkinter.Menu(barraHerramientas, tearoff=0) # Categoria Herramientas
        menuHerramientas.add_command(label="Cifrar", command=self.pestanaCifrado) # Pestaña cifrado
        menuHerramientas.add_command(label="Descifrar", command=self.pestanaDescifrado) #Pestaña descifrado
        
        barraHerramientas.add_cascade(label="Herramientas", menu=menuHerramientas) # Añadir a la barra de herramientas

        self.root.config(menu=barraHerramientas) # Configurar la barra de herramientas

    # Mostrar la pestaña de Cifrado
    def pestanaCifrado(self):
        self.limpiarVentana() # Limpiar la interfaz actual

        # Mostrar la interfaz de cifrado

        titulo = tkinter.Label(self.root, text="Cifrar Archivo", font=("Arial", 16))
        titulo.pack(pady=10)

        frame = tkinter.Frame(self.root)
        frame.pack(pady=20, padx=20)

        self.entradaArchivo = tkinter.Entry(frame, font=("Arial", 10), width=73)
        self.entradaArchivo.pack(side=tkinter.LEFT, padx=10)

        botonArchivo = tkinter.Button(
            frame, text="Seleccionar Archivo", command=self.seleccionarArchivo,
            bg="#0078D7", fg="white", font=("Arial", 12), padx=10, pady=5, relief=tkinter.GROOVE
        )
        botonArchivo.pack(side=tkinter.LEFT, padx=10)

        botonCifrar = tkinter.Button(
            self.root, text="Cifrar archivo", command=self.cifrarArchivo,
            bg="#28A745", fg="white", font=("Arial", 12), padx=10, pady=5, relief=tkinter.GROOVE
        )
        botonCifrar.pack(pady=10)

        self.log = tkinter.Text(self.root, height=22, width=100, font=("Courier", 9), state=tkinter.DISABLED)
        self.log.pack(pady=10)

    # Mostrar la pestaña de descifrado
    def pestanaDescifrado(self):
        self.limpiarVentana() # Limpiar la ventana

        # Interfaz de descifrado

        titulo = tkinter.Label(self.root, text="Descifrar Archivo", font=("Arial", 16))
        titulo.pack(pady=10)

        frame = tkinter.Frame(self.root)
        frame.pack(pady=20, padx=20)

        self.entradaArchivo = tkinter.Entry(frame, font=("Arial", 10), width=73)
        self.entradaArchivo.pack(side=tkinter.LEFT, padx=10)

        boton_archivo = tkinter.Button(
            frame, text="Seleccionar Archivo", command=self.seleccionarArchivo,
            bg="#0078D7", fg="white", font=("Arial", 12), padx=10, pady=5, relief=tkinter.GROOVE
        )
        boton_archivo.pack(side=tkinter.LEFT, padx=10)

        boton_descifrar = tkinter.Button(
            self.root, text="Descifrar archivo", command=self.descifrarArchivo,
            bg="#FFC107", fg="black", font=("Arial", 12), padx=10, pady=5, relief=tkinter.GROOVE
        )
        boton_descifrar.pack(pady=10)

        self.log = tkinter.Text(self.root, height=22, width=100, font=("Courier", 9), state=tkinter.DISABLED)
        self.log.pack(pady=10)

    # Funcion para limpiar todo lo que hay en la ventana
    def limpiarVentana(self):
        for widget in self.root.winfo_children():
            if widget != self.root.children.get("!menu"):
                widget.destroy()

    # Seleccionar archivo
    def seleccionarArchivo(self):
        self.entradaArchivo.delete(0, tkinter.END)
        self.entradaArchivo.insert(0, tkinter.filedialog.askopenfilename())
        self.addlog(f"[INIT] Archivo seleccionado: {self.entradaArchivo.get()}")

    # Añadir log
    def addlog(self, log):
        self.log.config(state=tkinter.NORMAL)

        self.allLogs.append(log)

        self.log.insert(tkinter.END, log + "\n")
        self.log.see(tkinter.END)
        
        self.log.config(state=tkinter.DISABLED)

    ########################
    def cifrarArchivo(self):

        def UpdateLog(message):
            self.addlog(message)

        def sha256(text):
            string = str(text)
            stringsha256 = sha3_256(string.encode("UTF-8")).hexdigest()
            return sha3_256(stringsha256.encode("UTF-8")).hexdigest()

        def ProcessInputFile(filePath, chunkLevel):
            processedContent = []
            with open(filePath, "rb") as file:
                fileContent = encodeb64(file.read())
                for i in range(0, len(fileContent), chunkLevel):
                    processedContent.append(fileContent[i:i+chunkLevel])
                    UpdateLog(f"[CHUNKS] Procesando chunk {i//chunkLevel+1}")
                UpdateLog(f"[CHUNKS] Cantidad de chunks procesados {len(processedContent)}")
            return processedContent

        def ProcessFileSeed(masterKey, chunkLevel):
            seed = randint(0, 64-chunkLevel)
            UpdateLog(f"[SEED] Seed de archivo calculado")

            hashedSeed = sha256(seed)
            UpdateLog(f"[SEED] Hash de seed calculado {hashedSeed}")

            hashedMasterKey = sha256(masterKey)
            UpdateLog(f"[SEED] Hash de llave calculado {hashedMasterKey}")

            hashedSeededMasterKey = hashedMasterKey[seed:seed+chunkLevel]
            UpdateLog(f"[SEED] Hash con seed de la llave calculado {hashedSeededMasterKey}")

            return seed, hashedSeed, hashedSeededMasterKey

        def CiperFile(content, seed, seededHashedMasterKey, chunkLevel):
            result = ""
            segments = []
            actualKey = seededHashedMasterKey

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
                # UpdateLog(f"[CRYPT] Encriptando {repr(seg)[1:-1]}") # Alternative
                UpdateLog(f"[CRYPT] Encriptando {seg}")

                actualKey = sha256(chunk+seg)[seed:seed+chunkLevel]
                # UpdateLog(f"[CRYPT] Calculando nueva llave {actualKey}")

            return result, segments

        def GenerateChecksum(segments):
            shaSeg = ""

            for seg in segments:
                hash = sha256(seg)
                shaSeg = shaSeg + hash
                UpdateLog(f"[CHECKSUM] Calculando checksum {hash}")

            checksum = sha256(shaSeg)
            UpdateLog(f"[CHECKSUM] Checksum final {checksum}")
            return checksum

        def MakeFile(seed, content, checksum, dstPath):
            with open(dstPath, "w+", encoding="UTF-8") as file:
                file.write(seed + content + checksum)
                UpdateLog(f"[MAKE] Guardando archivo encriptado {dstPath}")
            return None

        filePath = self.entradaArchivo.get()
        if filePath == "" or not isfile(filePath):
            UpdateLog("[INIT] No has seleccionado ningun archivo")
            return None

        datos = Datos(self.root)
        root.wait_window(datos.ventanaDatos)

        chunkLevel = int(datos.chunkLevel)
        masterKey = datos.masterKey

        dstPath = filePath + ".wei"

        content = ProcessInputFile(filePath, chunkLevel)

        seed, hashedSeed, hashedSeededMasterKey = ProcessFileSeed(masterKey, chunkLevel)

        result, segments = CiperFile(content, seed, hashedSeededMasterKey, chunkLevel)

        checksum = GenerateChecksum(segments)
        
        MakeFile(hashedSeed, result, checksum, dstPath)
        
    ###########################
    def descifrarArchivo(self):
        
        def UpdateLog(message):
            self.addlog(message)

        def sha256(text):
            string = str(text)
            stringsha256 = sha3_256(string.encode("UTF-8")).hexdigest()
            return sha3_256(stringsha256.encode("UTF-8")).hexdigest()
        
        def ProcessInputFile(filePath, chunkLevel):
            with open(filePath, "r", encoding="UTF-8") as file:
                fileContent = file.read()

                hashedSeed = fileContent[:64]
                checksum = fileContent[-64:]

                content = fileContent[64:-64]

                processedContent = []

                for i in range(0, len(content), chunkLevel):
                    processedContent.append(content[i:i+chunkLevel])
            return processedContent, hashedSeed, checksum
        
        def CheckChecksum(content, checksum):
            hashedContent = ""
            for chunk in content:
                hashedContent = hashedContent + sha256(chunk)
                # UpdateLog(f"[CHECKSUM] Hashing {repr(chunk)[1:-1]}") # Alternative
                UpdateLog(f"[CHECKSUM] Hashing {chunk}")

            contentChecksum = sha256(hashedContent)

            if contentChecksum == checksum:
                UpdateLog("[CHECKSUM] Checksum comprobado NO ERROR")
                UpdateLog("[CHECKSUM] Procediendo con la desencriptación")
            else:
                UpdateLog("[CHECKSUM] Checksum comprobado ERROR Checksum invalido")
                UpdateLog("[CHECKSUM] Error con la integridad del archivo, este archivo fue modificado!!")
                # Termina el programa si no falla en la integridad del archivo
                return False
            
        def CalculateSeed(hashedSeed, masterKey, chunkLevel):
            seed = ""
            for i in range(64):
                UpdateLog(f"[SEED] Calculando Seed")
                if sha256(i) == hashedSeed:
                    seed = i
                    UpdateLog(f"[SEED] Seed Calculado")
                    break

            hashedMasterkey = sha256(masterKey)

            seededHashedMasterKey = hashedMasterkey[seed:seed+chunkLevel]
            return seed, seededHashedMasterKey
        
        def DecriptFile(content, seed, chunkLevel, seededHashedMasterKey):
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
                UpdateLog(f"[CRYPT] Desencriptando segment {repr(seg)[1:-1]}")
                actualKey = sha256(seg+chunk)[seed:seed+chunkLevel]
                # UpdateLog(f"[yellow][CRYPT] [green]Calculando nueva llave {actualKey}")
            return result
        
        def MakeFile(content, dstPath):
            with open(dstPath, "wb") as file:
                file.write(decodeb64(content))
            
            UpdateLog(f"[MAKE] Guardando archivo Desencriptado {dstPath}")
            return None

        filePath = self.entradaArchivo.get()
        if filePath == "" or not isfile(filePath):
            UpdateLog("[INIT] No has seleccionado ningun archivo")
            return None

        dstPath = filePath.replace(".wei", "")

        datos = Datos(self.root)
        root.wait_window(datos.ventanaDatos)

        chunkLevel = int(datos.chunkLevel)
        masterKey = datos.masterKey

        processedContent, hashedSeed, checksum = ProcessInputFile(filePath, chunkLevel)

        if CheckChecksum(processedContent, checksum) == False:
            return None

        seed, seededHashedMasterKey = CalculateSeed(hashedSeed, masterKey, chunkLevel)

        result = DecriptFile(processedContent, seed, chunkLevel, seededHashedMasterKey)

        MakeFile(result, dstPath)        

class Datos:
    def __init__(self, root):
        self.ventanaDatos = tkinter.Toplevel(root)
        self.ventanaDatos.title("cipweiTool - Data")
        root.iconbitmap("resources/cipwei.ico")
        self.ventanaDatos.geometry("500x200")

        self.Informacion()
        self.Cerrar()

    @property
    def chunkLevel(self):
        return self._chunkLevel

    @property
    def masterKey(self):
        return self._masterKey

    def Informacion(self):
        frameBytes = tkinter.Frame(self.ventanaDatos)
        frameBytes.pack(pady=20, padx=20)
        bytes = tkinter.Label(frameBytes, text="Numero de Bytes (1 - 64):", font=("Arial", 12))
        bytes.pack(side=tkinter.LEFT, padx=10)
        self.bytesEntrada = tkinter.Entry(frameBytes, font=("Arial", 12), width=20)
        self.bytesEntrada.pack(side=tkinter.RIGHT, padx=10)

        framePasswd = tkinter.Frame(self.ventanaDatos)
        framePasswd.pack(pady=20, padx=20)
        passwd = tkinter.Label(framePasswd, text="Clave:", font=("Arial", 12),)
        passwd.pack(side=tkinter.LEFT, padx=10)
        self.passwdEntrada = tkinter.Entry(framePasswd, font=("Arial", 12), width=20, show="*")
        self.passwdEntrada.pack(side=tkinter.RIGHT, padx=10)

    def Update(self):
        self._chunkLevel = self.bytesEntrada.get()  
        self._masterKey = self.passwdEntrada.get()
        self.ventanaDatos.destroy()

    def Cerrar(self):
        # self.botonAceptar = tkinter.Button(self.ventanaDatos, text="Aceptar", command=self.GetterDatos)
        self.botonAceptar = tkinter.Button(self.ventanaDatos, text="Aceptar", command=self.Update)
        self.botonAceptar.pack(pady=20)

if __name__ == "__main__":
    root = tkinter.Tk()
    app = Aplication(root)
    root.mainloop()