import os
from optparse import OptionParser
from libraries import Vhost

parser = OptionParser()
parser.add_option("--user", dest="user",
                  help="Nome spazio (e utente di conseguenza)")

(options, args) = parser.parse_args(['--user=dev3.from-italy.local'])

print options

#host_ip = "192.168.2.109" steppa
host_ip = "192.168.2.109" #tundra

spazi = (
        {
            'user': 'web1.greendemo.local',
            'samba_share': 'Greendemo_Web1'
        },
        {
            'user': 'dev2.furla-backend.local',
            'samba_share': 'Furla_Backend_Dev2'
        },
        {
            'user': 'dev2.furla-branch.local',
            'samba_share': 'Furla_Branch_Dev2'
        },
        {
            'user': 'dev2.furla-backend-branch.local',
            'samba_share': 'Furla_Backend_Branch_Dev2'
        },
        )

#spazi = (
        #{
         #'user': 'dev3.from-italy.local',
         #'samba_share': 'From_Italy_Dev3'
        #},
        #{
         #'user': 'dev3-admin.from-italy.local',
         #'samba_share': 'From_Italy_Admin_Dev3'
        #},
        #{
         #'user': 'dev3-reed.from-italy.local',
         #'samba_share': 'From_Italy_Reed_Dev3'
        #},
        #{
         #'user': 'dev4.from-italy.local',
         #'samba_share': 'From_Italy_Dev4'
        #},
        #{
         #'user': 'dev4-admin.from-italy.local',
         #'samba_share': 'From_Italy_Admin_Dev4'
        #},
        #{
         #'user': 'dev4-reed.from-italy.local',
         #'samba_share': 'From_Italy_Reed_Dev4'
        #},
        #{
         #'user': 'dev5.from-italy.local',
         #'samba_share': 'From_Italy_Dev5'
        #},
        #{
         #'user': 'dev5-admin.from-italy.local',
         #'samba_share': 'From_Italy_Admin_Dev5'
        #},
        #{
         #'user': 'dev5-reed.from-italy.local',
         #'samba_share': 'From_Italy_Reed_Dev5'
        #},
        #{
         #'user': 'web1.from-italy.local',
         #'samba_share': 'From_Italy_Web1'
        #},
        #{
         #'user': 'web1-admin.from-italy.local',
         #'samba_share': 'From_Italy_Admin_Web1'
        #},
        #{
         #'user': 'web1-reed.from-italy.local',
         #'samba_share': 'From_Italy_Reed_Web1'
        #},
        #)

question = "Scrivi l'ultimo user id utilizzato: ";

vhosts = []

for spazio in spazi:
    vhosts.append(Vhost(spazio["user"], spazio["samba_share"]))



#vhost = Vhost(options.user)

last_user_id = raw_input(question)

path = os.path.dirname(os.path.abspath(__file__))


for vhost in vhosts:
    last_user_id = int(last_user_id) + 1
    vhost.user_id = last_user_id
    vhost.host_ip = host_ip
    vhost.generate_strings(path)

#user

f = open(path + r"\output.txt", "w")

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

#print "Copia questa stringa in webmin/creazione utenti: "

#print vhost.open_and_replace( path + r"\templates\user.tpl")

#question = "Premi un qualsiasi tasto per continuare quando hai fatto. "

#choice = raw_input("Premi invio per continuare quando hai fatto. ")


# logs
# accontentiamoci intanto

exit()

print "Log Rotation:"
print vhost.open_and_replace( path + r"\templates\logrotate.tpl")

#f = open("/etc/logrotate.d/httpd")

print "Log Rotation:"
print vhost.open_and_replace( path + r"\templates\samba.tpl")

print "Log Rotation:"
print vhost.open_and_replace( path + r"\templates\vhost.tpl")

print "Log Rotation:"
print vhost.open_and_replace( path + r"\templates\cmd.tpl")

print "Log Rotation:"
print vhost.open_and_replace( path + r"\templates\logrotate.tpl")

