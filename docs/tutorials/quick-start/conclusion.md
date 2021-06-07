# Conclusion
Congratulations on completing the tutorial! :fireworks: :champagne: :champagne:

This tutorial taught us how to:

- Create Playbooks
- Configure Integrations in Playbooks
- Use [Template Variables](../../reference/variables.md#template-variables) to pass execution context data (`{{context.*}}`) and secrets `{{secrets('/path/to/secret')}}` as parameters
- Create Endpoints
- Configure secrets as environment variables on Endpoints using the Serverless Variable `${{ssm:/path/to/secret~true}}`
- Create and upload secrets using the `socless secret add` command
- Implement simple authentication for an endpoint
- Implement a simple Task failure handler that alerts us of playbook failures
- Deploy our Playbooks and Endpoints using the `socless stack deploy`


!!! tip "Keep your work!"
    Keep a copy of your socless-tutorial-playbook repository handy! You'll need it for the [Developing Custom Integrations Tutorial](../writing-custom-integrations/introduction.md)

But the SOCless journey doesn't end here! There's so much else to learn such as:

- [Developing Custom Integrations](../writing-custom-integrations/introduction.md)

PS: Thanks to our InvestigateLogin Playbook, we now know that Bruce Wayne's account was logged into from China. Hmm... Is he really out there? :thinking: If so, what could he possibly be up to? Maybe we'll find out soon :wink:
