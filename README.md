# echonest-track-analyser
Simple script that uploads tracks to echonest's API and then parses and aggregate the output.

prerequisites
-------------

You need `git` and `python3`.

download
--------
    
    git clone https://github.com/simlmx/echonest-track-analyser.git
    cd echonest-track-analyser

install
-------

    virtualenv ve
    source ve/bin/activate
    pip install -r requirements.txt

usage
------

    ./analyse_tracks -k you_key -o json_folder input_files
    ./parse_json -o output.csv json_folder/*.json
