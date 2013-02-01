# -*- coding: utf-8 -*-

from libraries import Vhost
import os

class TestVhost:
    def test_init_only_user(self):

        vhost = Vhost(
                user="dev3.piquadro.local"
                )

        assert vhost.user == 'dev3.piquadro.local'
        assert vhost.vhost_name == 'dev3.piquadro.local'
        assert vhost.user_home == '/var/www/vhosts/dev3.piquadro.local'
        assert vhost.vhost_root == '/var/www/vhosts/dev3.piquadro.local'
        assert vhost.document_root == '/var/www/vhosts/dev3.piquadro.local/htdocs'
        assert vhost.samba_share is None
        assert vhost.shell is None
        assert vhost.password is not None
        assert vhost.vhost_directives is None
        assert vhost.vhost_directory_options == """Options All
    AllowOverride All"""

    def test_init_only_user_no_www(self):

        vhost = Vhost(
                user="piquadro.local"
                )

        assert vhost.user == 'piquadro.local'
        assert vhost.vhost_name == 'www.piquadro.local'
        assert vhost.user_home == '/var/www/vhosts/piquadro.local'
        assert vhost.vhost_root == '/var/www/vhosts/www.piquadro.local'
        assert vhost.document_root == '/var/www/vhosts/www.piquadro.local/htdocs'
        assert vhost.samba_share is None
        assert vhost.shell is None
        assert vhost.password is not None
        assert vhost.vhost_directives is None
        assert vhost.vhost_directory_options == """Options All
    AllowOverride All"""

    def test_render(self):
        vhost = Vhost(
                user="dev3.piquadro.local",
                password="test",
                shell="/sbin/nologin"
                )
        #path = os.path.abspath(__file__)
        # works only if pytest is launched from the project root
        assert vhost.render("templates\\user.tpl") == "create:dev3.piquadro.local:test::48::/var/www/vhosts/dev3.piquadro.local:/sbin/nologin:::::"

    def test_generate_string(self):
        vhost = Vhost(
                user="dev3.piquadro.local",
                password="test",
                shell="/sbin/nologin",
                samba_share = "dev3_piquadro"
                )

        vhost.host_ip = "192.168.2.111"

        vhost.generate_strings(os.path.abspath(".")) # from root project
        #path = os.path.abspath(__file__)
        # works only if pytest is launched from the project root
        assert vhost.user_string == "create:dev3.piquadro.local:test::48::/var/www/vhosts/dev3.piquadro.local:/sbin/nologin:::::"
        assert vhost.logrotate_string == "/var/www/vhosts/dev3.piquadro.local/logs/*log"
        assert vhost.samba_share == """
[dev3_piquadro]
	force create mode = 600
	force user = dev3.piquadro.local
	delete readonly = yes
	writeable = yes
	create mode = 644
	path = /var/www/vhosts/dev3.piquadro.local
	force group = apache
"""
        assert vhost.cmd_string == \
"""mkdir /var/www/vhosts/dev3.piquadro.local /var/www/vhosts/dev3.piquadro.local/logs /var/www/vhosts/dev3.piquadro.local/htdocs
chown dev3.piquadro.local:apache /var/www/vhosts/dev3.piquadro.local
chown dev3.piquadro.local:apache /var/www/vhosts/dev3.piquadro.local/htdocs"""

        assert vhost.vhost_string == """
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

