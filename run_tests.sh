for i in $(ls test_images); do
	python tester.py test_images/$i | grep '\[\]' > /dev/null 2>&1
	if [ $? == 0 ]; then
		echo -e "$(tput setaf 4)$i\t$(tput setaf 1)✘"
	else
		echo -e "$(tput setaf 4)$i\t$(tput setaf 2)✔"
	fi
done
