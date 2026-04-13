import tkinter as tk
from tkinter import messagebox, ttk
import pyautogui
import time
import threading # Para que la ventana no se congele al enviar

class LaMasitaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("La Masita - Auto Sender")
        self.root.geometry("350x300")
        
        # Configuración de PyAutoGUI
        pyautogui.FAILSAFE = True # Si mueves el mouse a una esquina, el script se detiene
        
        self.crear_interfaz()

    def crear_interfaz(self):
        # Estilo moderno con ttk
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Mensaje:", font=('Helvetica', 10, 'bold')).pack(pady=5)
        self.entrada_texto = ttk.Entry(main_frame, width=35)
        self.entrada_texto.pack(pady=5)

        ttk.Label(main_frame, text="Cantidad:", font=('Helvetica', 10, 'bold')).pack(pady=5)
        self.entrada_cantidad = ttk.Entry(main_frame, width=15)
        self.entrada_cantidad.pack(pady=5)

        # Botón con estilo
        self.btn_enviar = tk.Button(
            main_frame, 
            text="INICIAR SECUENCIA", 
            command=self.validar_y_enviar,
            bg="#2ecc71", 
            fg="white",
            font=('Helvetica', 10, 'bold'),
            activebackground="#27ae60"
        )
        self.btn_enviar.pack(pady=20)

        # Barra de estado
        self.estado = ttk.Label(main_frame, text="Listo para la acción", foreground="gray")
        self.estado.pack(side=tk.BOTTOM)

    def validar_y_enviar(self):
        texto = self.entrada_texto.get()
        cantidad_str = self.entrada_cantidad.get()

        if not texto or not cantidad_str.isdigit():
            messagebox.showwarning("Atención", "Revisá los campos de texto y cantidad.")
            return

        # Usamos un hilo (Thread) para que la ventana no se bloquee mientras envía
        hilo_envio = threading.Thread(target=self.proceso_envio, args=(texto, int(cantidad_str)))
        hilo_envio.start()

    def proceso_envio(self, texto, cantidad):
        try:
            self.btn_enviar.config(state=tk.DISABLED, bg="#95a5a6")
            
            for i in range(5, 0, -1):
                self.estado.config(text=f"Iniciando en {i} segundos...")
                time.sleep(1)

            self.estado.config(text="Enviando mensajes...")
            for _ in range(cantidad):
                pyautogui.write(texto)
                pyautogui.press('enter')
                time.sleep(0.2) # Un poco más de margen para evitar bloqueos

            self.estado.config(text="¡Misión cumplida!")
            messagebox.showinfo("Éxito", f"Se enviaron {cantidad} mensajes.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")
        finally:
            self.btn_enviar.config(state=tk.NORMAL, bg="#2ecc71")
            self.estado.config(text="Listo para la acción")

if __name__ == "__main__":
    root = tk.Tk()
    app = LaMasitaApp(root)
    root.mainloop()