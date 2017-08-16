import os, re, sys
#checkout to different branch name to your own and make sure it has upstream
responce = ''
while re.match(re.compile('y(es|eah)?'), responce) is None:
    print "\033[91m\nWARNING: THIS WILL DELETE THE IMAGES FOLDER AND ALL IT'S CONTENT"
    responce = raw_input('Type "yes" or "y" to continue:\n\033[0m')
    if  re.match(re.compile('n(o|ah)?'), responce):
        sys.exit('exiting....')
def getBranchName():
    with open('.git/HEAD','r') as head:
        branch = head.readline().split('/')[-1].rstrip()
        return branch if branch != 'master' else sys.exit('checkout to different branch then run again')
branchName = getBranchName()
deleteCommands = 'git rm -r --cached .; git add .; git commit -m "deleted images"; git push; rm -rf images'
with open('.gitignore','r') as gitignore:
    newIgnore = gitignore.readlines()
newIgnore[2] = 'images/*'
with open('.gitignore','w') as gitignore:
    gitignore.writelines(newIgnore)
    gitignore.close()
os.system(deleteCommands)
