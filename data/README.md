# Case Study Data

Original case study data is organized into one subfolder per case study. Datasets
that are hosted elsewhere are loaded directly from their source (see links below).

## Layout

### `ball_and_hoop/`
Ball-and-hoop apparatus experiments.

| File | Description |
|------|-------------|
| `closedLoop.mat` | Closed-loop acquisition |
| `fixedStepSequence.mat` | Fixed step reference sequence |
| `randomStepSequence.mat` | Random step reference sequence |

Used by: `ball_and_hoop.ipynb`, `narmax_activity_1.ipynb`, `narmax_activity_2.ipynb`,
`grey_box_activity_1.ipynb`, `grey_box_activity_2a.ipynb`, `grey_box_activity_2b.ipynb`.

### `quarter_drone/`
1/4 (quarter) drone test rig acquisitions.

| File | Description |
|------|-------------|
| `dados_14_drone.csv` | Identification dataset |
| `14_drone_seq_20260529_195254.csv` | Sequence acquisition used in the NARMAX example |

Used by: `read_data_14_drone.ipynb`, `narmax_example_drone.ipynb`.

### `ball_and_beam/`
Ball-and-beam MPC acquisition.

| File | Description |
|------|-------------|
| `aquisicao_02_mpc_modelo_NARX.mat` | MPC run with the identified NARX model |

Used by: `bab_ann_mpc_approximation.ipynb`.

## Data hosted elsewhere

Some case studies load their data from external sources rather than from this folder:

| Case study | Notebook | Source |
|------------|----------|--------|
| Ball and beam (excitation datasets) | `ball_and_beam_data.ipynb` | https://github.com/helonayala/bab_datasets |
| Wind turbine blade | `wind_blade.ipynb` | https://zenodo.org/records/3229743 |
| IFAC2015 LPV/LTV | `IFAC2015_LTV.ipynb` | https://www.kth.se/social/files/558d84b7f276541077ddc833/data_LPV.zip |

> The ball-and-beam excitation files (ramps, random steps, swept sine, multisine)
> previously stored here now live in the dedicated
> [`bab_datasets`](https://github.com/helonayala/bab_datasets) repository.
