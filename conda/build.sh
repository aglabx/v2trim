V2_DIR=$PREFIX/v2trim
mkdir $V2_DIR
cp -r $SRC_DIR/* $V2_DIR
cd $PREFIX/bin
ln -s $V2_DIR/*.exe .
ln -s $V2_DIR/*.data .
