# planet-api-downloader
Python script to download satellite data from Planet Labs API using geojson AOIs and MD5 checksum verification.

This project is written in Python and utilizes the following packages: requests, os, time, hashlib, json, and HTTPBasicAuth. The project does not require any external tools.

The main script in this project is planet_script.py, which contains several functions for downloading images from the Planet API and verifying their MD5 checksums. The script uses an API key for Planet, which is set at the beginning of the script. If an environment variable PL_API_KEY exists, then the script uses the value of the environment variable as the API key. 

The download_file function takes a URL and a file path as arguments and downloads a file from the specified URL to the specified file path. If an error occurs during the download process, the function waits for 20 seconds and retries. Once the file has been successfully downloaded, the function returns the name of the file.

The md5_check function takes an original MD5 hash and a file path as arguments, calculates the MD5 hash of the file at the specified file path, and compares it to the original MD5 hash. If the two hashes match, the function returns True and prints a message indicating that the MD5 checksum has passed. Otherwise, the function returns False and prints a message indicating that the MD5 checksum has failed.

The downloading_images function takes an image ID and an item type as arguments and downloads an image from the Planet API based on the specified ID and item type. It retrieves the download URL and MD5 checksum for the desired asset, activates the asset if it is not already active, and then downloads and verifies the file using the MD5 checksum. The function utilizes the download_file and md5_check functions.

To use this project, the user must have a Planet API key. The API key can be set as an environment variable PL_API_KEY, or it can be pasted directly into the script. Once the API key is set, the user can call the downloading_images function with the desired image ID and item type to download and verify the image.

## INSTRUCTIONS TO RUN THE PYTHON SCRIPT 
1. First you need to download python from https://www.python.org for you OS. Then, open the setup for python and install it. “Make sure to Select Add Python to PATH option” when you open the setup and then proceed to Install. Skip this step if you have python already installed. 

2. Open CMD if you are on windows / Terminal if you are on MACOS. Type in “pip install requests” for windows or “pip3 install requests” if you are on MACOS and press enter. Once this is done, go to the next step. 

3. Extract the provided folder (PLANET_SCRIPT.zip). You can use tools like “WinRAR” or “7Zip” for this purpose. 

4. Now, navigate to the extracted folder. When the folder is opened, perform a “Right Click” on an empty space in the folder while holding the (SHIFT) button on your keyboard. 

5. Then, from the options available click on “open PowerShell window here” or “open command prompt window here”. The terminal should open 

6. On the terminal, write “python planet_script.py” and press Enter. The program should begin now. 

7. When you press enter, the script will prompt you to enter the name/path of the GeoJSON file where the coordinates are, if there is no file found the script will ask again to enter the correct name/path of the file. 

8. Next, the script will prompt the user to enter the start date from where the it should capture the images from the API. The correct date format is: YYYY-MM-DD and if the user enters the date in wrong format, the script will ask again to enter the date in the correct format. 

9. Next, the script will prompt the user to enter the end date from where it should capture the images from the API. The correct date format is: YYYY-MM-DD and if the user enters the date in wrong format, the script will ask again to enter the date in the correct format. 

10. After entering the name/ path of the files and the date range, the script will start downloading the images for the specified date from the PLANET API. 

11. All the images will be stored into an images folder which will be automatically created in the folder where the script is. 

NOTE: 
* Do not interfere with the process.  
* Keep a stable internet connection. 
