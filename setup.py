import os, datetime
from optparse import OptionParser
from libraries import Vhost
import yaml


stream = file('config.yml', 'r')    # 'document.yaml' contains a single YAML document.
yaml_result = yaml.load(stream)

vhosts = []

for vhost in yaml_result['vhosts']:
    vhosts.append(Vhost.from_yaml(vhost, yaml_result['defaults']))

for vhost in vhosts:
    print vhost.__dict__

path = os.path.dirname(os.path.abspath(__file__))

#altre operazioni necessarie
for vhost in vhosts:
    vhost.host_ip = yaml_result['defaults']['ip']
    vhost.generate_strings(path)

#user

f = open(path + r"\output" + datetime.datetime.now().strftime("%Y-%m-%d.%H-%m") + ".txt", "w")

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

exit()

