// http://150.136.64.29:8080/pipeline-model-converter/validate

pipeline {
    agent any

    environment {
        BASE_PYTHON_PATH = "/bin/python3.11"

        NGINX_SRC = "./config/nginx/sentiments-" + "${param.BUILD_ENV}" + ".conf"
        NGINX_DEST = "/etc/nginx/conf.d/sentiments-" + "${param.BUILD_ENV}" + ".conf"

        BACKEND_SERVICE = "sentiments-" + "${param.BUILD_ENV}" + "-gunicorn.service"

        SYSTEMD_SRC = "./config/systemd" + "${BACKEND_SERVICE}"
        SYSTEMD_DEST = "/etc/systemd/system/" + "${BACKEND_SERVICE}"

        DB_CRED_ID = "${param.BUILD_ENV}" + "-wallet.env"
    }
    
    stages {
        stage('Server-setup') {
            steps {
                withCredentials([file(credentialsId: env.DB_CRED_ID, variable: 'WALLET_CRED_ENV')]) {
                    sh """
                    sudo mkdir -p /run/sentiments
                    sudo chown jenkins:jenkins /run/sentiments

                    sudo cp -f $SYSTEMD_SRC $SYSTEMD_DEST
                    sudo cp -f $NGINX_SRC $NGINX_DEST
                    sudo cp -f $WALLET_CRED_ENV ./back-end

                    rm -rf venv

                    $BASE_PYTHON_PATH -m pip install virtualenv
                    $BASE_PYTHON_PATH -m venv venv

                    ./venv/bin/python3 -m pip install -r requirements-unix.txt
                    """
                }
            }
        }

        stage('Server-instantiate') {
            steps {
                sh """
                sudo systemctl daemon-reload

                sudo systemctl restart nginx
                sudo systemctl restart $BACKEND_SERVICE
                """
            }
        }

        stage('Server-cleanup') {
            steps {
                sh ""
            }
        }

        stage('Client-setup') {
            steps {
                sh ""
            }
        }

        stage('Client-build') {
            steps { 
                sh ""
            }
        }

        stage('Client-instantiate') {
            steps {
                sh ""
            }
        }
    }
}