import re
from strings import MAIN
from strings import ENV_FIELD
# from batteries import *

# Global variables
env_var = {
        
        }

def function_call(func_name, args):
    print("Called function : {} with args : {}".format(func_name, args))
    return func_name, 0

def solve_args(args):
    global env_var
    new_args = []
    for i in args:
        if i.startswith(MAIN.var_prefix):
            var_without_prefix = i[1:]
            if var_without_prefix in env_var:
                new_args.append(env_var[var_without_prefix])
            elif var_without_prefix in env_var[ENV_FIELD.user_var_list]:
                new_args.append(env_var[ENV_FIELD.user_var_list][var_without_prefix])
            else:
                #TODO: Handle error
                pass
        else:
            new_args.append(i)
    return new_args

def parse(command):
    '''Parse the input'''
    global env_var
    env_var[ENV_FIELD.logical_function_list] = []
    env_var[ENV_FIELD.statement] = None

    label, *chain = command.split(MAIN.chain_separator)
    for invoke in chain:
        function, *args = list(filter(None,invoke.split()))
        arg_vals = solve_args(args)
        if function == ENV_FIELD.logical_function_list:
            env_var[ENV_FIELD.logical_function_list].append(env_var[ENV_FIELD.ans])
            env_var[ENV_FIELD.statement] = MAIN.true
            continue
        if len(env_var[ENV_FIELD.logical_function_list]) > 0:
            if (not env_var[ENV_FIELD.logical_function_list][-1]) and (env_var[ENV_FIELD.statement] == MAIN.true):
                continue
            elif (env_var[ENV_FIELD.logical_function_list][-1]) and (env_var[ENV_FIELD.statement] == MAIN.false):
                continue
        if env_var[ENV_FIELD.statement] == MAIN.true:
            env_var[ENV_FIELD.statement] = MAIN.false
        elif env_var[ENV_FIELD.statement] == MAIN.false:
            env_var[ENV_FIELD.statement] = None
            env_var[ENV_FIELD.logical_function_list].pop()
        number = re.match(r'\d+', function)
        times = int(number.group()) if number else 1
        env_var[ENV_FIELD.times] = 0
        func_name = function[number.span()[1]:] if number else function
        for i in range(times):
            res, err = function_call(func_name, arg_vals)
            env_var[ENV_FIELD.times] += 1
            env_var[ENV_FIELD.last] = res
        env_var[ENV_FIELD.ans] = res
    # Placeholder
    return env_var[ENV_FIELD.ans], 0

def main():
    global env_var
    print(MAIN.welcome_message)
    for i in dir(ENV_FIELD):
        if not i.startswith('__'):
            if i.endswith('_list'):
                env_var[getattr(ENV_FIELD, i)] = []
            else:
                env_var[getattr(ENV_FIELD, i)] = None

    while True:
        command = input(MAIN.terminal_prompt)
        res, err = parse(command)
        if err:
            print(error(res))
        else:
            print(res)


if __name__ == "__main__":
    main()
