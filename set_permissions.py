import os

script1 = './utils/find_index.sh'
script2 = './utils/update.sh'

try:
    os.chmod(script1, 0o755)
    os.chmod(script2, 0o755)
    print('Permissions set successfully!')
    
except Exception as e:
    print(f'Error setting permissions: {e}')
    