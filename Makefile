SHELL := /bin/zsh

zsh:
	python3 generate_aliases.py > ./tmp
	mv -f ./tmp ~/.kubectl_aliases
	exec zsh