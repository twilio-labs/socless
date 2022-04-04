import * as pulumi from '@pulumi/pulumi';
import * as aws from '@pulumi/aws';
import { FULL_NAME } from './utils';

const soclessVPC = new aws.ec2.Vpc(`${FULL_NAME}-vpc`, {
  cidrBlock: '10.1.0.0/16',
  enableDnsSupport: true,
  enableDnsHostnames: false,
  instanceTenancy: 'default',
  tags: {
    Name: 'Socless',
  },
});

// Security Groups
export const soclessLambdaVpcSG = new aws.ec2.SecurityGroup(`${FULL_NAME}-securitygroup`, {
  description: 'SG for Lambda functions in Socless VPC',
  vpcId: soclessVPC.id,
  tags: {
    Name: 'Socless Lambda SG',
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

const soclessPrivateFunctionSubnet = new aws.ec2.Subnet(`${FULL_NAME}-privatefunctionsubnet`, {
  cidrBlock: '10.1.4.0/22',
  mapPublicIpOnLaunch: false,
  vpcId: soclessVPC.id,
  tags: {
    Name: 'Socless Private Function Subnet',
  },
});

const soclessPrivateFunctionRouteTable = new aws.ec2.RouteTable(
  `${FULL_NAME}-privatefunctionRouteTable`,
  {
    vpcId: soclessVPC.id,
    tags: {
      Name: 'Socless Private Function RouteTable',
    },
  }
);

const soclessPrivateFunctionRouteTableAssociation = new aws.ec2.RouteTableAssociation(
  `${FULL_NAME}-privatefunctionRouteTableAssociation`,
  {
    routeTableId: soclessPrivateFunctionRouteTable.id,
    subnetId: soclessPrivateFunctionSubnet.id,
  }
);

const soclessPrivateServicesSubnet = new aws.ec2.Subnet(`${FULL_NAME}-privateservicessubnet`, {
  cidrBlock: '10.1.8.0/22',
  mapPublicIpOnLaunch: false,
  vpcId: soclessVPC.id,
  tags: {
    Name: 'Socless Private Services Subnet',
  },
});

const soclessPrivateServicesRouteTable = new aws.ec2.RouteTable(
  `${FULL_NAME}-privateservicesRouteTable`,
  {
    vpcId: soclessVPC.id,
    tags: {
      Name: 'Socless Private Services RouteTable',
    },
  }
);

const soclessPrivateServicesRouteTableAssociation = new aws.ec2.RouteTableAssociation(
  `${FULL_NAME}-privateServicesRouteTableAssociation`,
  {
    routeTableId: soclessPrivateServicesRouteTable.id,
    subnetId: soclessPrivateServicesSubnet.id,
  }
);

const soclessPublicRouteTable = new aws.ec2.RouteTable(`${FULL_NAME}-PublicRouteTable`, {
  vpcId: soclessVPC.id,
  tags: {
    Name: 'Socless Public RouteTable',
  },
});

const soclessPublicRouteTableAssociation = new aws.ec2.RouteTableAssociation(
  `${FULL_NAME}-PublicRouteTableAssociation`,
  {
    routeTableId: soclessPublicRouteTable.id,
    subnetId: soclessPublicSubnet.id,
  }
);

const soclessPublicRoute = new aws.ec2.Route(`${FULL_NAME}-PublicRoute`, {
  routeTableId: soclessPublicRouteTable.id,
  destinationCidrBlock: '0.0.0.0/0',
  gatewayId: soclessInternetGateway.id,
});

const soclessPrivateFunctionRoute = new aws.ec2.Route(`${FULL_NAME}-PrivateFunctionRoute`, {
  routeTableId: soclessPrivateFunctionRouteTable.id,
  destinationCidrBlock: '0.0.0.0/0',
  natGatewayId: soclessNat.id,
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
