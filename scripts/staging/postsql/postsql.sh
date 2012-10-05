#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


set -e

CURDIR=$(dirname $0)

# load all views in this directory
for file in `ls -1 $CURDIR/*.sql`; do
        psql -f $file breakpad
done

#done
exit 0
