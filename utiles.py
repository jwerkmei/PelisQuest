import re

def reemplazo_imagenes_y_links(texto):

    texto_modificado=''
    # Expresión regular para buscar imágenes en formato Markdown
    #regex = r'!\[.*?\]\((.*?)\)'
    #regex = r'\[(.*?)\]\((https?://.*?\.(?:png|jpg))\)' #r'\[(.*?)\]\((https?://.*?)\)'
    regex = r'\[([^\]]+)\]\((https?://[^\)]+\.(?:png|jpg))\)'

    # Reemplazar el formato Markdown por una etiqueta <img>
    #processed_content = re.sub(regex, r'<br/><img src="\1" alt="Imagen" style="max-width: 400px; height: 400px; margin-top: 10px; border-radius: 15px;">', last_message.content)

    texto_modificado= re.sub(r'!\[', r'[', texto)
    texto_modificado = re.sub(
        regex, 
        r'<br/><img src="\2" alt="\1" style="max-width: 400px; max-height: 400px; margin-top: 10px; border-radius: 15px;"><br/>', 
        texto_modificado
    )

    link_regex = r'\[([^\]]+)\]\((https?://(?!.*\.(?:png|jpg))([^\)]+))\)'

    # Reemplazar enlaces Markdown por etiquetas <a> en HTML
    texto_modificado = re.sub(link_regex, r'<a href="\2" target="_blank">\1</a>', texto_modificado)

    return texto_modificado