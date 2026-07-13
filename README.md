# spread.gl User Manual

**spread.gl v2.0-beta** is an integrated data pipeline designed to visualize pathogen dispersal over geographic space and time. It unifies complex backend data processing (the extraction, transformation, and loading [ETL] of phylogenetic trees and environmental rasters) with a highly interactive, GPU-accelerated web rendering engine into a single, user-friendly graphical interface.

---

## 🌟 Key Features of v2.0-beta

* **Universal File Support & Frictionless UX**: Offers a frictionless user experience through workspace-wide and global drag-and-drop upload functionality. The platform natively parses raw spatial files (`.geojson`, `.csv`) and instantly restores saved session states (`.json`), allowing users to transition seamlessly between dataset processing and visual exploration.
* **Tianditu (天地图) Official Basemaps**: Integrates China's official Tianditu basemaps natively into the mapping engine. This ensures strict geographic mapping compliance and seamless accessibility for researchers within Chinese academia.
* **Interactive Visual Analytics**: Supports real-time, exploratory analysis of phylogeographic structures. Users can dynamically filter transmission networks by Bayes Factor thresholds, play animations on a synchronized 4D spacetime timeline, and inspect raw geospatial data layers without dropping records.
* **Migration Network Calculation**: 
  * **Markov Jumps**: When a BEAST log file containing Markov jump count columns is supplied, the migration network's edge weight represents the **posterior expected number of jumps** (the average number of transitions across the MCMC sample distribution).
  * **Transition Counts**: If no log file is provided (or if Markov jump columns are missing), the pipeline automatically falls back to the **conditional consensus migration network** where edge weights represent the raw count of transitions mapped along the consensus branches of a single summary tree (e.g., MCC/HIPSTR).
* **Asymmetric BF Directionality**: For asymmetric (non-reversible) BEAST models, the Bayes Factor filter correctly enforces directionality — each migration route A→B must pass its own independent BF test without borrowing support from the reverse direction B→A.

---

## 🔐 Local Sandbox Run for Data Privacy

spread.gl is designed with a **privacy-first architecture**. 

Unlike conventional web visualization tools that upload your sequences to third-party cloud servers, spread.gl processes and renders all datasets locally. This relieves all security and compliance concerns regarding sensitive, unpublished molecular epidemiology sequences.

### 📦 Quick Start in Local Docker Sandbox (Command Line)
For full privacy-sandbox isolation, you can pull the official container images directly from Docker Hub and run them locally:

```bash
# Pull and run the backend processing toolkit (exposing port 8000)
docker run -d --name spreadgl-backend -p 8000:8000 florentlee/spread.gl.processing.toolkit:2.0-beta

# Pull and run the frontend web application (exposing port 3000)
docker run -d --name spreadgl-frontend -p 3000:3000 florentlee/spread.gl.web.page:2.0-beta
```
Open **[http://localhost:3000](http://localhost:3000)** in your web browser.

---

### 🖥️ Quick Start via Docker Desktop GUI

If you prefer using the **Docker Desktop Graphical User Interface (GUI)**:

1. **Pull the Images**:
   * Open Docker Desktop, select the search bar at the top, and search for `florentlee/spread.gl.processing.toolkit:2.0-beta`. Click **Pull**.
   * Search for `florentlee/spread.gl.web.page:2.0-beta` and click **Pull**.
2. **Run the Backend**:
   * Go to the **Images** tab on the left sidebar.
   * Locate `florentlee/spread.gl.processing.toolkit` with the `2.0-beta` tag, and click the play (**Run**) button.
   * Expand the **Optional settings** dropdown:
     * Set **Container name** to `spreadgl-backend`.
     * Set **Host port** to `8000` (mapping to container port `8000`).
     * Click **Run**.
3. **Run the Frontend**:
   * In the **Images** tab, locate `florentlee/spread.gl.web.page` with the `2.0-beta` tag, and click the play (**Run**) button.
   * Expand the **Optional settings** dropdown:
     * Set **Container name** to `spreadgl-frontend`.
     * Set **Host port** to `3000` (mapping to container port `3000`).
     * Click **Run**.
4. **Access the App**:
   * Go to the **Containers** tab to confirm both containers are green and running.
   * Click the link for port `3000` on the `spreadgl-frontend` row, or navigate to **[http://localhost:3000](http://localhost:3000)** in your browser.

---

## 📖 Tutorials & Examples

This section walks through three example visualizations covering continuous and discrete phylogeographic analyses.

---

### Example 1: Continuous Phylogeography with Environmental Rasters (YFV in Brazil)

Continuous phylogeography traces the exact latitude and longitude of viral lineages over time. By syncing this trajectory with environmental variables (e.g., temperature grids), researchers can correlate climate variations with dispersal speed.

* **Dataset**: Yellow Fever Virus (YFV) in Brazil
  * **Tree File**: `inputdata/YFV_Brazil/YFV.MCC.tree`
  * **Rasters**: Directory of monthly `.tif` rasters `inputdata/YFV_Brazil/wc2.1_5m_tmax_2015-2019/`
  * **Mask Boundary**: `inputdata/YFV_Brazil/GeoBoundaries.BRA.ADM1.geojson`
  * **Location List**: `inputdata/YFV_Brazil/Involved.Brazilian.states.txt`

#### 🚶 Step-by-Step Instructions:
1. Select the **Setup** tab and set **Analysis Type** to **Continuous**.
2. Upload `YFV.MCC.tree` in the **Tree File** field. Your tree file must strictly adhere to the standard `#NEXUS` format.
3. Enter `location1,location2` under **Location Trait** and set **Most Recent Tip Time** to `2019-04-16`.
4. Turn on the **Environmental Data Layer** and select **Rasters** as the type.
5. Upload the folder containing the `.tif` rasters, select `GeoBoundaries.BRA.ADM1.geojson` as the mask boundary, and choose `Involved.Brazilian.states.txt` as the location list. Set **Location Variable** to `shapeName`.
6. Click **Run Pipeline**. The backend maps the viral trajectories and clips the temperature rasters to the target states.
7. Click **Apply to Map**. The visualization engine natively binds the moving **Trip Layer** (which renders viral lineage trails set to 1/10th of the outbreak duration) and the shifting **Geo-Contextual Data Layer** (displaying temperature grid points) to the shared Kepler.gl **Timebar**.

A core feature of the Map tab is the synchronized 4D timeline. When you press play on the time slider, Kepler.gl perfectly synchronizes all spatial layers simultaneously: the viral lineages moving along the dynamic_pathway (Trips Layer), the shifting credible intervals of the hpd_polygons, and the fading dynamic environmental temperature rasters. This allows researchers to visually correlate pathogen spread directly with changing ecological conditions.

#### 📅 Outbreak Evolution (Local Detail View):

| Sep 2016 | Mar 2017 |
| :---: | :---: |
| ![Sep 2016](outputdata/YFV_Brazil/YFV_local_details/Sep%202016.png) | ![Mar 2017](outputdata/YFV_Brazil/YFV_local_details/Mar%202017.png) |

| Sep 2017 | Mar 2018 |
| :---: | :---: |
| ![Sep 2017](outputdata/YFV_Brazil/YFV_local_details/Sep%202017.png) | ![Mar 2018](outputdata/YFV_Brazil/YFV_local_details/Mar%202018.png) |

![YFV Legend](outputdata/YFV_Brazil/YFV_local_details/YFV%20Legend.png)

---

### Example 2: Continuous Phylogeography with Coordinate Reprojection (SARS-CoV-2 B.1.1.7 in England)

This example demonstrates the advanced **reprojection** and **trimming** features. The B.1.1.7 (VOC Alpha) dataset uses the British National Grid coordinate system (EPSG:27700), which must be reprojected to WGS84 (EPSG:4326) for global web mapping. Additionally, branches with missing UTLA (Upper Tier Local Authority) metadata are trimmed to remove geographic outliers.

* **Dataset**: SARS-CoV-2 lineage B.1.1.7 (VOC Alpha) in England
  * **Tree File**: `inputdata/SARS_CoV-2_B.1.1.7_UK/B.1.1.7.England.single.tree`
  * **Reference Metadata**: `inputdata/SARS_CoV-2_B.1.1.7_UK/TreeTime.metadata.csv`

#### 🚶 Step-by-Step Instructions:
1. Select the **Setup** tab and set **Analysis Type** to **Continuous**.
2. Upload `B.1.1.7.England.single.tree` in the **Tree File** field.
3. Enter `coordinates` under **Location Trait** and set **Most Recent Tip Time** to `2021-01-12`.
4. Upload `TreeTime.metadata.csv` as the **Referenced File** for trimming.
5. Enable **Reprojection** and configure:
   * **Source CRS**: `27700` (British National Grid)
   * **Target CRS**: `4326` (WGS84)
   * **Latitude columns**: `start_lat,end_lat`
   * **Longitude columns**: `start_lon,end_lon`
6. Enable **Trimming** and configure:
   * **Primary Key**: `endLat`
   * **Foreign Key**: `end_lat_original`
   * **Null Query Fields**: `startUTLA,endUTLA`
7. Click **Run Pipeline**. The backend reprojects all coordinates from British National Grid to WGS84 and filters out branches lacking UTLA assignment.
8. Click **Apply to Map**. The visualization shows B.1.1.7 diffusion paths across England with all coordinates correctly rendered in web-standard WGS84.

#### 📊 Temporal Snapshots of B.1.1.7 Diffusion:

| Nov 05–10, 2020 | Dec 05–10, 2020 |
| :---: | :---: |
| ![Nov 2020](outputdata/B.1.1.7_UK/Nov%2005%20-%20Nov%2010%202020.png) | ![Dec 2020](outputdata/B.1.1.7_UK/Dec%2005%20-%20Dec%2010%202020.png) |

| Dec 26–31, 2020 | Jan 05–10, 2021 |
| :---: | :---: |
| ![Late Dec 2020](outputdata/B.1.1.7_UK/Dec%2026%20-%20Dec%2031%202020.png) | ![Jan 2021](outputdata/B.1.1.7_UK/Jan%2005%20-%20Jan%2010%202021.png) |

![B.1.1.7 Legend](outputdata/B.1.1.7_UK/B.1.1.7%20legend.png)

---

### Example 3: Discrete Phylogeography with Posterior Markov Jump Weights (SARS-CoV-2 B.1.525 Global)

Discrete phylogeography reconstructions represent viral spread as transitions among discrete locations. This example demonstrates the full pipeline with an **asymmetric** BEAST model: posterior Markov jump weights derived from the MCMC log, Bayes Factor filtering with correct directional enforcement, and interactive BF threshold adjustment.

* **Dataset**: SARS-CoV-2 Eta Variant (B.1.525) — Global (31 regions)
  * **Tree File**: `inputdata/SARS_CoV-2_B.1.525_Global/B.1.525.Analysis2.joint.phylogeo.HIPSTR.tree`
  * **Locations**: `inputdata/SARS_CoV-2_B.1.525_Global/B.1.525.full.dataset.2910.region.coordinates.csv`
  * **BEAST Log**: `inputdata/SARS_CoV-2_B.1.525_Global/B.1.525.Analysis2.thorney.joint.phylogeo.burnin.removed.log`

#### Understanding the Edge Weights

When a BEAST `.log` file containing Markov jump counts is provided, the pipeline processes the transition history over all post-burn-in MCMC samples. The edge weight of the network represents the **posterior expected number of Markov jumps** for each directed pair A→B:

$$\text{weight}_{A \to B} = \frac{1}{N} \sum_{i=1}^{N} c_{A \to B}^{(i)}$$

where $c_{A \to B}^{(i)}$ is the exact transition count from state A to state B in the $i$-th MCMC sample and $N$ is the total post-burn-in sample size. This calculation tracks state changes over the entire tree distribution.

##### Consensus Fallback (Without BEAST Log)
If no BEAST `.log` file is uploaded, the pipeline falls back to the **conditional consensus migration network**. In this mode, the edge weight is computed as the raw count of transitions mapped along the consensus branches of the single Maximum Clade Credibility (MCC) tree. This fallback is useful when only the MCC summary tree is available, though it represents a single consensus topology rather than the full posterior distribution.

#### 🚶 Step-by-Step Instructions:
1. Select the **Setup** tab and set **Analysis Type** to **Discrete**.
2. Upload the B.1.525 `.tree` file.
3. Upload the `.csv` Location List (containing `location,latitude,longitude`) and type the corresponding **Location Trait** as `region`. Set **Most Recent Tip Time** to `2021-07-01`.
4. In the **Bayes Factors** section, upload the BEAST `.log` file. Set the **Burn-in** to `0` (the reference log file has already had burn-in removed). If your log still contains burn-in samples, set the appropriate fraction (e.g., `0.1` for 10%).
5. Click **Run Pipeline**. The backend:
   * Computes Bayes Factors from the BSSVS indicator columns and automatically detects the model as **asymmetric** (930 indicators for 31 locations = $31 \times 30$, not $31 \times 30 / 2$).
   * Parses all 930 Markov jump count columns and computes the posterior mean for each directed pair.
6. Click **Apply to Map**. The map will load the animated `dynamic_pathway` by default.
7. Click the layer visibility icon to turn on the **Aggregated Migration Network**. The arc widths now scale with the **posterior expected number of Markov jumps** — the standard phylogeographic edge weight. Use the auto-generated Bayes Factor filter in the left panel to dynamically threshold the network (e.g., slide to `>150` for decisive evidence, isolating the primary export hubs).

#### 📊 Visualizations:

| B.1.525 Dynamic Diffusion Paths | B.1.525 Migration Flows (BF > 150) |
| :---: | :---: |
| ![Dynamic Paths](outputdata/B.1.525_Global/B.1.525%20figure%20-%20dynamic%20paths.png) | ![Migration Flows](outputdata/B.1.525_Global/B.1.525%20figure%20-%20migration%20flows%20with%20cumulative%20exportations.png) |

| Trip Layer Legend | Arc Layer Legend | Cluster Layer Legend |
| :---: | :---: | :---: |
| ![Trip Legend](outputdata/B.1.525_Global/B.1.525%20legend%20-%20dynamic%20paths%20trip.png) | ![Arc Legend](outputdata/B.1.525_Global/B.1.525%20legend%20-%20migration%20flows%20arc.png) | ![Cluster Legend](outputdata/B.1.525_Global/B.1.525%20legend%20-%20cumulative%20exportations%20cluster.png) |

---

## 🗺️ The 3-Step Top Navigation GUI Architecture

The application is structured around a top navigation bar dividing the workflow into three sequential stages: **Setup**, **Workspace**, and **Map**.

```mermaid
graph LR
    A[Step 1: Setup] --> B[Step 2: Workspace]
    B --> C[Step 3: Map]
```

### Step 1: Setup (Pipeline Configuration)
In this initial step, you load your raw phylogenetic trees, location mappings, and environmental data layers to run them through the processing bridge.

* **Analysis Type**: Choose **Discrete** (for discrete spatial traits modeled on fixed location points) or **Continuous** (for continuous latitude/longitude traits representing geographic coordinates).
* **Upload Files**:
  * **Tree File**: Upload your NEXUS format tree file (e.g., `.tree` or `.trees` file from BEAST).
  * **Location File** *(Discrete only)*: Upload a CSV containing location names and coordinates. The CSV must have a comma separator and a header of `location,latitude,longitude`.
  * **BEAST Log File** *(Optional - Discrete only)*: Upload the BEAST `.log` file containing rate indicators to compute Bayes factors for the migration network. If the log also contains Markov jump count columns (from `MarkovJumpsTreeLikelihood`), the pipeline will parse them to derive posterior expected jump weights.
* **Metadata Traits**:
  * **Most Recent Tip Time**: Specify the calendar date (e.g., `2021-06-01`) or decimal year (e.g., `2021.42`) of the latest sampled taxon to calibrate the timeline.
  * **Location Trait**: Enter the name of the annotation trait representing geography (e.g., `region` or `coordinates`). If continuous and using separate lat/lon annotations, separate them with a comma (e.g., `location1,location2`).
* **Reprojection Options** *(Advanced)*: Convert coordinates on-the-fly from a local reference system (e.g., British National Grid EPSG:27700) to World Geodetic System 1984 (WGS84 EPSG:4326).
* **Trimming Options** *(Advanced)*: Exclude geographic outliers by referencing an external CSV file (e.g., checking for empty locations or null attributes).
* **Geo-Contextual Data Layers**:
  * **Regions**: Upload a CSV with environmental values and a GeoJSON boundary map to color state/provincial polygons based on variables (e.g. swine density).
  * **Rasters**: Upload a set of monthly climate `.tif` rasters, a GeoJSON boundary mask, and a list of target locations to clip and plot environmental grids.

### Step 2: Workspace (Data Preview)
Once the processing completes, the application automatically routes you to the **Workspace** panel. This stage allows you to review the outputs before loading them onto the map.

* **Summary Metrics**: Check how many features, branches, and polygons were successfully parsed.
* **Download Outputs**: Download the clean spatial outputs directly to your computer:
  * `dynamic_pathway.geojson`: Dynamic trajectories (trips) tracking migrations over time. You can create point, line and arc layers based on this file.
  * `aggregated_migration_network.geojson` *(Discrete only)*: Aggregated migration arcs between discrete locations with posterior expected Markov jump weights and Bayes factors. If no log was provided, the file contains edge count weights derived from the single consensus tree.
  * `geo_contextual_data.geojson / .csv`: Clipped rasters or populated region boundary maps.
* **Verification**: Verify that no coordinates are out of bounds or missing. Click the **Apply to Map** button to load the datasets into the Kepler engine.

### Step 3: Map (Visualization & Interaction)
The **Map** view launches the interactive, GPU-accelerated map engine.

* **Arc Layer (Migration Network)**: Displays arcs showing discrete dispersal patterns. Arc widths scale with the **posterior expected number of Markov jumps** (or fallback edge counts of a consensus tree) — the standard phylogeographic edge weight. Arcs are colored from source to target.
* **Trip Layer (Pathways)**: Renders phylogenetic branches as moving light trails. You can adjust the trail length and thickness.
* **Kepler Timebar**: Displays a timeline at the bottom of the map. Play the animation to watch the virus disperse across the globe chronologically, or drag the time window handles to see specific intervals.
* **Geo-Contextual Layer**: Shows overlay grid points (raster data) or styled boundary polygons (regional data) matching the map backdrop.

---

## ⚡ Non-Technical Configuration Guides

### 1. Uploading Files
1. In **Step 1: Setup**, locate the upload inputs.
2. Drag and drop your NEXUS tree file into the **Tree File** dropzone.
3. If doing a discrete analysis, drop your coordinate reference list into the **Location CSV** dropzone.
4. Click **Run Pipeline** at the bottom of the panel and wait for the Workspace view to appear.

### 2. Configuring Geo-Contextual Data Layers
To overlay climate grid cells or demographic polygons onto your dispersal map:
* **For Regional Polygons (e.g., PEDV in China)**:
  1. Set **Environmental Type** to `Regions`.
  2. Upload your environmental spreadsheet (`Environmental_variables.csv`).
  3. Upload your map boundary file (`China_map.geojson`).
  4. Specify the **Location Column** inside the CSV (e.g., `location`) and the **Location Variable** property inside the GeoJSON (e.g., `name`).
* **For Raster Grids (e.g., Climate Rasters)**:
  1. Set **Environmental Type** to `Rasters`.
  2. Upload one or more `.tif` files.
  3. Upload the geographic mask boundaries (`GeoBoundaries.BRA.ADM1.geojson`).
  4. Upload a text file listing the regions of interest (`Involved.Brazilian.states.txt`).

### 3. Shifting the Bayes Factor Slider
In discrete phylogeographic studies, many migration routes are tested, but only a few are statistically significant. 
1. In the **Setup** tab, if you uploaded a BEAST log file, the **Bayes Factor threshold** slider will be active.
2. The default threshold is `3.0` (indicating positive support).
3. Slide the value **higher** (e.g., `10.0` for strong support, or `30.0` for very strong support) to filter out support paths.
4. The map will instantly update, hiding weaker routes and adjusting the width of the remaining arcs based on their **posterior expected Markov jump weights** (or fallback MCC consensus edge counts).

---

## 🛠️ Developer Setup & Local Command Deployment

### Local Development
To run the decoupled backend and frontend locally from source:

1. **Activate Virtual Environment & Run Backend**:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install -e .
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Run Frontend**:
   ```bash
   cd frontend
   npm install --legacy-peer-deps
   npm start
   ```
   Open [http://localhost:3000](http://localhost:3000) in your browser. The frontend's `BACKEND_API_URL` defaults to `http://localhost:8000`.
