def new_tab(tab_name, delay, command):
    return "--tab --name '{tab_name}' -e 'bash -c \"echo Loading...; echo {command}; {command}; exec $SHELL\"'"\
        .format(**locals())


