import os
import json
import subprocess

# has been propagated from repo vars to env vars
try:
    current_scores= json.loads(os.getenv('SNIPPET_SCORE', '{"snippet_score": 0}'))
except json.decoder.JSONDecodeError:
    current_scores = {"snippet_score": 0}

# set by pytest in custom conftest reporting
new_scores = {}
with open('coverage/snippet_score.json', 'r') as f:
    new_scores = json.load(f)


# Compare the scores and update the repository variable if necessary
def add_summary(msg, current_scores:dict, new_scores:dict):
    with open(os.getenv('GITHUB_STEP_SUMMARY',0), 'a') as f:
        f.write("# Snippets\n")
        f.write(msg)
        f.write("\n```json\n")
        json.dump({'current': new_scores}, f)
        f.write("\n")
        json.dump({'previous':current_scores}, f)
        # f.write("[\n")
        # json.dump({'new': new_scores}, f)
        # json.dump({'previous': current_scores}, f)
        # f.write("\n]")
        f.write("\n```\n")

if new_scores['snippet_score'] < current_scores['snippet_score']:
    msg = f"The snippet_score has decreased from {current_scores['snippet_score']} to {new_scores['snippet_score']}"
    print(msg)
    add_summary(msg, current_scores, new_scores)
    exit(1) # Fail the test
elif new_scores['snippet_score'] == current_scores['snippet_score']:
    msg = f"The snippet_score has not changed from {current_scores['snippet_score']}"
    print(msg)
    add_summary(msg, current_scores, new_scores)
elif os.getenv('GITHUB_REF_NAME',"main") == "main" and new_scores['snippet_score'] > current_scores['snippet_score']:
    msg = f"The snippet_score has improved to {new_scores['snippet_score']}"
    print(msg)
    add_summary(msg, current_scores,new_scores)
    # Update the repository variable
    # ref: https://cli.github.com/manual/gh_auth_login
    repo = os.getenv('GITHUB_REPOSITORY',"Josverl/progress_is_good")
    set_repo_var = f"gh --repo {repo} variable set SNIPPET_SCORE < coverage/snippet_score.json"
    # Use a fine grained token to update the variable only
    gh_token_vars = os.getenv('GH_TOKEN_VARS', os.getenv('GH_TOKEN', '-'))
    subprocess.run(set_repo_var, cwd=os.getenv('GITHUB_WORKSPACE', '.'), shell=True, check=True, env={'GH_TOKEN': gh_token_vars})

exit(0)