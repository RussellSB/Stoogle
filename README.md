# Stoogle
A simple search engine inspired by [Steam](https://store.steampowered.com/) and [Google](https://www.google.com/).

## Prerequisites

In order to setup this project correctly, you will need to have the correct database files set up in the right directory, and have installed the necessary packages. 

### Data

The source data is located in the `backend/data/` directory. In the case that they are not present, you may proceed with the following steps: 

1. Download all .csv files from the [Steam Stores Games](https://www.kaggle.com/nikdavis/steam-store-games) dataset, publicly available on Kaggle. This stores data on 27033 digital video games, available for purchase from Steam around May 2019.
2. Copy and paste all .csv files to `backend/data/`. Your data directory should then look like this:

```
data
├── steam.csv
├── steam_description_data.csv
├── steam_media_data.csv
├── steam_requirements_data.csv
├── steam_support_info.csv
└── steamspy_tag_data.csv
```

Once the system is up and running, a temp dataset with all the necessary information will be processed and automatically saved in `backend/temp/` as `dataset.csv`.

### Packages

Firstly, Elasticsearch must be installed and set up locally. The documentation for doing so can be found [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html). You will  then need to have pip and npm downloaded for installing Python and Javascript packages respectively. Pip can be installed by default alongside Python [here](https://www.python.org/). Npm can be installed [here](https://www.npmjs.com/get-npm). After the package managers are installed you may proceed with the following steps:

For Elasticsearch access from Python:
```
pip install elasticsearch
```

For the data processing, filtering, and evaluation in the backend:
```
pip install pandas matplotlib 
```

For the Flask API, linking backend to frontend:
```
pip install flask flask_restful flask_cors
```

With npm installed, navigate to the `frontend` directory, and run:

```
npm install
```

This should automatically install all the utilised packages for the frontend user interface. By following all the above steps, you should be ready to execute the program.

## Execution

In order to start up the system one must proceed with the following steps:

### Backend

The backend is split into two main parts - Elasticsearch, and Flask. In Python the Flask API starts the code and makes a call to Elasticsearch to index and prepare for search queries appropriately.

#### Elasticsearch

If you don't have Elasticsearch installed in the default directory of installation, make sure you execute `elasticsearch.bat` on Windows, or equivalent (as deemed by the referenced docs for elasticsearch). By default the elasticsearch python package boots this up automatically if found in an identifiable global directory. If not, it will assume a local server of Elasticsearch is already running and connect to that.


#### Flask API

Navigate to the `backend` directory and run:

```
python apis.py
```

### Frontend

Navigate to the `frontend` directory and run:

```
npm start
```

You should now be able to interact with the frontend from any browser on the url `localhost:3000`. For external API requests using software such as PostMan, you can communicate to the backend server via `localhost:5000`. If any issues occur please ensure that you have followed the above steps carefully, and that none of the packages conflict with each other in a way that prohibits the program from functioning.


