# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 19:33:41 2025

@author: mano
"""

import ast

def extract_info(filename):
    with open(filename, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename)

    classes = []
    functions = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            # Funciones a nivel de módulo
            func_name = node.name
            args = [arg.arg for arg in node.args.args]
            docstring = ast.get_docstring(node)
            functions.append((func_name, args, docstring))

        elif isinstance(node, ast.ClassDef):
            class_name = node.name
            class_doc = ast.get_docstring(node)
            methods = []

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_name = item.name
                    args = [arg.arg for arg in item.args.args if arg.arg != 'self']
                    method_doc = ast.get_docstring(item)
                    methods.append((method_name, args, method_doc))

            classes.append((class_name, class_doc, methods))

    return classes, functions


def format_markdown(classes, functions):
    md = []

    if functions:
        md.append("## Funciones a nivel de módulo\n")
        for name, args, doc in functions:
            md.append(f"### def {name}({', '.join(args)})\n")
            if doc:
                md.append(f"> {doc}\n")
            md.append("")  # Línea en blanco

    if classes:
        md.append("## Clases\n")
        for class_name, class_doc, methods in classes:
            md.append(f"### class {class_name}\n")
            if class_doc:
                md.append(f"> {class_doc}\n")
            for method_name, args, doc in methods:
                md.append(f"##### {method_name}({', '.join(args)})\n")
                if doc:
                    md.append(f"> {doc}\n")
            md.append("")  # Línea en blanco

    return "\n".join(md)


# Cambia el nombre del archivo por tu módulo
if __name__ == "__main__":
    archivo = "INEAPIpy/INE_functions.py"  # Reemplaza con tu archivo real
    clases, funciones = extract_info(archivo)
    markdown = format_markdown(clases, funciones)
    print(markdown)
