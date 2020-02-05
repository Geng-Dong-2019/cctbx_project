from __future__ import absolute_import, division, print_function
import os
from libtbx import easy_run

pdb_string = '''
CRYST1  589.160  589.160  589.160  90.00  90.00  90.00 P 1
SCALE1      0.001697  0.000000  0.000000        0.00000
SCALE2      0.000000  0.001697  0.000000        0.00000
SCALE3      0.000000  0.000000  0.001697        0.00000
ATOM      1  N   CYS L 104     339.804 329.680 261.810  1.00 58.36           N
ATOM      2  CA  CYS L 104     338.530 329.122 261.395  1.00 60.90           C
ATOM      3  C   CYS L 104     337.438 329.433 262.396  1.00 63.21           C
ATOM      4  O   CYS L 104     336.436 330.048 262.048  1.00 65.22           O
ATOM      5  CB  CYS L 104     338.651 327.620 261.216  1.00 60.57           C
ATOM      6  SG  CYS L 104     339.341 326.788 262.654  1.00 60.22           S
ATOM      7  N   CYS L 108     338.113 325.778 267.745  1.00 68.92           N
ATOM      8  CA  CYS L 108     339.312 325.068 267.300  1.00 64.76           C
ATOM      9  C   CYS L 108     340.555 325.418 268.121  1.00 66.03           C
ATOM     10  O   CYS L 108     341.588 324.784 267.939  1.00 66.50           O
ATOM     11  CB  CYS L 108     339.571 325.286 265.807  1.00 60.82           C
ATOM     12  SG  CYS L 108     338.793 324.031 264.774  1.00 56.51           S
ATOM     13  N   CYS L 120     343.196 322.319 267.971  1.00 57.56           N
ATOM     14  CA  CYS L 120     342.863 321.598 266.735  1.00 57.89           C
ATOM     15  C   CYS L 120     344.051 321.463 265.784  1.00 59.16           C
ATOM     16  O   CYS L 120     344.945 322.303 265.759  1.00 57.82           O
ATOM     17  CB  CYS L 120     341.697 322.250 265.986  1.00 56.77           C
ATOM     18  SG  CYS L 120     341.374 321.502 264.369  1.00 53.53           S
ATOM     19  N   ILE L 121     344.035 320.383 265.006  1.00 61.55           N
ATOM     20  CA  ILE L 121     345.070 320.108 264.011  1.00 62.65           C
ATOM     21  C   ILE L 121     345.134 321.190 262.946  1.00 61.66           C
ATOM     22  O   ILE L 121     346.214 321.514 262.462  1.00 61.29           O
ATOM     23  CB  ILE L 121     344.869 318.724 263.337  1.00 64.79           C
ATOM     24  CG1 ILE L 121     346.106 318.329 262.529  1.00 65.49           C
ATOM     25  CG2 ILE L 121     343.629 318.694 262.442  1.00 64.60           C
ATOM     26  CD1 ILE L 121     346.129 316.868 262.147  1.00 66.90           C
ATOM     27  N   CYS L 122     343.982 321.748 262.588  1.00 64.24           N
ATOM     28  CA  CYS L 122     343.921 322.801 261.579  1.00 68.72           C
ATOM     29  C   CYS L 122     344.962 323.861 261.847  1.00 69.64           C
ATOM     30  O   CYS L 122     345.597 324.371 260.927  1.00 73.06           O
ATOM     31  CB  CYS L 122     342.536 323.448 261.549  1.00 70.95           C
ATOM     32  SG  CYS L 122     342.155 324.561 262.930  1.00 73.02           S
ATOM     33  N   CYS L 145     338.912 319.344 260.063  1.00 94.97           N
ATOM     34  CA  CYS L 145     338.541 318.949 261.422  1.00 92.47           C
ATOM     35  C   CYS L 145     337.032 318.807 261.564  1.00 88.78           C
ATOM     36  O   CYS L 145     336.270 319.314 260.742  1.00 89.04           O
ATOM     37  CB  CYS L 145     339.074 319.959 262.435  1.00 93.38           C
ATOM     38  SG  CYS L 145     338.049 321.426 262.672  1.00 97.07           S
ATOM     39  N   CYS L 148     334.801 322.398 262.418  1.00 90.56           N
ATOM     40  CA  CYS L 148     334.536 323.276 261.291  1.00 88.35           C
ATOM     41  C   CYS L 148     335.420 322.848 260.130  1.00 93.31           C
ATOM     42  O   CYS L 148     336.536 322.377 260.342  1.00 95.93           O
ATOM     43  CB  CYS L 148     334.872 324.701 261.685  1.00 84.75           C
ATOM     44  SG  CYS L 148     336.541 324.858 262.342  1.00 79.52           S
ATOM     45  N   CYS L 150     338.090 323.242 257.957  1.00 99.57           N
ATOM     46  CA  CYS L 150     339.243 324.167 257.968  1.00 99.81           C
ATOM     47  C   CYS L 150     340.562 323.546 257.510  1.00 98.81           C
ATOM     48  O   CYS L 150     341.485 323.322 258.299  1.00 93.05           O
ATOM     49  CB  CYS L 150     339.390 324.814 259.342  1.00 97.02           C
ATOM     50  SG  CYS L 150     339.376 323.663 260.725  1.00 94.12           S
TER
HETATM   51 ZN    ZN L1000     337.686 325.976 263.586  1.00 31.11          Zn
HETATM   52 ZN    ZN L1001     340.645 325.701 261.809  1.00 38.33          Zn
HETATM   53 ZN    ZN L1002     340.121 322.858 263.346  1.00 15.24          Zn
END
'''

def main():
  with open('tst_mcl_02.pdb', 'w') as f:
    f.write(pdb_string)
  cmd = 'phenix.pdb_interpretation tst_mcl_02.pdb write_geo=1'
  print (cmd)
  rc = easy_run.go(cmd)
  assert os.path.exists('tst_mcl_02.pdb.geo')
  return rc.return_code

if __name__ == '__main__':
  rc = main()
  assert not rc
  print('OK')