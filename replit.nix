{pkgs}: {
  deps = [
    pkgs.ffmpeg-full
    pkgs.which
    pkgs.libpng
    pkgs.libjpeg_turbo
    pkgs.pkg-config
    pkgs.postgresql
  ];
}
