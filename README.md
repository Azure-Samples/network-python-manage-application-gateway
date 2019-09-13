---
page_type: sample
languages:
- python
products:
- azure
description: "Getting Started with Application Gateway in Python"
urlFragment: network-python-manage-application-gateway
---

# Getting Started with Application Gateway in Python

**On this page**

- [Run this sample](#run)
- [More information](#more-info)

<a name="run"></a>
## Run this sample

1. If you don't already have it, [install Python](https://www.python.org/downloads/).

2. Set up a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to run this example. You can initialize a virtual environment this way:

    ```
    pip install virtualenv
    virtualenv mytestenv
    cd mytestenv
    source bin/activate
    ```

3. Clone the repository.

    ```
    git clone https://github.com/Azure-Samples/network-python-manager-application-gateway.git
    ```

4. Install the dependencies using pip.

    ```
    cd network-python-manager-application-gateway
    pip install -r requirements.txt
    ```

5. Create an Azure service principal, using
[Azure CLI](https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli?toc=%2fazure%2fazure-resource-manager%2ftoc.json),
[PowerShell](http://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal/)
or [Azure Portal](http://azure.microsoft.com/documentation/articles/resource-group-create-service-principal-portal/).

6. Export these environment variables into your current shell.

    ```
    export AZURE_TENANT_ID={your tenant id}
    export AZURE_CLIENT_ID={your client id}
    export AZURE_CLIENT_SECRET={your client secret}
    export AZURE_SUBSCRIPTION_ID={your subscription id}
    ```

7. Run the sample.

    ```
    python example.py
    ```

<a name="more-info"></a>
## More information

- [Azure SDK for Python](http://github.com/Azure/azure-sdk-for-python)


# Contributing

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
