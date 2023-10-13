import pytest
import json

SNIPPETS_PREFIX = 'snippets/'

def pytest_terminal_summary(terminalreporter, exitstatus, config:pytest.Config):
    stats = {}
    for status in ['passed', 'failed', 'xfailed', 'skipped']:
        stats[status] = snipcount(terminalreporter, status)
    stats['snippet_score'] = round(stats['passed'] / (stats['passed'] + stats['failed']) * 100, 1)

    # Write stats to file
    stats_file = config.rootpath / 'snippet_stats.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=4)
    print('----------------- terminal summary -----------------')
    print(stats)
    print('----------------------------------------------------')

def snipcount(terminalreporter, status:str):
    # Count the number of test snippets that have a given status
    if not terminalreporter.stats.get(status, []):
        return 0
    return len([rep for rep in terminalreporter.stats[status] if rep.nodeid.startswith(SNIPPETS_PREFIX)]) 