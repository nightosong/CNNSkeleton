import os
import tempfile
import shutil
import time


def parent_dir_path(path):
    ret = os.path.dirname(path)
    if ret == '':
        ret = os.getcwd()
    return ret


def dir_name(path, span=1):
    d = os.path.dirname(path)
    print(d)
    paths = (d, None)
    for _ in range(span):
        paths = os.path.split(paths[0])
    return paths[1]


def file_name(path, extension=True):
    name = os.path.basename(path)
    if not extension:
        name, _ = os.path.splitext(name)
    return name


def extension_name(path):
    _, extension = os.path.splitext(path)
    return extension


def sub_files(root_dir, include_file=False, include_dir=True):
    names = os.listdir(root_dir)
    paths = []
    for name in names:
        file_path = os.path.join(root_dir, name)
        if os.path.isdir(file_path):
            if include_dir:
                paths.append(file_path)
        else:
            if include_file:
                paths.append(file_path)
    return paths


def usr_home_dir():
    return os.path.expanduser('~')


def temp_dir():
    return tempfile.gettempdir()


def delete_file(file_path):
    os.remove(file_path)


def delete_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)


def copy_file(src_path, dst_path):
    shutil.copyfile(src_path, dst_path)


def copy_dir(src_dir, dst_dir):
    shutil.copytree(src_dir, dst_dir)


def mkdir(dir_path):
    os.makedirs(dir_path, exist_ok=True)


def move(src_path, dst_path):
    shutil.move(src_path, dst_path)


def memory_virtual_dir():
    pass


def to_linux_path_format(path):
    return path.replace('\\\\', '/').replace('\\', '/')


def absolute_path(path):
    return os.path.abspath(path)


def is_same_path(path1, path2):
    return os.path.normpath(os.path.abspath(path1)) == os.path.normpath(os.path.abspath(path2))


def subfiles(root_dir, include_dir=False):
    ret = []
    for filename in os.listdir(root_dir):
        path = os.path.join(root_dir, filename)
        if include_dir:
            ret.append(path)
        else:
            if os.path.isfile(path):
                ret.append(path)
    return ret


def subfiles_recursive(root_dir, include_dir=False):
    ret = []
    for root, sub_dirs, sub_files in os.walk(root_dir):
        for sub_filename in sub_files:
            path = os.path.join(root, sub_filename)
            ret.append(path)
        if include_dir:
            for sub_dirname in sub_dirs:
                path = os.path.join(root, sub_dirname)
                ret.append(path)
    return ret
