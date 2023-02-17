ls -t Nestle1904/nodes/*.xml | xargs -n 1 basename | while read filename; do basex -W -i Nestle1904/nodes/$filename mappings/lowfat-macula-greek.xquery > Nestle1904/lowfat/$filename; done
