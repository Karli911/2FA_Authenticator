{pkgs}: {
  deps = [
    pkgs.sqlcipher
    pkgs.rustc
    pkgs.pkg-config
    pkgs.openssl
    pkgs.libxcrypt
    pkgs.libiconv
    pkgs.cargo
    pkgs.libGLU
    pkgs.libGL
  ];
}
