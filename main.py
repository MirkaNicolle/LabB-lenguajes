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
import graphviz

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

    #casos de verifiacion 
    if balanceada and valida and pertenece: #si esta balanceada y es valida la cadena c
        output.delete(1.0, tk.END)
        output.insert(tk.END, "Sí")

        notacion_postfix = infix_to_postfix(r) #funcion de conversion
        print("Notación postfix:", notacion_postfix)

    elif not balanceada : #en caso de no estar balanceada
        output.delete(1.0, tk.END)
        output.insert(tk.END, "r no está balanceada")
    else:
        output.delete(1.0, tk.END) #otro caso
        output.insert(tk.END, "No")

        notacion_postfix = infix_to_postfix(r) #funcion de conversion
        print("Notación postfix:", notacion_postfix)

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

    pred = {'(': 1, '|': 2, '.': 3, '?': 4, '*': 4, '+': 4, '^': 5, '/': 6, '-': 6}
    postfix = []
    stack = []

    for char in r:
        if char.isalpha() or char in ('.', ';', '"'):
            postfix.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop() 
        else:  
            while stack and pred.get(char, 0) <= pred.get(stack[-1], 0):
                postfix.append(stack.pop())
            stack.append(char)

    while stack:
        [postfix].append(stack.pop())

    return ''.join(postfix)

def afn_afd(notacion_postfix):
    stack = []

    for char in notacion_postfix:
        if char.isalnum():
            # Crear un nuevo nodo para el símbolo alfanumérico
            stack.append({'label': char, 'edges': []})
        elif char == '.':
            # Concatenar dos últimos nodos de la pila
            if len(stack) >= 2:
                node2 = stack.pop()
                node1 = stack.pop()
                new_node = {'label': 'ε', 'edges': [(node1, ''), (node2, '')]}
                stack.append(new_node)
        elif char == '+':
            # Unir dos últimos nodos de la pila
            if len(stack) >= 2:
                node2 = stack.pop()
                node1 = stack.pop()
                new_node = {'label': 'ε', 'edges': [(node1, ''), (node2, '')]}
                stack.append(new_node)
        elif char == '*':
            # Crear un nuevo nodo para la clausura de Kleene
            if stack:
                node = stack.pop()
                new_node = {'label': 'ε', 'edges': [(node, ''), (new_node, '')]}
                stack.append(new_node)

    if stack:
        start_node = stack[0]
        final_node = stack[-1]
        
        # Generar el diagrama utilizando graphviz
        g = graphviz.Digraph(format='png')
        g.attr(rankdir='LR')
        g.attr('node', shape='doublecircle')
        g.node(final_node['label'])
        g.attr('node', shape='circle')
        g.attr('edge', arrowhead='empty')
        g.attr('edge', fontsize='10')

        visited = set()

        def generate_graph(node):
            if node not in visited:
                visited.add(node)
                for edge in node['edges']:
                    next_node, label = edge
                    g.edge(node['label'], next_node['label'], label=label)
                    generate_graph(next_node)

        generate_graph(start_node)
        g.render('afn', view=True)
    else:
        print("No se pudo completar el diagrama del AFN-AFD.")

def afd_directo(notacion_postfix):
    stack = []
    alphabet = set()
    states = []
    transitions = []

    for char in notacion_postfix:
        if char.isalnum():
            # Crear un nuevo estado para el símbolo alfanumérico
            stack.append(char)
            alphabet.add(char)
        elif char == '.':
            # Concatenar dos últimos estados de la pila
            if len(stack) >= 2:
                state2 = stack.pop()
                state1 = stack.pop()
                new_state = state1 + state2
                stack.append(new_state)
        elif char == '+':
            # Unir dos últimos estados de la pila
            if len(stack) >= 2:
                state2 = stack.pop()
                state1 = stack.pop()
                new_state = state1 + state2
                stack.append(new_state)
        elif char == '*':
            # Crear un nuevo estado para la clausura de Kleene
            if stack:
                state = stack.pop()
                new_state = state + "*"
                stack.append(new_state)

    if stack:
        start_state = stack[0]
        final_state = stack[-1]
        states = list(stack)

        # Generar las transiciones del AFD
        for state in states:
            for symbol in alphabet:
                if symbol in state:
                    if symbol.isalnum():
                        next_state = state.replace(symbol, "")
                        transitions.append((state, symbol, next_state))

        # Generar el diagrama utilizando graphviz
        g = graphviz.Digraph(format='png')
        g.attr(rankdir='LR')
        g.attr('node', shape='doublecircle')
        g.node(final_state)
        g.attr('node', shape='circle')
        g.attr('edge', arrowhead='empty')
        g.attr('edge', fontsize='10')

        for state in states:
            g.node(state)

        for transition in transitions:
            current_state, symbol, next_state = transition
            g.edge(current_state, next_state, label=symbol)

        g.render('afd', view=True)
    else:
        print("No se pudo completar el diagrama del AFD directo.")

def afd_subconjuntos(notacion_postfix):
    stack = []
    alphabet = set()
    states = []
    transitions = []

    for char in notacion_postfix:
        if char.isalnum():
            # Crear un nuevo estado para el símbolo alfanumérico
            stack.append({char})
            alphabet.add(char)
        elif char == '.':
            # Concatenar dos últimos estados de la pila
            if len(stack) >= 2:
                state2 = stack.pop()
                state1 = stack.pop()
                new_state = state1.union(state2)
                stack.append(new_state)
        elif char == '+':
            # Unir dos últimos estados de la pila
            if len(stack) >= 2:
                state2 = stack.pop()
                state1 = stack.pop()
                new_state = state1.union(state2)
                stack.append(new_state)
        elif char == '*':
            # Crear un nuevo estado para la clausura de Kleene
            if stack:
                state = stack.pop()
                new_state = state.copy()
                new_state.add('')
                stack.append(new_state)

    if stack:
        start_state = stack[0]
        final_state = stack[-1]
        states = list(stack)

        # Generar las transiciones del AFD utilizando el método de subconjuntos
        visited = set()
        unvisited = [start_state]
        
        while unvisited:
            current_state = unvisited.pop()
            visited.add(current_state)
            
            for symbol in alphabet:
                next_state = set()
                for state in current_state:
                    if state == '':
                        continue
                    if symbol in state:
                        next_state.add(state.replace(symbol, ''))
                
                if next_state and next_state not in visited:
                    unvisited.append(next_state)
                    transitions.append((current_state, symbol, next_state))

        # Generar el diagrama utilizando graphviz
        g = graphviz.Digraph(format='png')
        g.attr(rankdir='LR')
        g.attr('node', shape='doublecircle')
        g.node(final_state)
        g.attr('node', shape='circle')
        g.attr('edge', arrowhead='empty')
        g.attr('edge', fontsize='10')

        for state in states:
            state_label = ','.join(sorted(state, key=lambda x: (len(x), x)))
            g.node(state_label)
            if final_state.issubset(state):
                g.edge(state_label, final_state, label='ε')

        for transition in transitions:
            current_state, symbol, next_state = transition
            current_state_label = ','.join(sorted(current_state, key=lambda x: (len(x), x)))
            next_state_label = ','.join(sorted(next_state, key=lambda x: (len(x), x)))
            g.edge(current_state_label, next_state_label, label=symbol)

        g.render('afd_subconjuntos', view=True)
    else:
        print("No se pudo completar el diagrama del AFD por subconjuntos.")

def afd_minimizacion(notacion_postfix):
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