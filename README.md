# markdown-preview

Preview Markdown file via terminal.

## Install

### requirements

- Python 2.7 or later
- markdown2
- w3m
- bash-completion

### set up

```shell
cp files/mdv.conf /etc
cp files/mdv.bash /etc/bash-completion.d
. /etc/bash-completion.d/mdv.bash
complete -F _filedir_mdv mdv
ln -s ./mdv.py /usr/local/bin/mdv
```

### run

Just run with specifying markdown file you want to preview.

```shell
mdv README.md
```

Besides, you can set default directory where you store markdown files
in /etc/mdv.conf.

```shell
DefaultDir = ~/work/project/ABC/doc
```

In this case the following 2 excecutions have the same meaning.

```shell
mdv ~/work/project/ABC/doc/README.md
mdv -d README.md
```

It can be a shortcut that you don't have to specify all the long path
name. You can get filenames under default directory by hitting TAB
after "mdv -d".
