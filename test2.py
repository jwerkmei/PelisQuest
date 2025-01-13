import re

# Texto de ejemplo
texto_modificado = '''Puedes ver "Lost" en las siguientes plataformas:

[![Disney Plus](https://images.justwatch.com/icon/313118777/s100/disneyplus.png)](https://disneyplus.bn5x.net/c/1206980/705874/9358?u=https%3A%2F%2Fwww.disneyplus.com%2Fseries%2Flost%2F49VjIYAiy7oh&subId3=justappsvod)

[![Netflix](https://images.justwatch.com/icon/207360008/s100/netflix.png)](https://www.netflix.com/title/70136118)
'''

# Expresión regular para las imágenes embebidas en los enlaces Markdown
img_link_regex = r'\!\[([^\]]*)\]\((https?://[^\s)]+)\)\]\((https?://[^\s)]+)\)'

# Reemplazar imágenes embebidas en enlaces Markdown por <a> y <img>
texto_modificado = re.sub(img_link_regex, r'<a href="\3" target="_blank"><img src="\2" alt="\1"></a>', texto_modificado)

# Expresión regular para enlaces simples Markdown (sin imagen)
link_regex = r'\[([^\]]+)\]\((https?://[^\s)]+)\)'

# Reemplazar enlaces Markdown por etiquetas <a> en HTML
texto_modificado = re.sub(link_regex, r'<a href="\2" target="_blank">\1</a>', texto_modificado)

# Imprimir el resultado
print(texto_modificado)
