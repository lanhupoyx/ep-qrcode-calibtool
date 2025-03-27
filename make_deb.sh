#!/bin/bash

CRTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CurrentTime=$(date +"%Y%m%d_%H%M%S")


PackageName=$(cat $CRTDIR/deb_package/DEBIAN/control  | grep Package: | awk -F: '{print $2}' | awk '{sub(/^[\t ]*|[\t ]*$/,"");print}')
echo "PackageName:"$PackageName

echo "注意：版本号、包名不能有空格和下划线，建议格式：1.0.0-2023-12-34"
read -p '请输入版本号:' Version
if [ -z $Version ]; then
    echo "未输入版本号，退出"
    exit 1
fi

sed -i -r 's/^Version:.*/Version:'"$Version"'/g' $CRTDIR/deb_package/DEBIAN/control
#sed -i -r 's/^Build-Time:.*/Build-Time:'"$CurrentTime"'/g' $CRTDIR/deb_package/DEBIAN/control
if grep -q '^Build-Time:' "$CRTDIR/deb_package/DEBIAN/control"; then
    sed -i -E 's/^Build-Time:.*/Build-Time:'"$CurrentTime"'/g' "$CRTDIR/deb_package/DEBIAN/control"
else
    echo "Build-Time:$CurrentTime" >> "$CRTDIR/deb_package/DEBIAN/control"
fi

pyinstaller --onefile main.py

cp /home/xun/work/ep-qrcode-calibtool/dist/main /home/xun/work/ep-qrcode-calibtool/deb_package/opt/xmover/app/ep-qrcode-calibtool/ep-qrcode-calibtool
cp /home/xun/work/ep-qrcode-calibtool/readme.txt /home/xun/work/ep-qrcode-calibtool/deb_package/opt/xmover/app/ep-qrcode-calibtool/


rm -r build
rm -r dist
rm -r __pycache__
rm main.spec


PackageSize=$((`du -b --max-depth=1 ${CRTDIR}/deb_package|awk 'END {print}'|awk '{print $1}'`))
sed -i -r 's/^Installed-Size:.*/Installed-Size:'"$PackageSize"'/g' $CRTDIR/deb_package/DEBIAN/control

sudo chmod 755 -R /home/xun/work/ep-qrcode-calibtool/deb_package/DEBIAN
mkdir ./deb_output/
dpkg -b deb_package ./deb_output/$PackageName-$Version-$CurrentTime.deb


echo "构造完成 --> "./deb_output/$PackageName-$Version-$CurrentTime.deb
exit 0
