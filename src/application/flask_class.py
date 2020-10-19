class App_Flask(object):

    def __init__(self):
        import subprocess
        list_files = subprocess.run("python app_task.py run")





if __name__=='__main__':
    a=App_Flask()
    #  print(dir(a))