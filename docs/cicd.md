# CICD
Deployment from source code

## CICD resources

- **Github repository**: [gic-de-transactions](https://github.com/taylorhickem/gic-de-transactions) source code storage
- **Github Actions**: deployment engine
- **AWS CloudFormation**: IaC templates for managing cloud infrastructure on AWS

## repository layout
the repository files are organized in the following structure

/root
```
.github/
  workflows/            # github deploy actions
     ...
aws/                    # specifications for AWS infrastructure
  cloudformation/       # cloudformation templates
    ...
docs/                   # app documentation
  ...
.gitignore
AGENTS.md               # instructions for Developer AI assistants
LICENSE
LOGS.md                 # session logs
mkdocs.yml              # MKDocs template
requirements.txt
VERSION
```

__excluded__
files and directories excluded from the source code from `.gitignore`

.gitignore
```
env
site
.env
.pytest_cache*
s3-gic-transactions*           # local copy of the contents of the S3 directory
```

## S3 bucket layout

S3 bucket: `gic-transactions`
```
config/*
```

## Github Actions

__secrets__
secrets used by Github Actions runner to authenticate to AWS

| id | variable | value | description |
| - | - | - | - |
| 01 | AWS_ACCESS_KEY_ID | **** | AWS admin credential |
| 02 | AWS_SECRET_ACCESS_KEY | **** | AWS admin credential |

__environment variables__
environment variables used by Github Actions runner

| id | variable | value | description |
| - | - | - | - |
| 01 | AWS_REGION | ap-southeast-1 | AWS region |


## AWS Infrastructure
The AWS infrastructure is organized into layered CloudFormation stacks, segregated by function and coupled through the repository via parameters and configuration files.

__CloudFormation (CF) stacks__
CloudFormation stack layers

| id | stack | purpose | resources |
| - | - | - | - |
| 01 | gic-transactions | * |

__AWS CLI__
Additional resources created outside of the cloudformation stack either manually from local PC or via Github actions. 

These resources must be deleted in a separate cleanup workflow.

_manual setup resources_

| id | resource | executor | sequence |
| - | - | - | - |
| 01 | S3 bucket | Github Action | initial setup |

## CF Stack deploy
The stack deploy performed by GHA runner includes

 - **parameters** read-in/export to S3
 - **idempotent deploy** checks if the target stack is already in state `ROLLBACK_COMPLETE` or `CREATE_FAIL`
  - deletes the stack and then triggers a re-deploy
 - **fail diagnostics** captures diagnostic logs for stack deploy fail and prints out in the runner logs

The stack deploy AWS CLI command includes these standard arguments:

| argument | description |
| - | - |
| `--template-file` | Path to the rendered CFN template the runner will submit. Typically `${CF_TEMPLATE_DIR}/${STACK_TEMPLATE_FILE}`. |
| `--stack-name` | Logical name of the stack to create/update. Used for change sets, events, and cross-stack exports. |
| `--capabilities` | Required when your template creates/updates IAM resources. `CAPABILITY_NAMED_IAM` confirms you understand IAM changes with explicit names. |
| `--no-fail-on-empty-changeset` | Makes updates idempotent: if the template/params/tags don’t change, CFN returns an empty change set and the CLI exits **successfully** instead of erroring. |
| `--parameter-overrides` | Inline key=value pairs that bind to your template’s `Parameters`. Values here take precedence over any defaults in the template. |
| `--tags` | Key=value pairs to tag the **stack** (and, for many resource types, the resources). Useful for ownership, cost allocation, and environment scoping. |

 ```bash
aws cloudformation deploy \
--template-file $CF_TEMPLATE_DIR/$STACK_TEMPLATE_FILE \
--stack-name $STACK_NAME \
--capabilities CAPABILITY_NAMED_IAM \
--no-fail-on-empty-changeset \
--parameter-overrides \
  ...
--tags \
  role=$ROLE \
  project=$PROJECT_NAME

 ```

## Github Action Workflows

| id | workflow | app feature | description |
| - | - | - | - |
| 01 | cf stack | deploy stack | * |
