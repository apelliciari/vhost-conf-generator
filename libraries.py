import mmap, string, random

class Vhost:

    def __init__(self, user, user_home=None, document_root=None, samba_share=None, shell=None, password=None,
            vhost_directives=None, vhost_name=None, vhost_directory_options=None, vhost_root=None ):

        self.user = user

        opt = ""
        if not vhost_name or vhost_name is None:
            if len(user.split('.')) == 2:
                opt = "www."
            vhost_name = opt + user
        self.vhost_name = vhost_name

        if not user_home or user_home is None:
            user_home = "/var/www/vhosts/" + user
        self.user_home = user_home

        if not vhost_root or vhost_root is None:
            vhost_root = user_home + vhost_name
        self.vhost_root = vhost_root

        if not document_root or document_root is None:
            document_root = vhost_root + "/htdocs"
        self.document_root = document_root

        if not vhost_directory_options or vhost_directory_options is None:
            vhost_directory_options = """Options All
    AllowOverride All"""
        self.vhost_directory_options = vhost_directory_options

        self.apache_group_id = 48

        self.samba_share = samba_share

        if not password or password is None:
            password = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(10))
        self.password = password

        self.shell = shell

        self.vhost_directives = vhost_directives


    @classmethod
    def from_yaml(clss, yaml_block, yaml_defaults):

        vhost = clss(
                user=yaml_block['user'],
                user_home=yaml_block.get('user_home', None),
                vhost_root=yaml_block.get('vhost_root', None),
                document_root=yaml_block.get('document_root', None),
                samba_share=yaml_block.get('samba_share', None),
                password=yaml_block.get('password', None),
                vhost_directives=yaml_block.get('vhost_directives', None),
                shell=yaml_block.get('shell', None),
                vhost_name=yaml_block.get('vhost_name', None))

        vhost.shell = yaml_block['shell'] if yaml_block.get('shell', None) else yaml_defaults['shell']

        if yaml_block.get('vhost_directory_options', None):
            vhost.vhost_directory_options = yaml_block['vhost_directory_options']

        vhost.password = '' if yaml_block.get('nopassword', None) or yaml_defaults.get('nopassword', None) else vhost.password

        return vhost

    def replace_all(self, text):
        for i, j in self.__dict__.iteritems():
            text = text.replace("{{" + i + "}}", str(j))
        return text

    def open_and_replace(self, tpl):
        f = open(tpl)
        s = f.read()
        f.close()
        s = self.replace_all(s)
        return s

    def search_in_file(self, file, text):
        f = open(file)
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if text in s:
            return True

        return False

    def generate_strings(self, path):
       self.user_string = self.open_and_replace( path + r"\templates\user.tpl")
       self.logrotate_string = self.open_and_replace( path + r"\templates\logrotate.tpl")
       if self.samba_share:
           self.samba_string = self.open_and_replace( path + r"\templates\samba.tpl")
       else:
           self.samba_string = ""
       self.vhost_string = self.open_and_replace( path + r"\templates\vhost.tpl")
       self.cmd_string = self.open_and_replace( path + r"\templates\cmd.tpl")

    def prospect(self):
        return {
                'url': self.vhost_name,
                'user': self.user,
                'password': self.password,
                'samba': self.samba_share,
                'document_root': self.document_root
                }
