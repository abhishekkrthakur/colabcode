### [Adding the **`gitpod`** badge](https://community.gitpod.io/t/is-there-any-open-on-gitpod-badge-that-i-can-just-copy-and-paste/989/7)

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/.../...)

[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/.../...)


### [Git `fetch` **upstream** and `rebase`](https://stackoverflow.com/questions/7244321/how-do-i-update-a-github-forked-repository)
```bash
# Add the remote, call it "upstream":

git remote add upstream https://github.com/whoever/whatever.git

# Fetch all the branches of that remote into remote-tracking branches,
# such as upstream/master:

git fetch upstream

# Make sure that you're on your master branch:

git checkout master

# Rewrite your master branch so that any commits of yours that
# aren't already in upstream/master are replayed on top of that
# other branch:

git rebase upstream/master
```

If you've rebased your branch onto upstream/master you may need to force the push in order to push it to your own forked repository on GitHub. You'd do that with:

`git push -f origin master`

You only need to use the `-f` the first time after you've rebased.


### [Github `branch` and `pull request`](https://www.gun.io/blog/how-to-github-fork-branch-and-pull-request)
- track upstream : `git remote add --track master upstream git://github.com/upstreamname/projectname.git`
- then fetch, rebase, and push : 
    ```bash
    git fetch upstream
    git checkout master
    git rebase upstream/master
    git push origin master
    ```
- add `pull request` from a new branch : `git checkout -b newfeature`
    
    > So, `master` remains clean (even if pull request is **rejected**)