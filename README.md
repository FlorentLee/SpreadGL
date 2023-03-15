# Spread.gl - visualising pathogen dispersal in a high-performance browser application
Main development repository and webpage for spread.gl, hosting installation files, input data files and tutorials for several visualisation examples.

## Installation
Before start, make sure you have already installed Git, npm, and Python3 on your device.  
Please refer to the following links for installation:  
https://git-scm.com/book/en/v2/Getting-Started-Installing-Git  
https://docs.npmjs.com/downloading-and-installing-node-js-and-npm  
https://www.python.org/downloads

1. Clone Github repository in your working directory and then use npm to install the web application:
```
git clone git@github.com:GuyBaele/SpreadGL.git
cd SpreadGL
npm install
```
2. Go to https://mapbox.com, sign up for an account and create a Mapbox Access Token.  
You will need to associate your token with Spread.gl:
```
chmod +x addToken.js
./addToken.js <insert_your_token>
```
3. Start the project, which will open a browser window:
```
npm start
```
Note: In case of any problems running 'npm start', you may also have to install the 'assert' and 'url' packages:
```
npm install assert
npm install url
```
4. Open a new terminal at the same folder. Install SpreadTools to create legit input files for visualisation.  
More information about different scripts can be found in the README of the scripts folder.
```
cd scripts
python -m venv my_env
source my_env/bin/activate (Linux/Mac)
.\my_env\Scripts\activate (Windows)
python setup.py install
```
## Tree Processing
Process the MCC trees you want to visualise. For example, for each of the three visualisations shown below, these are the basic commands required (but see the examples below for more processing steps and the scripts directory for more detailed information):
```
space --tree rep1.mcc.tre --time 2021-06-01 --location region --list A.27.location.list.csv
space --tree RABV_US1_gamma_MCC.tree --time 2004-7 --location location1,location2
space --tree PEDV_China.MCC.tree --time 2019-12-14 --location location --list Involved_provincial_capital_coordinates.csv
space --tree YFV.MCC.tree --time 2019-04-16 --location location1,location2
space --tree B.1.1.7_England.single.tree --time 2021-01-12 --location coordinates --format csv
```

## Animation examples in spread.gl
In the 'inputdata' folder, you can find all the required input files for our 3 examples in the manuscript. We also provide example output videos by recording the screen on Mac using Screenshot.

### SARS-CoV-2 lineage A.27 Worldwide
1. Process the tree file using the following command:
```
space --tree rep1.mcc.tre --time 2021-06-01 --location region --list A.27.location.list.csv
```
This command executes the space.py script with 4 arguments:  
--tree: Specify the name of your input tree file with filename extension.  
--time: Enter the date of the most recent tip. It can be either in the format of YYYY-MM-DD or decimal year. In this case, it is 2021-06-01.  
--location: Type in the annotation that stores the location information (names or coordinates). In this case, the "region" annotation stores the names of regions and countries.  
--list: Only compulsory for discrete space analysis. Use a location list with its filename extension as an input. This file should be in the csv format with a comma (",") separator and comprised of three columns with a specific header of "location,latitude,longitude".  
When this processing step is done, you should be able to see a file called 'rep1.mcc.tre.output.geojson'. It represents the spatial layer.

2. Visualise the spatial layer in Spread.gl.  
Click the "Add Data" button and import the file named 'rep1.mcc.tre.output.geojson' by drag-and-drop. Then, you need to follow a series of steps to create different types of visuals.  
(1) Create a layer to display phylogenetic branches. Select 'Layers' from the navigation bar, then clicking 'Add Layer' and choose 'Arc' in Basic. When specifying the coordinate fields (latitude and longitude) and coloring the branches, the source and target should correspond to the starting and ending points, respectively. You can adjust other parameters, such as opacity and stroke, to customise the visualisation. Once completed, the phylogenetic tree branches will be rendered on this layer.  
(2) Create a layer that reflects the cumulative numbers of phylogenetic nodes at different places. Select 'Layers' from the navigation bar, then clicking 'Add Layer' and choose 'Cluster' in Basic. Specify the coordinate fields (latitude & longitude) of the ending points. Choose a sequential colour bar and set the colours based on 'Point Count' (by default). The radius parameters can be adjusted to set an appropriate size for the clusters. After that, the clusters that represent the cumulative numbers will be displayed on this layer.  
(3) Create an animation for the dispersal over time. You need to add a filter to your map by selecting 'Filters' from the navigation bar, then clicking 'Add Filter' and choosing the result dataset. You should then select a field on which to filter data, in this case, a timestamp called "ending_time". Once this filter is applied to the map, you can see a time bar at the bottom of the screen. Set a moving time window and then click the play button, you will be able to see the animation.

https://user-images.githubusercontent.com/74751786/221681883-46bc7d5c-efdb-439c-bfbb-98c5f12f11ff.mov

### Rabies virus (RABV) in the United States
1. Process the tree file using the following command:
```
space --tree RABV_US1_gamma_MCC.tree --time 2004-7 --location location1,location2
```
This step works in the similar way as the A.27 example. Please take notice of the "--location" argument:  
As there are two annotations (location1 & location2 in this case) to store coordinates, you need to enter them in the order of latitude and longitude with a comma (",") separator in between.

2. Visualise the spatial layer in Spread.gl.  
Click the "Add Data" button and import the file named 'RABV_US1_gamma_MCC.tree.output.geojson' by drag-and-drop.  
In this example, you can create an additional layer that enables the differentiation of nodes and tips. Select 'Layers' from the navigation bar, then clicking 'Add Layer' and choose 'Point' in Basic. Specify the coordinate fields (latitude & longitude) of the ending points. In order to effectively distinguish between the nodes and tips, it is recommended to utilise a qualitative colour bar and set the colours based on the 'type' field. As a result, the internal nodes and external tips will be categorised into distinct colours, allowing for clear and unambiguous observation.

https://user-images.githubusercontent.com/74751786/221672148-b5190444-cb32-4047-a395-ed2cc8427130.mov

### Porcine epidemic diarrhea virus (PEDV) in China
1. Process the tree file using the following command:
```
space --tree PEDV_China.MCC.tree --time 2019-12-14 --location location --list Involved_provincial_capital_coordinates.csv
```
This step works in the same way as the A.27 example.

2. Create an environmental layer. You need to add swine trade data to the map of China. The dataset 'National_swine_stocks.csv' was obtained from the original study (He et al.). The China map was generated via this link (http://datav.aliyun.com/portal/school/atlas/area_selector). Use the following command:
```
environment --region China_map.geojson --key name --data National_swine_stocks.csv --foreign location --output Swine_stocks_on_map.geojson
```
This command executes the environment.py script with 5 required arguments:  
--region: Specify the input map (.GeoJSON).  
--key: Enter the foreign key field name in the properties part of input.  
--data: Use environmental data (.csv).  
--foreign: Enter the foreign field name in your data.  
--output: Give a name for the output map (.GeoJSON).  
When this step is done, a file called 'Swine_stocks_on_map.geojson' will be created.

3. Visualise the spatial and environmental layers together in Spread.gl. To add a custom base map style, you need to create a custom map style on Mapbox Studio (https://studio.mapbox.com). An official manual can be found via this link (https://docs.mapbox.com/studio-manual/guides). Once completed, open the Base Map panel, click the add map style button to open the custom map style modal, paste in the mapbox style Url. Note that you need to paste in your mapbox access token if your style is not published.

https://user-images.githubusercontent.com/74751786/205175522-5f639239-79d6-48c4-a097-837df9e50fa6.mp4

### Yellow fever virus (YFV) in Brazil
1. Process the tree file using the following command:
```
space --tree YFV.MCC.tree --time 2019-04-16 --location location1,location2
```
This step works in the same way as the RABV example. Since the tree annotations also include the information about regions of highest posterior density (HPD), some more relevant data will automatically be saved in the output GeoJSON file.

2. Generate the file of 'brazil_region_maxtemp.csv' as a temperature layer.  
(To Be Continued: how to create)
Download the environmental raster data layer from here: https://www.worldclim.org/data/monthlywth.html. In this case, we chose to visualise the maximum temperature. Note that this is monthly data, so we take the mean for the years 2010 to 2018. Since we only wish to visualise a few Brazilian provinces (and not the entire world) we can apply a mask to this raster layer using R. You can modify the code below for most other environmental layers in raster format and other locations.
```
library(sf)
library(rgeoboundaries)
library(raster) 
library(rgdal) #load neccesary libraries

tmax_data <- getData(name = "worldclim", var = "tmax", res = 0.5) #download climate data
tmax_mean <- mean(tmax_data) #calculate mean
brazil_sf <- geoboundaries("Brazil", "adm1") #download a shapefile of only Brazil, with administrative borders on the province level
brazil_sf<- brazil_sf[brazil_sf$shapeName %in% c("Minas Gerais","Espírito Santo",
                                                    "Rio de Janeiro",  "São Paulo",
                                                    "Goiás",  "Bahia",
                                                    "Federal District",
                                                    "Rio Grande do Sul",
                                                    "Paraná", "Santa Catarina" ),] #select only the provinces you want to visualise

tmax_mean_brazil <- raster::mask(tmax_mean, as_Spatial(brazil_sf)) #apply mask of Brazilian provinces to temperature layer
polygon=rasterToPolygons(tmax_mean_brazil, fun=NULL, n=4, na.rm=TRUE, digits=2, dissolve=FALSE) #convert to a polygon file
writeOGR(polygon, "geojson_maxtemp_Brazil, layer="layer", driver="GeoJSON") #save polygon file as GeoJSON file
```

3. Visualise the spatial and environmental layers together in Spread.gl.  
(To Be Continued: tutorial of the contour layer)

https://user-images.githubusercontent.com/74751786/200294883-a1a28d8c-44c0-4a0a-ab89-b3d137e704f1.mp4

### SARS-CoV-2 lineage B.1.1.7 (VOC Alpha) in England
1. Process the tree file using the following command:
```
space --tree B.1.1.7_England.single.tree --time 2021-01-12 --location coordinates --format csv
```
This step works in the same way as the RABV example. Please take notice of the following argument:  
--format: It is optional. If you want to check the output in a table, use "csv" in this argument. For this example, we need tabular data for further data wrangling.

2. Reproject coordinates. Due to the original tree file using the British National Grid coordinate reference system (CRS), which is not supported in spread.gl, you need to perform an additional step (using the file 'B.1.1.7_England.single.tree.output.csv' created in step 2) to convert it to another CRS (i.e., the World Geodetic System 1984; WGS84). Use the following command:
```
reprojection --input B.1.1.7_England.single.tree.output.csv --lat starting_coordinates_1,ending_coordinates_1 --lng starting_coordinates_2,ending_coordinates_2 --src 27700 --trg 4326 --output B.1.1.7_England.single.tree.output.reprojected.csv
```
This command executes the reprojection.py script with 6 required arguments: input csv file, field names of source latitudes (comma separator in between), field names of source longitudes (comma separator in between), source CRS, target CRS and output csv file. When this step is done, a file 'B.1.1.7_England.single.tree.output.reprojected.csv' will be created.

3. Remove geographic outliers. If you visualise the reprojected output file created in step 3, there will be many points that fall outside Endland. These outliers were caused by missing geographic data. To identify them, it becomes necessary to refer to a dataset file 'TreeTime_270221.csv', which is an analysis result from the original study (Kraemer et al.). This file contains the location information of each point, i.e. UTLA (Upper Tier Local Authorities in England). You will need to check if this value is empty or not. If it is NULL, that point will fall outside of England. Therefore, the corresponding row(branch) has to be removed. Use the following command:
```
trimming --input B.1.1.7_England.single.tree.output.reprojected.csv --key ending_coordinates_1_original --refer TreeTime_270221.csv --foreign endLat --null startUTLA,endUTLA --output B.1.1.7_England.single.tree.output.reprojected.cleaned.csv
```
This command executes the trimming.py script with 6 required arguments: input csv file, foreign key field name of input, reference csv file, foreign field name of reference, queried field(s) of reference (comma separator in between if needed), and output csv file. When this step is done, a file 'B.1.1.7_England.single.tree.output.reprojected.cleaned.csv' will be created.

4. Visualise the end result.
Now, you can load the end result in Spread.gl in your browser. Click the buttom "Add Data". Drag & drop the file of 'B.1.1.7_England_final_output.csv' there. You can customise the visualisation by adjusting the parameters in the side panal, i.e. showing / hiding / creating / deleting / reordering / colouring different layers. To create an animation for the dispersal, you need to add the filter to your map. First, select Filters from the navigation bar. Then, click Add Filter. Choose the result dataset, and then a field on which to filter your data. In this case, it should be a timestamp called "ending_time". After that, this filter will be applied on your map. You can see a time bar at the bottom of the screen. Set the time window to increment and click the play buttom. You will eventually see an animation.

https://user-images.githubusercontent.com/74751786/200294175-24cf3c0a-92c6-49b6-ad9d-ed5dd57fe60d.mp4
