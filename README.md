R2D2
====

R2D2 is a git helper scripts

Prerequisite
------------

```bash
pip3 install colorama
```

Setup
-----

```bash
cd <r2d2>
ln -sf $(pwd)/git-branches-ext ~/bin
ln -sf $(pwd)/git-status-ext ~/bin
```

```bash
git config --global alias.config-ext '!git-config-ext' # TODO
git config --global alias.b '!git-branches-ext'
git config --global alias.s '!git-status-ext'
```

Usage
-----

```bash
cd <git_project_folder>

# git config-ext # TODO
git config --local r2d2.accesstoken <token>
git config --local r2d2.projectid <project_id>
git config --local r2d2.checkmergedto development

git s # branch info
git b # list branches
git branch --edit-description # Enter some comment and save
```
