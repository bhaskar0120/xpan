import re
from strings import MAIN
# from batteries import *

# Global variables
env_var = {
    'ans' : None,
    'user_def' : {}
}

def function_call(func_name, args):
    print("Called function : {} with args : {}".format(func_name, args))
    return func_name, 0

def use_mem(key, value):
    env_var["user_defined"][key] = value

def solve_args(args):
    global env_var
    new_args = []
    for i in args:
        if i.startswith(MAIN.var_prefix):
            var_without_prefix = i[1:]
            if var_without_prefix == 'ans'
                new_args.append(env_var[var_without_prefix])
            elif var_without_prefix in env_var["user_def"]:
                new_args.append(env_var["user_def"][var_without_prefix])
            else:
                #TODO: Handle error
                pass
        else:
            new_args.append(i)
    return new_args

def parse(command):
    '''Parse the input'''
    global env_var
    label, *chain = command.split(MAIN.chain_separator)
    for invoke in chain:
        function, *args = list(filter(None,invoke.split()))
        res, err = function_call(function, solve_args(args))
        env_var['ans'] = res
    # Placeholder
    return env_var['ans'], 0

def main():
    global env_var
    print(MAIN.welcome_message)

    while True:
        command = input(MAIN.terminal_prompt)
        res, err = parse(command)
        if err:
            print(error(res))
        else:
            print(res)


if __name__ == "__main__":
    main()
