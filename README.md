# planet-api-downloader
Python script to download satellite data from Planet Labs API using geojson AOIs and MD5 checksum verification.

This project is written in Python and utilizes the following packages: requests, os, time, hashlib, json, and HTTPBasicAuth. The project does not require any external tools.

The main script in this project is planet_script.py, which contains several functions for downloading images from the Planet API and verifying their MD5 checksums. The script uses an API key for Planet, which is set at the beginning of the script. If an environment variable PL_API_KEY exists, then the script uses the value of the environment variable as the API key. 

The download_file function takes a URL and a file path as arguments and downloads a file from the specified URL to the specified file path. If an error occurs during the download process, the function waits for 20 seconds and retries. Once the file has been successfully downloaded, the function returns the name of the file.

The md5_check function takes an original MD5 hash and a file path as arguments, calculates the MD5 hash of the file at the specified file path, and compares it to the original MD5 hash. If the two hashes match, the function returns True and prints a message indicating that the MD5 checksum has passed. Otherwise, the function returns False and prints a message indicating that the MD5 checksum has failed.

The downloading_images function takes an image ID and an item type as arguments and downloads an image from the Planet API based on the specified ID and item type. It retrieves the download URL and MD5 checksum for the desired asset, activates the asset if it is not already active, and then downloads and verifies the file using the MD5 checksum. The function utilizes the download_file and md5_check functions.

To use this project, the user must have a Planet API key. The API key can be set as an environment variable PL_API_KEY, or it can be pasted directly into the script. Once the API key is set, the user can call the downloading_images function with the desired image ID and item type to download and verify the image.
