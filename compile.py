#-------------------------------------------------------------------------------
#  $Id: compile.py 14 2011-03-18 14:42:43Z alessandro $ 
#  $Author: alessandro $
#  $Revision: 14 $
#  $Date: 2011-03-18 15:42:43 +0100 (ven, 18 mar 2011) $
#  $HeadURL: file:///X:/Consulenza/00-Redirect%20Checker/sviluppo/03%20SVN/trunk/compile.py $
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os
import pysvn

def saveVersion (filename,  repository):
    f = open(filename,  'w')
    f.write( str(retrieveVersion(repository) ) )
    f.close()

def retrieveVersion (repository):
    rev = pysvn.Revision( pysvn.opt_revision_kind.head )
    client = pysvn.Client()
    info = client.info2(repository, revision=rev, recurse=False)
    revno = info[0][1].rev.number # revision number as an integer    
    return revno

## 'python Makespec.py -w -o C:\Home\Python\check-301s\ -n "'+ projectname + '" --icon="C:\Home\Python\check-301s\salta-ai-risultati.ico" C:\Home\Python\check-301s\__init__.py'

pyinstallerfolder = 'C:/Home/Python/pyinstaller-1.5-rc1'
projectfolder = os.getcwd() + '\\'
executablesfolder = projectfolder + 'executables\\'

repository = 'file:///X:/Consulenza/00-Redirect%20Checker/sviluppo/03%20SVN/trunk/'

version = '-r' + str(retrieveVersion(repository))
projectname = 'redirect-checker' + version

makespec = 'python Makespec.py -w -F -o ' + executablesfolder + ' -n "'+ projectname + '" --icon="' + projectfolder + 'salta-ai-risultati.ico" ' + projectfolder + '__init__.py'
buildspec = 'python Build.py ' + executablesfolder +  projectname + '.spec'

if __name__ == "__main__":
    os.chdir(pyinstallerfolder)
    os.system(makespec)
    os.system(buildspec)
    saveVersion(projectfolder + 'version',  repository)
