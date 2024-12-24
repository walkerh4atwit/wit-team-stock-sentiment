// http://150.136.64.29:8080/pipeline-model-converter/validate

pipeline {
    agent any

    environment {
        BASE_PYTHON_PATH = "/bin/python3.11"

        NGINX_SRC = "config/nginx/sentiments-${param.BUILD_ENV}.conf"
        NGINX_DEST = "/etc/nginx/conf.d/sentiments-${param.BUILD_ENV}.conf"

        BACKEND_SERVICE = "sentiments-${param.BUILD_ENV}-gunicorn.service"

        BACKEND_SYSTEMD_SRC = "config/systemd/${BACKEND_SERVICE}"
        BACKEND_SYSTEMD_DEST = "/etc/systemd/system/${BACKEND_SERVICE}"

        WALLET_CRED_ENV = "${param.BUILD_ENV}_wallet_params"
        WALLET_CRED_FILENAME = "${param.BUILD_ENV}-wallet.env"

        REACT_SETUP_LOCATION = "config/react/react-${param.BUILD_ENV}.env"

        API_SERVICE = "sentiments-${param.BUILD_ENV}-alpaca.service"

        API_SYSTEMD_SRC = "config/systemd/${API_SERVICE}"
        API_SYSTEMD_DEST = "/etc/systemd/system/${API_SERVICE}"

        ALPACA_KEYS_ENV = "alpaca_api_keys"
        ALPACA_KEYS_FILENAME = "alpaca-keys.env"
    }
    
    stages {
        stage('Server-setup') {
            steps {
                withCredentials([file(credentialsId: env.WALLET_CRED_ENV, variable: 'WALLET_CRED')]) {
                    sh """
                    sudo mkdir -p /run/sentiments
                    sudo chown jenkins:jenkins /run/sentiments

                    sudo cp -f $BACKEND_SYSTEMD_SRC $BACKEND_SYSTEMD_DEST
                    sudo cp -f $NGINX_SRC $NGINX_DEST
                    cp -f $WALLET_CRED back-end

                    rm -rf venv

                    $BASE_PYTHON_PATH -m pip install virtualenv
                    $BASE_PYTHON_PATH -m venv venv

                    venv/bin/python3 -m pip install -r requirements-unix.txt
                    """
                }
            }
        }

        stage('Server-instantiate') {
            steps {
                sh """
                sudo systemctl daemon-reload

                sudo systemctl restart $BACKEND_SERVICE
                sudo systemctl restart nginx
                """
            }
        }

        stage('Server-cleanup') {
            steps {
                sh "rm back-end/$WALLET_CRED_FILENAME"
            }
        }

        stage('Client-setup') {
            steps {
                sh """
                cp $REACT_SETUP_LOCATION front-end/react-setup.env
                cd front-end
                npm ci
                """
            }
        }

        stage('Client-build') {
            steps { 
                sh "npm build"
            }
        }

        stage('API-setup') {
            steps {
                withCredentials([
                    file(credentialsId: env.ALPACA_KEYS_ENV, variable: 'ALPACA_KEYS'),
                    file(credentialsId: env.WALLET_CRED_ENV, variable: 'WALLET_CRED')
                ]) {
                    sh """
                    cp -f $ALPACA_KEYS data-collection
                    cp -f $WALLET_CRED data-collection
                    sudo cp -f $ALPACA_SYSTEMD_SRC $ALPACA_SYSTEMD_DEST
                    """
                }
            }
        }

        stage('API-instantiate') {
            steps {
                sh """
                sudo systemctl daemon-reload

                sudo systemctl restart $API_SERVICE
                """
            }
        }

        stage('API-cleanup') {
            steps {
                sh """
                rm data-collection/$ALPACA_KEYS_FILENAME
                
                rm data-collection/$WALLET_CRED_FILENAME
                """

            }
        }
    }
}