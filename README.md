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
sudo ln -sf ~/gitlabR2D2/git-branches-ext /usr/local/bin/
sudo ln -sf ~/gitlabR2D2/git-status-ext /usr/local/bin/
```

```bash
git config --global alias.b '!git-branches-ext'
git config --global alias.s '!git-status-ext'
```

Usage
-----

```bash
git branch --edit-description
```

Enter some comment and save

```bash
git b - list branches
git s - branch info
```
