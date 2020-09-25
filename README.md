git-helpers
===========

Prerequisite
------------

```bash
pip3 install colorama
```

Setup
-----

```bash
sudo ln -s ~/git-helpers/git-branch-list-with-description /usr/local/bin/
```

```bash
git config --global alias.b '!git-branch-list-with-description'
```

Usage
-----

```bash
git branch --edit-description
```

Enter some comment and save.

```bash
git b
```

Comment can be splited by pipe charecter (|)  
Text after pipe will have different color  
