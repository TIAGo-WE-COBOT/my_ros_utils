# Get the path to the script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# Change wd to the root of the package
cd $SCRIPT_DIR/../
# Overwrite the existing documentation
python -m pdoc --html --force --output-dir docs src/my_ros_utils
# Move the .html files one folder up
cp -r docs/my_ros_utils/. docs
# Remove the docs/my_ros_utils folder
rm -r docs/my_ros_utils/

