import graphviz

# dot = graphviz.Digraph(comment='The Round Table')

# dot.node('A', 'King Arthur')
# dot.node('B', 'Sir')
# dot.node('L', 'Sir Lancelot the Brave')

# dot.edges(['AB', 'BL'])

# print(dot.source)

# dot.render('./test-output/lotto.gv', view=True)
def make_graph(cfg):
    import graphviz
    dot = graphviz.Digraph(comment=cfg["dataset_name"])
    root_name = "root"
    layer_name = "layer"
    
    layer_keys = list(filter(lambda key: layer_name in key, cfg.keys()))
    
    if cfg[layer_keys[0]] != len(layer_keys[1:]):
        print("Please Check Yaml file, layer num is not matched")
        return
    
    layer_keys = [root_name] + layer_keys[1:]
    
    for layer_key in layer_keys:
        layer = cfg[layer_key]
        
        for keys in layer["info"].keys():
            node_name = f"{layer['name']}_{keys}"
            if layer["next"] == "None":
                break
            next_layer = cfg[layer["next"]]
            
            for next_keys in next_layer["info"].keys():
                next_node_name = f"{next_layer['name']}_{next_keys}"
                dot.node(name=node_name, label=keys)
                dot.node(name=next_node_name, label=next_keys)
                # print(node_name, next_node_name)
                dot.edge(node_name, next_node_name, constraint="false")
    
    print(dot.source)
    dot.render('./test-output/round-table.gv', view=True)  
    
    # for layer in layer_keys:
    #     layer_info = layer["info"]
    #     next_layer_name = layer["next"]
        
    #     if next_layer_name is None:
    #         break
        
    #     cfg[next_layer_name]["info"]
        
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", default="./graph.yaml")
    args = parser.parse_args()
    
    with open(args.config_path, 'r') as f:
        import yaml
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    
    make_graph(cfg)