#! /bin/bash

topDir="public_html"
if [ ! -d "${topDir}" ]; then
    echo "Run this script from the directory containing ${topDir}"
    exit
fi

pattern_file=.exclude
exclude_patterns=${TMPDIR:-/tmp}/${pattern_file}
cat - > ${exclude_patterns} <<EOF
._*
.DS_Store
website.db
settings.py
__pycache__
mah*
*.xcf
*~
EOF

export destHost="shakumant1" destDir="test-shakumant"
while (( $# > 0 )); do
    dest="$1"
    shift
    if [[ "${dest}" == "test" ]]; then
	export destDir="test-shakumant"
    elif [[ "${dest}" == "prod" || "${dest}" == "production" ]]; then
	export destDir="shakumant"
    else
	echo "Unrecognized destination: '${dest}'.  Use test or prod"
	continue
    fi
    
    echo "Pushing content below ${topDir} to ${destHost}:${destDir}" \
	 "with exclusions"

    scp ${exclude_patterns} ${destHost}:
    (cd ${topDir}; \
     tar --exclude-from ${exclude_patterns} --exclude-vcs -c -f - * ) | \
	ssh ${destHost} \
	    "(cd ${destDir}; tar --exclude-from ~/.exclude -x -v -f -)"
    
    echo "Content pushed to ${destHost}:${destDir}"
done

rm ${exclude_patterns}


