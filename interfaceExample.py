import tkinter as tk
from tkinter import filedialog

# Límite de líneas en el cuadro de texto
LIMITE_LINEAS = 20

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta de Cifrado/Descifrado")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        # Barra de herramientas
        self.crear_barra_herramientas()

        # Contenido predeterminado (Cifrado)
        self.mostrar_cifrado()

    def crear_barra_herramientas(self):
        # Crear la barra de menú
        barra_herramientas = tk.Menu(self.root)

        # Menú "Herramienta"
        menu_herramienta = tk.Menu(barra_herramientas, tearoff=0)
        menu_herramienta.add_command(label="Cifrar", command=self.mostrar_cifrado)
        menu_herramienta.add_command(label="Descifrar", command=self.mostrar_descifrado)
        barra_herramientas.add_cascade(label="Herramienta", menu=menu_herramienta)

        # Añadir la barra de herramientas a la ventana
        self.root.config(menu=barra_herramientas)

    def mostrar_cifrado(self):
        # Limpiar la ventana actual
        self.limpiar_ventana()

        # Título
        titulo = tk.Label(self.root, text="Cifrar Archivo", font=("Arial", 16), bg="#f0f0f0")
        titulo.pack(pady=10)

        # Marco para organizar elementos
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=20, padx=20)

        # Campo de texto para la ruta del archivo
        self.entrada_archivo = tk.Entry(frame, font=("Arial", 10), width=50)
        self.entrada_archivo.pack(side=tk.LEFT, padx=10)

        # Botón para seleccionar archivo
        boton_archivo = tk.Button(
            frame, text="Seleccionar Archivo", command=self.seleccionar_archivo,
            bg="#0078D7", fg="white", font=("Arial", 12), padx=10, pady=5, relief=tk.GROOVE
        )
        boton_archivo.pack(side=tk.LEFT, padx=10)

        # Botón para cifrar archivo
        boton_cifrar = tk.Button(
            self.root, text="Cifrar archivo", command=self.cifrar_archivo,
            bg="#28A745", fg="white", font=("Arial", 12), padx=10, pady=5, relief=tk.GROOVE
        )
        boton_cifrar.pack(pady=10)

        # Cuadro de texto para logs
        self.log = tk.Text(self.root, height=10, width=70, font=("Arial", 10), state=tk.DISABLED)
        self.log.pack(pady=10)

    def mostrar_descifrado(self):
        # Limpiar la ventana actual
        self.limpiar_ventana()

        # Título
        titulo = tk.Label(self.root, text="Descifrar Archivo", font=("Arial", 16), bg="#f0f0f0")
        titulo.pack(pady=10)

        # Marco para organizar elementos
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=20, padx=20)

        # Campo de texto para la ruta del archivo
        self.entrada_archivo = tk.Entry(frame, font=("Arial", 10), width=50)
        self.entrada_archivo.pack(side=tk.LEFT, padx=10)

        # Botón para seleccionar archivo
        boton_archivo = tk.Button(
            frame, text="Seleccionar Archivo", command=self.seleccionar_archivo,
            bg="#0078D7", fg="white", font=("Arial", 12), padx=10, pady=5, relief=tk.GROOVE
        )
        boton_archivo.pack(side=tk.LEFT, padx=10)

        # Botón para descifrar archivo
        boton_descifrar = tk.Button(
            self.root, text="Descifrar archivo", command=self.descifrar_archivo,
            bg="#FFC107", fg="black", font=("Arial", 12), padx=10, pady=5, relief=tk.GROOVE
        )
        boton_descifrar.pack(pady=10)

        # Cuadro de texto para logs
        self.log = tk.Text(self.root, height=10, width=70, font=("Arial", 10), state=tk.DISABLED)
        self.log.pack(pady=10)

    def limpiar_ventana(self):
        # Eliminar todos los widgets de la ventana
        for widget in self.root.winfo_children():
            if widget != self.root.children.get("!menu"):  # Evitar eliminar la barra de herramientas
                widget.destroy()

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename()
        self.entrada_archivo.delete(0, tk.END)
        self.entrada_archivo.insert(0, archivo if archivo else "No se seleccionó ningún archivo")
        self.añadir_log(f"Archivo seleccionado: {archivo}")

    def añadir_log(self, mensaje):
        self.log.config(state=tk.NORMAL)
        num_lineas = int(self.log.index('end-1c').split('.')[0])
        if num_lineas >= LIMITE_LINEAS:
            self.log.delete(1.0, 2.0)
        self.log.insert(tk.END, mensaje + "\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    def cifrar_archivo(self):
        ruta_archivo = self.entrada_archivo.get()
        if ruta_archivo and ruta_archivo != "No se seleccionó ningún archivo":
            self.añadir_log("Cifrando archivo...")
            # Aquí iría tu lógica de cifrado
            self.añadir_log("Archivo cifrado correctamente.")
        else:
            self.añadir_log("Error: No se ha seleccionado ningún archivo para cifrar.")

    def descifrar_archivo(self):
        ruta_archivo = self.entrada_archivo.get()
        if ruta_archivo and ruta_archivo != "No se seleccionó ningún archivo":
            self.añadir_log("Descifrando archivo...")
            # Aquí iría tu lógica de descifrado
            self.añadir_log("Archivo descifrado correctamente.")
        else:
            self.añadir_log("Error: No se ha seleccionado ningún archivo para descifrar.")


# Crear la ventana principal y ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()