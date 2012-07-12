#-------------------------------------------------------------------------------
#  $Id: compile.py 14 2011-03-18 14:42:43Z alessandro $
#  $Author: alessandro $
#  $Revision: 14 $
#  $Date: 2011-03-18 15:42:43 +0100 (ven, 18 mar 2011) $
#  $HeadURL: file:///X:/Consulenza/00-Redirect%20Checker/sviluppo/03%20SVN/trunk/compile.py $
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os

## 'python Makespec.py -w -o C:\Home\Python\check-301s\ -n "'+ projectname + '" --icon="C:\Home\Python\check-301s\salta-ai-risultati.ico" C:\Home\Python\check-301s\__init__.py'

pyinstallerfolder = 'C:/Home/Python/pyinstaller-1.5-rc1'
projectfolder = os.getcwd() + '\\'
executablesfolder = projectfolder + 'executables\\'

projectname = 'vhost-conf-generator' + "-" + retrieveVersion()

buildspec = 'python Build.py ' + projectfolder + 'spec.py'

if __name__ == "__main__":
    os.chdir(pyinstallerfolder)
    os.system(buildspec)
