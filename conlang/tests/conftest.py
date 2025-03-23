import pytest


successes = []
failures = []


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        params = item.callspec.params if hasattr(item, 'callspec') else {}
        original, mutated, target = params.get('original'), params.get('mutated'), params.get('target')
        if report.passed:
            successes.append((original, mutated, target))
        elif report.failed:
            failures.append((original, mutated, target))


def pytest_sessionfinish(session, exitstatus):
    print(f"\n\n{BOLD}==================== Test Summary ===================={RESET}")
    if successes:
        print(f'{GREEN}{BOLD}\n✅Passed:{RESET}')
        for original, mutated, target in successes:
            print(f'{GREEN}  *{original[0]} -> {mutated[0]} == {target[0]}{RESET}')

    if failures:
        print(f'{RED}{BOLD}\n❌Failed:{RESET}')
        for original, mutated, target in failures:
            print(f'{RED}  *{original[0]} -> {mutated[0]} != {target[0]}{RESET}')

    session.config.pluginmanager.unregister(name="terminalreporter")
