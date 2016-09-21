import subprocess
import os
from subprocess import PIPE


def detect_client(AIID, port):
    foundClient = False
    isJava = False
    path = ""
    for root, dirnames, filenames in os.walk("./Test/" + str(AIID)):
        for filename in filenames:
            if filename.lower() == "playerai.java":
                foundClient = compile_java_client(AIID, root + "/")
                isJava = True
                path = root
                break
            elif filename.lower() == "playerai.py":
                foundClient = True
                path = root
                break
        if foundClient:
            break
    path = path + "/"
    return foundClient, isJava, path


def start_client(AIID, port, isJava, path):
    if isJava:
        return start_java_client(AIID, port, path)
    else:
        return run_python_client(AIID, port, path)


def run_python_client(AIID, port, path):
    return subprocess.Popen(
        "py -3 ./RunPythonClient.py -p " + str(port) + " -d " + path + " -n " + str(AIID),
        shell=True)


def compile_java_client(AIID, path):
    originalPath = os.getcwd()
    os.chdir(path)
    subprocess.call(
        "javac -classpath " + originalPath + "/JavaClient.jar;./;" + originalPath + "/BotRampage.jar; PlayerAI.java")
    os.chdir(originalPath)
    return (os.path.isfile(path + "PlayerAI.class"))


def start_java_client(AIID, port, path):
    return subprocess.Popen("java -classpath ./JavaClient.jar;./;" + path + ";./BotRampage.jar; RunClient  -n " + str(
        AIID) + " -p " + str(port))


def runGame(portNumber, AIID1, map):
    AI1_valid, AI1_isJava, AI1_path = detect_client(AIID1, portNumber)

    if (AI1_valid):
        p = subprocess.Popen(
            "java -jar BotRampage.jar -go -u -n 1 -p" + str(portNumber) + " -map "+ map, stdout=PIPE, bufsize=1)

        output = b''
        with p.stdout:
            for line in iter(p.stdout.readline, b''):
                output += line
                print(output)
                if (b'Listening' in output):
                    break
        AI1 = start_client(AIID1, portNumber, AI1_isJava, AI1_path)
        p.wait()
        p.terminate()
        AI1.terminate()
        p.kill()
        AI1.kill()



if __name__ == '__main__':
    runGame(15853,"botplayer","SimpleMap1.json")
