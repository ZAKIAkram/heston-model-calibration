pipeline {
    agent any

    environment {
        POETRY_HOME = "${HOME}/.local"
        PATH = "${env.POETRY_HOME}/bin:${env.PATH}"
    }

    stages {
        stage('Install Poetry') {
            steps {
                sh '''
                curl -sSL https://install.python-poetry.org | python3 -
                export PATH="$HOME/.local/bin:$PATH"
                poetry --version
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'poetry install --no-interaction --no-ansi'
            }
        }

        stage('Run tests') {
            steps {
                sh 'poetry run pytest tests/ --maxfail=1 --disable-warnings -q'
            }
        }
    }
}
