#!/bin/bash
set -x
if [ $TRAVIS_BRANCH == 'master' ] ; then
    git remote add deploy "travis@138.68.98.172:/apps/repo/paxos.git"
    git config user.name "Travis CI"
    git config user.email "michalkrezelewski@gmail.com"

    git add -A .
    git commit -m "Deploy"
    git push --force deploy master
else
    echo "Not deploying, since this branch isn't master."
fi
