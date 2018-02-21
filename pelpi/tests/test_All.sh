PYTHON="python"
SEPARATOR="#######################################################################"
separator="__________________________"

# Testing the module import
echo $SEPARATOR
echo "Running test_init.py ..."
# echo $separator
$PYTHON test_init.py

# Testing pelpi objects
for FILE in test_[A-Z]*.py
do
  echo "\n"$SEPARATOR
  echo "Running "$FILE" ..."
  # echo $separator
  $PYTHON $FILE
done
