import sys
import os
import subprocess

TEMP_DIRECTORY_NAME = 'crawl'

def stripLines(lines):
    return [l.strip('\n') for l in lines]

def cmdOutputLines(cmd):
    return stripLines(os.popen(cmd).readlines())

def printTree(tree):
    os.system(f"git cat-file -p {tree} | awk '{{print $3}}'")

def walkCommit(commit):
    lines = cmdOutputLines(f"git cat-file -p {commit} | head -n 2 ")
    d = dict([ (l.split(' ')[0], l.split(' ')[1]) for l in lines ])
    printTree(d['tree'])
    if 'parent' in d:
        walkCommit(d['parent'])

def main():
    url = sys.argv[1]
    os.mkdir(TEMP_DIRECTORY_NAME)
    os.chdir(TEMP_DIRECTORY_NAME)

    subprocess.run(args=["git", "clone", url, "."], stderr=subprocess.DEVNULL)
    commits = cmdOutputLines('find .git/refs/heads -type f | xargs cat')
    for c in commits:
        walkCommit(c)

    os.chdir('..')
    subprocess.run(args=['rm','-rf', TEMP_DIRECTORY_NAME])

main()