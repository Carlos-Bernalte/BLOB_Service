from kubernetes import client,config,utils
import argparse


yaml_file = 'deployments.yaml'

def create_services(yaml_file):
    print('*** Creating services...')
    config.load_kube_config()
    k8s_client = client.ApiClient()
    services = utils.create_from_yaml(k8s_client,yaml_file,verbose=True)

def deploy_services(yaml_file):
    print('*** Deploying services...')
    config.load_kube_config()
    k8s_client = client.ApiClient()
    utils.create_from_yaml(k8s_client, yaml_file,verbose=True)

def args_parser():
    '''Parse command line'''
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        '-s', '--services', type=str, default='services.yaml',
        help='Configuration file (default: %(default)s)', dest='services'
    )
    parser.add_argument(
        '-d', '--deployments', type=str, default='deployments.yaml',
        help='Configuration file (default: %(default)s)', dest='deployments'
    )
    args = parser.parse_args()
    return args

if __name__ == "__main__":

    args = args_parser()
    try:
        open(args.services, 'r').close()
        open(args.deployments, 'r').close()
        create_services(args.services)
        deploy_services(args.deployments)
    except FileNotFoundError as e:
        print(e)


    