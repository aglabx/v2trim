set -e

echo "Building v2trim..."

cp -r $SRC_DIR/* $PREFIX/

mkdir $PREFIX/bin
cd $PREFIX/bin
ln -s  $PREFIX/v2trim.py ./v2trim
chmod +x ./v2trim
chmod +x ../data/V2_trim.exe
