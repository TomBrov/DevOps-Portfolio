pipeline {
    agent any
    parameters {
      booleanParam defaultValue: false, name: 'deploy'
    }
    stages {
        stage ('ENV Prep') {
            steps {
                script{
                    deleteDir()
                    git branch: env.GIT_BRANCH, credentialsId: 'github', url: 'git@github.com:TomBrov/portfolio.git'
                }
            }
        }
        stage ('Build') {
            steps {
                sh '''cd application
                docker build -t gcr.io/testing-env-352509/testing/backend:latest .
                docker push gcr.io/testing-env-352509/testing/backend:latest
                cd ..
                zip -r test_env/app.zip application/'''
            }
        }
        stage ('Test') {
            steps{
                script{
                   env.bool = 'test'
                   sh '''cd test_env
                        terraform init
                        terraform apply --auto-approve
                        IP=$(terraform output IP | tr "\\"" ":" | cut -d ":" -f2)
                        INSTANCE=$(terraform output instance_name | tr "\\"" ":" | cut -d ":" -f2)
                        until gcloud compute ssh --strict-host-key-checking=no ubuntu@$INSTANCE --command="bash -c \\"docker-compose --version\\""; do sleep 5; done
                        gcloud compute scp --strict-host-key-checking=no app.zip ubuntu@$INSTANCE:~/app.zip
                        gcloud compute ssh --strict-host-key-checking=no ubuntu@$INSTANCE --command="bash -c \\"unzip app.zip && cd application &&docker-compose up -d\\""
                        until curl $IP; do sleep 5; done
                        python3 E2E.py $IP
                        terraform destroy --auto-approve
                        cd ..'''
                }
            }
        }
        stage ('Tag') {
            when{
                expression{env.GIT_BRANCH ==~ "master"}
            }
            steps {
                sh '''docker tag gcr.io/testing-env-352509/testing/backend:latest gcr.io/testing-env-352509/production/backend:latest
                      docker push gcr.io/testing-env-352509/production/backend:latest'''
            }
        }
        stage ('Deploy') {
            when{
                expression{env.GIT_BRANCH ==~ "master"}
            }
            steps {
                script{
                    env.bool = 'deploy'
                    if (param.deployed ==~ true){
                        sh '''cd deploy
                              terraform init
                              terraform apply --auto-approve
                              REGION=$(terraform output region | tr "\\"" ":" | cut -d ":" -f2)
                              INSTANCE_NAME=$(terraform output instance_name | tr "\\"" ":" | cut -d ":" -f2)
                              gcloud container clusters get-credentials $INSTANCE_NAME --region $REGION'''
                    } else {
                        sh '''cd deploy
                              REGION=$(cat variables.tf | head -8 | tail -1 | tr "\\"" ":" | cut -d ":" -f2)
                              INSTANCE_NAME=$(cat variables.tf | head -3 | tail -1 | tr "\\"" ":" | cut -d ":" -f2)
                              gcloud container clusters get-credentials $INSTANCE_NAME --region $REGION'''
                    }

                }
            }
        }
    }
    post{
        failure{
            script{
                if(env.bool ==~ 'test'){
                    sh '''cd test_env && terraform destroy --auto-approve'''
                } else if(env.bool ==~ 'deploy'){
                    sh '''cd deploy && terraform destroy --auto-approve'''
                }
            }
        }
        success{
            sh '''echo yes'''
        }
    }
}