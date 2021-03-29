import os
import sys

with open('/opt/sftpy/conf/users.conf') as file:
    users = [p.strip() for p in file.read().split("\n") if p.strip() != '' and '#' not in p]

with open('/etc/group') as file:
    passwd = [p.strip() for p in file.read().split("\n") if p.strip() != '' and '#' not in p]

# layout
# <name>:<password>:<uid>
with open("/etc/rsyslog.d/sftp.conf", 'w+') as sftpconf:
    for user in users:
        param = user.split(":")
        if [p for p in passwd if param[0] in passwd] == 1:
            print(f"User {param[0]} already exists")
            sys.exit(os.EX_CONFIG)

        if len(param) == 3:
            if [p for p in passwd if param[2] in passwd] == 1:
                print(f"UID {param[2]} already exists")
                sys.exit(os.EX_CONFIG)

            os.system(f"adduser --shell /sbin/nologin --uid {param[2]} {param[0]}")
        else:
            os.system(f"adduser --shell /sbin/nologin {param[0]}")

        os.system(f"chown root:root /home/{param[0]}")
        os.system(f"chmod 0755 /home/{param[0]}")
        os.system(f"mkdir -m2755 /home/{param[0]}/dev")
        os.system(f'echo "{param[0]}:{param[1]}" | chpasswd')

        sftpconf.write(f'input(type="imuxsock" Socket="/home/{param[0]}/dev/log" CreatePath="on")\n')
        with open(f"/home/{param[0]}/.profile", 'w') as file:
            file.write("umask 0002")

    sftpconf.write("if $programname == 'internal-sftp' then /dev/stdout\n")
    sftpconf.write("& stop\n")
