import os
gitbranch = 'test'
deleteCommands = 'git checkout -b %s; git checkout %s; git rm -r --cached .; git add .; git commit -m "deleted images"; git push;'%(branchName, branchName)
with open('.gitignore','r') as gitignore:
    newIgnore = gitignore.readlines()
newIgnore[2] = 'images/*'
with open('.gitignore','w') as gitignore:
    gitignore.writelines(newIgnore)
    gitignore.close()
os.system(deleteCommands)
