import argparse
import os
import re
import requests
import sys
import json

def main(url: str, folder: str):
    match = re.search(r"/(\d+)/?$", url)

    query = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphql", "ProgramSetEpisodesQuery.graphql") ).read()
    variables = {
        "id": match.group(1)
    }

    if match:
        response = requests.get('https://api.ardaudiothek.de/graphql', params={
            'query': query,
            'variables': json.dumps(variables)
        })

        response_json = response.json()
        nodes = response_json.get("data").get("result").get("items").get("nodes")
        
        for index, node in enumerate(nodes):
            number = node["id"]

            id = node.get("id")
            title = node.get("title")

            # get title from infos
            array_filename = re.findall(r"(\w+)", title)
            if len(array_filename) > 0:
                filename = "_".join(array_filename)
            else:
                filename = id
            
            filename = filename + "_" + str(number)

            # get image information
            image_url = node.get("image").get("url")
            image_url = image_url.replace("{width}", "500")
            mp3_url = node.get("audios")[0].get("downloadUrl")
            programset_id = node.get("programSet").get("id")

            program_path = os.path.join(folder, programset_id)

            # get information of program
            if programset_id:
                try:
                    os.makedirs(program_path)
                except FileExistsError:
                    pass
                except Exception as e:
                    print("[Error] Couldn't create output directory!", file=sys.stderr)
                    print(e, file=sys.stderr)
                    return

                # write image
                image_file_path = os.path.join(program_path, filename + '.jpg')
                
                
                if os.path.exists(image_file_path) == False:
                    response_image = requests.get(image_url)
                    with open(image_file_path, 'wb') as f:
                        f.write(response_image.content)

                # write mp3
                mp3_file_path = os.path.join(program_path, filename + '.mp3')

                print("Download: " + str(index + 1) + " of " + str(len(nodes)) + " -> " + mp3_file_path)
                if os.path.exists(mp3_file_path) == False:
                    response_mp3 = requests.get(mp3_url)
                    with open(mp3_file_path, 'wb') as f:
                        f.write(response_mp3.content)
            else:
                print("No programset_id found!", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ARD Audiothek downloader."
    )
    parser.add_argument(
        "--url", "-u", type=str, default="", required=True, help="Insert audiothek url (e.g. https://www.ardaudiothek.de/sendung/2035-die-zukunft-beginnt-jetzt-scifi-mit-niklas-kolorz/12121989/)"
    )
    parser.add_argument(
        "--folder", "-f", type=str, default="./output", help="Folder to save all mp3s"
    )

    args = parser.parse_args()
    url = args.url
    folder = os.path.realpath(args.folder)
    main(url, folder)