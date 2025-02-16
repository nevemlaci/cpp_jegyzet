import subprocess
import sys


def commit_publish():
    print(f'Commit publish with commit message: {sys.argv[1]}')
    subprocess.run(['mdbook', 'build'])
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', sys.argv[1]])

def push_publish():
    print('Push publish')
    subprocess.run(['git', 'push'])
    subprocess.run(['git', 'subtree', 'push', '--prefix', 'book', 'origin', 'book'])

def normal_publish():
    print(f'Doing normal publish...')
    commit_publish()
    push_publish()

if len(sys.argv) < 2:
    raise RuntimeError

if len(sys.argv) == 2:
    if(sys.argv[1] == '--only_push'):
        push_publish()
    else:
        normal_publish()
else: 
    if(sys.argv[2] == '--no_push'):
        commit_publish()      
    else:
        normal_publish()


