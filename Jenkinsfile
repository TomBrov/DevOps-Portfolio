pipeline {
    agent any
    stages {
        stage ('ENV Prep') {
            steps {
                script{
                    deleteDir()
                    git branch: env.GIT_BRANCH, credentialsId: 'github', url: 'git@github.com:TomBrov/portfolio.git'
                    env.bool = False
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
                    withCredentials([sshUserPrivateKey(credentialsId: 'GCP_central', keyFileVariable: 'SSH_KEY', usernameVariable: 'USERNAME')]) {
                       sh '''cd test_env
                            terraform init
                            terraform apply --auto-approve
                            IP=$(terraform output IP | tr "\\"" ":" | cut -d ":" -f2)
                            cd ..
                            gcloud compute scp --strict-host-key-checking=no --ssh-key-file=$SSH_KEY app.zip $USERNAME@$IP:~/app.zip
                            gcloud compute ssh --strict-host-key-checking=no --ssh-key-file=$SSH_KEY $USERNAME@$IP "bash -c \\"unzip app.zip && docker-compose up -d\\""
                            python3 E2E.py $IP'''
                    }
                    env.success = sh (script: """$?""", returnStdout:true).trim()
                    if (env.success == 0){
                        env.bool = True
                    }
                    sh '''terraform destroy --auto-approve'''
                }
            }
        }
        stage ('Push Image') {
            when{
                expression{env.bool ==~ True}
                expression{env.GIT_BRANCH ==~ "master"}
            }
            steps {

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