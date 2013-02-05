# -*- coding: utf-8 -*-

import os, datetime
import argparse
from libraries import Vhost
import yaml
import pymssql, _mssql, uuid, decimal
from pprint import pprint, pformat
import settings

# per pyinstaller
resource_path = os.environ.get("_MEIPASS2", os.path.abspath(".") )

parser = argparse.ArgumentParser(
formatter_class=argparse.RawDescriptionHelpFormatter,
description="""
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

""" % (settings.DEFAULT_VHOST_IP, settings.DEFAULT_VHOST_DIRECTORY_OPTIONS, settings.DEFAULT_USER_SHELL,
        settings.DEFAULT_GROUP_NAME, settings.DEFAULT_GROUP_ID, settings.DEFAULT_OUTPUT_DIR  )
)

parser.add_argument('config_file', metavar='CONFIG_FILE', nargs=1,
                   help='File di configurazione')
parser.add_argument("-o", '--output_dir',
                   help='Directory in cui salvare il file/la directory generata, percorso assoluto',
                   default=settings.DEFAULT_OUTPUT_DIR)
parser.add_argument('--write_to_netposition',
                    action="store_true",
                   help='Scrive in NetPosition user e password generati',
                   default=False)
args = parser.parse_args()

output_dir = args.output_dir

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

stream = file(options.config_file, 'r')    # 'document.yaml' contains a single YAML document.
yaml_result = yaml.load(stream)

vhosts = []

yaml_defaults = yaml_result.get('defaults', {}) if type(yaml_result.get('defaults', {})) is dict else {}

for yaml_vhost in yaml_result['vhosts']:
    vhosts.append(Vhost.yaml( dict(yaml_defaults.items() + yaml_vhost.items()) ) )


#altre operazioni necessarie
for vhost in vhosts:
    #vhost.host_ip = yaml_result['defaults']['ip']
    vhost.generate_strings(resource_path)

print "PARSED: "

for index, vhost in enumerate(vhosts):
    print "#" + unicode(index)
    pprint(vhost.prospect())

#user
print "Writing configurations..."

if len(vhosts) < 5:
    f = open(output_dir + "\\" + datetime.datetime.now().strftime("%Y-%m-%d.%H-%M") + ".txt", "w")

    for vhost in vhosts:
        f.write(vhost.user_string)
    for vhost in vhosts:
        f.write(vhost.logrotate_string)
    for vhost in vhosts:
        f.write(vhost.samba_string)
    for vhost in vhosts:
        f.write(vhost.vhost_string)
    for vhost in vhosts:
        f.write(vhost.cmd_string)

    f.close()

else:
    dir = output_dir + "\\" + datetime.datetime.now().strftime("%Y-%m-%d.%H-%M")
    if not os.path.exists(dir):
        os.makedirs(dir)

    f = open(dir + r"\users.txt", "w")
    for vhost in vhosts:
        f.write(vhost.user_string)
    f.close()

    f = open(dir + r"\logrotation.txt", "w")
    for vhost in vhosts:
        f.write(vhost.logrotate_string)
    f.close()

    f = open(dir + r"\samba.txt", "w")
    for vhost in vhosts:
        f.write(vhost.samba_string)
    f.close()

    f = open(dir + r"\vhosts.txt", "w")
    for vhost in vhosts:
        f.write(vhost.vhost_string)
    f.close()

    f = open(dir + r"\mkdir-default-dirs.txt", "w")
    for vhost in vhosts:
        f.write(vhost.cmd_string)
    f.close()


if args.write_to_netposition:
    print "Writing on SQL server..."
    conn = pymssql.connect(host='CASTORE', user='python', password='python', database='NetPosition', as_dict=True)
    cur = conn.cursor()
    descrizione = ">> python vhost generator @ " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    for vhost in vhosts:
        cur.execute('SELECT * FROM DominiSingoli WHERE URL=%s and Username=%s', (vhost.vhost_name, vhost.user ))

        row = cur.fetchone()
        if row is not None:
            cur.execute('UPDATE DominiSingoli SET Password=%s, Descrizione=%s where IdDominioSingolo = %s', (vhost.password, descrizione, row['IdDominioSingolo'] ))
        else:
            cur.execute('INSERT INTO DominiSingoli (URL, Username, Password, Descrizione) \
                            VALUES (%s, %s, %s, %s)', (vhost.vhost_name, vhost.user, vhost.password, descrizione ))
    conn.commit()
    conn.close()


