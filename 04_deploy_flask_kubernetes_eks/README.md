# Deploying a Flask API

This is the project starter repo for the fourth course in the [Udacity Full Stack Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004): Server Deployment, Containerization, and Testing.

In this project you will containerize and deploy a Flask API to a Kubernetes cluster using Docker, AWS EKS, CodePipeline, and CodeBuild.

The Flask app that will be used for this project consists of a simple API with three endpoints:

- `GET '/'`: This is a simple health check, which returns the response 'Healthy'.
- `POST '/auth'`: This takes a email and password as json arguments and returns a JWT based on a custom secret.
- `GET '/contents'`: This requires a valid JWT, and returns the un-encrpyted contents of that token.

The app relies on a secret set as the environment variable `JWT_SECRET` to produce a JWT. The built-in Flask server is adequate for local development, but not production, so you will be using the production-ready [Gunicorn](https://gunicorn.org/) server when deploying the app.

## Dependencies

- Docker Engine
  - Installation instructions for all OSes can be found [here](https://docs.docker.com/install/).
  - For Mac users, if you have no previous Docker Toolbox installation, you can install Docker Desktop for Mac. If you already have a Docker Toolbox installation, please read [this](https://docs.docker.com/docker-for-mac/docker-toolbox/) before installing.

- AWS Account
  - You can create an AWS account by signing up [here](https://aws.amazon.com/#).

## Project Steps

### 1) Write a Dockerfile for a simple Flask API & Build and test the container locally

Steps to run the API locally using the Flask server (no containerization)
The following steps describe how to run the Flask API locally with the standard Flask server, so that you can test endpoints before you containerize the app:

1. Install python dependencies. These dependencies are kept in a requirements.txt file. To install them, use pip:

    ```bash
    pip install -r requirements.txt
    ```

2. Set up the environment. You do not need to create an env_file to run locally but you do need the following two variables available in your terminal environment. The following environment variable is required:

    **JWT_SECRET** - The secret used to make the JWT, for the purpose of this course the secret can be any string.

    The following environment variable is optional:

    **LOG_LEVEL** - The level of logging. This will default to 'INFO', but when debugging an app locally, you may want to set it to 'DEBUG'. To add these to your terminal environment, run the 2 lines below.

    ```bash
    export JWT_SECRET='myjwtsecret'
    export LOG_LEVEL=DEBUG
    ```

3. Run the app using the Flask server, from the top directory, run:

    ```bash
    python main.py
    ```

4. To try the API endpoints, open a new shell and run the following commands, replacing <EMAIL> and <PASSWORD> with any values:

   - To try the /auth endpoint, use the following command:

       ```bash
       export TOKEN=`curl -d '{"email":"<EMAIL>","password":"<PASSWORD>"}' -H "Content-Type: application/json" -X POST localhost:8080/auth  | jq -r '.token'`
       ```

       This calls the endpoint 'localhost:8080/auth' with the `{"email":"<EMAIL>","password":"<PASSWORD>"}` as the message body. The return value is a JWT token based on the secret you supplied. We are assigning that secret to the environment variable 'TOKEN'. To see the JWT token, run:

       ```bash
       echo $TOKEN
       ```

   - To try the `/contents` endpoint which decrypts the token and returns its content, run:

       ```bash
       curl --request GET 'http://127.0.0.1:8080/contents' -H "Authorization: Bearer ${TOKEN}" | jq .
       ```

You should see the email that you passed in as one of the values.

### 2) Create an EKS cluster

Before you can deploy your application, you will need to create an EKS cluster and set up an IAM role that CodeBuild can use to interact with EKS. You can follow the steps below to do this from the command line.

#### Create a Kubernetes (EKS) Cluster

- Create an EKS cluster named simple-jwt-api.

#### Set Up an IAM Role for the Cluster

The next steps are provided to quickly set up an IAM role for your cluster.

1. Create an IAM role that CodeBuild can use to interact with EKS. :

    - Set an environment variable ACCOUNT_ID to the value of your AWS account id. You can do this with awscli:

        ```bash
        ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
        ```

    - Create a role policy document that allows the actions `"eks:Describe*"` and `"ssm:GetParameters"`. You can do this by setting an environment variable with the role policy:

        ```bash
        TRUST="{ \"Version\": \"2012-10-17\", \"Statement\": [ { \"Effect\": \"Allow\", \"Principal\": { \"AWS\": \"arn:aws:iam::${ACCOUNT_ID}:root\" }, \"Action\": \"sts:AssumeRole\" } ] }"
        ```

    - Create a role named 'UdacityFlaskDeployCBKubectlRole' using the role policy document:

        ```bash
        aws iam create-role --role-name UdacityFlaskDeployCBKubectlRole --assume-role-policy-document "$TRUST" --output text --query 'Role.Arn'
        ```

    - Create a role policy document that also allows the actions `"eks:Describe*"` and `"ssm:GetParameters"`. You can create the document in your tmp directory:

        ```text
        echo '{ "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Action": [ "eks:Describe*", "ssm:GetParameters" ], "Resource": "*" } ] }' > /tmp/iam-role-policy
        ```

    - Attach the policy to the 'UdacityFlaskDeployCBKubectlRole'. You can do this using awscli:

        ```bash
        aws iam put-role-policy --role-name UdacityFlaskDeployCBKubectlRole --policy-name eks-describe --policy-document file:///tmp/iam-role-policy
        ```

        You have now created a role named 'UdacityFlaskDeployCBKubectlRole'

2. Grant the role access to the cluster. The 'aws-auth ConfigMap' is used to grant role based access control to your cluster.

   - Get the current configmap and save it to a file:

        ```bash
        kubectl get -n kube-system configmap/aws-auth -o yaml > /tmp/aws-auth-patch.yml
        ```

   - In the data/mapRoles section of this document add, replacing <ACCOUNT_ID> with your account id:

        ```text
        - rolearn: arn:aws:iam::<ACCOUNT_ID>:role/UdacityFlaskDeployCBKubectlRole
        username: build
        groups:
            - system:masters
        ```

   - Now update your cluster's configmap:

        ```bash
        kubectl patch configmap/aws-auth -n kube-system --patch "$(cat /tmp/aws-auth-patch.yml)"
        ```

### 3) Create a CodePipeline pipeline triggered by GitHub checkins

You will now create a pipeline which watches your Github. When changes are checked in, it will build a new image and deploy it to your cluster.

1. Generate a GitHub access token. A Github acces token will allow CodePipeline to monitor when a repo is changed. A token can be generated [here](https://github.com/settings/tokens/). You should generate the token with full control of private repositories, as shown in the image below. Be sure to save the token somewhere that is secure.

2. The file buildspec.yml instructs CodeBuild. We need a way to pass your jwt secret to the app in kubernetes securly. You will be using AWS Parameter Store to do this. First add the following to your buildspec.yml file:

    ```yaml
    env:
    parameter-store:
        JWT_SECRET: JWT_SECRET
    ```

    This lets CodeBuild know to set an evironment variable based on a value in the parameter-store.

3. Put secret into AWS Parameter Store

    ```bash
    aws ssm put-parameter --name JWT_SECRET --value "YourJWTSecret" --type SecureString
    ```

4. Modify CloudFormation template.

    There is file named ci-cd-codepipeline.cfn.yml, this the the template file you will use to create your CodePipeline pipeline. Open this file and go to the 'Parameters' section. These are parameters that will accept values when you create a stack. Fill in the 'Default' value for the following:

    - EksClusterName : use the name of the EKS cluster you created above
    - GitSourceRepo : use the name of your project's github repo.
    - GitHubUser : use your github user name
    - KubectlRoleName : use the name of the role you created for kubectl above

    Save this file.

5. Create a stack for CodePipeline

    - Go the the CloudFormation service in the aws console.
    - Press the 'Create Stack' button.
    - Choose the 'Upload template to S3' option and upload the template file 'ci-cd-codepipeline.cfn.yml'
    - Press 'Next'. Give the stack a name, fill in your GitHub login and the Github access token generated in step 1.
    - Confirm the cluster name matches your cluster, the 'kubectl IAM role' matches the role you created above, and the repository matches the name of your forked repo.
    - Create the stack.

    You can check it's status in the [CloudFormation console](https://us-east-2.console.aws.amazon.com/cloudformation/).

6. Check the pipeline works. Once the stack is successfully created, commit a change to the master branch of your github repo. Then, in the aws console go to the CodePipeline UI. You should see that the build is running.

7. To test your api endpoints, get the external ip for your service:

    ```bash
    kubectl get services simple-jwt-api -o wide
    ```

    Now use the external ip url to test the app:

    ```bash
    export TOKEN=`curl -d '{"email":"<EMAIL>","password":"<PASSWORD>"}' -H "Content-Type: application/json" -X POST <EXTERNAL-IP URL>/auth  | jq -r '.token'`
    curl --request GET '<EXTERNAL-IP URL>/contents' -H "Authorization: Bearer ${TOKEN}" | jq
    ```

8. Save the external IP from above to provide to the reviewer when you submit your project.

### 4) Create a CodeBuild stage which will build, test, and deploy your code

The final part of this project involves adding tests to your deployment. You can follow the steps below to accomplish this.

1. Add running tests as part of the build.

    To require the unit tests to pass before our build will deploy new code to your cluster, you will add the tests to the build stage. Remember you installed the requirements and ran the unit tests locally at the beginning of this project. You will add the same commands to the buildspec.yml:

    - Open buildspec.yml
    - In the prebuild section, add a line to install the requirements and a line to run the tests. You may need to refer to 'pip' as 'pip3' and 'python' as 'python3'
    - Save the file

2. You can check the tests prevent a bad deployment by breaking the tests on purpose:

    - Open the test_main.py file
    - Add assert False to any of the tests
    - Commit your code and push it to Github
    - Check that the build fails in CodePipeline

For more detail about each of these steps, see the project lesson [here](https://classroom.udacity.com/nanodegrees/nd004/parts/1d842ebf-5b10-4749-9e5e-ef28fe98f173/modules/ac13842f-c841-4c1a-b284-b47899f4613d/lessons/becb2dac-c108-4143-8f6c-11b30413e28d/concepts/092cdb35-28f7-4145-b6e6-6278b8dd7527).
