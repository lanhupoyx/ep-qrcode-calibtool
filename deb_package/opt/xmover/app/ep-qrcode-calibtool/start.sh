#!/bin/bash

CRTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

AppName=ep-qrcode-calibtool
AppRunPath=$CRTDIR/$AppName

#引入依赖库
   
cd $CRTDIR
$AppRunPath
