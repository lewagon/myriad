
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

✅ missing global git config prevents commit:
   - git config --global user.name
   - git config --global user.email

other alternatives:

1. tmate debug
2. try manually cloning the repo in another location
3. clone empty repo and switch .git dir
