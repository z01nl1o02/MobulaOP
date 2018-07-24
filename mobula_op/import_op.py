import os
import re
from .func import IN, OUT, CFuncDef, bind
from .build import config, update_build_path, source_to_so_ctx, build_exit, ENV_PATH

def assert_file_exists(fname):
    assert os.path.exists(fname), IOError("{} not found".format(fname))

MOBULA_KERNEL_REG = re.compile(r'^\s*MOBULA_KERNEL.*?')
MOBULA_KERNEL_FUNC_REG = re.compile(r'^\s*MOBULA_KERNEL\s*(.*?)\s*\((.*?)\)(?:.*?)*')

def parse_parameters_list(plist):
    g = MOBULA_KERNEL_FUNC_REG.search(plist)
    head, plist = g.groups()
    head_split = re.split(r'\s+', head)
    plist_split = re.split(r'\s*,\s*', plist)
    func_name = head_split[-1]
    rtn_type = 'void'
    pars_list = []
    for p in plist_split:
        r = re.split(r'\s+', p)
        ptype = ' '.join(r[:-1])
        # remove const
        ptype = re.split(r'\s*const\s*', ptype)[-1]
        pname = r[-1]
        pars_list.append((ptype, pname))
    return rtn_type, func_name, pars_list

def get_so_path(fname):
    path, name = os.path.split(fname)
    return os.path.join(path, 'build', os.path.splitext(name)[0])

def build_lib(cpp_fname):
    cpp_path, cpp_basename = os.path.split(cpp_fname)
    build_path = os.path.join(cpp_path, 'build')
    # update_build_path(build_path)
    if not os.path.exists(build_path):
        os.mkdir(build_path)
    # build so for cpu
    target_name = get_so_path(cpp_fname) + '_cpu.so'
    srcs = [cpp_fname]
    for src in ['defines.cpp', 'context.cpp']:
        srcs.append(os.path.join(ENV_PATH, 'src', src))
    source_to_so_ctx(build_path, srcs, target_name, 'cpu')

STR2TYPE = {
    'void': None,
    'int': int,
    'float': float,
    'IN': IN,
    'OUT': OUT
}

def get_functions_from_cpp(cpp_fname):
    # Build
    build_lib(cpp_fname)
    build_exit()

    unmatched_brackets = 0
    func_def = ''
    func_started = False
    functions = dict()
    for line in open(cpp_fname):
        if not func_started:
            u = MOBULA_KERNEL_REG.search(line)
            if u is not None:
                func_def = ''
                func_started = True
        if func_started:
            unmatched_brackets += line.count('(') - line.count(')')
            func_def += line
            if unmatched_brackets == 0:
                func_started = False
                rtn_type, func_name, plist = parse_parameters_list(func_def)
                # Check Type
                for ptype, pname in plist:
                    assert ptype in STR2TYPE, TypeError('Unsupported Type: {}'.format(ptype))
                lib_path = get_so_path(cpp_fname)
                cfuncdef = CFuncDef(func_name = func_name,
                            arg_names = [t[1] for t in plist],
                            arg_types = [STR2TYPE[t[0]] for t in plist],
                            rtn_type = STR2TYPE[rtn_type],
                            lib_path = lib_path)
                functions[func_name] = cfuncdef

    assert unmatched_brackets == 0, Exception('# unmatched brackets: {}'.format(unmatched_brackets))
    return functions


def import_op(path):
    op_name = os.path.basename(path)
    cpp_fname = os.path.join(path, op_name + '.cpp')
    assert_file_exists(cpp_fname)
    py_fname = os.path.join(path, op_name + '.py')
    assert_file_exists(py_fname)
    functions = get_functions_from_cpp(cpp_fname)
    bind(functions)
