import tkinter as tk
from tkinter import messagebox
from lxml import etree

# Función para evaluar XPath con limpieza de XML
def evaluar_xpath(xml_str, xpath_expr):
    try:
        # Eliminar la declaración de codificación si está presente
        if xml_str.startswith("<?xml"):
            xml_str = "\n".join(xml_str.splitlines()[1:])

        # Limpiar espacios en blanco al inicio y al final
        xml_str = xml_str.strip()

        # Convertir XML a bytes antes de parsearlo
        xml_bytes = xml_str.encode("utf-8")

        # Intentar cargar el XML
        root = etree.fromstring(xml_bytes)

        # Evaluar la expresión XPath
        resultado = root.xpath(xpath_expr)

        # Si no se encuentran resultados, devolver un mensaje
        if not resultado:
            return "No se encontraron resultados para la expresión XPath."
        
        # Convertir los resultados a texto si son elementos XML
        if isinstance(resultado, list):
            resultado = [etree.tostring(elem, pretty_print=True).decode() if isinstance(elem, etree._Element) else str(elem) for elem in resultado]

        return "\n".join(resultado)
    except etree.XMLSyntaxError as e:
        return f"Error de sintaxis XML: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

# Función para ejecutar el evaluador
def ejecutar_evaluacion(event=None):  # Agregamos 'event' para que funcione con "Enter"
    # Obtener el código XML y la expresión XPath desde las cajas de texto
    xml_str = caja_xml.get("1.0", "end-1c")
    xpath_expr = caja_xpath.get()

    if not xml_str or not xpath_expr:
        messagebox.showerror("Error", "Por favor, ingresa tanto el código XML como la expresión XPath.")
        return

    # Evaluar XPath
    resultado = evaluar_xpath(xml_str, xpath_expr)

    # Mostrar resultados
    caja_resultados.config(state=tk.NORMAL)  # Hacer el área de texto editable
    caja_resultados.delete(1.0, tk.END)  # Limpiar la caja de resultados
    caja_resultados.insert(tk.END, resultado)
    caja_resultados.config(state=tk.DISABLED)  # Hacer el área de texto no editable

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Evaluador de XPath")
ventana.geometry("600x500")

# Etiquetas y campos de entrada
etiqueta_xml = tk.Label(ventana, text="Código XML:")
etiqueta_xml.pack(pady=5)

# Caja de texto para ingresar el código XML
caja_xml = tk.Text(ventana, height=10, width=70)
caja_xml.pack(pady=5)

etiqueta_xpath = tk.Label(ventana, text="Expresión XPath:")
etiqueta_xpath.pack(pady=5)

# Caja de texto para ingresar la expresión XPath
caja_xpath = tk.Entry(ventana, width=70)
caja_xpath.pack(pady=5)

# Botón para ejecutar la evaluación
boton_evaluar = tk.Button(ventana, text="Evaluar XPath", command=ejecutar_evaluacion)
boton_evaluar.pack(pady=10)

# Vincular la tecla "Enter" al cuadro de XPath y a la ventana
caja_xpath.bind("<Return>", ejecutar_evaluacion)  # Enter en la caja de XPath
ventana.bind("<Return>", ejecutar_evaluacion)  # Enter en cualquier parte de la ventana

# Caja de texto para mostrar los resultados
etiqueta_resultados = tk.Label(ventana, text="Resultados:")
etiqueta_resultados.pack(pady=5)

caja_resultados = tk.Text(ventana, height=10, width=70, wrap=tk.WORD, state=tk.DISABLED)
caja_resultados.pack(pady=5)

# Iniciar la aplicación
ventana.mainloop()

