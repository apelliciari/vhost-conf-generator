# -*- coding: utf-8 -*-

from libraries import Vhost, User, Group
import os
import yaml
import pprint
import settings

class TestVhost:
    def test_init_only_user(self):

        vhost = Vhost(
                user=User(name="dev3.piquadro.local", password="test"),
                name="dev3.piquadro.local"
                )

        print vhost.directory_options
        assert vhost.user.name == 'dev3.piquadro.local'
        assert vhost.name == 'dev3.piquadro.local'
        assert vhost.user.home == '/var/www/vhosts/dev3.piquadro.local'
        assert vhost.root == '/var/www/vhosts/dev3.piquadro.local'
        assert vhost.document_root == '/var/www/vhosts/dev3.piquadro.local/htdocs'
        assert vhost.user.samba is None
        assert vhost.user.shell == '/sbin/nologin'
        assert vhost.directives is None
        assert vhost.directory_options == settings.DEFAULT_VHOST_DIRECTORY_OPTIONS
        assert vhost.dns_zone == "piquadro.local"
        assert vhost.dns_record == "dev3"



    def test_yaml_simple(self):
        yaml_test = """
--- # config

options:
    write_in_netposition: 0

vhosts:
      - name: 'webtest.greendemo.local'
        root: "/var/www/vhost/webtests/webtest.greendemo.local"
        ip: "192.168.2.106"
        user:
            name: "webtests"
            samba: 'Greendemo_WebTest'
            shell: /bin/bash
            group:
                name: 'nginx'
                id: 45

"""

        yaml_result = yaml.load(yaml_test)

        vhosts = []

        yaml_defaults = yaml_result.get('defaults', {}) if type(yaml_result.get('defaults', {})) is dict else {}

        for yaml_vhost in yaml_result['vhosts']:
            vhosts.append(Vhost.yaml( dict(yaml_defaults.items() + yaml_vhost.items()) ) )

        vhost = vhosts.pop()

        assert vhost.name == 'webtest.greendemo.local'
        assert vhost.root == "/var/www/vhost/webtests/webtest.greendemo.local"
        assert vhost.document_root == "/var/www/vhost/webtests/webtest.greendemo.local/htdocs"
        assert vhost.user.name == 'webtests'
        assert vhost.user.home == '/var/www/vhosts/webtests'
        assert vhost.user.samba == "Greendemo_WebTest"
        assert vhost.user.shell == "/bin/bash"
        assert vhost.user.group.name == "nginx"
        assert vhost.user.group.id == 45

    def test_yaml_defaults(self):
        yaml_test = """
--- # config

defaults:
    ip: "192.168.2.111"
    user:
        name: "webtests"
        samba: 'Greendemo_WebTest'
        shell: /bin/bash
        group:
            name: 'nginx'
            id: 45

options:
    write_in_netposition: 0

vhosts:
      - name: 'webtest.greendemo.local'
        root: "/var/www/vhost/webtests/webtest.greendemo.local"
        ip: "192.168.2.106"

"""

        yaml_result = yaml.load(yaml_test)

        vhosts = []

        yaml_defaults = yaml_result.get('defaults', {}) if type(yaml_result.get('defaults', {})) is dict else {}


        for yaml_vhost in yaml_result['vhosts']:
            pprint.pprint(yaml_defaults)
            pprint.pprint(yaml_vhost)
            # da testare il merge dei dizionari
            #pprint.pprint(yaml_defaults)
            #pprint.pprint(dict(yaml_defaults, **yaml_vhost))
            #pprint.pprint(dict(yaml_defaults.items() + yaml_vhost.items()))
            #pprint.pprint(dict(yaml_vhost.items() + yaml_defaults.items()))
            #yaml_defaults.update(yaml_vhost)
            #pprint.pprint(yaml_defaults.update(yaml_defaults))
            vhosts.append(Vhost.yaml( dict(yaml_defaults.items() + yaml_vhost.items()) ) )

        vhost = vhosts.pop()

        assert vhost.name == 'webtest.greendemo.local'
        assert vhost.root == "/var/www/vhost/webtests/webtest.greendemo.local"
        assert vhost.document_root == "/var/www/vhost/webtests/webtest.greendemo.local/htdocs"
        assert vhost.user.name == 'webtests'
        assert vhost.user.home == '/var/www/vhosts/webtests'
        assert vhost.user.samba == "Greendemo_WebTest"
        assert vhost.user.shell == "/bin/bash"
        assert vhost.user.group.name == "nginx"
        assert vhost.user.group.id == 45


    def test_render_user(self):
        vhost = Vhost(
                user=User(name="dev3.piquadro.local", password="test"),
                name="dev3.piquadro.local"
                )
        #path = os.path.abspath(__file__)
        # works only if pytest is launched from the project root
        assert vhost.render("templates\\user.tpl") == "create:dev3.piquadro.local:test::48::/var/www/vhosts/dev3.piquadro.local:/sbin/nologin:::::"

    def test_render_logrotate(self):
        vhost = Vhost(
                user=User(name="dev3.piquadro.local", password="test"),
                name="dev3.piquadro.local"
                )
        #path = os.path.abspath(__file__)
        # works only if pytest is launched from the project root
        assert vhost.render("templates\\logrotate.tpl") == "/var/www/vhosts/dev3.piquadro.local/logs/*log"

    def test_render_vhost(self):
        vhost = Vhost(
                user=User(name="dev3.piquadro.local", password="test"),
                name="dev3.piquadro.local"
                )

        print vhost.render("templates\\vhost.tpl")
        assert vhost.render("templates\\vhost.tpl") == """
<VirtualHost 192.168.2.111:80>
    DocumentRoot /var/www/vhosts/dev3.piquadro.local/htdocs
    ServerName dev3.piquadro.local
    ServerAlias dev3.piquadro.local
    <Directory "/var/www/vhosts/dev3.piquadro.local/htdocs">
        Options All
        AllowOverride All
    </Directory>
    ErrorLog /var/www/vhosts/dev3.piquadro.local/logs/error_log
    CustomLog /var/www/vhosts/dev3.piquadro.local/logs/access_log combined

</VirtualHost>"""

    def test_render_samba(self):
        vhost = Vhost(
                user=User(
                    name="dev3.piquadro.local",
                    password="test",
                    samba="dev3_piquadro"),
                name="dev3.piquadro.local"
                )
        #path = os.path.abspath(__file__)
        # works only if pytest is launched from the project root
        assert vhost.render("templates\\samba.tpl") == """
[dev3_piquadro]
	force create mode = 600
	force user = dev3.piquadro.local
	delete readonly = yes
	writeable = yes
	create mode = 644
	path = /var/www/vhosts/dev3.piquadro.local
	force group = apache
"""

    def test_render_cmd(self):
        vhost = Vhost(
                user=User(name="dev3.piquadro.local", password="test"),
                name="dev3.piquadro.local"
                )
        #path = os.path.abspath(__file__)
        # works only if pytest is launched from the project root
        assert vhost.render("templates\\cmd.tpl") == \
"""mkdir /var/www/vhosts/dev3.piquadro.local /var/www/vhosts/dev3.piquadro.local/logs /var/www/vhosts/dev3.piquadro.local/htdocs
chown dev3.piquadro.local:apache /var/www/vhosts/dev3.piquadro.local
chown dev3.piquadro.local:apache /var/www/vhosts/dev3.piquadro.local/htdocs"""

    def test_extend_dict(self):
        default = {'ip': '192.168.2.111',
                'user': {'group': {'id': 45, 'name': 'nginx'},
                    'name': 'webtests',
                    'samba': 'Greendemo_WebTest',
                    'shell': '/bin/bash'}}
        vhost = {'ip': '192.168.2.106',
                'name': 'webtest.greendemo.local',
                'root': '/var/www/vhost/webtests/webtest.greendemo.local',
                'user': {'name': 'webtests'}}

        merge = {
                'ip': '192.168.2.106',
                'name': 'webtest.greendemo.local',
                'root': '/var/www/vhost/webtests/webtest.greendemo.local',
                'user': {'name': 'webtests'},
                #'user': {'group': {'id': 45, 'name': 'nginx'},
                    #'name': 'webtests',
                    #'samba': 'Greendemo_WebTest',}
                }

        assert dict(default.items() + vhost.items()) == merge

    def test_render_giasone(self):
        vhost = Vhost(
                user=User(
                    name="dev3.piquadro.local",
                    password="test",
                    samba="dev3_piquadro"),
                name="dev3.piquadro.local"
                )

        # works only if pytest is launched from the project root
        assert vhost.render("templates\\dns-giasone.tpl") == \
"""dnscmd /ZoneAdd piquadro.local /Primary /file piquadro.local.dns
dnscmd /RecordAdd piquadro.local dev3 A 192.168.2.111
dnscmd /RecordAdd piquadro.local @ NS castore.netidea.local"""

    def test_render_castore(self):
        vhost = Vhost(
                user=User(
                    name="dev3.piquadro.local",
                    password="test",
                    samba="dev3_piquadro"),
                name="dev3.piquadro.local"
                )

        # works only if pytest is launched from the project root
        assert vhost.render("templates\\dns-castore.tpl") == \
"""dnscmd /zoneadd piquadro.local /secondary 192.168.2.100 piquadro.local.dns"""
