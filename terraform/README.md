# Terraform infrastructure

The original EKS lab used Terraform in AWS region `ap-south-1` and created the VPC/networking, EKS cluster, managed node group, IAM resources, and ECR repository. The cluster name used was `devops-eks-cluster`.

**The original Terraform source files are not currently present in this repository.** The infrastructure was destroyed after testing, so this repository cannot recreate it yet.

To make the infrastructure reproducible, restore the exact Terraform files from your local lab folder, review them, and commit only the source files. Do not commit:

- `terraform.tfstate` or backup state files
- `.terraform/`
- real `terraform.tfvars` values
- AWS credentials, access keys, private keys, or kubeconfig files

Use a `terraform.tfvars.example` with non-secret example values if variables are needed. Run `terraform fmt`, `terraform validate`, and `terraform plan` before applying. Applying EKS infrastructure can incur AWS charges.
