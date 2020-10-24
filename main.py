import os
import logging
import configparser
# from datetime import datetime
import time
import subprocess

ts = time.localtime()
now = time.strftime("%Y-%m-%d-%H:%M:%S", ts)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

conf = configparser.ConfigParser()


def config():

    global dir
    global resources
    global namespaces

    if os.path.exists('conf.cfg'):
        print('##config.cfg is exist##')
    else:
        conf.add_section('resources-type')
        conf.set('resources-type', 'resources',
                 'deploy,svc,svc,ingress,serviceaccount,statefulset,clusterrolebindings,clusterroles,pv,pvc,roles,secrets,cm,cronjob')
        conf.add_section('namespaces')
        conf.set('namespaces', 'ns', 'mon, dev,stg,prod,kube-system')
        conf.add_section('backupdir')
        conf.set('backupdir', 'dir', '/tmp/test/')
        with open('conf.cfg', 'w') as configfile:
            conf.write(configfile)
        configfile.close()
        print('config was created')
    conf.read('conf.cfg')
    namespaces = conf.get('namespaces', 'ns').split(',')
    resources = conf.get('resources-type', 'resources').split(',')
    dir = conf.get('backupdir', 'dir').split(',')


def backup():
    for i in range(len(namespaces)):
        logging.info('\nstarting Backup  {0} Namespace .... \n'.format(namespaces[i]))
        for j in range(len(resources)):
            #   if not os.path.exists('{0}/{1}/{2}'.format(dir[0],namespaces[i],resources[j])):
            #     os.makedirs('{0}/{1}/{2}'.format(dir[0],namespaces[i],resources[j]))
            # cmd1="kubectl get {1} -n {0} -o yaml   > {0}-{1}.yaml  ".format(namespaces[i],resources[j])
            # os.system(cmd1)
            cmd1 = "kubectl get {1} -n {0} | cut -d ' ' -f1 | sed '1d'".format(namespaces[i], resources[j], dir[0])
            proc = subprocess.Popen([cmd1], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            k8s = out.split(b'\n')
            for k in range(len(k8s)):
                if not os.path.exists('{1}/{0}'.format(now, dir[0])):
                    os.makedirs('{0}/{1}'.format(dir[0], now))
                os.system("kubectl get {0} -n {2}  {1} -o yaml > {4}/{3}/{2}-{0}-{3}.yaml ".format(resources[j],
                                                                                                   k8s[k].decode(
                                                                                                       'utf-8').replace(
                                                                                                       '\n', '  '),
                                                                                                   namespaces[i], now,
                                                                                                   dir[0]))


config()
backup()
