import paramiko
import traceback
import tkinter as tk
from tkinter import filedialog
from termcolor import colored

def choose_local_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a file to upload")
    return file_path

def get_remote_file_path():
    remote_file_path = input("Enter the name for the file on the server (include the file extension, e.g., python.py): ")
    return remote_file_path

def print_colored_message(message, color):
    print(colored(message, color))

def upload_file_to_server(server_info, local_file_path, remote_file_path):
    try:
        print(f"Connecting to {server_info['ip']}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_info['ip'], port=server_info['port'], username=server_info['username'], password=server_info['password'])

        print(f"Connected to {server_info['ip']}. Uploading file...")
        sftp = ssh.open_sftp()
        sftp.put(local_file_path, remote_file_path)
        print_colored_message(f"File uploaded successfully to {server_info['ip']}", 'green')

    except paramiko.AuthenticationException:
        print_colored_message(f"Authentication failed for {server_info['ip']}. Check username and password.", 'red')
    except paramiko.SSHException as e:
        print_colored_message(f"SSH connection failed for {server_info['ip']}: {str(e)}", 'red')
    except Exception as e:
        traceback.print_exc()
        print_colored_message(f"Error uploading file to {server_info['ip']}: {str(e)}", 'red')

    finally:
        if ssh:
            ssh.close()
        if sftp:
            sftp.close()

def run_post_upload_command(server_info, command):
    try:
        print(f"Connecting to {server_info['ip']}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_info['ip'], port=server_info['port'], username=server_info['username'], password=server_info['password'])

        print(f"Connected to {server_info['ip']}. Running post-upload command: {command}")
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout.read().decode('utf-8'))

    except paramiko.AuthenticationException:
        print_colored_message(f"Authentication failed for {server_info['ip']}. Check username and password.", 'red')
    except paramiko.SSHException as e:
        print_colored_message(f"SSH connection failed for {server_info['ip']}: {str(e)}", 'red')
    except Exception as e:
        traceback.print_exc()
        print_colored_message(f"Error running command on {server_info['ip']}: {str(e)}", 'red')

    finally:
        if ssh:
            ssh.close()

if __name__ == "__main__":
    servers = [
        {
            'ip': 'your server ip here',
            'port': 22,
            'username': 'server username',
            'password': 'server password'
        },
        {
            'ip': 'your server ip here',
            'port': 22,
            'username': 'server username',
            'password': 'server password'
        },
        # Add entries for the remaining servers, just copy and paste the ones above below
    ]

    # Local file path
    local_file_path = choose_local_file()

    # Remote file path
    remote_file_path = get_remote_file_path()

    # Upload the file to all servers
    for server_info in servers:
        upload_file_to_server(server_info, local_file_path, remote_file_path)
 
    enable_post_upload_command = False # You can enable this feature by replacing False with True and vice versa
    if enable_post_upload_command:
        post_upload_command = ''  # This feature allows you to run a command on all servers after upload eg chmod 777 * will make everything an executable after moving all files
        for server_info in servers:
            run_post_upload_command(server_info, post_upload_command)

    # Prompt the user to press enter to exit
    input("Press enter to exit")
