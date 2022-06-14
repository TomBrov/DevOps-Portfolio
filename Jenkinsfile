pipeline {
    agent any
    environment{
        emailAddress = ''
    }
    stages {
        stage ('ENV Prep') {
            steps {
                script{
                    deleteDir()
                    git branch: env.GIT_BRANCH, credentialsId: 'github', url: 'git@github.com:TomBrov/portfolio.git'
                    if (env.GIT_BRANCH ==~ 'master'){
                    env.RELEASE_TAG = sh (script: """git log --format="medium" -1 ${GIT_COMMIT} | tail -1 | cut -d "v" -f2""", returnStdout:true).trim()
                    sh """echo ${env.RELEASE_TAG}"""
                    env.HOTFIX = sh (script: """git tag  | grep ${RELEASE_TAG}.* | wc -l""", returnStdout:true).trim()
                    sh """echo ${env.HOTFIX}"""
                    }
                    env.emailAddress = sh(script: """git log | head -4 | grep Author | cut -d '<' -f2 | cut -d '>' -f1""", returnStdout:true).trim()
                    sh """echo ${env.emailAddress}"""
                }
            }
        }
        stage ('Build') {
            steps {
                script{
                    if (env.GIT_BRANCH ==~ 'master'){
                        sh '''cd application
                        docker build -t gcr.io/testing-env-352509/testing/backend:latest .
                        docker push gcr.io/testing-env-352509/testing/backend:latest
                        cd ..
                        zip -r test_env/app.zip application/'''
                    } else {
                        sh '''cd application
                        docker build -t gcr.io/testing-env-352509/$env.GIT_BRANCH/backend:latest .
                        docker push gcr.io/testing-env-352509/$env.GIT_BRANCH/backend:latest
                        sed -i "s/testing/$env.GIT_BRANCH/" application/docker-compose.yaml
                        cd ..
                        zip -r test_env/app.zip application/'''
                    }

                }

            }
        }
        stage ('Test') {
            steps{
                script{
                   env.stage = 'test'
                   sh '''cd test_env
                        terraform init
                        terraform apply --auto-approve
                        IP=$(terraform output IP | tr "\\"" ":" | cut -d ":" -f2)
                        INSTANCE=$(terraform output instance_name | tr "\\"" ":" | cut -d ":" -f2)
                        until gcloud compute ssh --strict-host-key-checking=no ubuntu@$INSTANCE --command="bash -c \\"docker-compose --version\\""; do sleep 5; done
                        gcloud compute scp --strict-host-key-checking=no app.zip ubuntu@$INSTANCE:~/app.zip
                        gcloud compute ssh --strict-host-key-checking=no ubuntu@$INSTANCE --command="bash -c \\"unzip app.zip && cd application && docker-compose up -d\\""
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
                script{
                    env.stage = 'tag'
                    withCredentials([usernamePassword(credentialsId: 'GithubHTTP', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
                        sh """docker tag gcr.io/testing-env-352509/testing/backend:latest gcr.io/testing-env-352509/production/backend:${env.RELEASE_TAG}.${env.HOTFIX}
                              docker push gcr.io/testing-env-352509/production/backend:${env.RELEASE_TAG}.${env.HOTFIX}
                              git tag ${env.RELEASE_TAG}.${env.HOTFIX}
                              git push --tags https://${USERNAME}:${PASSWORD}@github.com/TomBrov/portfolio.git"""
                    }
                }
            }
        }
        stage ('Deploy') {
            when{
                expression{env.GIT_BRANCH ==~ "master"}
            }
            steps {
                script{
                    env.stage = 'deploy'
                    withCredentials([usernamePassword(credentialsId: 'GithubHTTP', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
                        sh '''sed -i "s/tag: latest/tag: \\$RELEASE_TAG.\\$HOTFIX/g" phonebook/values.yaml
                              git commit -am \\"v${env.RELEASE_TAG}.${env.HOTFIX}\\"
                              git push -u https://$USERNAME:$PASSWORD@github.com/TomBrov/portfolioGitops.git'''
                    }
                }
            }
        }
    }
    post{
        failure{
            script{
                if (env.stage ==~ 'test'){
                    sh '''cd test_env && terraform destroy --auto-approve'''
                }
                mail body: "failure", charset: 'UTF-8', mimeType: 'text/html', subject: "CI Failed", to: "${emailAddress}"
            }
        }
        success {
            mail body: "success", charset: 'UTF-8', mimeType: 'text/html', subject: "success CI", to: "${emailAddress}"
        }
    }
}