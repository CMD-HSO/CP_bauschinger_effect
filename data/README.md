# Models and data

Finite element models and experimental data for the article
[Zandomeni et al. (2026), Mechanics of Materials 222, 105821](https://doi.org/10.1016/j.mechmat.2026.105821).

This directory is a copy of the Zenodo dataset
**https://doi.org/10.5281/zenodo.21869496** (v1.0.0). The Zenodo record is the archived,
citable version. Please cite its DOI when you use the data.

The data are licensed under **CC BY-SA 4.0** (see [LICENSE](LICENSE)), separately from
the code in this repository (AGPL-3.0).

## Contents

| Path | Content | Article |
|---|---|---|
| `Cyclic_data.dat` | Measured cyclic stress–strain data of 316L (`;`-separated: time, true stress in MPa, true strain, cycle, temperature in °C, type) | Fig. 1 |
| `EBSD.ctf` | EBSD orientation map of 316L (CTF format, exported from MTEX), basis for the RVE | Section 3.1 |
| `Models/Mesh0_Main_64k/` | 75-grain RVE, 40³ C3D8 elements, used for all main simulations | Section 3, Fig. 2 |
| `Models/Mesh1_8k[_conforming]/` | 10-grain volume element, 20³ elements, staircase / conforming grain boundaries | Appendix B |
| `Models/Mesh2_64k[_conforming]/` | 10-grain volume element, 40³ elements | Appendix B |
| `Models/Mesh3_512k[_conforming]/` | 10-grain volume element, 80³ elements, **not included in Git** (see below) | Appendix B |
| `Models/AbaqusInput_AmpTmp/` | Loading amplitude and output time points | |

Each model directory contains a job file `Job_*.inp` and the include files in
`AbaqusInput/`:

| File | Content |
|---|---|
| `*_grains.inp` | Nodes, elements and element sets per grain |
| `*_ANodes.inp` | Assembly node sets |
| `*_bc.inp` | Periodic boundary conditions (equations) |
| `*_mat.inp` | One `*User Material` per grain: elastic constants, hardening parameters, Euler angles (72 constants, 300 state variables) |

The job files run unchanged with Abaqus on Windows and Linux.

## 80³ meshes (`Mesh3_512k*`)

The two 80³ models are about 217 MB (single files up to 72 MB) and are therefore not
stored in Git. Download them from Zenodo with

```bash
python scripts/download_512k_meshes.py
```

run from the repository root. Alternatively, download `Dataset.zip` from the Zenodo
record by hand and copy the two `Mesh3_512k*` directories into `data/Models/`.

## Acknowledgments

The experimental data (EBSD, cyclic tests) were provided by W. Zhao, S. N. Babaei and
U. Krupp, RWTH Aachen University.
