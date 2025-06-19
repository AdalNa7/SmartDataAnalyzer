{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.python310Packages.pip
    pkgs.python310Packages.numpy
    pkgs.python310Packages.pandas
    pkgs.python310Packages.flask
    pkgs.python310Packages.openpyxl
    pkgs.python310Packages.scikit-learn
    pkgs.python310Packages.plotly
    pkgs.python310Packages.statsmodels
    pkgs.stdenv.cc.cc.lib  # This is the key dependency for libstdc++.so.6
  ];
}
