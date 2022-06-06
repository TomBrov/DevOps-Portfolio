pipeline {
    agent any
    stages {
        stage ('ENV Prep') {
            steps {
                script{
                    deleteDir()
                    git branch: env.GIT_BRANCH, credentialsId: 'gitlab', url: 'git@github.com:TomBrov/portfolio.git'
                    env.RELEASE_NOTES = sh(script: """git log --format="medium" -1 ${GIT_COMMIT} | tail -1""", returnStdout:true).trim()
                }
            }
        }
        stage ('Build') {
            steps {
                sh '''cd application
                docker build -t <gcr_repo> .
                cd ..
                zip -r test_env/app.zip application/''
            }
        }
        stage ('Test') {
            steps{
                script{
                    withCredentials([sshUserPrivateKey(credentialsId: 'AWS_ireland', keyFileVariable: 'SSH_KEY', usernameVariable: 'USERNAME')]) {
                       sh '''cd test_env
                            terraform init
                            terraform apply --auto-approve
                            IP=$(terraform output IP | tr "\\"" ":" | cut -d ":" -f2)
                            cd ..
                            until ssh -o StrictHostKeyChecking=no -tt -i $SSH_KEY $USERNAME@$IP "bash -c \\"docker --version\\""; do sleep 5; done
                            until ssh -o StrictHostKeyChecking=no -tt -i $SSH_KEY $USERNAME@$IP "bash -c \\"docker-compose --version\\""; do sleep 5; done
                            scp -o StrictHostKeyChecking=no -v -i $SSH_KEY -p app.zip $USERNAME@$IP:~/app.zip
                            ssh -o StrictHostKeyChecking=no -tt -i $SSH_KEY $USERNAME@$IP "bash -c \\"unzip app.zip && docker-compose up -d\\""
                            ./E2E.sh $IP
                            terraform destroy --auto-approve'''
                    }
                }
            }
        }
        stage ('Push Image') {
            when{
                expression{env.GIT_BRANCH ==~ "master"}
            }
            steps {
                sh '''docker push <gcr_repo>
                git remote add gitops <url>
                git push -u gitops'''
            }
        }
    }
    post{
        failure{
            sh '''terraform destroy --auto-approve'''
        }
        success{
        }
    }