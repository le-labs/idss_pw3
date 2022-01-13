# Data

As described in the report, we used the review dataset provided by Netflix. Since the files are in total several GB in size, we provide download links instead of including them directly in the submission.

## Netflix Dataset

These are all the files as provided by Netflix. Since a Kaggle account is required to download them, we mirrored them to our own server.

 * https://storage.googleapis.com/idss-static/combined_data_1.txt (472 MB)
 * https://storage.googleapis.com/idss-static/combined_data_2.txt (530 MB)
 * https://storage.googleapis.com/idss-static/combined_data_3.txt (444 MB)
 * https://storage.googleapis.com/idss-static/combined_data_4.txt (527 MB)
 * https://storage.googleapis.com/idss-static/movie_titles.csv (564 KB)


## Pre-processed Dataset

The following file includes all `combined_data_*.txt` files parsed and pre-processed. Refer to the `data_parser` folder in the source code for more details.

 * https://storage.googleapis.com/idss-static/preprocessed_reviews_all.bin (671 MB)


## Movie Metadata

The following file includes the metadata for all movies in the dataset. Refer to the `data_scraping` folder in the source code for more details.

 * https://storage.googleapis.com/idss-static/movie_metadata_all.json (11 MB)


## Recommender Cache (Pivot Table)

The following file is a Python `pickle` (serialized Python Object) containing the pivot table that can be used to drastically speed up the startup time of the backend.
 
 * https://storage.googleapis.com/idss-static/recommender_cache.pickle (5.7 GB)