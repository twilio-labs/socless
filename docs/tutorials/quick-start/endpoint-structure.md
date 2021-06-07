# Endpoint Structure Overview
Endpoints are how external systems can trigger Playbooks in SOCless.

SOCless Endpoints are Python functions that are deployed to [AWS Lambda](https://aws.amazon.com/lambda/) service.

They use the `socless_python` library to register events in SOCless and start the desired playbook execution.

The basic structure for a SOCless endpoint is shown below

```python
--8<-- "docs-snippets/endpoint_basic_structure.py"
```

Endpoints can receive data in arbitrary formats, and enable their creators implement authentication in any fashion as needed. This makes them capable of receiving information from various kinds of HTTP-based sources such as Log Aggregation platforms, user endpoints, etc.

For now, let's setup the skeleton for the endpoint we'll write in this tutorial.

Endpoints are always written in the `functions` directory of a SOCless repository. Each Endpoint is stored in its own folder within the `functions` directory and in a file called `lambda_function.py`.

To setup the skeleton for our endpoint,

- Create a folder in the `functions` directory called `tutorial_endpoint`
- create a file within that folder called `lambda_function.py`
- Paste the code snippet above into that file

Our `socless-tutorial-playbook` stack should now look similar to the below (note: only the relevant structure is shown)

```
/socless-tutorial-playbook/
  ├── functions
  └── tutorial_endpoint
      ├── lambda_function.py
  ├── playbooks
      └── investigate_login
          ├── playbook.json
  ├── serverless.yml
```

!!! tip "Delete our sample functions!"
    There may be subfolder function in your `functions` folder called `send_old_timey_telegram`. This function is actually a Custom Integration. We'll cover how to create those in our [Developing Custom Integrations](../writing-custom-integrations/introduction.md) tutorial.

    Feel free to take a peek at it to get a taste of what's coming. But for now, feel free to delete the `send_old_timey_telegram` folder.
