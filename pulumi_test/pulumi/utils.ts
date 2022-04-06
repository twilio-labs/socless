import { getCallerIdentity, Tags } from '@pulumi/aws';
import * as pulumi from '@pulumi/pulumi';
import * as aws from '@pulumi/aws';
import { AssertionError } from 'assert';
import { defaultMaxListeners } from 'events';
import { dedupTable } from './dynamodb';

export const accountID = getCallerIdentity().then((result) => result.accountId);
export const PROJECT = pulumi.getProject();
export const STACK = pulumi.getStack();
export const FULL_NAME = `${PROJECT}_${STACK}`;

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

/**
 * registerAutoTags registers a global stack transformation that merges a set
 * of tags with whatever was also explicitly added to the resource definition.
 */
export function registerLambdaDefaults(defaultArgs: aws.lambda.FunctionArgs): void {
  pulumi.runtime.registerStackTransformation((args) => {
    if (args.type === 'aws:lambda/function:Function') {
      const oldProps = args.props as aws.lambda.FunctionArgs;
      const newProps: aws.lambda.FunctionArgs = {
        ...defaultArgs,
        ...oldProps,
        environment: {
          variables: {
            ...(defaultArgs.environment?.variables || {}),
            ...(oldProps.environment?.variables || {}),
          },
        },
        layers: [...new Set([...(defaultArgs.layers || []), ...oldProps.layers])],
      };
      return { props: { ...defaultArgs, ...oldProps }, opts: args.opts };
    }

    return undefined;
  });
}

const test = [...['asdf']];

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

export function newSoclessLambda(
  lambdaNameWithoutIntegration: string,
  args: aws.lambda.FunctionArgs,
  opts?: pulumi.CustomResourceOptions
): {
  [key: string]: aws.lambda.Function;
} {
  let fullName = `${pulumi.getProject().replace('-', '_')}_${lambdaNameWithoutIntegration}`;
  if (lambdaNameWithoutIntegration.startsWith('_')) {
    // private function, don't prepend `socless_<integration_name>`
    fullName = lambdaNameWithoutIntegration;
  }
  return {
    [fullName]: new aws.lambda.Function(fullName, { ...args, name: fullName }, opts),
  };
}

export function pretty(obj: any) {
  JSON.stringify(obj, null, 2);
}

export function dbg(obj: any) {
  console.log(pretty(obj));
}
