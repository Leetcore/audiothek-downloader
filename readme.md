This script can download mp3s and covers from ARD audiothek.

# Installation
``` bash
pip3 install -r setup.txt
```

# Usage
``` bash
python3 audiothek.py --url 'https://www.ardaudiothek.de/sendung/2035-die-zukunft-beginnt-jetzt-scifi-mit-niklas-kolorz/12121989/'
```

Can only download the first 999999 episodes! ;)

# Folder
`./output/id/index_episodename.mp3`

# Source URL
`https://api.ardaudiothek.de/graphql?query=query ProgramSetEpisodesQuery($id:ID!,$offset:Int!,$count:Int!){result:programSet(id:$id){items(offset:$offset first:$count orderBy:PUBLISH_DATE_DESC filter:{isPublished:{equalTo:true}}){pageInfo{hasNextPage endCursor}nodes{id title publishDate summary duration path image{url url1X1 description attribution}programSet{id title path publicationService{title genre path organizationName}}audios{url downloadUrl allowDownload}}}}}&variables={"id":"72633432","offset":0,"count":999999}`