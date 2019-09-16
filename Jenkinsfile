def prodimgtag
stage('test-deploy'){
    node('master'){
        
        cleanWs()
        echo "${WORKSPACE}"
        echo "test logs add"
        git url:'https://github.com/priteshkumar/linuxac-bash.git', branch:'master'      
        sh "cp /home/jenkins/ansible/jenkins-test-provision.yml $WORKSPACE/jenkins-test-provision.yml"
        sh "cp /home/jenkins/ansible/keys.yml $WORKSPACE/keys.yml"
        sh "cp /home/jenkins/ansible/jenkins-test-terminate.yml $WORKSPACE/jenkins-test-terminate.yml"
        sh "ls -als $WORKSPACE"
        
        //clean old temp testresults from slave
        try{
            sh "rm -rf /home/jenkins/workspace/ec2*"
        }
        catch(err){
            echo "no old ec2-linux-test testresults exist"
        }
        
        //launch ec2-linux-test slave , build docker image , start webapp , do test
        try{
            ansiblePlaybook become: true, becomeUser: null, colorized: true, disableHostKeyChecking: true, playbook: 'jenkins-test-provision.yml', sudoUser: null
        }
        catch(err){
            echo "jenkins test server deploy playbook failed..."
            //try terminating the test slave
            ansiblePlaybook become: true, becomeUser: null, colorized: true, disableHostKeyChecking: true, playbook: 'jenkins-test-terminate.yml', sudoUser: null
            error "playbook execution failed exit"
            
        }
        
        //terminate ondemand ec2 linux test slave
        ansiblePlaybook become: true, becomeUser: null, colorized: true, disableHostKeyChecking: true, playbook: 'jenkins-test-terminate.yml', sudoUser: null
        
        
        try{
            
            sh "ls -als"
            sh "tar -xvf testresult.gz"
            sh "ls -als"
            def imgtag=sh label: '', returnStdout: true, script: 'cat imgtag.txt*'
            echo "${imgtag}"
            prodimgtag=imgtag
            properties([parameters([string(name: 'imgtag', defaultValue: "${imgtag}")])])
            archiveArtifacts '*.png'
            sh "mkdir -p xmlres"
            sh "mv seleniumresults.xml ./xmlres/"
            junit 'xmlres/*.xml'
            sh "rm testresult.gz"
            sh "rm *.png"
            //sh "rm *.xml"
    
        }
        catch(err){
            echo "testresult archieve failed"
            error "test results dont exist exiting..."
        }
        
        echo "${params.imgtag}"
        
    }
    

}
stage("production-deploy"){
    node('ec2-linuxprod'){
        echo "${params.imgtag}"
        echo "deploy eduweabpp on production server"
         try{
           sh "docker container rm -f eduwebapp"
           sh "docker container prune -f"
        }
        catch(err){
           echo "no such eduwebapp running"
        }
        
        docker.withRegistry('https://index.docker.io/v1/', 'docker'){
                echo "deploy webapp on production server"
                echo "${params.imgtag}"
                echo "${prodimgtag}"
                try{
	                docker.image("mavpks/eduwebapp:${params.imgtag}").run("--name eduwebapp -p 3000:80/tcp")
                }
                catch(err){
                    docker.image("mavpks/eduwebapp:${prodimgtag}").run("--name eduwebapp -p 3000:80/tcp")
                }
	        }
    }

    
}
