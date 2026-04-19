#!/bin/sh

set -xe

LOCALES_DIR=./locales/
DOMAIN=nbodysim
SOURCE=./src/nbodysim/

mkdir -p $LOCALES_DIR

TEMPLATE="$LOCALES_DIR$DOMAIN.pot"

COPY_HOLDERS=$(paste -sd ", " AUTHORS)
VERSION=$(grep "__version__" "$SOURCE"__init__.py | cut -d'"' -f2)

if [ ! -f $TEMPLATE ]; then
    find $SOURCE -name "*.py" | xgettext -d $DOMAIN \
        -L Python -f- -o $TEMPLATE \
        --strict --copyright-holder="$COPY_HOLDERS" \
        --package-name=$DOMAIN --package-version="$VERSION"
else
    find $SOURCE -name "*.py" | xgettext -d $DOMAIN -j \
        -L Python -f- -o $TEMPLATE \
        --strict --copyright-holder="$COPY_HOLDERS" \
        --package-name=$DOMAIN --package-version="$VERSION"
fi

$EDITOR $TEMPLATE

SUPPORTED_LOCALES="en pt_PT"

for LOCALE in $SUPPORTED_LOCALES; do
    MESSAGES_DIR="$LOCALES_DIR$LOCALE/LC_MESSAGES/"
    mkdir -p "$MESSAGES_DIR"

    FILE="$MESSAGES_DIR/$DOMAIN.po"

    if [ ! -f "$FILE" ]; then
        msginit -i $TEMPLATE -o "$FILE" -l "$LOCALE"
    else
        msgmerge -U --lang="$LOCALE" --strict "$FILE" $TEMPLATE
    fi
done
