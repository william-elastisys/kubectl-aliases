SHELL := /bin/zsh

zsh: install
	exec zsh

install:
	python3 generate_aliases.py > ./tmp
	mv -f ./tmp ~/.kubectl_aliases
	which kubecolor > /dev/null 2>&1 && sed -i -r 's/(kubecolor.*) --watch/watch -c \1/g' ~/.kubectl_aliases


