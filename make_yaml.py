import yaml

class Node:
    def __init__(self, name, parent, child) -> None:
        self.node_dict = {}
        self.name = name
        self.node_dict[f"{self.name}"] = {}
        self.parent = parent
        self.child = child
        
    def make(self):
        self.node_dict[f"{self.name}"]["parent"] = self.parent
        self.node_dict[f"{self.name}"]["child"] = self.child
        
    def get_node(self):
        self.make()
        return self.name, self.node_dict

class Layer:
    def __init__(self, prev, name, nodes, next) -> None:
        self.layer_dict = {}
        self.prev = prev
        self.name = name
        self.nodes = nodes
        self.next = next
        
    def make(self):
        self.layer_dict["prev"] = self.prev
        self.layer_dict["name"] = self.name
        self.layer_dict["next"] = self.next
        tmp_dict = {}
        print(len(self.nodes))
        for node in self.nodes:
            node_name, node_info = node.get_node()
            print(node_name)
            tmp_dict[node_name] = node_info[node_name]
            
        self.layer_dict["info"] = tmp_dict
    
    def get_layer(self):
        self.make()
        return self.name, self.layer_dict

class YamlMaker:
    def __init__(self, cfg) -> None:
        self.cfg = cfg
        self.root_name = "root"
        self.layer_name = "layer"
        self.layer_num = len(list(filter(lambda x: type(x) is int, self.cfg)))
        self.yaml_dict = {}
    
    def get_node_obj(self, name, parent, child = None):
        return Node(name=name, parent=parent, child=child)
        
    def make_node_dict(self, name, parent, child = None):
        _, dict = self.get_node_obj(name, parent, child).get_node()
        return dict
        
    def make_layer_dict(self, prev, name, nodes, next):
        _, dict = Layer(prev=prev, name=name, nodes=nodes, next=next).get_layer()
        return dict
    
    def add_child_tagetNode(self, layer_name, node_name, child_name):
        target_node = self.yaml_dict[layer_name]["info"][node_name]
        if target_node["child"] is None:
            target_node["child"] = []
        for name in child_name:
            target_node["child"].append(name)
    
    def make(self):
        import os
        self.yaml_dict["dataset_name"] = self.cfg["dataset_name"]
        self.yaml_dict["save_path"] = self.cfg["save_path"]
        self.yaml_dict["save_format"] = self.cfg["save_format"]
        self.yaml_dict["view"] = self.cfg["view"]
        self.yaml_dict["layer_num"] = self.layer_num - 1
        
        for key in range(self.layer_num):
            
            node_list = []
            if key > 1:
                prev = f"layer_{key-1}"
            elif key == 0:
                prev = None
                node_list.append(self.get_node_obj(name=self.cfg[0][0][0], parent=None))
            else:
                prev = "root"
            
            for group in self.cfg[key].keys():
                node_names = self.cfg[key][group]
                print('names', node_names)
                next = f"layer_{key+1}" if key < self.layer_num - 1 else None
                layer_name = f"layer_{key}" if key > 0 else "root"
                parent=None
                
                if key >= 1:
                    parent = input(f"[Current Input Node is ***{node_names}***] \n What is a parent node of this : ")
                    self.add_child_tagetNode(layer_name=prev, node_name=parent, child_name=node_names)
                    
                for node_name in node_names:
                    if key < 1:
                        continue
                    node_objs = self.get_node_obj(name=node_name, parent=parent)
                    node_list.append(node_objs)
                
                layer = self.make_layer_dict(name=layer_name, prev=prev, nodes=node_list, next=next)
                self.yaml_dict[layer_name] = layer
        
        os.makedirs(self.cfg["output_path"], exist_ok=True)
        save_path = os.path.join(self.cfg["output_path"], self.cfg["dataset_name"]+".yaml")
        with open(save_path, 'w') as f:
            yaml.safe_dump(self.yaml_dict, f, sort_keys=False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", default="./make_yaml.yaml")
    args = parser.parse_args()

    with open(args.config_path, 'r') as f:
        import yaml
        cfg = yaml.load(f, Loader=yaml.FullLoader)
            
    maker = YamlMaker(cfg)
    maker.make()
    
    import sys
    sys.exit()