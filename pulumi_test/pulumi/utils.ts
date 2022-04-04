import { getCallerIdentity, Tags } from '@pulumi/aws';
import * as pulumi from '@pulumi/pulumi';
import { AssertionError } from 'assert';

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

export const soclessEnvs = ['dev', 'stage', 'prod', 'sandbox'] as const;

export type SoclessEnv = typeof soclessEnvs[number];

export function assertStackIsSoclessEnv(stackString: string): asserts stackString is SoclessEnv {
  if (!soclessEnvs.includes(stackString as SoclessEnv)) {
    throw new AssertionError({
      message: `value: '${stackString}' is not a soclessEnv (${pretty(soclessEnvs)})`,
    });
  }
}

export function convertEnvToRegion(envString: SoclessEnv) {
  assertStackIsSoclessEnv(envString);
  switch (envString) {
    case 'dev':
      return 'us-west-2';
    case 'stage':
      return 'us-east-2';
    case 'prod':
      return 'us-east-1';
    case 'sandbox':
      return 'us-west-1';
  }
}

export function stackToRegion() {
  const stack = pulumi.getStack().toLowerCase();
  return convertEnvToRegion(stack as SoclessEnv);
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
