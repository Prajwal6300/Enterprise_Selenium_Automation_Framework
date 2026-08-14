pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox', 'edge', 'browserstack'], description: 'Browser target')
        booleanParam(name: 'HEADLESS', defaultValue: true, description: 'Run local browsers headlessly')
    }

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh 'python -m venv .venv'
                sh '. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                script {
                    def headlessFlag = params.HEADLESS ? '--headless' : ''
                    sh ". .venv/bin/activate && pytest --browser=${params.BROWSER} ${headlessFlag} -n auto --reruns 1 --junitxml=reports/junit/results.xml"
                }
            }
        }
    }

    post {
        always {
            publishHTML(target: [
                reportDir: 'reports',
                reportFiles: 'dashboard.html',
                reportName: 'Enterprise Test Automation Dashboard',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: true
            ])
            archiveArtifacts artifacts: 'screenshots/**/*.png, logs/**/*.log, reports/**/*', allowEmptyArchive: true
            junit allowEmptyResults: true, testResults: 'reports/junit/results.xml'
        }
    }
}
