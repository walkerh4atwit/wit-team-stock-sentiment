// http://150.136.64.29:8080/pipeline-model-converter/validate

pipeline {
    agent any

    tools {
        nodejs 'Node'
    }

    environment {
        BASE_PYTHON_PATH = "/bin/python3.11"

        ALPACA_KEYS_ENV = "alpaca_api_keys"
        ALPACA_KEYS_FILENAME = "alpaca-keys.env"
    }
    
    stages {
        stage('Dynamic-variable-setup') {
            steps {
                script {
                    env.NGINX_SRC = "config/nginx/sentiments-${params.BUILD_ENV}.conf"
                    env.NGINX_DEST = "/etc/nginx/conf.d/sentiments-${params.BUILD_ENV}.conf"

                    env.BACKEND_SERVICE = "sentiments-${params.BUILD_ENV}-gunicorn.service"

                    env.BACKEND_SYSTEMD_SRC = "config/systemd/${env.BACKEND_SERVICE}"
                    env.BACKEND_SYSTEMD_DEST = "/etc/systemd/system/${env.BACKEND_SERVICE}"

                    env.WALLET_CRED_ENV = "${params.BUILD_ENV}_wallet_params"
                    env.WALLET_CRED_FILENAME = "${params.BUILD_ENV}-wallet.env"

                    env.REACT_SETUP_LOCATION = "config/react/react-${params.BUILD_ENV}.env"

                    env.API_SERVICE = "sentiments-${params.BUILD_ENV}-alpaca.service"

                    env.API_SYSTEMD_SRC = "config/systemd/${env.API_SERVICE}"
                    env.API_SYSTEMD_DEST = "/etc/systemd/system/${env.API_SERVICE}"
                }
            }
        }

        stage('Server-setup') {
            steps {
                withCredentials([file(credentialsId: "${env.WALLET_CRED_ENV}", variable: "WALLET_CRED")]) {
                    sh """
                    sudo mkdir -p /run/sentiments

                    sudo cp -f "$BACKEND_SYSTEMD_SRC" "$BACKEND_SYSTEMD_DEST"
                    sudo cp -f "$NGINX_SRC" "$NGINX_DEST"
                    cp -f "$WALLET_CRED" back-end

                    "$BASE_PYTHON_PATH" -m pip install virtualenv
                    "$BASE_PYTHON_PATH" -m venv venv

                    venv/bin/python3 -m pip install -r requirements-unix.txt
                    """
                }
            }
        }

        stage('Server-instantiate') {
            steps {
                sh """
                sudo systemctl daemon-reload

                sudo systemctl restart "$BACKEND_SERVICE"
                sudo systemctl restart nginx
                """
            }
        }

        stage('Server-cleanup') {
            steps {
                sh "rm back-end/$WALLET_CRED_FILENAME"
            }
        }

        stage('Client-build') {
            steps {
                sh """
                cp "$REACT_SETUP_LOCATION" front-end/react-setup.env
                cd front-end
                npm ci
                npm run build
                """
            }
        }

        stage('API-setup') {
            steps {
                withCredentials([
                    file(credentialsId: "${env.ALPACA_KEYS_ENV}", variable: 'ALPACA_KEYS'),
                    file(credentialsId: "${env.WALLET_CRED_ENV}", variable: 'WALLET_CRED')
                ]) {
                    sh """
                    cp -f "$ALPACA_KEYS" data-collection
                    cp -f "$WALLET_CRED" data-collection
                    sudo cp -f "$API_SYSTEMD_SRC" "$API_SYSTEMD_DEST"
                    """
                }
            }
        }

        stage('API-instantiate') {
            steps {
                sh """
                sudo systemctl daemon-reload

                sudo systemctl restart "$API_SERVICE"
                """
            }
        }

        stage('API-cleanup') {
            steps {
                sh """
                rm "data-collection/$ALPACA_KEYS_FILENAME"

                rm "data-collection/$WALLET_CRED_FILENAME"
                """

            }
        }
    }
}