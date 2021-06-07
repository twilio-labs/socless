# Setup
Like we did in the Getting Started Tutorial, we'll use the `socless-template` repository to setup a stack for our integrations.

Open up the terminal on your machine and run the below commands to setup the `socless-template` repository


```bash
git clone [[ socless_repos_gh_org + '/socless-template']] socless-tutorial-integrations
cd socless-tutorial-integrations
npm install
```

Finally, rename the repository using the command
```
npm run rename
```

This time, we'll rename our repository to `socless-[yourname]-tutorial-integrations`

After running the commands, we should be left with a directory that looks similar to the below

``` hl_lines="6 10 13"
/socless-tutorial-integrations/
  ├── LICENSE
  ├── README.md
  ├── build.yaml
  ├── common_files
  ├── functions
  ├── node_modules
  ├── package-lock.json
  ├── package.json
  ├── playbooks
  ├── pyproject.toml
  ├── rename.py
  ├── serverless.yml
  ├── setup.cfg
  └── tests
```

Like in our Getting Started tutorial, we'll be working primarily in the `functions`, `serverless.yml` and `playbooks` files/folders.
