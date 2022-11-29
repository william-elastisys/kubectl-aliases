SHELL := /bin/zsh

zsh:
	python3 generate_aliases.py > ~/.kubectl_aliases
	source ~/.zshrc