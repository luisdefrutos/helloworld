pipeline {
    agent none

    stages {
        stage('Inicio') {
            agent any
            steps {
                echo 'Reto 2 - Inicio del pipeline distribuido'
            }
        }

        stage('Servicios en paralelo') {
            parallel {
                stage('Flask') {
                    agent { label 'flask-agent' }
                    steps {
                        echo 'Lanzando servidor Flask'
                        bat 'pip install flask'
                        bat '''
                            cd app
                            start /B python api.py
                            ping 127.0.0.1 -n 6 >nul
                        '''
                        stash includes: 'app/**', name: 'flask-app'
                    }
                }

                stage('WireMock') {
                    agent { label 'wiremock-agent' }
                    steps {
                        echo 'Lanzando WireMock'
                        bat '''
                            echo === DIRECTORIO ACTUAL ===
                            cd
                            dir
                            echo === INTENTANDO EJECUTAR WIREMOCK ===
                            if exist wiremock-standalone-4.0.0-beta.2.jar (
                                start /B java -jar wiremock-standalone-4.0.0-beta.2.jar --port 8081
                            ) else (
                                echo ERROR: No se encuentra wiremock-standalone-4.0.0-beta.2.jar
                                exit /b 1
                            )
                        '''
                        bat '''
                            if exist mappings (
                                echo === Carpeta mappings encontrada ===
                                dir mappings
                            ) else (
                                echo WARNING: No se encontró la carpeta mappings
                            )
                        '''
                        stash includes: 'mappings/**', name: 'wiremock-mappings', allowEmpty: true
                    }
                }
            }
        }

stage('Pruebas') {
    agent { label 'test-agent' }
    steps {
        unstash 'flask-app'
        unstash 'wiremock-mappings'
        
        echo 'Lanzando servidor Flask en test-agent'
        bat '''
            cd app
            start /B python api.py
            ping 127.0.0.1 -n 6 >nul
        '''

        echo 'Lanzando WireMock en test-agent'
        bat '''
            if exist wiremock-standalone-4.0.0-beta.2.jar (
                start /B java -jar wiremock-standalone-4.0.0-beta.2.jar --port 8081
                ping 127.0.0.1 -n 6 >nul
            ) else (
                echo ERROR: No se encuentra wiremock-standalone-4.0.0-beta.2.jar
                exit /b 1
            )
        '''

        echo 'Ejecutando pruebas REST'
        bat 'pytest test/rest --maxfail=1 --disable-warnings -q'

        echo 'Ejecutando pruebas unitarias'
            bat '''
                set PYTHONPATH=%CD%
                pytest test/unit --maxfail=1 --disable-warnings -q
            '''
    }
}


        stage('Fin') {
            agent any
            steps {
                echo 'Reto 2 finalizado correctamente.'
            }
        }
    }



}
