import pytest
import json

SNIPPETS_PREFIX = 'snippets/'

def pytest_terminal_summary(terminalreporter, exitstatus, config:pytest.Config):
    stats = {}
    for status in ['passed', 'failed', 'xfailed', 'skipped']:
        stats[status] = snipcount(terminalreporter, status)
    try :
        stats['snippet_score'] = int(stats['passed'] / (stats['passed'] + stats['failed']) * 100)
    except ZeroDivisionError:
        stats['snippet_score'] = -1

    if stats['snippet_score'] >= 0:
        # Write stats to file
        (config.rootpath / "coverage").mkdir(exist_ok=True)
        with open(config.rootpath / "coverage"/ 'snippet_score.json', 'w') as f:
            json.dump(stats, f, indent=4)
        with open(config.rootpath / 'snippet_score.txt', 'w') as f:
            f.write(str(stats['snippet_score']))
        
        print('----------------- terminal summary -----------------')
        print(stats)
        print('----------------------------------------------------')

def snipcount(terminalreporter, status:str):
    # Count the number of test snippets that have a given status
    if not terminalreporter.stats.get(status, []):
        return 0
    return len([rep for rep in terminalreporter.stats[status] if rep.nodeid.startswith(SNIPPETS_PREFIX)]) 