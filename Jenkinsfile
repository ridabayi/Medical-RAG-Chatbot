pipeline {
    agent any

    stages {
        stage('Clone GitHub Repo') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-toekn', url: 'https://github.com/ridabayi/Medical-RAG-Chatbot.git']])checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-toekn', url: 'https://github.com/ridabayi/Medical-RAG-Chatbot.git']])
                }
            }
        }
    }
}
