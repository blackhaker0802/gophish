sudo pip3 install -e .
a=$(getconf LONG_BIT)
if [ a == 64 ]; then
  wget https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux64.tar.gz &>/dev/null
  tar -xvf geckodriver-v0.28.0-linux64.tar.gz &>/dev/null && rm geckodriver-v0.28.0-linux64.tar.gz && sudo mv geckodriver /usr/local/bin
else
  wget https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux32.tar.gz &>/dev/null
  tar -xvf geckodriver-v0.28.0-linux32.tar.gz &>/dev/null && rm geckodriver-v0.28.0-linux32.tar.gz && sudo mv geckodriver /usr/local/bin
fi
