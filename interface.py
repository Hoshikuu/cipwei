import tkinter as tk
from tkinter import filedialog

class Aplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta")
        self.root.geometry("600x400")
        self.allLogs = []

        self.BarraHerramientas()

        self.pestanaCifrado()

    def BarraHerramientas(self):
        barraHerramientas = tk.Menu(self.root)

        menuHerramientas = tk.Menu(barraHerramientas, tearoff=0)
        menuHerramientas.add_command(label="Cifrar", command=self.pestanaCifrado)
        menuHerramientas.add_command(label="Descifrar", command=self.pestanaDescifrado)
        
        barraHerramientas.add_cascade(label="Herramientas", menu=menuHerramientas)

        self.root.config(menu=barraHerramientas)

    def pestanaCifrado(self):
        self.limpiarVentana()

        titulo = tk.Label(self.root, text="Cifrar Archivo", font=("Arial", 16))
        titulo.pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=20, padx=20)

        self.entradaArchivo = tk.Entry(frame, font=("Arial", 10), width=50)
        self.entradaArchivo.pack(side=tk.LEFT, padx=10)

        botonArchivo = tk.Button(
            frame, text="Seleccionar Archivo", command=self.seleccionarArchivo,
            bg="#0078D7", fg="white", font=("Arial", 12), padx=10, pady=5, relief=tk.GROOVE
        )
        botonArchivo.pack(side=tk.LEFT, padx=10)

        botonCifrar = tk.Button(
            self.root, text="Cifrar archivo", command=self.cifrarArchivo,
            bg="#28A745", fg="white", font=("Arial", 12), padx=10, pady=5, relief=tk.GROOVE
        )
        botonCifrar.pack(pady=10)

        self.log = tk.Text(self.root, height=10, width=70, font=("Arial", 10), state=tk.DISABLED)
        self.log.pack(pady=10)

    def pestanaDescifrado(self):
        self.limpiarVentana()

        titulo = tk.Label(self.root, text="Descifrar Archivo", font=("Arial", 16))
        titulo.pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=20, padx=20)

        self.entradaArchivo = tk.Entry(frame, font=("Arial", 10), width=50)
        self.entradaArchivo.pack(side=tk.LEFT, padx=10)

        boton_archivo = tk.Button(
            frame, text="Seleccionar Archivo", command=self.seleccionarArchivo,
            bg="#0078D7", fg="white", font=("Arial", 12), padx=10, pady=5, relief=tk.GROOVE
        )
        boton_archivo.pack(side=tk.LEFT, padx=10)

        boton_descifrar = tk.Button(
            self.root, text="Descifrar archivo", command=self.descifrarArchivo,
            bg="#FFC107", fg="black", font=("Arial", 12), padx=10, pady=5, relief=tk.GROOVE
        )
        boton_descifrar.pack(pady=10)

        self.log = tk.Text(self.root, height=10, width=70, font=("Arial", 10), state=tk.DISABLED)
        self.log.pack(pady=10)

    def limpiarVentana(self):
        for widget in self.root.winfo_children():
            if widget != self.root.children.get("!menu"):
                widget.destroy()

    def seleccionarArchivo(self):
        self.selectedFile = filedialog.askopenfilename()
        self.entradaArchivo.delete(0, tk.END)
        self.entradaArchivo.insert(0, self.selectedFile if self.selectedFile else "No se seleccionó ningún archivo")
        self.anadirLog(f"Archivo seleccionado: {self.selectedFile}")

    def anadirLog(self, log):
        self.log.config(state=tk.NORMAL)

        self.allLogs.append(log)

        self.log.insert(tk.END, log + "\n")
        self.log.see(tk.END)
        
        self.log.config(state=tk.DISABLED)

    def cifrarArchivo(self):
        datos = Datos(self.root)
        root.wait_window(datos.ventanaDatos)
        chunkLevel = datos.chunkLevel
        masterKey = datos.masterKey

        with open(self.selectedFile, "r", "UTF-8") as f:
            pass
        #open all the things for encrypting this file
    
        
    def descifrarArchivo(self):
        self.anadirLog("adios")

class Datos:
    def __init__(self, root):
        self.ventanaDatos = tk.Toplevel(root)
        self.ventanaDatos.title("Herramienta de Cifrado/Descifrado")
        self.ventanaDatos.geometry("600x400")

        self.Informacion()
        self.Cerrar()

    @property
    def chunkLevel(self):
        return self._chunkLevel

    @property
    def masterKey(self):
        return self._masterKey

    def Informacion(self):
        frameBytes = tk.Frame(self.ventanaDatos)
        frameBytes.pack(pady=20, padx=20)
        bytes = tk.Label(frameBytes, text="Numero de Bytes:", font=("Arial", 12))
        bytes.pack(side=tk.LEFT, padx=10)
        self.bytesEntrada = tk.Entry(frameBytes, font=("Arial", 12), width=20)
        self.bytesEntrada.pack(side=tk.RIGHT, padx=10)

        framePasswd = tk.Frame(self.ventanaDatos)
        framePasswd.pack(pady=20, padx=20)
        passwd = tk.Label(framePasswd, text="Clave:", font=("Arial", 12))
        passwd.pack(side=tk.LEFT, padx=10)
        self.passwdEntrada = tk.Entry(framePasswd, font=("Arial", 12), width=20)
        self.passwdEntrada.pack(side=tk.RIGHT, padx=10)

    def Update(self):
        self._chunkLevel = self.bytesEntrada.get()  
        self._masterKey = self.passwdEntrada.get()
        self.ventanaDatos.destroy()

    def Cerrar(self):
        # self.botonAceptar = tk.Button(self.ventanaDatos, text="Aceptar", command=self.GetterDatos)
        self.botonAceptar = tk.Button(self.ventanaDatos, text="Aceptar", command=self.Update)
        self.botonAceptar.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplication(root)
    root.mainloop()