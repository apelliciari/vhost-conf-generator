# -*- coding: utf-8 -*-

import os, datetime
from optparse import OptionParser
from libraries import Vhost
import yaml
import pymssql, _mssql, uuid, decimal
from pprint import pprint, pformat

# per pyinstaller
resource_path = os.environ.get("_MEIPASS2", os.path.abspath(".") )
parser = OptionParser()
parser.add_option("-c", "--conf", dest="config_file",
                  help="Nome file con le definizioni degli spazi (in formato YAML, .yml)")

(options, args) = parser.parse_args()

if not options.config_file:
    parser.error("Il file di configurazione e' richiesto")

stream = file(options.config_file, 'r')    # 'document.yaml' contains a single YAML document.
yaml_result = yaml.load(stream)

import pdb; pdb.set_trace()

vhosts = []

yaml_defaults = yaml_result.get('defaults', {}) if type(yaml_result.get('defaults', {})) is dict else {}

for yaml_vhost in yaml_result['vhosts']:
    vhosts.append(Vhost.yaml( dict(yaml_defaults.items() + yaml_vhost.items()) ) )

path = os.path.dirname(os.path.abspath(__file__))

output_dir = path + r"\output"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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

print "Writing on SQL server..."

if yaml_result["options"]["write_in_netposition"]:
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


