# Data Embedding Exploration

Develop a proof-of-concept for integrating  literature data



## Installation

Pay atterntion to install requiremnts from both subfolder

```bash
pip install -r requirements.txt
```

## Overview
This project consists of two main parts:

1. **api_fetcher**: This component fetches data from the Nomad API and retrieves literature abstracts from the CrossRef library.
   

2. **Data Processing**: This component processes the fetched abstracts by embedding them and clustering them based on their subject matter


## Usage


To start fetching data from the APIs, run the following command:

```bash
python main.py
```
After fetching the data, open the provided Jupyter Notebook in the **embedding_clustering** folder. Run the notebook to embed the abstracts and cluster them for further analysis.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
