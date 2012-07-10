import mmap

class Vhost:

    def __init__(self, user, samba_share):
        self.user = user
        self.user_home = "/var/www/vhosts/" + user
        self.document_root = self.user_home + "/htdocs"
        self.apache_group_id = 48
        self.samba_share = samba_share

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
       self.samba_string = self.open_and_replace( path + r"\templates\samba.tpl")
       self.vhost_string = self.open_and_replace( path + r"\templates\vhost.tpl")
       self.cmd_string = self.open_and_replace( path + r"\templates\cmd.tpl")

