import os, time
import requests
import json, hashlib
from requests.auth import HTTPBasicAuth


# if your Planet API Key is not set as an environment variable, you can paste it below
if os.environ.get('PL_API_KEY', ''):
    API_KEY = os.environ.get('PL_API_KEY', '')
else:
    API_KEY = 'API_KEY'

# comment the below function

def download_file(url, file_path):
    # get file name from url
    local_filename = url.split('/')[-1]
    try:
        # download file in binary mode
        with requests.get(url, stream=True) as r:
            # raise error if status code is not 200
            r.raise_for_status()
            # write file
            with open(file_path, 'wb') as f:
                # iterate over response content
                for chunk in r.iter_content(chunk_size=8192): 
                    # filter out keep-alive new chunks
                    if chunk: 
                        f.write(chunk)
    # if an error occured
    except:
        # print error message
        print("Error, trying again...")
        # wait 20 seconds
        time.sleep(20)
        # download file again
        download_file(url, file_path)

    # return file name
    return local_filename


def md5_check(original_md5, filepath):
    # Open the file in binary mode
    with open(filepath, 'rb') as f:
        # Create a new md5 object
        md5_hash = hashlib.md5()
        # Read the file in 4kb chunks
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            # Update the md5 object with the current chunk
            md5_hash.update(chunk)

    # Get the final hash
    md5_checksum = md5_hash.hexdigest()

    # Check if the original and calculated hashes match
    if original_md5 == md5_checksum:
        print('\nMD5 checksum passed!')
        return True
    else:
        print('\nMD5 checksum failed!')
        return False


def downloading_images(image_id, item_type):
    # save the image id into a variable
    id0 = image_id

    # Request the data for the image from the API
    id0_url = 'https://api.planet.com/data/v1/item-types/{}/items/{}/assets'.format(item_type, id0)

    # keep trying to get the data until it is successful
    while True:
        try:
            result = \
            requests.get(
                id0_url,
                auth=HTTPBasicAuth(API_KEY, '')
            )
            break

        except:
            print("Error, trying again...")
            time.sleep(20)
            continue
    
    # Get the status of the 'ortho_analytic_4b' asset
    act_result = result.json()['ortho_analytic_4b']['status']
    print("\nAsset status: ", act_result)

    # Get the link to activate the 'ortho_analytic_4b' asset
    links = result.json()[u"ortho_analytic_4b"]["_links"]
    self_link = links["_self"]
    activation_link = links["activate"]

    print('\nAsset is activating, waiting...')

    # Activate the 'ortho_analytic_4b' asset
    activate_result = \
        requests.get(
            activation_link,
            auth=HTTPBasicAuth(API_KEY, '')
        )

    # keep trying to check if the asset is active and if not, then activate it
    while True:
        # Request activation of the 'ortho_analytic_4b' asset:
        try:
            activation_status_result = \
            requests.get(
                self_link,
                auth=HTTPBasicAuth(API_KEY, '')
            )
            
        except:
            print("Error, trying again...")
            time.sleep(20)
            continue

        # Get the status of the 'ortho_analytic_4b' asset 
        act_result = activation_status_result.json()["status"]
        print(act_result)

        # Check if the asset is active
        if act_result == 'activating':
            time.sleep(30)
            continue

        # If the asset is active, break the loop because now we can download the image
        elif act_result == 'active':
            break

        # If the asset is inactive, activate it and wait 30 seconds before checking again
        elif act_result == 'inactive':
            activate_result = \
                requests.get(
                    activation_link,
                    auth=HTTPBasicAuth(API_KEY, '')
                )
            time.sleep(30)
            continue
        else:
            print("Error, trying again...")
            exit()

    print('\nAsset is active!')

    # Get the download link and MD5 checksum
    download_link = activation_status_result.json()["location"]
    md5_digest = activation_status_result.json()["md5_digest"]

    # Download the image
    while True:
        print("\nDownloading image...")
        # download the image by calling the download_file function
        download_file(download_link, f"images/{id0}.tif")
        print("\nDownload complete!")

        # Check the MD5 checksum
        print("\nChecking MD5 checksum...")

        # call the md5_check function to see if the image is downloaded correctly
        if md5_check(md5_digest, f"images/{id0}.tif"):
            break
        else:
            print("\nMD5 checksum does not match, downloaded file is corrupt, downloading again...")
            time.sleep(10)
            continue


def main(geojson_geometry_data, date_start, date_end):
    # get the geometry from the geojson file
    geojson_geometry = geojson_geometry_data["features"][0]["geometry"]

    # add this to a filter to only get images that intersect with the geometry
    geometry_filter = {
    "type": "GeometryFilter",
    "field_name": "geometry",
    "config": geojson_geometry
    }

    # filter images acquired in a certain date range
    date_range_filter = {
        "type": "DateRangeFilter",
        "field_name": "acquired",
        "config": {
    "gte": date_start,
    "lte": date_end
        }
    }


    item_type = "PSScene"

    # create a filter that combines the geo and date filters
    combined_filter = {
        "type": "AndFilter",
        "config": [geometry_filter, date_range_filter]
    }

    # create a search request that includes the item type (PSScene) and the filter we just created
    search_request = {
        "item_types": [item_type], 
        "filter": combined_filter
    }

    # fire off the POST request with the above filters
    search_result = \
    requests.post(
        'https://api.planet.com/data/v1/quick-search',
        auth=HTTPBasicAuth(API_KEY, ''),
        json=search_request)
    
    geojson = search_result.json()
    search_results = []
    count = 1

    # iterate over all the results and print the id
    while True:
        print(f"Retrieving search results from page {count}...")
        search_results.extend(geojson["features"])
        for item in geojson["features"]:
            print(item["id"])

        next_url = geojson["_links"]["_next"]
        if next_url is None:
            break

        search_result = \
            requests.get(
                next_url,
                auth=HTTPBasicAuth(API_KEY, ''),
            )
        geojson = search_result.json()
        count += 1

    print("\nTotal number of listings found: ",len(search_results))

    # search_results = search_results[0:5]

    # if there are any results, iterate over them and download the image
    if len(search_results) > 0:
        print("*"*40)

        # iterate over the search results and download the image
        for i in range(len(search_results)):
            item_id = search_results[i]["id"]

            if os.path.exists(f"images/{item_id}.tif"):
                print("\nItem already exists, Skipping...")
                print("*"*40)
                continue

            print(f"\nDownloading item {item_id}\n")
            # call the download_image function to download the image
            downloading_images(item_id, item_type)
            print("*"*40)

    else: # if no results found then exit
        print(f"No results found")
        exit()


if __name__ == "__main__":
    print("Program started\n")

    # check if the images folder exists, if not then create it
    if os.path.exists("images") == False:
        os.mkdir("images")

    # input the name of the geojson file
    while True:
        filename = input("\nEnter the name of the GeoJSON file : ")

        if os.path.exists(filename):
            break
        else:
            print("File not found, Try again...")
            continue
    
    # load the geojson file
    with open (filename, "r") as file:
        geojson_geometry = json.load(file)

    # input the start with the correct format
    while True:
        date_start = input("\nEnter the start date in YYYY-MM-DD format : ")
        date_st_split = date_start.split("-")
        if len(date_st_split) == 3:
            if len(date_st_split[0]) == 4 and len(date_st_split[1]) == 2 and len(date_st_split[2]) == 2:
                break
            else:
                print("Invalid date format, Try again...")
                continue

    # input the end date with the correct format
    while True:
        date_end = input("\nEnter the end date in YYYY-MM-DD format : ")
        date_end_split = date_end.split("-")
        if len(date_end_split) == 3:
            if len(date_end_split[0]) == 4 and len(date_end_split[1]) == 2 and len(date_end_split[2]) == 2:
                break
            else:
                print("Invalid date format, Try again...")
                continue
    
    date_start = date_start + "T00:00:00.000Z"
    date_end = date_end + "T00:00:00.000Z"

    # call the main function
    main(geojson_geometry, date_start, date_end)

    print("\nProgram Ended")


