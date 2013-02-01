# -*- coding: utf-8 -*-

from libraries import Vhost

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


