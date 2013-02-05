# -*- coding: utf-8 -*-

import os

DEFAULT_VHOST_DIRECTORY_OPTIONS = \
"""    Options All
        AllowOverride All"""

DEFAULT_VHOST_IP = "192.168.2.111"

DEFAULT_USER_SHELL = "/sbin/nologin"

DEFAULT_GROUP_NAME = "apache"

DEFAULT_GROUP_ID = 48

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

DEFAULT_OUTPUT_DIR = ROOT_PATH + r"\output"

DESCRIPTION =  """
Applicazione per generare i file di configurazione per nuovi virtual hosts.

L'applicazione legge un file .yml strutturato in questo modo (vedi esempio sotto):

--- # config di esempio

defaults:
    ip: 192.168.2.100

vhosts:
  # vhost n 1, con tutti i campi
  - name: 'dev.greenbox.local'
    root: "/var/www/vhost/greenbox/dev.greenbox.local"
    document_root: "/var/www/vhost/greenbox/dev.greenbox.local/htdocs/gu-admin"
    directory_options: "AllowOverride All"
    directives: "RewriteMap $lc"
    ip: "192.168.2.106"
    user:
        name: "greenbox"
        samba: 'Dev_Greenbox'
        password: "box"
        shell: "/bin/bash"
        group:
            name: 'lighttpd'
            id: 40

  # vhost n 2
  - name: 'dev2.greenbox.local'
    user:
        name: "greenbox"

Descrizione parametri:

defaults: valori di default che vengono assunti se non e' specificato altrimenti

vhosts: elenco dei virtual host da creare

Elenco campi disponibili per il vhost (* sono obbligatori):
- name*: il nome del virtual host, eg. dev3.greenbox.local
- root: percorso del virtual host. Default: /var/www/vhosts/{name}
- document_root: autoesplicativo. Default: {root}/htdocs
- ip: l'ip del virtual host. Default: %s
- directory_options: opzioni per il campo <Directory> dentro al vhost. Default: %s
- directives: direttive eccezionali (tipo rewriteMap). Finiscono in fondo alla
configurazione del vhost, appena prima della chiusura </VirtualHost>. Default: vuoto
- user: utente a cui legare il virtual host. e' un oggetto a parte

Elenco campi disponibili per l'user (* sono obbligatori):
- name*: nome utente
- home: user home. Default: /var/www/vhosts/{name}
- shell. shell utente. Default: %s
- password: password utente. Default: se non settata, stringa random di 10
  caratteri alfanumerici
- samba: nome della cartella samba da creare. Default: nessuno. Se non viene
  passato questo dato, la configurazione samba non viene creata (probabilmente perchè già presente)
- group: il gruppo dell'utente. e' un oggetto a parte

Elenco campi disponibili per il group (* sono obbligatori):
- name: nome gruppo. Default: %s
- id: id del gruppo. Default: %s

La directory default di output e': "%s". E' possibile cambiarla, vedi opzione -o.

""" % (DEFAULT_VHOST_IP, DEFAULT_VHOST_DIRECTORY_OPTIONS, DEFAULT_USER_SHELL,
        DEFAULT_GROUP_NAME, DEFAULT_GROUP_ID, DEFAULT_OUTPUT_DIR  )
