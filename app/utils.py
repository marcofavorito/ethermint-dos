def new_tab(tab_name, command):
    return "--tab --name '{tab_name}' -e 'bash -c \"echo Loading...; {command}; exec $SHELL\"'"\
        .format(**locals())


