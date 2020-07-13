#!/bin/sh

URL="https://symkowick.org/posts/index.xml"

curl -s "$URL" | sed 's/<description><\/description>//g;
s/<content type="html">/<description>/g;
s/<\/content>/<\/description>/g' > feed.xml
