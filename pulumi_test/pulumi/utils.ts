import { getCallerIdentity, Tags } from '@pulumi/aws';
import * as pulumi from '@pulumi/pulumi';

export const accountID = getCallerIdentity().then((result) => result.accountId);
export const PROJECT = pulumi.getProject();
export const STACK = pulumi.getStack();
export const FULL_NAME = `${PROJECT}-${STACK}`;

/**
 * registerAutoTags registers a global stack transformation that merges a set
 * of tags with whatever was also explicitly added to the resource definition.
 */
export function registerAutoTags(autoTags: Record<string, string>): void {
  pulumi.runtime.registerStackTransformation((args) => {
    if ('tags' in args.props) {
      args.props['tags'] = { ...args.props['tags'], ...autoTags };
      return { props: args.props, opts: args.opts };
    }
    return undefined;
  });
}

export const tagSoclessPlatform: Tags = {
  platform: 'socless',
};

export const tagDeprecated: Tags = {
  deprecation_status: 'deprecated',
};

export function stackToRegion() {
  switch (pulumi.getStack().toLowerCase()) {
    case 'dev':
      'us-west-2';
      break;
    case 'stage':
      'us-east-2';
      break;
    case 'prod':
      'us-east-1';
      break;
    case 'sandbox':
      'us-west-1';
      break;
    default:
      throw new Error(`No region set for stage: ${pulumi.getStack()}`);
  }
}

export function buildIntegrationTag(soclessIntegrationName: string): Tags {
  return {
    integration: soclessIntegrationName,
  };
}

export function pretty(obj: any) {
  JSON.stringify(obj, null, 2);
}

export function dbg(obj: any) {
  console.log(pretty(obj));
}
