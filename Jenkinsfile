pipeline {
  agent any
  stages {
    stage('Clone') {
      steps {
        checkout([$class: 'GitSCM',
          branches: [[name: '*/main']],
          userRemoteConfigs: [[
            url: 'https://github.com/ridabayi/Medical-RAG-Chatbot.git',
            credentialsId: 'github-token'
          ]],
          extensions: [[$class: 'LocalBranch', localBranch: '**']]
        ])
      }
    }
  }
}
