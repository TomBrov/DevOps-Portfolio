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
                docker build -t <gcr_repo_testing> .
                docker push <gcr_repo_testing>
                cd ..
                zip -r test_env/app.zip application/'''
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
                            gcloud compute scp --strict-host-key-checking=no --ssh-key-file=$SSH_KEY app.zip $USERNAME@$IP:~/app.zip
                            gcloud compute ssh --strict-host-key-checking=no --ssh-key-file=$SSH_KEY $USERNAME@$IP "bash -c \\"unzip app.zip && docker-compose up -d\\""
                            python3 E2E.py $IP'''
                    }
                    env.success = sh(script: "$?", returnStdout:true).trim()
                    if (env.success == '0'){
                        env.bool = True
                    }
                    sh '''terraform destroy --auto-approve
                          cd ..'''
                }
            }
        }
        stage ('Tag') {
            when{
                expression{env.bool ==~ True}
                expression{env.GIT_BRANCH ==~ "master"}
            }
            steps {
                sh '''docker tag <gcr_repo_testing> <gcr_repo_production>'''
            }
        }
        stage ('Publish') {
            when{
                expression{env.bool ==~ True}
                expression{env.GIT_BRANCH ==~ "master"}
            }
            steps {
                sh '''echo yes'''
            }
        }
        stage ('Deploy') {
            when{
                expression{env.bool ==~ True}
                expression{env.GIT_BRANCH ==~ "master"}
            }
            steps {
                script{
                    sh '''cd deploy
                          terraform init
                          terraform apply --auto-approve
                          REGION=$(terraform output region | tr "\\"" ":" | cut -d ":" -f2)
                          gcloud container clusters get-credentials phonebook --region $REGION
                          '''
                }
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