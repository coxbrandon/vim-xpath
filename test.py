import sys

import nose

import re
import glob
import subprocess

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def run_python_tests():
    loader = nose.loader.TestLoader(workingDir='python')
    python_success = nose.run(testLoader=loader)

    if (python_success):
        print OKGREEN + 'All python tests passed' + ENDC
    else:
        print FAIL + 'Python tests failed' + ENDC

    return python_success

def run_vspec_tests():
    vim_success = False

    total_passed = 0
    total_run = 0

    for name in glob.glob('tests/**.vim'):
        cmd = ['./deps/vim-vspec/bin/vspec',
               './deps/vim-vspec', '.',
               name]

        try:
            output = subprocess.check_output(cmd)
        except Exception as e:
            print e
            raise


        passed, run = get_vspec_pass_fail(output)
        output = format_vspec_output(output)
        print output

        if run != '?':
            total_passed += int(passed)
            total_run += int(run)

    print

    if total_passed == total_run:
        vim_success = True
        print OKGREEN + 'All {0} vspec tests passed'.format(total_passed) + ENDC
    else:
        failed = total_run - total_passed
        print FAIL + '{0} of {1} vspec tests failed'.format(failed, total_run) + ENDC

    return vim_success


def format_vspec_output(output):
    output_lines = output.split('\n')
    formatted_lines = []

    for line in output_lines[:-2]:
        f_line = line

        if line.startswith("ok"):
            f_line = OKGREEN + f_line + ENDC

        if line.startswith("not ok"):
            f_line = FAIL + f_line + ENDC

        if line.startswith("#"):
            f_line = FAIL + "    " + line[1:] + ENDC

        formatted_lines.append(f_line)

    return '\n'.join(formatted_lines)

def get_vspec_pass_fail(output):
    output_lines = output.split('\n')
    stats_line = output_lines[-2]
    return stats_line.split('..')

if __name__ == '__main__':
    print "Running python tests:"
    print
    python_success = run_python_tests()

    print
    print "Running vspec tests:"
    print 
    vspec_success = run_vspec_tests()

    total_success = (python_success and vspec_success)
    if (total_success):
        print OKGREEN
    else:
        print FAIL

    print "-------------------------------"

    if (not python_success and not vspec_success):
        sys.exit("Python and vspec tests failed" + ENDC)

    if (not python_success):
        sys.exit("Python tests failed" + ENDC)

    if (not vspec_success):
        sys.exit("vspec tests failed" + ENDC)

    print ENDC

    sys.exit()
