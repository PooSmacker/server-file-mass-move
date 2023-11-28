import subprocess

# List your dependencies here
dependencies = ['paramiko', 'termcolor']

# Install dependencies
subprocess.run(['pip', 'install'] + dependencies)

# Run mass_move.py
subprocess.run(['python', 'mass_move.py'])
