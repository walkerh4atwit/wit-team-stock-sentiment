pipeline {
    agent any
    
    stages{
        stage('Initialize') {
            steps {
                script {
                    env.BASE_PYTHON_PATH = "/bin/python3.11"

                    env.NGINX_SRC = "./config/nginx/sentiments-" + param.BUILD_ENV + ".conf"
                    env.NGINX_DEST = "/etc/nginx/conf.d/sentiments-" + param.BUILD_ENV + ".conf"

                    env.BACKEND_SERVICE = "sentiments-" + param.BUILD_ENV + "-gunicorn.service"

                    env.SYSTEMD_SRC = "./config/systemd" + env.BACKEND_SERVICE
                    env.SYSTEMD_DEST = "/etc/systemd/system/" + env.BACKEND_SERVICE
                }
            }
        }

        stage('Server-setup') {
            steps {
                sh """
                sudo mkdir -p /run/sentiments
                sudo chown jenkins:jenkins /run/sentiments

                sudo cp -f $SYSTEMD_SRC $SYSTEMD_DEST
                sudo cp -f $NGINX_SRC $NGINX_DEST

                $BASE_PYTHON_PATH -m pip install virtualenv
                $BASE_PYTHON_PATH -m venv venv

                """
            }
        }

        stage('Server-instantiate') {
            steps{
                sh """
                sudo systemctl restart nginx
                sudo systemctl restart $BACKEND_SERVICE
                """
            }
        }

        stage('Client-setup') {
            
        }

        stage('Client-build') {
            
        }

        stage('Client-instantiate') {
            
        }
    }
}