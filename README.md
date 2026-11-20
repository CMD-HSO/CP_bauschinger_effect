# Supporting material for the article “Quantitative assessment of the Bauschinger effect in cyclically loaded polycrystals using single crystal plasticity modeling with local and non-local kinematic hardening”

Crystal plasticity user material subroutine (UMAT) for Abaqus/Standard with
local and non-local kinematic hardening, together with the finite element models and
experimental data of the article

> R. Zandomeni, T. Seifert, A. Hartmaier (2026).
> *Quantitative assessment of the Bauschinger effect in cyclically loaded polycrystals
> using single crystal plasticity modeling with local and non-local kinematic hardening.*
> Mechanics of Materials 222, 105821.
> https://doi.org/10.1016/j.mechmat.2026.105821

> **Status of the code:** The UMAT version used in the article contains third-party
> numerical routines whose license does not permit redistribution of source code. These
> routines are currently being replaced by independently implemented, openly licensed
> equivalents. The code will then be released in `src/` under the AGPL-3.0 license,
> together with a verification against the results of the article.
>
> Until then, please refer to the ICAMS crystal plasticity UMAT
> (https://github.com/ICAMS/Crystal_Plasticity_UMAT, AGPL-3.0), on which this
> implementation is based. It provides the underlying single crystal plasticity framework,
> including Frederick–Armstrong-type kinematic hardening and gradient plasticity.
>
> The models and data in `data/` are available now.

<!-- After the code release, replace the status block above with:
> **Status:** `v1.0.0` is the code version used in the article. Later versions may differ;
> use the tagged release to reproduce the published results.
-->

## Repository structure

| Path | Content | License |
|---|---|---|
| `data/` | FE models (Abaqus input files, meshes, material parameters), EBSD map, cyclic stress–strain data, see [data/README.md](data/README.md) | CC BY-SA 4.0 |
| `scripts/download_512k_meshes.py` | Downloads the 80³ meshes of the mesh study from Zenodo | AGPL-3.0 |
| `src/` | UMAT source code (*not yet released*, see status above) | AGPL-3.0 |
| `CITATION.cff` | Citation metadata | |

The models and data are also archived on Zenodo: https://doi.org/10.5281/zenodo.21869496.
The two 80³ meshes (`Mesh3_512k*`, about 217 MB) are only available there; use
`python scripts/download_512k_meshes.py` to fetch them.

## Hardening models

The article compares the following kinematic hardening models, all implemented in one
UMAT and selected by integer switches in `src/UMATHT_global_ini.for`:


| Model (article) | Description | Switches |
|---|---|---|
| FA-KH  | Frederick–Armstrong local kinematic hardening | `iAFHKin = 3` |
| FA-LKH | Frederick–Armstrong local latent kinematic hardening (Harder) | `iAFHKin = 1` |
| FO     | First-order non-local kinematic hardening (GND back stress) | `iGNDOSKIN = 1`, `iGradCalc = 2` |
| SO-1   | Second-order non-local model 1 (Ma & Hartmaier) | `iGNDKin = 1`, `iGradCalc = 2` |
| SO-2   | Second-order non-local model 2 (Bayley et al.) | `iGNDKin = 2`, `iGradCalc = 3` |

Material parameters, crystal orientation (Euler angles) and length scale parameters are
passed via `*User Material` (`PROPS`, 72 constants); see the `*_mat.inp` files in
`data/`. For the non-local models, the gradients are computed with an FFT-based scheme
on an auxiliary grid whose size must match the finite element model.

## Requirements

- Abaqus/Standard (used: 2023) with a compatible Intel Fortran or gfortran compiler
- Python ≥ 3.8 (standard library only) for the download script
- Tested on Windows and Linux (Ubuntu 22.04)

## Usage

Once the code is released, run a job from the corresponding model directory, e.g.

```bash
cd data/Models/Mesh0_Main_64k
abaqus job=Job_Hom_316L_PX user=../../../src/UMATHTH_SXGRADPlast_grDefo_v11sdv.for cpus=8 interactive
```

`Mesh0_Main_64k` is the 75-grain RVE (40³ C3D8 elements) used in the main part of the
article; `Mesh1_8k` … `Mesh3_512k` (staircase and `_conforming`) belong to the mesh
sensitivity study in Appendix B.

## Related software

- ICAMS crystal plasticity UMAT (AGPL-3.0), on which parts of this code are based:
  https://github.com/ICAMS/Crystal_Plasticity_UMAT
- Octree search adapted from `fortran_snippets` by H. Miranda (BSD-3-Clause):
  https://github.com/henriquemiranda/fortran_snippets
- RVE generation: Dream3D, Kanapy (https://doi.org/10.5281/zenodo.3662366)

## License

- Code (`src/`, `scripts/`): GNU Affero General Public License v3.0, see [LICENSE](LICENSE).
  Third-party parts keep their original license notices (see the file headers).
- Models and data (`data/`): CC BY-SA 4.0, see [data/LICENSE](data/LICENSE).

## Citation

If you use this repository, please cite the article above and, for the data, the
Zenodo dataset. Citation metadata is provided in [CITATION.cff](CITATION.cff)
(GitHub shows a “Cite this repository” button).

## Acknowledgments

Funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation),
project number 504195877. Experimental data were provided by W. Zhao, S. N. Babaei and
U. Krupp (RWTH Aachen University).

## Contact

René Zandomeni, Thomas Seifert — Institute for Digital Engineering and Production (IDEeP),
Offenburg University of Applied Sciences. Please use the GitHub issue tracker for questions.
