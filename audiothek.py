import argparse
import os
import re
import requests

def main(url: str, folder: str):
    match = re.search(r"/(\d+)/?$", url)
    if match:
        response = requests.get('https://api.ardaudiothek.de/graphql?query=query ProgramSetEpisodesQuery($id:ID!,$offset:Int!,$count:Int!){result:programSet(id:$id){items(offset:$offset first:$count orderBy:PUBLISH_DATE_DESC filter:{isPublished:{equalTo:true}}){pageInfo{hasNextPage endCursor}nodes{id title publishDate summary duration path image{url url1X1 description attribution}programSet{id title path publicationService{title genre path organizationName}}audios{url downloadUrl allowDownload}}}}}&variables={"id":"' + match.group(1) +'","offset":0,"count":999999}')
        response_json = response.json()
        nodes = response_json.get("data").get("result").get("items").get("nodes")
        
        for index, node in enumerate(nodes):
            number = len(nodes) - index
            id = node.get("id")
            title = node.get("title")

            # get title from infos
            array_filename = re.findall(r"(\w+)", title)
            if len(array_filename) > 0:
                filename = "_".join(array_filename)
            else:
                filename = id

            # get image information
            image_url = node.get("image").get("url")
            image_url = image_url.replace("{width}", "500")
            mp3_url = node.get("audios")[0].get("downloadUrl")
            programset_id = node.get("programSet").get("id")

            # get information of program
            if programset_id:
                try:
                    os.mkdir(folder + "/" + programset_id)
                except:
                    pass

                # write image
                image_file_path = folder + '/' + programset_id + "/" + str(number) + "_" + filename + '.jpg'
                if os.path.exists(image_file_path) == False:
                    response_image = requests.get(image_url)
                    with open(image_file_path, 'wb') as f:
                        f.write(response_image.content)

                # write mp3
                mp3_file_path = folder + '/' + programset_id + "/" + str(number) + "_" + filename + '.mp3'
                print("Download: " + str(index + 1) + " of " + str(len(nodes)) + " -> " + mp3_file_path)
                if os.path.exists(mp3_file_path) == False:
                    response_mp3 = requests.get(mp3_url)
                    with open(mp3_file_path, 'wb') as f:
                        f.write(response_mp3.content)
            else:
                print("No programset_id found!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ARD Audiothek downloader."
    )
    parser.add_argument(
        "--url", "-u", type=str, default="", required=True, help="Insert audiothek url (https://www.ardaudiothek.de/sendung/2035-die-zukunft-beginnt-jetzt-scifi-mit-niklas-kolorz/12121989/)"
    )
    parser.add_argument(
        "--folder", "-f", type=str, default="./output", help="Folder to save all mp3s"
    )
    args = parser.parse_args()
    url = args.url
    folder = args.folder
    main(url, folder)