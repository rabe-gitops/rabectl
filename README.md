# Infrastructure

[![License](https://img.shields.io/github/license/rabe-gitops/infrastructure)](LICENSE)

Repository containing the CDK files to get started with Rabe GitOps on AWS

### Getting started

1. Make sure you have [Python](https://www.python.org/downloads/), [Node.js](https://nodejs.org/it/download/), the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html), and [Helm](https://helm.sh/docs/intro/install/) installed
Note: as of now, some Helm charts still don't support Helm 3

2. Globally install the CDK CLI:
    ```
    npm install -g cdk
    ```

3. Install the dependencies:
    ```
    pip3 install -r requirements.txt
    ```

4. Deploy the template:
    ```
    cdk deploy
    ```
