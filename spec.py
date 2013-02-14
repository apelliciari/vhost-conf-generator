# -*- mode: python -*-
#from pack import projectfolder, version, pyinstallerfolder

projectfolder = 'C:/Home/vhost_generator/'
pyinstallerfolder = 'C:/Home/Python/pyinstaller-1.5-rc1'


f = open(projectfolder + 'version')
version = f.read()
f.close()

a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), projectfolder + 'main.py'],
             pathex=[pyinstallerfolder])

a.datas += [("templates/user.tpl", projectfolder + 'templates\\user.tpl',"DATA")]
a.datas += [("templates/logrotate.tpl", projectfolder + 'templates\\logrotate.tpl',"DATA")]
a.datas += [("templates/samba.tpl", projectfolder + 'templates\\samba.tpl',"DATA")]
a.datas += [("templates/cmd.tpl", projectfolder + 'templates\\cmd.tpl',"DATA")]
a.datas += [("templates/vhost.tpl", projectfolder + 'templates\\vhost.tpl',"DATA")]
a.datas += [("templates/dns-giasone.tpl", projectfolder + 'templates\\vhost.tpl',"DATA")]
a.datas += [("templates/dns-castore.tpl", projectfolder + 'templates\\vhost.tpl',"DATA")]

pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'vhost-conf-generator-'+ version + '.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=True , icon=projectfolder + 'salta-ai-risultati.ico')


