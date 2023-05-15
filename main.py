'''
Diseño de lenguajes de programacion 
Ing. Gabriel Brolo
Seccion 40

Mirka Monzon 18139
16 de mayo de 2023
Laboratorio B
'''

import tkinter as tk
import re

'''
Laboratorio B 
Construccion de un AFN (NFA), el cual deberá transformar posteriormente a un AFD (DFA); además, 
deberá generar también un AFD directamente de la expresión regular r. Con los autómatas generados deberá determinar si 𝑤 ∈ 𝐿(𝑟).
'''
def ingresar():
    #variables r y w
    r = entry_r.get()
    w = entry_w.get()

    #implementacion de funciones 
    balanceada = verificar_balance(r)
    valida = verificar_validez(r)
    pertenece = verificar_pertenece(r, w)

    #casos variados de verifiacion 
    if balanceada and valida and pertenece: #si esta balanceada y es valida la cadena c
        output.delete(1.0, tk.END)
        output.insert(tk.END, "Sí")
    elif not balanceada : #en caso de no estar balanceada
        output.delete(1.0, tk.END)
        output.insert(tk.END, "r no está balanceada")
    else:
        output.delete(1.0, tk.END) #otro caso
        output.insert(tk.END, "No")

def verificar_balance(r):
    stack = []
    #combinacion principio y final de brackets
    opening_brackets = ['(', '[', '{']
    closing_brackets = [')', ']', '}']
    
    for char in r:
        if char in opening_brackets:
            stack.append(char) #implementacion de brackest inicio
        elif char in closing_brackets:
            if len(stack) == 0: #verificacion de brackets finales
                return False
            last_opening_bracket = stack.pop()
            if opening_brackets.index(last_opening_bracket) != closing_brackets.index(char): #verifiacion de par de brackets correctos
                return False
    
    return len(stack) == 0

def verificar_validez(r):
    #patron de expresion r
    pattern = r'^[a-z|A-Z|0-9|\(|\)|\[|\]|\{|\}|\+|\*|\?|\.|\||\;|\"|\^|\$|#|%|!|@|&|-|ε|\s]+$'
    return re.match(pattern, r) is not None

def verificar_pertenece(r, w):
    #en caso de vacio
    if not w: 
        return False

    
    #match con patron
    pattern = r'^' + r + r'$'
    return re.match(pattern, w) is not None

#conversión de una expresión regular en notación infix a notación postfix basado en algoritmo Shunting Yard
def infix_to_postfix(r):
    r = entry_r.get()
    #postfix_r = infix_to_postfix(r)

    pred = {'(': 1, '|': 2, '.': 3, '?': 4, '*': 4, '+': 4, '^': 5, '/': 6, '-': 6}
    output = []
    stack = []

    for char in r:
        if char.isalpha():
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop() 
        else:  
            while stack and pred.get(char, 0) <= pred.get(stack[-1], 0):
                output.append(stack.pop())
            stack.append(char)

    while stack:
        output.append(stack.pop())

    expresion_postfix = ''.join(output)
    return expresion_postfix

def afn_afd():
    pass

def afd_directo():
    pass

def afd_subconjuntos():
    pass

def afd_minimizacion():
    pass




'''
Interfaz grafica Tkinter
'''
#ventana principal
window = tk.Tk()
window.title("Autómatas - LAB B")

#label e imputs r y w
label_r = tk.Label(window, text="Expresión 𝑟:")
entry_r = tk.Entry(window, width=35, background="light steel blue")

label_w = tk.Label(window, text="Cadena 𝑤:")
entry_w = tk.Entry(window, width=35, background="light steel blue")

#boton verificar
button_verificar = tk.Button(window, text="Verificar", command=ingresar)

#"si" o "no"
text_pertenece = tk.Label(window, text="𝑤 ∈ 𝐿(𝑟)")
output = tk.Text(window, height=4, width=35, background="light steel blue")

#botones af
button_afn_afd = tk.Button(window, text="AFN - AFD", command=afn_afd)
button_afd_directo = tk.Button(window, text="AFD directo", command=afd_directo)
button_afd_subconjuntos = tk.Button(window, text="AFD subconjuntos", command=afd_subconjuntos)
button_afd_minimizacion = tk.Button(window, text="AFD minimización", command=afd_minimizacion)

#pack ubicacion de elementos
label_r.pack()
entry_r.pack()

label_w.pack()
entry_w.pack()

button_verificar.pack()

text_pertenece.pack()

output.pack()

button_afn_afd.pack()
button_afd_directo.pack()
button_afd_subconjuntos.pack()
button_afd_minimizacion.pack()

#iniciazion de ventana
window.mainloop()