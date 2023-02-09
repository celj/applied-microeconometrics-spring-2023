import os
import re
import requests
import time

url = "https://ecobici.cdmx.gob.mx/datos-abiertos/"
response = requests.get(url)

if response.status_code == 200:
    content = response.text

    links = re.findall('(?<=a href=")/wp-content/uploads/[^"]+', content)

    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    for link in links:
        file_url = "https://ecobici.cdmx.gob.mx" + link
        file_path = os.path.join(data_folder, os.path.basename(link))
        print(file_url)
        if os.path.exists(file_path):
            print(
                "Skipping",
                file_url,
                "as it already exists in",
                file_path,
            )
            continue

        print(
            "Downloading",
            file_url,
            "in",
            file_path,
        )
        start_time = time.time()
        response = requests.get(file_url)
        if response.status_code == 200:
            open(file_path, "wb").write(response.content)
            print(
                "Downloaded",
                file_url,
                "in",
                "{:.2f}".format((time.time() - start_time) / 60),
                "minutes",
            )
        else:
            print("Failed to download", file_url)
else:
    print("Failed to retrieve the content of", url)
