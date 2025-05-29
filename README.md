# Protocell Simulation & Analysis Suite

## Overview
This project simulates protocell models exhibiting growth and division using stochastic chemical kinetics (via GillesPy2). It also provides tools for running multiple simulations and analyzing their evolutionary trajectories using angular distance metrics.

## Features
*   Stochastic simulation of chemical reaction networks.
*   Modeling of protocell growth and division events based on lipid thresholds.
*   Support for different protocell types influencing division mechanics and volume calculation.
*   Batch execution of multiple simulation runs.
*   Post-simulation analysis including:
    *   Aggregation of data across multiple runs.
    *   Calculation of angular distance between simulation states at each generation.
    *   Statistical summary of angular distances (min, max, mean, median, std dev).
*   Output generation in Excel format for detailed analysis.

## File Structure
*   `input/`: Contains configuration files.
    *   `params.txt`: Main parameters for the simulation.
    *   `AngularParams.txt`: Parameters for the angular distance analysis.
    *   `*.txt` (e.g., `chimica.txt`): Chemical definition file (species, reactions).
*   `output/`: Default directory for simulation and analysis results.
*   `modules/`: Contains Python modules for core logic.
    *   `Module.py`: Defines the `gillespy2` simulation model and logic.
    *   `ReadParams.py`: Functions to read parameters from input files.
*   `Main.py`: Core script to run a single simulation.
*   `MultiRun.py`: Script to automate multiple runs of `Main.py`.
*   `AngularDistance.py`: Script to perform post-simulation analysis on data from multiple runs.
*   `README.md`: This file.

## Input Files Details

### `input/params.txt`
Tab-separated key-value pairs.
*   `INPUT`: Name of the chemical definition file (e.g., `chimica.txt`).
*   `OUTPUT`: Base name for the main output Excel file.
*   `SYNTHESIS`: Base name for the synthesis output Excel file.
*   `TIME`: Total simulation time for each generation.
*   `POINTS`: Number of data points to record within the simulation time.
*   `TRAJECTORIES`: Number of trajectories (usually 1 for this workflow).
*   `COEFF`: Coefficient used in propensity functions, relating to volume.
*   `GENERATIONS`: Maximum number of generations to simulate.
*   `MAX_LIPID`: Threshold of lipid quantity that triggers cell division.
*   `PROTO_TYPE`: Defines protocell behavior (1, 2, or 3). See "PROTO_TYPE Explanation".
*   `RHO`: Density of the lipid (used in `PROTO_TYPE 3`).
*   `DELTA`: Thickness of the membrane (used in `PROTO_TYPE 3`).

### `input/AngularParams.txt`
Tab-separated key-value pairs.
*   `SPECIES`: Comma-separated list of species names to be used in angular distance calculation (e.g., `A,B`).
*   `TOTAL_SIM`: Total number of simulations that were run (written by `MultiRun.py`).
*   `GENERATIONS`: Number of generations analyzed (written by `MultiRun.py`).

### Chemical Input File (e.g., `input/chimica.txt`)
*   Format: Tab-separated.
*   Species Definition Section:
    *   `[SpeciesName]	[InitialQuantity]	[CatalysisFactor]`
    *   The first species listed is considered the primary "lipid."
    *   `CatalysisFactor > 0` means this species catalyzes lipid production.
*   Empty line separates species from reactions.
*   Reaction Definition Section:
    *   `[Reactant1]	+	[Reactant2]	>	[Product1]	+	[Product2]	;	[Rate]`
    *   Example: `A	+	B	>	C	;	0.1`
    *   Special input reaction: `10	>	A	;	0.05` (Influx of A, handled by `PROTO_TYPE` logic).

## Output Files Details

*   **`output/<OUTPUT_specified_in_params.txt>` (e.g., `output/results.xlsx`):**
    *   Created by `Main.py`. If `MultiRun.py` is used, files will be named like `results_Sim1.xlsx`, `results_Sim2.xlsx`, etc.
    *   Contains detailed time-series data for species quantities for each generation of a single simulation run.
    *   Includes "TIME" and "ABSOLUTE TIME" columns.
    *   Formatted with colored rows/headers to indicate division events.
*   **`output/<SYNTHESIS_specified_in_params.txt>` (e.g., `output/sintesi.xlsx`):**
    *   Created by `Main.py`. If `MultiRun.py` is used, files will be named like `sintesi_Sim1.xlsx`, `sintesi_Sim2.xlsx`, etc.
    *   Contains a snapshot of species quantities at the point of division for each generation.
*   **`output/DistanzaAngolare.xlsx`:**
    *   Created/updated by `AngularDistance.py` (and initialized by `MultiRun.py`).
    *   `Dati Simulazione` sheet: Initial summary from `MultiRun.py`. (This sheet might be overwritten or used as a base by `AngularDistance.py`)
    *   `Dati GenX` sheets: Aggregated data for each generation (`X`) across all simulations, focusing on the species defined in `AngularParams.txt`.
    *   `Distanza Angolare Dati GenX` sheets: Matrix of angular distances (in degrees) between each pair of simulations for generation `X`.
    *   `Sintesi` sheet:
        *   Statistical summary (Min, Media, Mediana, Max, Dev. Std.) of angular distances for each generation.
        *   Count of "Sim Vive" (simulations that reached that generation).
        *   Table of "tempo" (division time) for each simulation and generation.

## Workflow / How to Run

1.  **Setup:**
    *   Ensure all dependencies are installed (see below).
    *   Prepare your chemical input file (e.g., `input/my_chemistry.txt`).
2.  **Configure `input/params.txt`:**
    *   Set `INPUT` to your chemical file name.
    *   Define `OUTPUT` and `SYNTHESIS` base names.
    *   Set other simulation parameters (`TIME`, `POINTS`, `GENERATIONS`, `MAX_LIPID`, `PROTO_TYPE`, etc.).
3.  **Running Simulations:**
    *   **Single Run:**
        ```bash
        python Main.py
        ```
        Output will be in files like `output/results.xlsx` and `output/sintesi.xlsx`.
    *   **Multiple Runs & Analysis:**
        1.  Run `MultiRun.py`:
            ```bash
            python MultiRun.py
            ```
            It will ask for the number of simulations to run. This script will call `Main.py` multiple times. Output files will be suffixed with `_SimN` (e.g., `results_Sim1.xlsx`, `sintesi_Sim1.xlsx`). It also creates/updates `input/AngularParams.txt` and an initial `output/DistanzaAngolare.xlsx`.
        2.  (Optional) Review and modify `input/AngularParams.txt`. The `SPECIES` field is hardcoded to "A,B" by `MultiRun.py` if not already present. You might need to update this to the species relevant to your analysis.
        3.  Run `AngularDistance.py` for analysis:
            ```bash
            python AngularDistance.py
            ```
            This will process the `_SimN` files and generate the full `output/DistanzaAngolare.xlsx` report.

## `PROTO_TYPE` Explanation
The `PROTO_TYPE` parameter in `input/params.txt` affects how cell division and reaction propensities (especially volume considerations) are handled:

*   **`PROTO_TYPE 1` & `PROTO_TYPE 2`:**
    *   `DIVISION = 0.5`: Upon division, non-lipid species are halved.
    *   `LIPID_EXP = 1.0`: Volume term in propensity functions is proportional to `COEFF * Lipid^1.0`.
    *   Influx reactions (e.g., `10 > A ; k`) are split into:
        *   `-> A` with rate `k * 10 * Lipid`
        *   `A ->` with rate `k * A / COEFF`
*   **`PROTO_TYPE 3`:**
    *   `DIVISION = 0.35`: Upon division, non-lipid species are multiplied by 0.35.
    *   `LIPID_EXP = 1.5`: Volume term in propensity functions is proportional to `COEFF * Lipid^1.5`.
    *   Influx reactions (e.g., `10 > A ; k`) are split into:
        *   `-> A` with rate `(k / (RHO * DELTA)) * 10 * Lipid` (rate is adjusted by RHO and DELTA)
        *   `A ->` with rate `(k / (RHO * DELTA)) * A / (COEFF * Lipid^0.5)`

## Dependencies
*   `gillespy2`
*   `openpyxl`
*   `matplotlib` (Note: `matplotlib` is imported in `Main.py` but not explicitly used. It might be a remnant or for future use.)
