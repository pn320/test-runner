import importlib.machinery
import os
import traceback
import types
from inspect import getmembers
from inspect import isfunction
from .import utils
from typing import List
import sys
from .expectation import FailedExpectationError


class TestRunner:
    _ignored_run_files = ["__pycache__", ".idea"]

    def __init__(self, path: str):
        self.test_files = []
        self.load_test_files(path)

    def load_test_files(self, path: str):
        if os.path.isfile(path):
            self.test_files.append(path)
        if path.endswith(tuple(self._ignored_run_files)):
            return
        elif os.path.isdir(path):
            for nested_path in os.listdir(path):
                self.load_test_files(os.path.join(path, nested_path))

    @staticmethod
    def load_tests(module):
        return [m for m in getmembers(module) if isfunction(m[1]) and m[0].startswith("test_")]

    @staticmethod
    def load_module(file):
        loader = importlib.machinery.SourceFileLoader("testmodule", file)
        module = types.ModuleType(loader.name)
        loader.exec_module(module)
        return module

    def run_single_test_file(self, file):
        success = True
        failed_tests: List[str] = []
        module = self.load_module(file)
        tests = self.load_tests(module)
        print(f"Running {file}")
        for test in tests:
            test_name, test_function = test
            try:
                test_function()
                print(f"  - Running test {test_name}: {utils.GREEN}passed{utils.RESET}")
            except FailedExpectationError as _:
                success = False
                failed_tests.append(test_name)

                def format_failure_log():
                    """
                    Just some nasty string manipulation, don't even bother understanding how this works.
                    :return:
                    """
                    first, *log, last = traceback.format_exc().splitlines()
                    log = [' ' * 6 + log_element for index, log_element in enumerate(log)]
                    nl = '\n'
                    last = f"{utils.RED} {last.split(':')[1]} {utils.RESET}"
                    first = f"{f'{utils.RESET}('.join(first.split('('))}"
                    return f"{utils.RED}{(' ' * 6) + first}" \
                           f"{utils.RESET}\n{nl.join(log)}\n" \
                           f"{(' ' * 6) + last}"

                failure_log = format_failure_log()
                print(f"  - Running test {test_name} {utils.RED}(failed){utils.RESET}")
                print(f"{failure_log}")

        self.print_runner_results(success, failed_tests, tests, file)
        print()

    @staticmethod
    def print_runner_results(status, failed_tests: List[str], tests, file: str):
        if status:
            print(f"{file} {utils.GREEN}({len(tests)} out of {len(tests)} tests passed: ok ✔){utils.RESET}")
        else:
            print(f"\n{len(failed_tests)} test{'s' if len(failed_tests) > 1 else ''} {utils.RED}failing.{utils.RESET}")
            for failed_test in failed_tests:
                print(f"{utils.RED}(fail){utils.RESET} {failed_test}")

    def run(self):
        for test_file in self.test_files:
            self.run_single_test_file(test_file)


def main():
    TestRunner(sys.argv[1]).run()
