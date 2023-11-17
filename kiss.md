# keep it simple, stupid

- a list of sitemap urls where take the urls (input/sitemap_list.txt)
- obtener el listado de urls de cada sitemap y incluirlos en un fichero (input/urls_list.txt)
- de cada url, buscar los links contenidos en esa página.
- reportar todo: source, link, anchor, location tag(header,body,footer)

acutalmente el programa va muy lento. y esta reportando todos los enlaces, de todas las paginas.
como mucho de ellos son iguales, si el link que tiene ya esta reportado en la lista, no deberia de

- lists de sitemaps
- extraer listado de urls a analizar
- cachear urls para una lectura mas rapida
  -- for url in urls
  --- de cada url crea un soup y busca los hrefs -> links
  --- links = find all links in this url
  ---- for link in links
  ----- if request.header(link).status_code != 200
  ----- solo reporta enlaces que no sean 200
  ----- crear lista: status_code,link,source_url,anchor,tag_location

1 url, 30 links 10 head, 10 footer, 10 body.
request_header if no 200, reporta todo
si es 200 solo reporta el estado sin buscar
