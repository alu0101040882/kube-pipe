from kubernetes import client, config
from time import sleep
import uuid
import sys


from kubernetes.client.models.v1_persistent_volume_claim import V1PersistentVolumeClaim
from kubernetes.client.models.v1_persistent_volume_claim_spec import V1PersistentVolumeClaimSpec
from kubernetes.client.models.v1_persistent_volume_claim_volume_source import V1PersistentVolumeClaimVolumeSource
from kubernetes.client.models.v1_pod_status import V1PodStatus

# Configs can be set in Configuration class directly or using helper utility

"""
        job={
            name="load",
            inputs=[],
            outputs=["X_train","y_train","X_test","y_test"],
            program="app.py",
            image="alu0101040882/load,
            dependencies=[]
        }

"""

class Kube_pipe:

    
    def __init__(self,jobs):
        config.load_kube_config()

        self.api = client.CoreV1Api()

        self.pipeid = str(uuid.uuid4())[:8]

        self.completedJobs = []

        self.jobs = jobs



    def start(self):
        self.launchDepCompletedJobs()
        self.checkJobStatus()


        
    def checkJobStatus(self):
        jobCompleted = False
        for job in self.jobs:
            try:
                
                api_response = self.api.read_namespaced_pod_status(
                name="pipeline-"  + self.pipeid + "-" + job.get("name"),
                namespace="default")

                
                if api_response.status.phase == "Succeeded":
                    self.jobs.remove(job)
                    self.completedJobs.append(job.get("name"))
                    jobCompleted = True
                    print("Pod '" + job.get("name") + "' ha finalizado")
                    if(job.get("stdout",False)):
                        print("Stdout del pod '" + job.get("name") + "':")
                        api_response_logs = self.api.read_namespaced_pod_log(name="pipeline-"  + self.pipeid + "-" + job.get("name"),namespace="default")
                        print(api_response_logs)

                elif api_response.status.phase == "Failed" and job.get("critical",False):
                    print("Job '" + job.get("name") + "' failed, exiting now...\n")
                    print("ERROR logs:\n")
                    api_response_logs = self.api.read_namespaced_pod_log(name="pipeline-"  + self.pipeid + "-" + job.get("name"),namespace="default")
                    print(api_response_logs)
                    sys.exit()
            
            except Exception as e:
                if(e.__class__.__name__ == "ApiException" and e.status == 404):
                    print("...")
                else:
                    raise e




        if(jobCompleted):
            self.launchDepCompletedJobs()

        sleep(1)

        if(len(self.jobs)>0):
            self.checkJobStatus()

        

    def launchDepCompletedJobs(self):
        for job in self.jobs:
            depCompleted = True
            for dep in job.get("dependencies"):
                if dep not in self.completedJobs:
                    depCompleted = False
                    break
            if depCompleted:
                self.launchJob(job)
            



    def launchJob(self,job):
        # Configureate Pod template container

        inputs = job.get("inputs",[])
        outputs = job.get("outputs",[])


 
        inputcommand = "import pickle\n"
        for input in inputs:
            inputcommand+="""with open(\'/usr/local/share/{}\', \'rb\') as input_file:
    {} = pickle.load(input_file)
""".format(input,input,input)


        inputcommand += """

with open('/usr/src/app/app.py') as f:
    exec(f.read())\n"""

        inputcommand+="""

EXPORT_PATH = \'/usr/local/share/\'
def exportVariable(variable,name):
    with open(EXPORT_PATH +  name, \'wb\') as handle:
        pickle.dump(variable, handle, protocol=pickle.HIGHEST_PROTOCOL)\n"""

        for output in outputs:
            inputcommand+="""exportVariable({},'{}')\n""".format(output,output)


        #print(inputcommand)

        command = ["python3" ,"-c", inputcommand]

        container = client.V1Container(
            name=job.get("name"),
            image=job.get("image"),
            command=command,
            volume_mounts=[client.V1VolumeMount(mount_path="/usr/local/share", name="volume-"+job.get("name"))]
            )


        volume = client.V1Volume(
            name="volume-"+job.get("name"), 
            persistent_volume_claim=V1PersistentVolumeClaimVolumeSource
            (
                claim_name="pipeline-shared-storage-claim"
            )
        )

        spec=client.V1PodSpec(restart_policy="Never", containers=[container],volumes=[volume])
       

        # Instantiate the job object
        body = client.V1Job(
            api_version="v1",
            kind="Pod",
            metadata=client.V1ObjectMeta(name="pipeline-"  + self.pipeid + "-" + job.get("name")),
            spec=spec)

        api_response = self.api.create_namespaced_pod(
        body=body,
        namespace="default")
        print("Lanzado el pod: '" + job.get("name") + "'")
