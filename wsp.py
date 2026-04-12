import tkinter as tk
from tkinter import messagebox
import pyautogui
import time

def enviar_mensajes():
    texto = entrada_texto.get()
    cantidad_str = entrada_cantidad.get()

    if not texto:
        messagebox.showerror("Error", "El campo de texto está vacío.")
        return

    if not cantidad_str.isdigit():
        messagebox.showerror("Error", "La cantidad debe ser un número.")
        return

    cantidad = int(cantidad_str)

    messagebox.showinfo("Preparación", "Tenés 5 segundos para hacer click en donde queres el msj.")
    time.sleep(5)

    for _ in range(cantidad):
        pyautogui.write(texto)
        pyautogui.press('enter')
        time.sleep(0.1)

    messagebox.showinfo("Joya man", f"Ya mandaste {cantidad} mensajes.")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Auto WhatsApp Sender")
ventana.geometry("300x200")
ventana.resizable(False, False)

# Etiqueta y campo de texto
tk.Label(ventana, text="Texto a enviar:").pack(pady=5)
entrada_texto = tk.Entry(ventana, width=30)
entrada_texto.pack()

# Etiqueta y campo de cantidad
tk.Label(ventana, text="Cantidad de veces:").pack(pady=5)
entrada_cantidad = tk.Entry(ventana, width=10)
entrada_cantidad.pack()

# Botón para ejecutar
tk.Button(ventana, text="Enviar", command=enviar_mensajes, bg="#4CAF50", fg="white").pack(pady=20)

# Ejecutar la interfaz
ventana.mainloop()