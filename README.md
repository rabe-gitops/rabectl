# rabectl

[![License](https://img.shields.io/github/license/rabe-gitops/rabectl)](LICENSE)

Repository containing the Rabe GitOps CLI (rabectl) source code

### Getting started

1. Before getting started, make sure you have installed in your system:
    * [Python 3](https://www.python.org/downloads/)
    * [Git](https://git-scm.com/downloads/)
    * [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
    * [Terraform](https://www.terraform.io/downloads.html)
    * [Helm](https://helm.sh/docs/intro/install/)

    Note: as of now, some Helm charts still don't support Helm 3, but only Helm 2

2. Install the rabectl CLI from the source code:
    ```
    git clone https://github.com/rabe-gitops/rabectl.git
    cd rabectl
    python3 setup.py install
    ```

