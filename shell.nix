{ pkgs ? import <nixpkgs> { } }:

let
  myPyPkgs = pypkgs: with pypkgs; [
    ipython
    matplotlib
    netcdf4
    pandas
    python-language-server
    xarray
    dask
    wrf-python
  ];

  myPython3 = pkgs.python3.withPackages myPyPkgs;

in pkgs.mkShell rec {
  buildInputs = with pkgs; [
    myPython3
    gmt
  ];
}
