from aws_cdk import Stack
from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_rds as rds,
    aws_ecs_patterns as ecs_patterns,
)


class FastAPIStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            id="VPC",
            cidr="10.0.0.0/16",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", cidr_mask=24,
                    reserved=False, subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(
                    name="private", cidr_mask=24,
                    reserved=False, subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                ec2.SubnetConfiguration(
                    name="DB", cidr_mask=24,
                    reserved=False, subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
                )
            ],
        )

        self.rds_security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                                    vpc=self.vpc,
                                                    description="Allow ssh access to RDS",
                                                    allow_all_outbound=True
                                                    )

        self.rds_security_group.add_ingress_rule(
            ec2.Peer.ipv4('10.0.0.0/16'),
            ec2.Port.tcp(5432)
        )

        subnet_ids = []
        for subnet in self.vpc.isolated_subnets:
            subnet_ids.append(subnet.subnet_id)

        self.rds = rds.CfnDBCluster(self, 'DBCluster',
                                    engine_mode='serverless',
                                    engine='aurora-postgresql',
                                    engine_version='11.9',
                                    port=5432,
                                    database_name='dev_database',
                                    master_username='deuser',
                                    master_user_password='depasswd',
                                    db_subnet_group_name=rds.CfnDBSubnetGroup(self, 'AuroraSubnetGroup',
                                                                              db_subnet_group_description='subnet group to access rds',
                                                                              db_subnet_group_name='aurora-subnet-group',
                                                                              subnet_ids=subnet_ids
                                                                              ).db_subnet_group_name,
                                    scaling_configuration=rds.CfnDBCluster.ScalingConfigurationProperty(
                                        auto_pause=True,
                                        max_capacity=2,
                                        min_capacity=2,
                                        seconds_until_auto_pause=3600
                                    ),
                                    vpc_security_group_ids=[self.rds_security_group.security_group_id]
                                    )

        self.ecs_cluster = ecs.Cluster(
            self,
            "ECSCluster",
            vpc=self.vpc,
        )

        self.ecs_cluster.node.add_dependency(self.rds)

        self.ecs_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "FastAPIService",
            cluster=self.ecs_cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=2,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("public.ecr.aws/h6v8e9c5/data-app:latest"),
                environment={
                    'USER_NAME': 'deuser',
                    'PASSWORD': 'depasswd',
                    'HOST': self.rds.attr_endpoint_address,
                    'DATABASE': 'dev_database'
                }
            )
        )

        self.ecs_service.node.add_dependency(self.ecs_cluster)
