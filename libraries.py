# -*- coding: utf-8 -*-

import mmap
import string
import random
import settings
from jinja2 import Template

class Vhost:

    basepath = "/var/www/vhosts/"

    def __init__(self,
                    user,
                    name=None,
                    root=None,
                    document_root=None,
                    directives=None,
                    directory_options=None,
                    ip=None ):


        self.user = user

        opt = ""

        if not name or name is None:
            if len(user.name.split('.')) == 2:
                opt = "www."
            name = opt + user.name # se l'utente è senza www, lo aggiungo automaticamente al vhost
        self.name = name

        if not root or root is None:
            root = self.basepath + self.name
        self.root = root

        if not document_root or document_root is None:
            document_root = self.root + "/htdocs"
        self.document_root = document_root

        if not directory_options or directory_options is None:
            directory_options = settings.DEFAULT_VHOST_DIRECTORY_OPTIONS
        self.directory_options = directory_options

        if not ip or ip is None:
            ip = settings.DEFAULT_VHOST_IP
        self.ip = ip

        self.directives = directives


        # interni
        self.dns_record, self.dns_zone = self.name.split(".", 1) # maxsplit a 1

    def __repr__(self):
        return "%(name)s, with user %(user_name)s" % {'name': self.name, 'user_name': self.user.name}

    @classmethod
    def yaml(clss, yaml_opts):

        new = clss(
                user=User.yaml(yaml_opts['user']),
                root=yaml_opts.get('root', None),
                document_root=yaml_opts.get('document_root', None),
                directives=yaml_opts.get('directives', None),
                directory_options=yaml_opts.get('directory_options', None),
                name=yaml_opts.get('name', None),
                ip=yaml_opts.get('ip', None)
                )

        return new

    def generate_strings(self, path):
       self.user_string = self.render(path + r"\templates\user.tpl")
       self.logrotate_string = self.render(path + r"\templates\logrotate.tpl")
       self.samba_string = self.render(path + r"\templates\samba.tpl")
       self.vhost_string = self.render(path + r"\templates\vhost.tpl")
       self.cmd_string = self.render(path + r"\templates\cmd.tpl")

       if self.ip.startswith("192.168"):
           self.dns_giasone_string = self.render(path + r"\templates\dns-giasone.tpl")
           self.dns_castore_string = self.render(path + r"\templates\dns-castore.tpl")
       else:
           self.dns_giasone_string = None
           self.dns_castore_string = None


    def render(self, template_file):
       with open(template_file) as f:
           s = f.read()

       t = Template(s)
       return t.render(vhost=self)


class User:
    def __init__(self, name,
                    home=None, group=None,
                        password=None, samba=None,
                            shell=None):

        if name is None:
            raise ValueError("il parametro 'user' è obbligatorio")
        self.name = name

        if home is None:
            home = Vhost.basepath + name
        self.home = home

        if shell is None:
            shell = settings.DEFAULT_USER_SHELL
        self.shell = shell

        if group is None:
            group = Group()
        self.group = group

        if password is None:
           password = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(10))
        self.password = password

        self.samba = samba

    @classmethod
    def yaml(clss, yaml_opts):

        new = clss(
                group=Group.yaml(yaml_opts.get('group', {})),
                name=yaml_opts.get('name', None),
                password=yaml_opts.get('password', None),
                home=yaml_opts.get('home', None),
                samba=yaml_opts.get('samba', None),
                shell=yaml_opts.get('shell', None)
                )

        return new

class Group:
    def __init__(self, id=None, name=None):

        if name is None:
            name = settings.DEFAULT_GROUP_NAME
        self.name = name

        if id is None:
            id = settings.DEFAULT_GROUP_ID
        self.id = id

    @classmethod
    def yaml(clss, yaml_opts):

        new = clss(
                name=yaml_opts.get('name', None),
                id=yaml_opts.get('id', None)
                )

        return new

