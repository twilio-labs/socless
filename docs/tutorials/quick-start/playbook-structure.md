# Playbook Structure Overview
SOCless Playbooks are simply JSON objects that describe the steps to take and resources to use to automate a workflow.

The basic structure for any SOCless Playbook JSON object is shown below:

```json
--8<-- "docs-snippets/playbook_basic_structure.json"
```

It consists of the following top-level fields:

- `Playbook`: (required) The name of the playbook. eg. InvestigateLogin. **Must follow UpperCamelCase notation (no spaces, dashes or underscores)**
- `Comment`: (optional) Human readable description of the playbook
- `StartAt`: (required) The starting `State` (i.e first step) of the playbook
- `States`: (required) Configurations off all the States in the playbook and how they relate to each other i.e transitions.
- `Decorators`: (optional) Decorators provide functionality that is applied to all states in your playbook, for example, a global `TaskFailureHandler` state which is called if any state in your playbook fails



`States` in the `State` object are also configured as JSON objects. Each state has a name.  Different `Types` of states accept different configurations. For this tutorial, we'll focus on `Task` type, which is used when configuring an Integration.

Below shows the basic configuration of a `Task` state. We'll call the state `Geolocate_IP` for our example.

```json hl_lines="3-12"
{
    "Playbook": "",
    "Comment": "",
    "StartAt": "Geolocate_IP",
    "States": {
      "Geolocate_IP": {
        "Type": "Task",
        "Resource": "",
        "Parameters": {

        },
        "Next": ""
      }
    },
    "Decorators": {

    }
}
```

* `Type`: The type of state it is. For States that use Integrations, this is usually `Task`. Other types exist such as `Choice`, `Parallel`, `Interaction` and `Wait` exist but we'll cover them in future tutorials.
* `Resource`: The Integration the State uses to perform its Task
* `Parameters`: The parameters to pass to the Integration
* `Next`: The next state to transition to after the State's task is completed


While these aren't the only fields supported for a `Task` state, these are the basic (and required) fields which we'll cover in this tutorial.

Playbooks are always written in the `playbooks` directory of a SOCless repository. Each Playbook is stored in its own folder within the `playbooks` directory and in a file called `playbook.json`.



**To setup the skeleton for our playbook:**

- Create a folder under the playbooks directory called `investigate_login`
- Create a file inside the `investigate_login` folder called `playbook.json`
- Write the code snippet above into the `playbook.json` file

Our `socless-tutorial-playbook` stack should now look similar to the below (note: only the relevant structure is shown)

```
/socless-tutorial-playbook/
  ├── functions
  ├── playbooks
      └── investigate_login
          ├── playbook.json
  ├── serverless.yml
```
