from modules.controller import Controller


def main():
    # scale_driver = ScaleDriver()
    # print(scale_driver.read_stable_weight_kg())
    # reporter = SharePointManager(json.load(open(CREDENTIALS_PATH)))
    Controller().run()
    
    

main()
