import pathlib
import shutil
from subprocess import Popen, PIPE, STDOUT


# python编译so
def py_to_so(py_to_so_list):
    """
    :param py_to_so_list:  py文件列表，例如[test.py,]
    :return:
    """
    for py_to_so_item in py_to_so_list:
        # 将python代码翻译成c代码
        basename = py_to_so_item[:-3]
        py_to_c = "cython -D -3 --directive always_allow_keywords=true --embed {}".format(py_to_so_item)
        pl = Popen(py_to_c, shell=True, stdout=PIPE, stderr=STDOUT)
        pl.communicate()[0].decode('utf-8', errors='ignore')

        # 将c代码编译为linux动态链接库文件（
        c_to_so = "gcc {} -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I /usr/include/python3.8 -L /usr/bin -lpython3.8 -o {}".format(basename + ".c", basename + ".so")
        p2 = Popen(c_to_so, shell=True, stdout=PIPE, stderr=STDOUT)
        p2.communicate()[0].decode('utf-8', errors='ignore')


def py_to_bin(py_to_bin_list):
    """
    :param py_to_bin_list: py文件列表，例如[main.py,]
    :return:
    """
    for py_to_bin_item in py_to_bin_list:
        basename = py_to_bin_item[:-3]
        # 将python代码翻译成c代码
        py_to_c = "cython -D -3 --directive always_allow_keywords=true --embed {}".format(py_to_bin_item)
        p1 = Popen(py_to_c, shell=True, stdout=PIPE, stderr=STDOUT)
        p1.communicate()[0].decode('utf-8', errors='ignore')

        # 将c代码编译为二进制可执行文件
        c_to_bin = "gcc {} -I /usr/include/python3.8 -L /usr/bin -lpython3.8 -o {}".format(basename + ".c", basename)
        p2 = Popen(c_to_bin, shell=True, stdout=PIPE, stderr=STDOUT)
        p2.communicate()[0].decode('utf-8', errors='ignore')


def clean_build(project):
    """
    清理编译文件夹中的文件
    :param project:
    :return:
    """
    # 清理py文件
    for i in project.glob("**/*.py"):
        if i.name != "__init__.py" or i.name != "setup.py":
            i.unlink()

    # 清理c文件
    for j in project.glob("**/*.c"):
        j.unlink()

    # 清理__pycache__文件夹
    for k in project.glob("**/__pycache__"):
        shutil.rmtree(k)


if __name__ == "__main__":
    # 源文件夹
    project_pathlib = pathlib.Path.cwd()

    py_to_bin_list = ["main.py"]
    py_to_bin(py_to_bin_list)

    py_to_so_list = ["test.py"]
    for py in project_pathlib.glob("**/*.py"):
        if py.name != "__init__.py" and py.name != "setup.py" and py.name != "main.py":
            py_to_so_list.append(str(py))
    py_to_so(py_to_so_list)

    clean_build(project_pathlib)