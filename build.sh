#!/bin/sh
if [ "x$1" = "x" ];
then
  echo Must specify output directory for zipped bundle
else
  git archive --format zip --output $1/jshint-external.tmbundle.zip master
fi
