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
description=settings.DESCRIPTION
)

parser.add_argument('config_file', metavar='CONFIG_FILE',
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

try:
    stream = file(args.config_file, 'r')    # 'document.yaml' contains a single YAML document.
except IOError as e:
    print "IO error, %s: %s " % (e.strerror, e.filename)
    exit()

yaml_result = yaml.load(stream)

vhosts = []

yaml_defaults = yaml_result.get('defaults', {}) if type(yaml_result.get('defaults', {})) is dict else {}

for yaml_vhost in yaml_result['vhosts']:
    vhosts.append(Vhost.yaml( dict(yaml_defaults.items() + yaml_vhost.items()) ) )


#altre operazioni necessarie
for vhost in vhosts:
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


