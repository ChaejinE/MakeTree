import graphviz

class DataTree:
    def __init__(self, dataset_cfg) -> None:
        self.cfg = dataset_cfg
        self.dot = graphviz.Digraph(self.cfg["dataset_name"], format="png")
        self.root_name = self.cfg["root"]["name"]
        
        layer_name = "layer"
        self.layer_keys = list(filter(lambda key: layer_name in key, self.cfg.keys()))
        
        if self.cfg[self.layer_keys[0]] != len(self.layer_keys[1:]):
            assert("Please Check Yaml file, layer num is not matched")

        self.layer_keys = [self.root_name] + self.layer_keys[1:]
        
    def make(self):
        for layer_key in self.layer_keys:
            layer = self.cfg[layer_key]
    
            for key in layer["info"].keys():
                if layer["next"] is None:
                    break
                
                node_name = f"{layer['name']}_{key}"
                self.dot.node(name=node_name, label=key)
        
                next_layer_keys = layer["info"][key]["child"]        
                for next_keys in next_layer_keys:
                    next_node_name = f"{layer['next']}_{next_keys}"  
                    self.dot.node(name=next_node_name, label=next_keys)
                    self.dot.edge(node_name, next_node_name)
                    
    def save(self, view=True):
        self.dot.render(self.cfg["save_path"] + f"/{self.cfg['dataset_name']}.gv", view=view)  
    
    def operate(self, save=True):
        self.make()
        self.save() if save else print("Not Save")
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", default="./graph.yaml")
    args = parser.parse_args()
    
    with open(args.config_path, 'r') as f:
        import yaml
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    
    tree = DataTree(cfg)
    tree.operate(save=True)