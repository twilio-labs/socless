# Setup
SOCless Playbooks are typically developed and stored in code repositories.

The quickest way to setup a Playbook repository is to use the `socless-template` repository.

Open up the terminal on your machine and run the below  commands in a `Projects` folder to setup the `socless-template` repository.


```
git clone [[ socless_repos_gh_org + '/socless-template']] socless-tutorial-playbook
cd socless-tutorial-playbook
npm install
```

The commands:

* clone the `socless-template` into a folder named `socless-tutorial-playbook`
* change into the `socless-tutorial-playbook` directory
* Install dependencies the template needs using NPM

Lastly, run the below command to rename our template according to the format `socless-[yourname]-tutorial-playbook`

```
npm run rename
```

After running the commands, we should be left with a `socless-tutorial-playbook` directory that looks similar to the below

``` hl_lines="5 9 12"
/socless-tutorial-playbook/
  ├── LICENSE
  ├── README.md
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

Take a quick peek at the first line of your `serverless.yml` to confirm that our service was renamed correctly. It should look similar to

```yaml
service: socless-[yourname]-tutorial-playbook
```




While there are number of files and folders here, we'll only be concerned with the following in this tutorial:

- functions (directory): We'll write code for our Endpoint here. In later tutorials, we'll write code for Integrations here too.
- playbooks (directory): We'll write our playbooks here
- serverless.yml (file): We'll configure our Endpoint and Playbook for deployment here

In fact, most of our time as SOCless developers will be spent in these three locations. We'll cover each in more detail as we move through our tutorial.
