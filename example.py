import os
from haikunator import Haikunator
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient

LOCATION = 'westus'
GROUP_NAME = 'AdatumAppGateway'
VNET_NAME = 'AdatumAppGatewayVNET'
SUBNET_NAME = 'Appgatewaysubnet'
APPLICATION_GATEWAY_NAME = 'AdatumAppGateway'

# Manage Application Gateway
#
# This script expects that the following environment vars are set:
#
# AZURE_TENANT_ID: with your Azure Active Directory tenant id or domain
# AZURE_CLIENT_ID: with your Azure Active Directory Application Client ID
# AZURE_CLIENT_SECRET: with your Azure Active Directory Application Secret
# AZURE_SUBSCRIPTION_ID: with your Azure Subscription Id
#
def run_example():
    """Application Gateway example."""
    #
    # Create the Resource Manager Client with an Application (service principal) token provider
    #
    subscription_id = os.environ.get(
        'AZURE_SUBSCRIPTION_ID',
        '11111111-1111-1111-1111-111111111111') # your Azure Subscription Id
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    resource_client = ResourceManagementClient(credentials, subscription_id)
    network_client = NetworkManagementClient(credentials, subscription_id)

    # You MIGHT need to add Network as a valid provider for these credentials
    # If so, this operation has to be done only once for each credentials
    resource_client.providers.register('Microsoft.Network')

    # Create Resource group
    print('Create Resource Group')
    resource_group_params = {'location':LOCATION}
    resource_group = resource_client.resource_groups.create_or_update(GROUP_NAME, resource_group_params)
    print_item(resource_group)

    # Create VNet
    print('\nCreate Vnet')
    async_vnet_creation = network_client.virtual_networks.create_or_update(
        GROUP_NAME,
        VNET_NAME,
        {
            'location': LOCATION,
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
    )
    async_vnet_creation.wait()

    # Create Subnet
    print('\nCreate Subnet')
    async_subnet_creation = network_client.subnets.create_or_update(
        GROUP_NAME,
        VNET_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.0.0.0/28'}
    )
    subnet_info = async_subnet_creation.result()

    # Create Application Gateway
    print('\nCreate Application Gateway')
    appgateway_id = resource_group.id + '/providers/Microsoft.Network/applicationGateways/' + APPLICATION_GATEWAY_NAME
    appgateway_frontip_name = "appGatewayFrontendIP"
    appgateway_frontport_name = "appGatewayFrontendPort"
    appgateway_http_listener_name = "appGatewayHttpListener"
    appgateway_backend_pool_name = "appGatewayBackendPool"
    appgateway_httpsettings_name = "appGatewayBackendHttpSettings"
    async_ag_creation = network_client.application_gateways.create_or_update(
        GROUP_NAME,
        APPLICATION_GATEWAY_NAME,
        {
            'location': LOCATION,
            "sku": {
                "name": "Standard_Small",
                "tier": "Standard",
                "capacity": 2
            },
            "gateway_ip_configurations": [{
                "name": "appGatewayIpConfig",
                "subnet": {
                    "id": subnet_info.id
                }
            }],
            "frontend_ip_configurations": [{
                "name": appgateway_frontip_name,
                "subnet": {
                    "id": subnet_info.id
                }
            }],
            "frontend_ports": [{
                "name": appgateway_frontport_name,
                "port": 90
            }],
            "backend_address_pools": [{
                "name": appgateway_backend_pool_name,
                "backend_addresses": [{
                    "ip_address": "10.0.0.4"
                }, {
                    "ip_address": "10.0.0.5"
                }]
            }],
            "backend_http_settings_collection": [{
                "name": appgateway_httpsettings_name,
                "port": 80,
                "protocol": "Http",
                "cookie_based_affinity": "Enabled"
            }],
            "http_listeners": [{
                "name": appgateway_http_listener_name,
                "frontend_ip_configuration": {
                    "id": appgateway_id + "/frontendIPConfigurations/" + appgateway_frontip_name
                },
                "frontend_port": {
                    "id": appgateway_id + '/frontendPorts/' + appgateway_frontport_name
                },
                "protocol": "Http",
                "ssl_certificate": None
            }],
            "request_routing_rules": [{
                "name": "rule1",
                "rule_type": "Basic",
                "http_listener": {
                    "id": appgateway_id + '/httpListeners/' + appgateway_http_listener_name
                },
                "backend_address_pool": {
                    "id": appgateway_id + '/backendAddressPools/' + appgateway_backend_pool_name
                },
                "backend_http_settings": {
                    "id": appgateway_id + '/backendHttpSettingsCollection/' + appgateway_httpsettings_name
                }
            }]
        }
    )
    application_gateway = async_ag_creation.result()
    print_item(application_gateway)

    # Delete Resource group and everything in it
    print('Delete Resource Group')
    delete_async_operation = resource_client.resource_groups.delete(GROUP_NAME)
    delete_async_operation.wait()
    print("Deleted: {}".format(GROUP_NAME))
    print("\n\n")


def print_item(group):
    """Print an Azure object instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    print("\tLocation: {}".format(group.location))
    print("\tTags: {}".format(group.tags))
    if hasattr(group, 'properties'):
        print_properties(group.properties)

def print_properties(props):
    """Print a ResourceGroup properties instance."""
    if props and props.provisioning_state:
        print("\tProperties:")
        print("\t\tProvisioning State: {}".format(props.provisioning_state))
    print("\n\n")

if __name__ == "__main__":
    run_example()
