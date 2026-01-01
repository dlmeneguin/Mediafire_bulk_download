# Mediafire_bulk_download
Pastas que não foram comprimidas do mediafire são difíceis de baixar e requerem o premium do site, esta série de scripts python busca resolver este problema, baixando a pasta por meio do scrapping do Url fornecido

Neste repositório, você encontrará ao todo 3 scripts em python

mediafire_scraper.py,
downloader_requests.py,
downloader_selenium.py

Para funcionar, é necessário ter o chrome e o python instalados, além de baixar as depêndencias dos scripts, rodando no cmd "pip install requirement.txt"

A maneira que eles funcionam é que, primeiro deve-se pegar o link da pasta que deseja baixar do mediafire, agora, colocando este url em (START_URL = "SUA_URL") ao final do mediafire_scraper.py, o código irá recursivamente passar por todos os arquivos que devem ser instalados, mantendo o caminho de cada um e salvando o link de download, o output deste arquivo será mediafire_links.csv contendo todas essas informações.

Com o mediafire_links.csv, rode o downloader_requests, que baixará todos os arquivos enquanto mantém a estrutura original da pasta, naturalmente haverá erros, pois o mediafire bloqueia algumas solicitações autônomas, os arquivos que o código não conseguir baixar serão salvos em erros.csv e devem ser instalados por meio do downloader_selenium, que lerá o erros.csv e instalará os arquivos faltantes de maneira mais confiável, porém mais lenta.
