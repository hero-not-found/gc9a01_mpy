# TODO: make sure esp-idf is exported in path

# microphython directory - submodule, symlink, absolute path, whatever
MICROPYTHON_DIR=~/projects/hnf/lv_micropython
USERMODULES_DIR=$(pwd)/src
BOARDS_DIR=$MICROPYTHON_DIR/ports/esp32/boards
BOARD=ESP32_GENERIC_S3
FROZEN_MANIFEST=$(pwd)/manifest.py


# if PORT wasn't passed in then find it with the right shell command
PORT=$2
if [ -z "$PORT" ]; then
    PORT=$(ls /dev/cu.usb* | head -n 1)
fi

BUILD=$(pwd)/.build/$BOARD
if [ -n "$BOARD_VARIANT" ]; then
    BUILD=$BUILD-$BOARD_VARIANT
fi

MAKE_CMD="make \
    -C $MICROPYTHON_DIR/ports/esp32 \
    BOARD=$BOARD \
    BOARD_VARIANT=$BOARD_VARIANT \
    BOARD_DIR=$BOARDS_DIR/$BOARD \
    BUILD=$BUILD \
    FROZEN_MANIFEST=$FROZEN_MANIFEST \
    USER_C_MODULES=$USERMODULES_DIR/micropython.cmake"

if [ "$1" == "deploy" ]; then
    MAKE_CMD="$MAKE_CMD PORT=$PORT deploy"
fi

if [ "$1" == "clean" ]; then
    MAKE_CMD="$MAKE_CMD clean"
fi

if [ "$1" == "erase" ]; then
    MAKE_CMD="$MAKE_CMD PORT=$PORT erase"
fi

eval $MAKE_CMD
