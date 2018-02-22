PYTHON="python"
SEPARATOR="#######################################################################"
separator="__________________________"

# Testing pelpi objects
for FILE in test_[A-Z]*.py
do
  echo "\n"$SEPARATOR
  echo "Running "$FILE" ..."
  # echo $separator
  $PYTHON $FILE
done
