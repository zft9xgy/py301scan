# py301scan

`py301scan` pretende ayudar al usuario a encontrar enlaces con redirecciones en un web.


> **Notice:**
> El proyecto es todavía en desarrollo y puede tener algunos bugs, te agradecería mucho que añadieras un issue o te pusieras en contacto conmigo por email zft9xgy@proton.me si encuentras algún bug, error o te gustaría añadir nuevas funcionalidades.

> Disclaimer:
> Este proyecto ha sido realizado para un uso particular y especifico y no esta diseñado para ser robusto y versatil.
> Actualmente el programa es lento para paginas web grandes, se mejorará en futuras versiones.

## Instalación 

### Requisitos

Tener instalado python3.

```sh 
git clone https://github.com/zft9xgy/py301scan.git
cd py301scan
pip3 intall -r requirements.txt
python3 app/init.py
```

## Uso

Actualmente el programa esta pensado para extraer lasd URLs desde un listas de sitemaps dados, por lo que deberas pegar las urls de tus sitema en el archivo `sitemaps_list.txt` que se encuentra dentro de la carpeta input. 

En caso de tener mas de una sitemap, introducelo uno por linea.

Para ejecutar el script, asegurate de estar en el directorio 'py301scan'

```sh
python3 app/main.py
```


## Documentación

 

## TODO

- implementar concurrencia en creacion de cache 
- implementar concurrecia en scanner interno

link_scanner.append_link_data_to_file
- crear funcion que obtenga el anchor, a veces link.text esta vacio
- usar modulo csv 
- posibilidad de crear objeto link para que sea mas simple el codigo


# Ideas
- desarrolar un modelo basado en objetos
- desarrolar interface grafica con pyqt o similar
- desarrollar cli interface con argsparser