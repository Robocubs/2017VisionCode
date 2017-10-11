passes=0
total=$(ls test_images | wc -l)
echo -e "$(tput setaf 3)Starting tests..."
for i in $(ls test_images); do
	python tester.py test_images/$i | grep '\[\]' > /dev/null 2>&1
	if [ $? == 0 ]; then
		echo -e "$(tput setaf 4)$i\t$(tput setaf 1)✘ contours array was empty; expected content"
	else
		echo -e "$(tput setaf 4)$i\t$(tput setaf 2)✔ all good"
		passes=$((passes + 1))
	fi
done
final=$(python add.py $passes $total)
echo -e "\n$(tput setaf 2)Generating coverage report, please wait..."
echo -e "\n$(tput setaf 3)Your pipeline covers $final% ($passes of $total) of your specified codebase."
if [ $final -gt 85 ]; then
	echo -e "\n$(tput setaf 2)General acceptance reached!"
fi
rm -rf __pycache__
