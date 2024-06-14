#!/bin/bash
WEB_LOCATION=/home/submit/freerc/public_html/MonoZ_CMSDAS
if [ ".$1" != "." ]
then
   WEB_SERVER="$1"
fi
RSYNC_TARGET=$WEB_LOCATION

echo " Installing into: $RSYNC_TARGET (hit return)"
read

sphinx-build -b html source build
if [ ".$?" != ".0" ]
then
    echo " Sphinx build failed ... please fix."
    exit 1
fi

make html
if [ ".$?" != ".0" ]
then
    echo " Making the html sources failed ... please fix."
    exit 2
fi

# hack to get colors right - overwrite theme pygments file.
echo "\
cp css/pygments.css build/_static/"
cp css/pygments.css build/_static/

echo "\
rsync -Cavz --delete build/* $RSYNC_TARGET"
rsync -Cavz --delete build/* $RSYNC_TARGET
