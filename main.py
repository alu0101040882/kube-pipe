from kube_pipe import Kube_pipe

pipeline = Kube_pipe([
    {
        "name":"load",
        "inputs":[],
        "outputs":["X_train","y_train","X_test","y_test"],
        "program":"app.py",
        "image":"alu0101040882/load",
        "dependencies":[],
        "critical": True,
        "stdout" : False
    },
        {
        "name":"preprocessing",
        "inputs":["X_train","y_train","X_test","y_test"],
        "outputs":["X_train","X_test"],
        "program":"app.py",
        "image":"alu0101040882/preprocessing",
        "dependencies":["load"],
        "critical": True
    },
        {
        "name":"training",
        "inputs":["X_train","y_train"],
        "outputs":["model"],
        "program":"app.py",
        "image":"alu0101040882/training",
        "dependencies":["preprocessing"],
        "critical": True
    },
        {
        "name":"validation",
        "inputs":["model","X_test","y_test"],
        "outputs":[],
        "program":"app.py",
        "image":"alu0101040882/validation",
        "dependencies":["training"],
        "critical": True,
        "stdout" : True
    }
])

pipeline.start()

print("Pipeline finalizado")