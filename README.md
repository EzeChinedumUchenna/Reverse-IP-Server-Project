# CI/CD Pipeline with Jenkins, SonarQube, Docker, ArgoCD, Azure container registry, gmail, Helm and Azure Kubernetes Service (AKS)

This repository explains a comprehensive Continuous Integration/Continuous Deployment (CI/CD) pipeline using Jenkins, SonarQube, Docker, Azure Container Registry, Argo CD, and Kubernetes. Below is a detailed explanation of each step in the workflow, accompanied by a visual diagram.

## Workflow Overview
The CI/CD pipeline in this repository automates the building, testing, and deploying of applications. Code changes in GitHub trigger SonarQube to check for vulnerabilities and bugs, stopping the build if any are found. If the code passes, Jenkins builds the artifact and pushes it to Azure Container Registry (ACR). Jenkins then updates a separate GitHub repository (https://github.com/EzeChinedumUchenna/Reverse-IP-Server-CD-Project) with the Kubernetes Helm chart for continuous delivery. Argo CD monitors this repository for changes, synchronizes the Kubernetes cluster to match the desired state, and manages continuous deployment. The Kubernetes cluster runs the workload, and Gmail Notification sends alert about the pipeline's success or failure to "ezechinedum504@gmail.com"

![image](https://github.com/EzeChinedumUchenna/Reverse-IP-Server-Project/assets/102483586/a1814db9-95c5-4683-a0c2-867061c42866)


## Pipeline Steps
* __GitHub:__ Acts as the source control repository. Code changes are pushed to GitHub, which triggers the Jenkins build process.
* __Jenkins:__ Serves as the Continuous Integration server. It pulls the latest code from GitHub, runs unit tests to ensure code integrity, initiates a code quality analysis using SonarQube. If the code passes the quality checks, builds a Docker image.
* __SonarQube:__ Performs static code analysis. Analyzes the code for quality, bugs, vulnerabilities, and code smells. Sends the results back to Jenkins.
* __Docker:__ Containerizes the application. Jenkins builds a Docker image from the codebase.
*__Docker Hub:__ Stores Docker images. The Docker image is pushed to the Azure Container Registry for versioning and storage.
*__Argo CD:__ Argo CD continuously monitors the Git repository for changes to application manifests (Kubernetes YAML files, Helm charts, Kustomize configurations, etc.). When changes are detected, Argo CD automatically synchronizes the state of the Kubernetes cluster to match the desired state defined in the Git repository. It will then manage the continuous deployment. Automates the deployment of the applications to Kubernetes clusters, ensuring that application deployments are consistent, repeatable, and auditable and deploys it to the Kubernetes cluster.

![image](https://github.com/EzeChinedumUchenna/Reverse-IP-Server-Project/assets/102483586/b470f7be-017d-4b19-8882-b9f2db16ebf7)


* __Kubernetes:__ Orchestrates containerized applications. Runs the deployed Docker image, ensuring the application is up and running. Monitors the health and scaling of the application. The application can be accessed via the Kubernetes service as a Load balancer

![image](https://github.com/EzeChinedumUchenna/http-echo-project/assets/102483586/93072e54-3b47-495e-a223-0591b6986e30)


* __Email Notification:__ Alerts stakeholders. Sends notifications about the deployment status. See below
![Uploading image.png…]()




## Conclusion
This CI/CD pipeline streamlines the development process by automating code integration, testing, and deployment. By incorporating tools like Jenkins, SonarQube, Docker, Azure Container Registry, Argo CD, and Kubernetes, we ensure high-quality code and efficient application deployment. For the configuration and integration see COMMAND file in this repo

__NEXT:__ To integrate a monitoring systems to oversee workload metrics and application availability. Failure to do so may result in unaddressed risks to operational stability and performance.



