echo -e "$(tput setaf 3)Starting tests..."
for i in $(ls test_images); do
	python tester.py test_images/$i | grep '\[\]' > /dev/null 2>&1
	if [ $? == 0 ]; then
		echo -e "$(tput setaf 4)$i\t$(tput setaf 1)✘ contours array was empty; expected content"
	else
		echo -e "$(tput setaf 4)$i\t$(tput setaf 2)✔ all good"
	fi
done
rm -rf __pycache__
