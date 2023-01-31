from kubernetes import client,config,utils
import argparse

def main():
    config.load_kube_config()
    k8s_client = client.ApiClient()
    yaml_file = 'services.yaml'
    yaml_file = 'deployments.yaml'
    utils.create_from_yaml(k8s_client,yaml_file,verbose=True)

if __name__ == "__main__":

    # argparser = argparse.ArgumentParser()
    # argparser.add_argument('--host', type=str, required=True)
    # try:
    #     open(argparser.config)
    # except FileNotFoundError:
    #     print('File not found')

    main()