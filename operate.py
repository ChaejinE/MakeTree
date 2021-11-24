from make_yaml import YamlMaker
from tree import DataTree

if __name__ == "__main__":
    import yaml
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--make_yaml_path", default="./make_yaml.yaml")
    parser.add_argument("--tree_yaml_path", default="./tree.yaml")
    args = parser.parse_args()

    with open(args.make_yaml_path, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    
    maker = YamlMaker(cfg)
    maker.make()
    
    with open(args.tree_yaml_path, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
            
    tree = DataTree(cfg)
    tree.operate(save=True)
    
    import sys
    sys.exit()