#! /bin/bash

export TOP=public_html
export HOST=shakumant1 TARGETDIR=test-shakumant

if [ ! -d ${TOP} ]; then
    echo "Run this script from the directory containing ${TOP}"
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

scp ${exclude_patterns} ${HOST}:
REMOTE_CMD="(cd ${TARGETDIR}; tar --exclude-from ~/.exclude -x -v -f -)"
echo "Tar'ing contents of ${TOP} and remotely executing on ${HOST}"
echo ${REMOTE_CMD}
(cd ${TOP}; tar --exclude-from ${exclude_patterns} --exclude-vcs -c -f - * ) | \
    ssh ${HOST} ${REMOTE_CMD}
rm ${exclude_patterns}

