import tkinter as tk
from tkinter import messagebox, ttk
import pyautogui
import time
import threading

class LaMasitaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("La Masita - Control Total")
        self.root.geometry("350x350")
        
        # Atributo de control: La bandera (flag)
        self.cancelar = False 
        
        pyautogui.FAILSAFE = True
        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Mensaje:").pack(pady=5)
        self.entrada_texto = ttk.Entry(main_frame, width=35)
        self.entrada_texto.pack(pady=5)

        ttk.Label(main_frame, text="Cantidad:").pack(pady=5)
        self.entrada_cantidad = ttk.Entry(main_frame, width=15)
        self.entrada_cantidad.pack(pady=5)

        # Botón para Iniciar
        self.btn_enviar = tk.Button(
            main_frame, text="INICIAR", command=self.validar_y_enviar,
            bg="#2ecc71", fg="white", font=('Helvetica', 10, 'bold')
        )
        self.btn_enviar.pack(pady=10, fill=tk.X)

        # BOTON DE PÁNICO
        self.btn_panico = tk.Button(
            main_frame, text="¡DETENER ENVÍO!", command=self.activar_panico,
            bg="#e74c3c", fg="white", font=('Helvetica', 10, 'bold'),
            state=tk.DISABLED # Apagado hasta que empiece el envío
        )
        self.btn_panico.pack(pady=5, fill=tk.X)

        self.estado = ttk.Label(main_frame, text="Esperando instrucciones...", foreground="gray")
        self.estado.pack(side=tk.BOTTOM)

    def activar_panico(self):
        # Cuando tocas el boton, cambiamos la señal a TRUE
        self.cancelar = True
        self.estado.config(text="Cancelando envio...", foreground="red")

    def validar_y_enviar(self):
        texto = self.entrada_texto.get()
        cant = self.entrada_cantidad.get()
        if not texto or not cant.isdigit():
            messagebox.showwarning("Error", "Datos no válidos")
            return

        self.cancelar = False # Resetear la bandera antes de empezar
        hilo = threading.Thread(target=self.proceso_envio, args=(texto, int(cant)))
        hilo.start()

    def proceso_envio(self, texto, cantidad):
        self.btn_enviar.config(state=tk.DISABLED)
        self.btn_panico.config(state=tk.NORMAL)
        
        for i in range(5, 0, -1):
            if self.cancelar: break # Por si el usuario cancela en la cuenta regresiva
            self.estado.config(text=f"Iniciando en {i}...")
            time.sleep(1)

        # Bucle principal de envio
        enviados = 0
        for _ in range(cantidad):
            if self.cancelar: # REVISION DE LA SEÑAL
                break # Sale del bucle inmediatamente
            
            pyautogui.write(texto)
            pyautogui.press('enter')
            enviados += 1
            self.estado.config(text=f"Enviando: {enviados}/{cantidad}")
            time.sleep(0.2)

        # Resultado final
        if self.cancelar:
            self.estado.config(text=f"Proceso detenido en {enviados}")
            messagebox.showwarning("Pánico", f"Envío cancelado. Se mandaron {enviados} mensajes.")
        else:
            self.estado.config(text="Finalizado con exito")
            messagebox.showinfo("Éxito", "Todos los mensajes fueron enviados.")

        self.btn_enviar.config(state=tk.NORMAL)
        self.btn_panico.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = LaMasitaApp(root)
    root.mainloop()