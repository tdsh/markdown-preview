#!bash
#
# bash completion file for mdv command
#
# This script provides supports completion of:
#  - filename of mdv -d
# To enable the completion either:
#  - place this file in /etc/bash_completion.d
# or
#  - copy this file and add the line below to your .bashrc after
#    bash completion features are loaded
#    . mdv.bash
#
# And enable this completion
#  complete -F _filedir_mdv mdv

_filedir_mdv () {
	local cur prev words cword
	_init_completion || return

	case "$3" in
		-d)
			local md_dir="$( egrep "^DefaultDir" /etc/mdv.conf | sed -e 's/\t//g' | sed -e 's/ *//g' | cut -d = -f2 )"
			local result="$( cd $md_dir; ls $md_dir )"
			COMPREPLY=( `compgen -W "$result" $2` );;
		*)
			_filedir;;
	esac
}
