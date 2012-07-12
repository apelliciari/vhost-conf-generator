# -*- mode: python -*-


def version ():
    command = r"git --git-dir=C:\Users\alessandro\Desktop\vhost_generator\.git rev-parse HEAD"
    return subprocess.check_output(command.split(), shell=True).rstrip('\r\n')

a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'C:\\Users\\alessandro\\Desktop\\vhost_generator\\setup.py'],
             pathex=['C:\\Home\\Python\\pyinstaller-1.5-rc1'])

a.datas += [("templates/user.tpl",'C:\\Users\\alessandro\\Desktop\\vhost_generator\\templates\\user.tpl',"DATA")]
a.datas += [("templates/logrotate.tpl",'C:\\Users\\alessandro\\Desktop\\vhost_generator\\templates\\logrotate.tpl',"DATA")]
a.datas += [("templates/samba.tpl",'C:\\Users\\alessandro\\Desktop\\vhost_generator\\templates\\samba.tpl',"DATA")]
a.datas += [("templates/cmd.tpl",'C:\\Users\\alessandro\\Desktop\\vhost_generator\\templates\\cmd.tpl',"DATA")]
a.datas += [("templates/vhost.tpl",'C:\\Users\\alessandro\\Desktop\\vhost_generator\\templates\\vhost.tpl',"DATA")]

pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'vhost-conf-generator-'+ version() + '.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='C:\\Users\\alessandro\\Desktop\\vhost_generator\\salta-ai-risultati.ico')

