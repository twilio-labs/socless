import * as pulumi from '@pulumi/pulumi';
import * as aws from '@pulumi/aws';
import * as awsx from '@pulumi/awsx';
import { FULL_NAME } from './helpers';

const soclessVPC = new aws.ec2.Vpc(`${FULL_NAME}-vpc`, {
  cidrBlock: '10.1.0.0/16',
  enableDnsSupport: true,
  enableDnsHostnames: false,
  instanceTenancy: 'default',
  tags: {
    Name: 'Socless',
  },
});

const soclessEIP = new aws.ec2.Eip(`${FULL_NAME}-eip`, {
  vpc: true,
});

const soclessInternetGateway = new aws.ec2.InternetGateway(`${FULL_NAME}-internetgateway`, {
  tags: {
    Name: 'Socless Internet Gateway',
  },
});

const soclessInternetGatewayAttachment = new aws.ec2.InternetGatewayAttachment(
  `${FULL_NAME}-ig-attachment`,
  {
    internetGatewayId: soclessInternetGateway.id,
    vpcId: soclessVPC.id,
  }
);

const soclessPublicSubnet = new aws.ec2.Subnet(`${FULL_NAME}-publicsubnet`, {
  cidrBlock: '10.1.0.0/22',
  mapPublicIpOnLaunch: false,
  vpcId: soclessVPC.id,
  tags: {
    Name: 'Socless Public Subnet',
  },
});

const soclessNat = new aws.ec2.NatGateway(`${FULL_NAME}-natgateway`, {
  allocationId: soclessEIP.id,
  subnetId: soclessPublicSubnet.id,
});

// const soclessPrivateFunctionRouteTableAssociation = new aws.ec2.RouteTableAssociation(`${FULL_NAME}-privatefunctionRouteTableAssociation`, {
//   routeTableId: routetable
// });

const soclessPrivateFunctionRouteTable = new aws.ec2.RouteTable(
  `${FULL_NAME}-privatefunctionRouteTable`,
  {
    vpcId: soclessVPC.id,
    tags: {
      Name: 'Socless Private Function RouteTable',
    },
  }
);

const soclessPrivateFunctionSubnet = new aws.ec2.Subnet(`${FULL_NAME}-privatefunctionsubnet`, {
  cidrBlock: '10.1.4.0/22',
  mapPublicIpOnLaunch: false,
  vpcId: soclessVPC.id,
  tags: {
    Name: 'Socless Private Function Subnet',
  },
});

const soclessPrivateServicesSubnet = new aws.ec2.Subnet(`${FULL_NAME}-privateservicessubnet`, {
  cidrBlock: '10.1.8.0/22',
  mapPublicIpOnLaunch: false,
  vpcId: soclessVPC.id,
  tags: {
    Name: 'Socless Private Services Subnet',
  },
});

// VPC Configurations
export const vpcConfig = {
  vpc: soclessVPC,
  eip: soclessEIP,
  publicSubnet: soclessPublicSubnet,
  privateFunctionSubnet: soclessPrivateFunctionSubnet,
  gatewayAttachment: new aws.ec2.VpnGatewayAttachment(`${FULL_NAME}-internetgateway`, {
    vpcId: soclessVPC.id,
    vpnGatewayId: soclessInternetGateway.id,
  }),
};
