MAGENTA=$(tput setaf 5)
NORMAL=$(tput sgr0)

echo "${MAGENTA}\n\nUNITTEST:\n${NORMAL}"
sh run-unittest.sh
echo "${MAGENTA}\n\nPYTEST:\n${NORMAL}"
sh run-pytest.sh
echo "${MAGENTA}\n\nLETTUCE:\n${NORMAL}"
sh run-lettuce.sh
