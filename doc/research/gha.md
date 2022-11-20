
## from local execution env to gha env

everything works fine on local machine
on gha context, push to gh repo fails on the newly init local git repo

❌ try to work on auth
❌   - git config user.name name
❌   - git config user.email email
❌ try to change local branch name to main vs master
❌   - git init --initial-branch name
❌   - git branch -M name
❌   - git checkout -b name
❌ try to add a commit so that the branch exists
❌   - git commit --allow-empty
❌ try to push branch
❌   - git push -u remote branch
❌   - git push -u --set-upstream remote branch
❌   - git push -u remote HEAD:branch
❌ try to clone repo with full history
❌   - with depth 0

1. clone empty repo and switch .git dir
2. debug using gha tool to understand the context & diff between git init and git clone
3. try manually cloning the repo
