SHELL := /bin/zsh

zsh: install
	exec zsh

install:
	python3 generate_aliases.py > ./tmp
	mv -f ./tmp ~/.kubectl_aliases


